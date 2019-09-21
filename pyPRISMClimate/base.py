from ftplib import FTP
from datetime import datetime, timedelta
import os
import zipfile
import time
import urllib.request

class PrismFTP:
    def __init__(self, 
                 host='prism.nacse.org', 
                 user='anonymous', passwd='abc123',
                 dest_path='./',
                 keep_zip=True,
                 verbose=False):
        self.host=host
        self.user=user
        self.passwd=passwd
        self._folder_file_lists={}
        self.keep_zip = keep_zip
        self.verbose = verbose
        
        self.dest_path = os.path.abspath(dest_path) + '/'
        if not os.path.exists(self.dest_path):
            raise RuntimeError('Path does not exist: '+self.dest_path)
        
        self.connect()
    
    def _query_ftp_folder(self, folder, attempts_made=0):
        connect_attempts=5
        retry_wait_time=300
        try:
            dir_listing = self.con.nlst(folder)
            return dir_listing
        except:
            if attempts_made + 1 == connect_attempts:
                raise IOError('Cannot query PRISM ftp')
            else:
                print('Cannot query PRISM folder, reconnecting and retrying in {t} sec'.format(t=retry_wait_time))
                time.sleep(retry_wait_time)
                self.close()
                time.sleep(1)
                self.connect()
                return self._query_ftp_folder(folder, attempts_made = attempts_made + 1)
    
    def connect(self):
        self.con = FTP(host=self.host, user=self.user, passwd=self.passwd)

    def close(self):
        self.con.close()
        
    def _validate_variable(self):
        if self.variable not in ['tmean','ppt','tmax','tmin','vpdmin','vpdmax']:
            raise ValueError('unknown variable name: '+self.variable)

    def _get_folder_listing(self, folder):
        """
        Querying the ftp takes a few moments, so if a folder is queried once,
        save the listing for future reference.
        """
        if folder in self._folder_file_lists:
            return self._folder_file_lists[folder]
        else:
            dir_listing = self._query_ftp_folder(folder)
            self._folder_file_lists[folder]=dir_listing
            return dir_listing

    def _get_date_folder(self, date):
        """
        All prism data are in folders organized at the bottom level by year.
        ie. /daily/tmean/2010/ contains all 2010 data, for tmean dailies
        """
        year = date.strftime('%Y')
        return self.base_url_dir+'/'+year+'/'
    
    def _get_date_filename(self, date):
        folder_to_check = self._get_date_folder(date)
        folder_contents = self._get_folder_listing(folder_to_check)
        date_str = self._file_search_string(date)
        matching = [filename for filename in folder_contents if date_str in filename]
        assert len(matching)<=1, 'More than 1 matching filename in folder'
        
        if len(matching)==0:
            return None
        else:
            return matching[0]
    
    def _download_file(self, download_path, dest_path, num_attempts=2):
        """
        Perform the actual download for a single file, with multiple
        tries if the connection/server is spotty.
        """
        for attempt in range(1,num_attempts+1):
            try:
                urllib.request.urlretrieve(download_path, dest_path)
            except:
                if attempt==num_attempts:
                    raise
                else:
                    time.sleep(30)
                    continue
    
    def _local_bil_filename(self, date):
        """
        The final unzipped bil file
        """
        local_zip = self.dest_path + os.path.basename(self._get_download_url(date))
        local_bil = local_zip.split('.')[0]+'.bil'
        return local_bil
        
    def download(self):
        """
        Download the specified files.
        """
        for d in self.dates:
            if self.date_available(d):
                url = self._get_download_url(d)
                local_file = self.dest_path + os.path.basename(url)
                self._download_file(download_path = url, 
                                    dest_path = local_file)
                
                z = zipfile.ZipFile(local_file)
                z.extractall(path = self.dest_path)
                
                if not self.keep_zip:
                    os.remove(local_file)
        
        #self.close()
    
    def check_downloads(self):
        """
        Ensures all dates are availalbe
        """
        date_status = [self.get_date_status(d) for d in self.dates]
        if all(date_status):
            print('All Dates specified are available')
        else:
            missing_dates = []
            for date_i, d in self.dates:
                if not date_status[date_i]:
                    missing_dates.append(d.strftime('%Y-%m-%d'))
            print('The following dates are not available:' + missing_dates)
    
    def _get_download_url(self, date):
        """
        The full download url
        """
        date_filename = self._get_date_filename(date)
        return 'ftp://'+self.host+'/'+date_filename

    # returns stable,provisional,early, or none
    def get_date_status(self, date):
        """
        Pulls the status from the date filename.
        Either stable, provisional, or early. 
        Return None if it's not available. 
        """
        date_filename = self._get_date_filename(date)
        if date_filename is not None:
            status = date_filename.split(sep='_')[-4]
            return status
        else:
            return None
    
    def date_available(self, date):
        return self.get_date_status(date)!=None


class PrismDaily(PrismFTP):
    def __init__(self,
                 variable,
                 min_date,
                 max_date,
                 dates=None,
                 **kwargs):
        """
        Interface to the daily data
        """
        super().__init__(**kwargs)
        self.base_url_dir = 'daily/' + variable
        
        self.variable = variable
        self.min_date = min_date
        self.max_date = max_date
        self.dates = dates
        
        self._validate_dates()
        self._validate_variable()
        
    def _validate_dates(self):
        """
        Check that dates are valid and, if needed, convert min_date and  max_date
        to a list of dates.
        """
        if self.dates is None:
            self.min_date = datetime.strptime(self.min_date, '%Y-%m-%d')
            self.max_date = datetime.strptime(self.max_date, '%Y-%m-%d')
            if self.max_date < self.min_date:
                raise ValueError('max_date must be after min_date')
            
            interval_length = (self.max_date - self.min_date).days
            self.dates = [self.max_date - timedelta(days=x) for x in range(0,interval_length+1)]
        else:
            if not all([isinstance(d, datetime) for d in self.dates]):
                raise TypeError('dates must be a list of dates (python datetime)')

    def _file_search_string(self, date):
        """
        For dailies this will be YYYYMMDD
        """
        return date.strftime('%Y%m%d')


class PrismMonthly(PrismFTP):
    def __init__(self,
                 variable,
                 years,
                 months,
                 dates=None,
                 **kwargs):
        """
        Interface to the monthly data
        """
        super().__init__(**kwargs)
        self.base_url_dir = 'monthly/' + variable
        
        self.variable = variable
        self.years = years
        self.months = months
        self.dates = dates
        
        self._validate_dates()
        self._validate_variable()
        
    def _validate_dates(self):
        """
        Check that dates are valid and, if needed, convert years/months
        to a list of dates.
        """
        if self.dates is None:
            # years must be [1998,1999,2000,...]
            if not isinstance(self.years, list):
                raise TypeError('years must be a list of integer years')
            if not all(isinstance(y, int) for y in self.years):
                raise TypeError('years must be a list of integer years')
            # months must be [1,2,3,...]
            if not isinstance(self.months, list):
                raise TypeError('months must be a list of integer months')
            if not all(isinstance(m, int) for m in self.months):
                raise TypeError('months must be a list of integer months')
            
            self.dates = []
            for y in self.years:
                for m in self.months:
                    date_str = str(y) + '-' + str(m)
                    self.dates.append(datetime.strptime(date_str,'%Y-%m'))
        else:
            if not all([isinstance(d, datetime) for d in self.dates]):
                raise TypeError('dates must be a list of dates (python datetime)')

    def _file_search_string(self, date):
        """
        For monthlies this will be YYYYMM
        """
        return date.strftime('%Y%m')
    
class PrismNormals(PrismFTP):
    def __init__(self,
                 variable,
                 resolution,
                 months=None,
                 annual=False,
                 **kwargs):
        """
        Interface to the normals data.
        
        Normals have a simpler file structure that doesn't rely on dates,
        so two methods below replace the more complex ones of PrismFTP.
        """
        super().__init__(**kwargs)
        self.base_url_dir = 'normals_{r}/{v}/'.format(r=resolution, v=variable)
        
        self.variable = variable
        self.resolution = resolution
        self.months = months
        self.annual = annual
        
        self._validate_dates()
        self._validate_variable()
        
        if resolution not in ['4km','800m']:
            raise ValueError('resolution must be either "4km" or "800m", got: {r}'.format(r=resolution))
        
    def _validate_dates(self):
        """
        Check that months are valid
        """
        if self.months is None:
            self.months = [1,2,3,4,5,6,7,8,9,10,11,12]
        else:
            # months must be [1,2,3,...]
            if not isinstance(self.months, list):
                raise TypeError('months must be a list of integer months')
            if not all(isinstance(m, int) for m in self.months):
                raise TypeError('months must be a list of integer months')
        
        # put in leading 0 and convert to str
        self.months = [str(m) if m >=10 else '0'+str(m) for m in self.months]
        
        if self.annual:
            self.months = ['annual']
        
        # dates is used in the PrismFTP class, so keep that consistent here.
        self.dates = self.months
    
    def date_available(self, date):
        """
        Supersedes the PrismFTP method which relies on datetime
        """
        return date in ['01','02','03','04','05','06','07','08','09','10','11','12','annual']
    
    def _get_download_url(self, date):
        """
        The full download url
        Supersedes the PrismFTP methods since normals have a
        simpler format which rarely gets updated with new data.
        """
        filename = 'PRISM_{v}_30yr_normal_{r}M2_{d}_bil.zip'.format(v = self.variable,
                                                                    r = self.resolution,
                                                                    d = date)
        return 'ftp://{host}/{p}/{f}'.format(host = self.host,
                                             p    = self.base_url_dir,
                                             f    = filename)
    
    def _file_search_string(self, date):
        pass