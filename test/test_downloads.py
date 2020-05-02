import pyPRISMClimate
import os

"""
Integration tests for the 4 primary download functions.
Will test the majory of the stuff in the package. 
"""

def prism_item_in_list(qury_item, list_of_items_to_check):
    """
    Compare a single prism specifiation to a list of PRISM files
    returned by pyPRISMClimate.prism_iterator

    """
    for item_to_check in list_of_items_to_check:
        matches = [item_to_check[key] == key_contents for key, key_contents in qury_item.items()]
        if all(matches):
            return True 
    return False

def test_daily_single(tmpdir):
    """Download a single day"""
    to_download = {'variable':'tmean',
                   'date'    : '2017-01-01'}
    
    pyPRISMClimate.get_prism_daily_single(dest_path=tmpdir,
                                          verbose=True,
                                          **to_download)
    
    folder_contents = pyPRISMClimate.prism_iterator(tmpdir)
    
    assert prism_item_in_list(to_download, folder_contents)

def test_daily_series(tmpdir):
    """Download a series of days"""
    
    to_download = [{'variable':'tmax',
                    'date'    : '2016-01-01',
                    'date_details': {'year':2016,'month': 1, 'day' : 1},
                    'type'    : 'daily'},
                   {'variable':'tmax',
                    'date'    : '2016-01-02',
                    'date_details': {'year':2016,'month': 1, 'day' : 2},
                    'type'    : 'daily'},
                   {'variable':'tmax',
                    'date'    : '2016-01-03',
                    'date_details': {'year':2016,'month': 1, 'day' : 3},
                    'type'    : 'daily'}]
    
    pyPRISMClimate.get_prism_dailys(variable='tmax',
                                    min_date='2016-01-01',
                                    max_date='2016-01-03',
                                    dest_path=tmpdir,
                                    verbose=True)
    
    folder_contents = pyPRISMClimate.prism_iterator(tmpdir)
    
    all_items_present = [prism_item_in_list(i, folder_contents) for i in to_download]
    
    assert all(all_items_present)

def test_monthly_single(tmpdir):
    """Download a single month"""
    to_download = {'variable':'tmean',
                   'date'    : '2015-05-01',
                   'date_details': {'year':2015,'month': 5},
                   'type'    : 'monthly'}
        
    pyPRISMClimate.get_prism_monthly_single(variable='tmean',
                                            year=2015,
                                            month=5,
                                            dest_path=tmpdir,
                                            verbose=True)
    
    folder_contents = pyPRISMClimate.prism_iterator(tmpdir)

    assert prism_item_in_list(to_download, folder_contents)
    
def test_monthly_series(tmpdir):
    """Download several months"""
    to_download = [{'variable':'tmean',
                    'date'    : '2014-11-01',
                    'date_details': {'year':2014,'month': 11},
                    'type'    : 'monthly'},
                   {'variable':'tmean',
                    'date'    : '2014-12-01',
                    'date_details': {'year':2014,'month': 12},
                    'type'    : 'monthly'},
                   {'variable':'tmean',
                    'date'    : '2015-11-01',
                    'date_details': {'year':2015,'month': 11},
                    'type'    : 'monthly'},
                   {'variable':'tmean',
                    'date'    : '2015-12-01',
                    'date_details': {'year':2015,'month': 12},
                    'type'    : 'monthly'}]
    
    pyPRISMClimate.get_prism_monthlys(variable='tmean',
                                      years=[2014,2015],
                                      months=[11,12],
                                      dest_path=tmpdir,
                                      verbose=True)
    
    folder_contents = pyPRISMClimate.prism_iterator(tmpdir)
    
    all_items_present = [prism_item_in_list(i, folder_contents) for i in to_download]
    
    assert all(all_items_present)

def test_normals_1_month(tmpdir):
    to_download = [{'variable':'ppt',
                    'date'    : '2000-10-01',
                    'date_details': {'month': 10},
                    'type'    : 'monthly_normals'},
                   {'variable':'ppt',
                    'date'    : '2000-06-01',
                    'date_details': {'month': 6},
                    'type'    : 'monthly_normals'}]
    
    pyPRISMClimate.get_prism_normals(variable='ppt',
                                     resolution='4km',
                                     months=[6,10],
                                     annual=False,
                                     dest_path=tmpdir,
                                     verbose=True)
    
    folder_contents = pyPRISMClimate.prism_iterator(tmpdir)
    
    all_items_present = [prism_item_in_list(i, folder_contents) for i in to_download]
    
    assert all(all_items_present)
