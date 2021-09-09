Five [primary functions](api.html) are available to get a single date, or series of dates,
of either the daily or monthly prism data.

Available variables are `tmean`, `tmin`, `tmax`, `ppt`, `vpdmin`, and `vpdmax`.

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
