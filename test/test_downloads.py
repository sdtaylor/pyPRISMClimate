import pyPRISMClimate
import os

"""
Integration tests for the 4 primary download functions.
Will test the majory of the stuff in the package. 
"""


def test_daily_single(tmpdir):
    """Download a single day"""
    pyPRISMClimate.get_prism_daily_single(variable='tmean',
                                          date='2017-01-01',
                                          dest_path=tmpdir,
                                          verbose=True)
    
    assert os.path.exists(tmpdir.join('PRISM_tmean_stable_4kmD1_20170101_bil.bil'))

def test_daily_series(tmpdir):
    """Download a series of days"""
    pyPRISMClimate.get_prism_dailys(variable='tmax',
                                    min_date='2016-01-01',
                                    max_date='2016-01-03',
                                    dest_path=tmpdir,
                                    verbose=True)
    
    to_check = ['PRISM_tmax_stable_4kmD1_20160101_bil.bil',
                'PRISM_tmax_stable_4kmD1_20160102_bil.bil',
                'PRISM_tmax_stable_4kmD1_20160103_bil.bil']
    all_present = [os.path.exists(tmpdir.join(f)) for f in to_check]
    
    assert all(all_present)

def test_monthly_single(tmpdir):
    """Download a single month"""
    pyPRISMClimate.get_prism_monthly_single(variable='tmean',
                                            year=2015,
                                            month=5,
                                            dest_path=tmpdir,
                                            verbose=True)
    
    assert os.path.exists(tmpdir.join('PRISM_tmean_stable_4kmM2_201505_bil.bil'))
    
def test_monthly_series(tmpdir):
    """Download several months"""
    pyPRISMClimate.get_prism_monthlys(variable='tmean',
                                      years=[2014,2015],
                                      months=[11,12],
                                      dest_path=tmpdir,
                                      verbose=True)
    
    to_check = ['PRISM_tmean_stable_4kmM2_201411_bil.bil',
                'PRISM_tmean_stable_4kmM2_201412_bil.bil',
                'PRISM_tmean_stable_4kmM2_201511_bil.bil',
                'PRISM_tmean_stable_4kmM2_201512_bil.bil']
    
    all_present = [os.path.exists(tmpdir.join(f)) for f in to_check]
    
    assert all(all_present)