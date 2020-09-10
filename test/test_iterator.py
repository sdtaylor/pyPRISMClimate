import pyPRISMClimate
from pathlib import Path
import pytest

"""
Integration test for the iterator. When given a path this will return a list
of dictionaries with prism metadata such as variable, month, resolution, etc.
"""

# Create some blank files to pull metadata from
prism_filenames = ['PRISM_tmean_stable_4kmM2_200308_bil.bil',
                   'PRISM_ppt_stable_4kmD2_20180521_bil.bil',
                   'PRISM_tmean_stable_4kmM2_200309_bil.bil',
                   'PRISM_tmean_stable_4kmM2_200108_bil.bil',
                   'PRISM_tmax_stable_4kmD1_20170101_bil.bil',
                   'PRISM_tmean_stable_4kmM2_200007_bil.bil',
                   'PRISM_tmax_stable_4kmD1_20170104_bil.bil',
                   'PRISM_tmean_stable_4kmM2_200307_bil.bil',
                   'PRISM_tmax_stable_4kmD1_20170103_bil.bil',
                   'PRISM_tmean_stable_4kmM2_200109_bil.bil',
                   'PRISM_tmax_stable_4kmD1_20170105_bil.bil',
                   'PRISM_tmean_stable_4kmM2_200009_bil.bil',
                   'PRISM_ppt_stable_4kmD2_20180523_bil.bil',
                   'PRISM_tmean_stable_4kmM2_200008_bil.bil',
                   'PRISM_tmax_stable_4kmD1_20170102_bil.bil',
                   'PRISM_ppt_stable_4kmD2_20180520_bil.bil',
                   'PRISM_tmean_30yr_normal_800mM2_annual_bil.bil',
                   'PRISM_tmax_30yr_normal_800mM2_annual_bil.bil',
                   'PRISM_tmin_30yr_normal_800mM2_annual_bil.bil',
                   'PRISM_tmax_30yr_normal_4kmM2_08_bil.bil',
                   'PRISM_tmax_30yr_normal_800mM2_04_bil.bil',
                   'PRISM_tmean_stable_4kmM2_200107_bil.bil',
                   'PRISM_ppt_stable_4kmD2_20180522_bil.bil']


def test_full_iterator(tmpdir):
    for f in prism_filenames:
        Path(tmpdir + f).touch()
    
    prism_metadata = pyPRISMClimate.utils.prism_iterator(str(tmpdir))
    
    # if all are parsable=True it means the metadata was fully parsed
    assert all([f['parsable'] for f in prism_metadata])

"""
Test specific filenames for exactly matching metadata
"""

filename_test_cases = []

"""
Good filenames
"""
filename_test_cases.append(('PRISM_tmean_stable_4kmM2_200008_bil.bil',
                                 {'variable':'tmean',
                                  'type':'monthly',
                                  'resolution': '4km',
                                  'status':'stable',
                                  'date':'2000-08-01',
                                  'date_details':{'month': 8, 'year': 2000},
                                  'parsable':True,
                                  'parse_failue':None}))
filename_test_cases.append(('PRISM_tmin_stable_4kmM2_200107_bil.bil',
                                 {'variable':'tmin',
                                  'type':'monthly',
                                  'resolution': '4km',
                                  'status':'stable',
                                  'date':'2001-07-01',
                                  'date_details':{'month': 7, 'year': 2001},
                                  'parsable':True,
                                  'parse_failue':None}))
filename_test_cases.append(('PRISM_ppt_stable_4kmD2_20180520_bil.bil',
                                 {'variable':'ppt',
                                  'type':'daily',
                                  'resolution': '4km',
                                  'status':'stable',
                                  'date':'2018-05-20',
                                  'date_details':{'day' : 20, 'month': 5, 'year': 2018},
                                  'parsable':True,
                                  'parse_failue':None}))
filename_test_cases.append(('PRISM_tmax_provisional_4kmD1_20170101_bil.bil',
                                 {'variable':'tmax',
                                  'type':'daily',
                                  'resolution': '4km',
                                  'status':'provisional',
                                  'date':'2017-01-01',
                                  'date_details':{'day' : 1, 'month': 1, 'year': 2017},
                                  'parsable':True,
                                  'parse_failue':None}))
filename_test_cases.append(('PRISM_tmean_stable_4kmM3_201412_bil.bil',
                                 {'variable':'tmean',
                                  'type':'monthly',
                                  'resolution': '4km',
                                  'status':'stable',
                                  'date':'2014-12-01',
                                  'date_details':{'month': 12, 'year': 2014},
                                  'parsable':True,
                                  'parse_failue':None}))

filename_test_cases.append(('PRISM_ppt_30yr_normal_4kmM2_06_bil.bil',
                                 {'variable':'ppt',
                                  'type':'monthly_normals',
                                  'resolution': '4km',
                                  'status':'stable',
                                  'date':'2000-06-01',
                                  'date_details':{'month': 6},
                                  'parsable':True,
                                  'parse_failue':None}))

filename_test_cases.append(('PRISM_ppt_30yr_normal_4kmM2_annual_bil.bil',
                                 {'variable':'ppt',
                                  'type':'annual_normals',
                                  'resolution': '4km',
                                  'status':'stable',
                                  'date':'2000-01-01',
                                  'date_details':{},
                                  'parsable':True,
                                  'parse_failue':None}))

"""
Bad filenames
"""
filename_test_cases.append(('some_other_bil_file.bil',
                                 {'variable':None,
                                  'type':None,
                                  'resolution': None,
                                  'status':None,
                                  'date':None,
                                  'date_details':None,
                                  'parsable':False,
                                  'parse_failue':'Not a PRISM bil file'}))
filename_test_cases.append(('PRISM_ppt_stable_4kmD2_20180520_bil_extrainfo.bil',
                                 {'variable':None,
                                  'type':None,
                                  'resolution': None,
                                  'status':None,
                                  'date':None,
                                  'date_details':None,
                                  'parsable':False,
                                  'parse_failue':'Unknown filename format'}))    

@pytest.mark.parametrize('filename, expected_metadata', filename_test_cases)
def test_prism_filenames(filename, expected_metadata):
    md = pyPRISMClimate.utils.prism_md(filename)
    assert md == expected_metadata
