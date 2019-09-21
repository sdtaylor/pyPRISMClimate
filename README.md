# pyPRISMClimate

An interface to the PRISM Climate data with functions similar
to the R package [prism](https://github.com/ropensci/prism)


- [Installation](#installation)
- [Quick Start](#quick-start)
- [API](#api)
  - [pyPRISMClimate.get_prism_dailys()](#pyprismclimateget_prism_dailys)
  - [pyPRISMClimate.get_prism_daily_single()](#pyprismclimateget_prism_daily_single)
  - [pyPRISMClimate.get_prism_monthlys()](#pyprismclimateget_prism_monthlys)
  - [pyPRISMClimate.get_prism_monthly_single()](#pyprismclimateget_prism_monthly_single)
  - [pyPRISMClimate.get_prism_normals()](#pyprismclimateget_prism_normals)
  - [pyPRISMClimate.utils.prism_iterator()](#pyprismclimateutilsprism_iterator)
- [Acknowledgments](#acknowledgments)

## Installation

Requires python 3. No other packages needed.

```
pip install git+git://github.com/sdtaylor/pyPRISMClimate
```

## Quick Start

Five primary functions are available to get a single date, or series of dates,
of either the daily or monthly prism data.

Available variables are tmean, tmin, tmax, ppt, vpdmin, and vpdmax.

```
from pyPRISMClimate import get_prism_monthlys, get_prism_monthly_single, 
                    get_prism_dailys, get_prism_daily_single,
                    get_prism_normals

# Get monthly mean temperature
get_prism_monthlys(variable='tmean', years=[2017,2018], months=[1,2,3,4], dest_path='/tmp/prism')

# Get a single monthly temperature file and return path of the final bil file
may_2017_tmin = get_prism_monthly_single(variable='tmin', year=2017, month=5, return_path=True)
may_2017_tmin 
> '/tmp/p/PRISM_tmin_stable_4kmM2_201705_bil.bil'

# Get daily maximum temperature for Jan. 1, 2017 to Feb. 20, 2017
get_prism_dailys('tmax',min_date='2017-01-01', max_date='2017-02-01', dest_path='/tmp/p/')

# Get the daily minimum temperature for July 1, 2005
get_prism_daily_single('tmax', '2005-07-07')

# Get the 30 year normal temperature for Jan, Feb, Mar at 800m resolution.
get_prism_normals(variable = 'tmean', resolution = '800m', months=[1,2,3],
                  dest_path = './')
                  
# Get the 30 year annual temperature at 4km resolution.
get_prism_normals(variable = 'tmean', resolution = '4km', annual=True,
                  dest_path = './')

```

If you end up with many files to work with you can use the included iterator
which returns metadata extracted from the PRISM filenames.
```
from pyPRISMClimate.utils import prism_iterator

# Assuming the files in the prism_ppt folder are:
# PRISM_ppt_stable_4kmD2_20010520_bil.bil
# PRISM_ppt_stable_4kmD2_20010521_bil.bil
# PRISM_ppt_stable_4kmD2_20010522_bil.bil

prism_iterator('prism_ppt')

[{'variable': 'ppt',
  'type': 'daily',
  'status': 'stable',
  'date': '2001-04-20',
  'date_details': {'day': 20, 'month': 4, 'year': 2001},
  'parsable': True,
  'parse_failue': None,
  'bil_filename': 'PRISM_ppt_stable_4kmD2_20010520_bil.bil',
  'full_path': './prism_ppt/PRISM_ppt_stable_4kmD2_20010520_bil.bil'},
  
  {'variable': 'ppt',
  'type': 'daily',
  'status': 'stable',
  'date': '2001-04-21',
  'date_details': {'day': 21, 'month': 4, 'year': 2001},
  'parsable': True,
  'parse_failue': None,
  'bil_filename': 'PRISM_ppt_stable_4kmD2_20010521_bil.bil',
  'full_path': './prism_ppt/PRISM_ppt_stable_4kmD2_20010521_bil.bil'},
  
  {'variable': 'ppt',
  'type': 'daily',
  'status': 'stable',
  'date': '2001-04-22',
  'date_details': {'day': 22, 'month': 4, 'year': 2001},
  'parsable': True,
  'parse_failue': None,
  'bil_filename': 'PRISM_ppt_stable_4kmD2_20010522_bil.bil',
  'full_path': './prism_ppt/PRISM_ppt_stable_4kmD2_20010522_bil.bil'}]


# Using recursive will search in nested directories. Such as:
# PRISM/
# PRISM/daily
# PRISM/daily/2001
# PRISM/daily/2002
# PRISM/monthly
# PRISM/monthly/2004
# PRISM/monthly/2005

prism_iterator('prism_ppt', recursive = True)

[{'variable': 'tmean',
  'type': 'monthly',
  'status': 'stable',
  'date': '2005-01-01',
  'date_details': {'month': 1, 'year': 2005},
  'parsable': True,
  'parse_failue': None,
  'bil_filename': 'PRISM_tmean_stable_4kmM2_200501_bil.bil',
  'full_path': './PRISM/monthly/2005/PRISM_tmean_stable_4kmM2_200501_bil.bil'},
 {'variable': 'tmean',
  'type': 'monthly',
  'status': 'stable',
  'date': '2005-02-01',
  'date_details': {'month': 2, 'year': 2005},
  'parsable': True,
  'parse_failue': None,
  'bil_filename': 'PRISM_tmean_stable_4kmM2_200502_bil.bil',
  'full_path': './PRISM/monthly/2005/PRISM_tmean_stable_4kmM2_200502_bil.bil'},
 
 .....
 
 {'variable': 'ppt',
  'type': 'daily',
  'status': 'stable',
  'date': '2001-04-15',
  'date_details': {'day': 15, 'month': 4, 'year': 2001},
  'parsable': True,
  'parse_failue': None,
  'bil_filename': 'PRISM_ppt_stable_4kmD2_20010415_bil.bil',
  'full_path': './PRISM/daily/2001/4/PRISM_ppt_stable_4kmD2_20010415_bil.bil'},
 {'variable': 'ppt',
  'type': 'daily',
  'status': 'stable',
  'date': '2001-04-14',
  'date_details': {'day': 14, 'month': 4, 'year': 2001},
  'parsable': True,
  'parse_failue': None,
  'bil_filename': 'PRISM_ppt_stable_4kmD2_20010414_bil.bil',
  'full_path': './PRISM/daily/2001/4/PRISM_ppt_stable_4kmD2_20010414_bil.bil'}]

```

## API

##### pyPRISMClimate.get_prism_dailys()

    get_prism_dailys(variable,
                     min_date,
                     max_date,
                     dates=None,
                     dest_path='./',
                     keep_zip=True)
    Downlaod PRISM Daily data

    Parameters:
        variable : str
            Either tmean, tmax, tmin, ppt, vpdmin, or vpdmax.
        
        min_date : str
            Start date to download in the format YYYY-MM-DD
        
        max_date : str
            End date to download in the format YYYY-MM-DD. Note min and max
            are inclusive. 
            
        dates : list of python datetimes, optional
            Specific dates to download, should be a list of python datetimes.           
            years and months parameters are ignored if this is set. 
        
        dest_path : str, optional
            Folder to download to, defaults to the current working directory.
        
        keep_zip : bool, optional
            Keeps the originally downloaded zip files, default True
            
##### pyPRISMClimate.get_prism_daily_single()

    get_prism_daily_single(variable,
                           date,
                           dest_path='./',
                           return_path=False,
                           keep_zip=True)
    Download data for a single day
    
    Parameters:
        variable : str
            Either tmean, tmax, tmin, ppt, vpdmin, or vpdmax.
        
        date : str
            The date to download in the format YYYY-MM-DD
        
        dest_path : str, optional
            Folder to download to, defaults to the current working directory.
    
        return_path : bool, optional
            Returns the full path to the final bil file, default False
        
        keep_zip : bool, optional
            Keeps the originally downloaded zip file, default True
            
#### pyPRISMClimate.get_prism_monthlys()

    get_prism_monthlys(variable,
                       years,
                       months,
                       dates=None,
                       dest_path='./',
                       keep_zip=True)
                       
    Download monthly PRISM data
    
    Parameters:
        variable : str
            Either tmean, tmax, tmin, ppt, vpdmin, or vpdmax.
        
        years : list of integers
            The years to download
        
        months : list of integers
            The months to download
            
        dates : list of python datetimes, optional
            Specific months to download, should be a list of python datetimes.
            The day for each date should be set to the 1st            
            years and months parameters are ignored if this is set. 
        
        dest_path : str, optional
            Folder to download to, defaults to the current working directory.
        
        keep_zip : bool, optional
            Keeps the originally downloaded zip files, default True


#### pyPRISMClimate.get_prism_monthly_single()

    get_prism_monthly_single(variable,
                             year,
                             month,
                             date=None,
                             dest_path='./',
                             return_path=False,
                             keep_zip=True)
                             
    Download data for a single day
    
    Parameters:
        variable : str
            Either tmean, tmax, tmin, ppt, vpdmin, or vpdmax.
        
        year : int
            The year to download
        
        month : int
            The month to download
        
        date : str, optional
            The date to download as a python datetime. The day should
            be set to 01. If set than year and month are ignored.
        
        dest_path : str, optional
            Folder to download to, defaults to the current working directory.
    
        return_path : bool, optional
            Returns the full path to the final bil file, default False
        
        keep_zip : bool, optional
            Keeps the originally downloaded zip file, default True

### pyPRISMClimate.get_prism_normals()

    get_prism_normals(variable,
                      resolution,
                      months=None,
                      annual=False,
                      dest_path='./',
                      return_path=False,
                      keep_zip=True)
                      
    Download 30 year normals PRISM data. These are available at either a 4km
    or 800m spatial resolution.
    
    Parameters:
        variable : str
            Either tmean, tmax, tmin, ppt, vpdmin, or vpdmax.
        
        resolution : str
            The spatial resolution, either 4km or 800m.
        
        months : list of integers
            The months to download. If None (the default) all 12 months are 
            downloaded.
        
        annual : boolean
            Whether to download the annualized normals. If True then months
            is ignored. False by default.
        
        dest_path : str, optional
            Folder to download to, defaults to the current working directory.
        
        keep_zip : bool, optional
            Keeps the originally downloaded zip files, default True


### pyPRISMClimate.utils.prism_iterator()

    prism_iterator(path, recursive=False)
    
    Returns metadata for all PRISM bil files located in path.
    
    Parameters:
        path : str
            Path to a folder to search for PRISM files
        
        recursive : boolean
            If False (default) only search in the path given, it True
            then search the full directory tree. The metadata returned
            will include the full path of each file regardless.
    
    Returns: list of dictionaries
## Acknowledgments

Development of this software was funded by
[the Gordon and Betty Moore Foundation's Data-Driven Discovery Initiative](http://www.moore.org/programs/science/data-driven-discovery) through
[Grant GBMF4563](http://www.moore.org/grants/list/GBMF4563) to Ethan P. White.
