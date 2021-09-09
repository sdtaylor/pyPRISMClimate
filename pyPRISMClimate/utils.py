from datetime import datetime
import os
from glob import glob
from re import match

def prism_md(filename):
    """Extract metdata from a PRISM filename
    
    Parameters
    ----------
    filename : str
        A PRISM filename, ie. PRISM_tmax_stable_4kmM2_201601_bil.zip
    
    Returns
    -------
    dictionary of metadata
    
    {'variable':'tmean',
     'type':monthly,
     'status':'stable',
     'date':'2017-01-01',
     'date_details':{'month':1,
                     'year':2017'}
     }
    """
    md = {'variable':None,
          'type':None,
          'resolution':None,
          'status':None,
          'date':None,
          'date_details':None,
          'parsable':None,
          'parse_failue':None}
    
    if not 'PRISM' in filename:
        md['parsable'] = False
        md['parse_failue'] = 'Not a PRISM bil file'
        return md
    
    # Cutoff any extensions and get the 6 filename parts
    #    0    1    2       3     4    5
    # PRISM_tmax_stable_4kmM2_201601_bil.zip       # monthly/daily files
    # PRISM_tmax_30yr_normal_800mM2_05_bil.bil     # Normals files
    filename_parts = filename.split('.')[0].split('_')
    
    if len(filename_parts) != 6:
        if 'normal' in filename:
            '30 year normals data do not have 6 parts'
            pass
        else:
            'otherwise unknown'
            md['parsable'] = False
            md['parse_failue'] = 'Unknown filename format'
            return md
    
    md['variable'] = filename_parts[1]
    
    if 'normal' in filename:
        md['status'] = 'stable'
    else:
        md['status'] = filename_parts[2]
    
    if '4km' in filename:
        md['resolution'] = '4km'
    elif '800m' in filename:
        md['resolution'] = '800m'
        
    ################
    # Extract the date.
    date_parsed = False
        
    # daily data?
    try:
        if len(filename_parts[4]) != 8:
            raise ValueError()
        d = datetime.strptime(filename_parts[4], '%Y%m%d')
        md['type'] = 'daily'
        date_parsed = True
    except:
        pass
    
    # monthly?
    if not date_parsed:
        try:
            if len(filename_parts[4]) != 6:
                raise ValueError()
            d = datetime.strptime(filename_parts[4], '%Y%m')
            md['type'] = 'monthly'
            date_parsed = True
        except:
            pass
    
    # monthly normals?
    # insert the year 2000 here because it should be something instead of nothing.
    if not date_parsed:
        try:
            if filename_parts[3] == 'normal':
                d = datetime.strptime('2000' + filename_parts[5], '%Y%m')
                md['type'] = 'monthly_normals'
                date_parsed = True
            else:
                raise ValueError()
        except:
            pass
    
    # annual normals?
    # insert jan 1, 2000 here because it should be something intead of nothing
    if not date_parsed:
        try:
            if filename_parts[3] == 'normal' and filename_parts[5] == 'annual':
                d = datetime.strptime('20000101', '%Y%m%d')
                md['type'] = 'annual_normals'
                date_parsed = True
            else:
                raise ValueError()
        except:
            pass
    
    # giving up
    if not date_parsed:
        md['parsable'] = False
        md['parse_failue'] = 'Unknown PRISM file date format'
        return md
    
    # The 'date' entry should be a parsable YYYY-MM-DD date string to be 
    # consistent among all filetypes.
    # Even though monthly & annual data do not have exact dates. The details 
    # are in 'date_details'.
    md['date'] = str(d.date())
    
    if md['type']=='daily':
        md['date_details'] = {'day'  : d.day,
                              'month': d.month,
                              'year' : d.year}
    elif md['type']=='monthly':
        md['date_details'] = {'month': d.month,
                              'year' : d.year}
    elif md['type']=='monthly_normals':
        md['date_details'] = {'month': d.month}
    elif md['type']=='annual_normals':
        md['date_details'] = {}

    md['parsable'] = True
    return md

def prism_iterator(path, recursive=False):
    """Returns a list of metadata for all PRISM bil files located in path
    
    Parameters
    ----------
    path : str
        Path to a folder to search for PRISM files
    
    recursive : boolean
        If False (default) only search in the path given, it True
        then search the full directory tree. The metadata returned
        will include the full path of each file regardless.

    Returns
    -------
    list
        List of dictionaries where each entry contains metadata for a single 
        PRISM bil file.
    """
    dir_listing = glob('{p}{s}**'.format(p=path,s=os.sep),
                       recursive=recursive)
    
    bil_file_paths = [f for f in dir_listing if match('^\S*\.bil$',f)]
    
    listing = []
    for file_path in bil_file_paths:
        filename = os.path.basename(file_path)
        file_md = prism_md(filename)
        file_md['bil_filename'] = filename
        file_md['full_path'] = file_path
        
        listing.append(file_md)
    
    return listing
    
