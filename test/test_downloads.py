import pyPRISMClimate
import os

def test_daily_single(tmpdir):
    """Download a single day"""
    pyPRISMClimate.get_prism_daily_single(variable='tmean',
                                          date='2017-01-01',
                                          dest_path=tmpdir)
    
    assert os.path.exists(tmpdir.join('PRISM_tmean_stable_4kmD1_20170101_bil.bil'))