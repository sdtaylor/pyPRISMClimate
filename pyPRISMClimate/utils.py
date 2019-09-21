from datetime import datetime
import os
from re import match

def prism_md(filename):
    """Extract metdata from a PRISM filename
    
    Parameters:
        filename : str
            A PRISM filename, ie. PRISM_tmax_stable_4kmM2_201601_bil.zip
    
    Returns:
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
    # PRISM_tmax_stable_4kmM2_201601_bil.zip
    filename_parts = filename.split('.')[0].split('_')
    
    if len(filename_parts) != 6:
        md['parsable'] = False
        md['parse_failue'] = 'Unknown filename format'
        return md
    
    md['variable'] = filename_parts[1]
    md['status'] = filename_parts[2]
    
    try:
        d = datetime.strptime(filename_parts[4], '%Y%m%d')
        md['type'] = 'daily'
    except ValueError:
        d = datetime.strptime(filename_parts[4], '%Y%m')
        md['type'] = 'monthly'
    except:
        md['parsable'] = False
        md['parse_failue'] = 'Unknown PRISM file date format'
        return md
    
    md['date'] = str(d.date())
    
    if md['type']=='daily':
        md['date_details'] = {'day'  : d.day,
                              'month': d.month,
                              'year' : d.year}
    elif md['type']=='monthly':
        md['date_details'] = {'month': d.month,
                              'year' : d.year}

    md['parsable'] = True
    return md

def prism_iterator(path):
    """Returns a list of metadata for all PRISM bil files located in path
    
    """
    dir_listing = os.listdir(path)
    
    bil_files = [f for f in dir_listing if match('^\S*\.bil$',f)]
    
    listing = []
    for f in bil_files:
        file_md = prism_md(f)
        file_md['bil_filename'] = f
        file_md['full_path'] = os.path.join(path, f)
        
        listing.append(file_md)
    
    return listing
    