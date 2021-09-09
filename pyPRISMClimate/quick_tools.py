from .base import PrismDaily, PrismMonthly, PrismNormals

def get_prism_dailys(variable,
                     min_date=None,
                     max_date=None,
                     dates=None,
                     **kwargs):
    """Downlaod PRISM Daily data

    Parameters
    ----------
    variable : str
        Either tmean, tmax, tmin, or ppt
        
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
    
    """
    daily = PrismDaily(variable=variable,
                       min_date=min_date,
                       max_date=max_date,
                       dates=dates,
                       **kwargs)
    daily.download()
    daily.close()

def get_prism_daily_single(variable,
                           date,
                           return_path=False,
                           **kwargs):
    """Download data for a single day
    
    Parameters
    ----------
    variable : str
        Either tmean, tmax, tmin, or ppt
    
    date : str
        The date to download in the format YYYY-MM-DD
    
    dest_path : str, optional
        Folder to download to, defaults to the current working directory.

    return_path : bool, optional
        Returns the full path to the final bil file, default False
    
    keep_zip : bool, optional
        Keeps the originally downloaded zip file, default True
    """
    daily = PrismDaily(variable=variable,
                       min_date=date,
                       max_date=date,
                       **kwargs)
    daily.download()
    daily.close()
    
    if return_path:
        return daily._local_bil_filename(daily.dates[0])
    
    
def get_prism_monthlys(variable,
                       years=None,
                       months=None,
                       dates=None,
                       **kwargs):
    """Download monthly PRISM data
    
    Parameters
    ----------
    variable : str
        Either tmean, tmax, tmin, or ppt
    
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
    """
    monthly = PrismMonthly(variable=variable,
                           years=years,
                           months=months,
                           dates=dates,
                           **kwargs)
    monthly.download()
    monthly.close()
    
def get_prism_monthly_single(variable,
                             year=None,
                             month=None,
                             date=None,
                             return_path=False,
                             **kwargs):
    """Download data for a single day
    
    Parameters
    ----------
    variable : str
        Either tmean, tmax, tmin, or ppt
    
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
    """
    if date is not None:
        date = [date]
        
    monthly = PrismMonthly(variable=variable,
                           years=[year],
                           months=[month],
                           dates=date,
                           **kwargs)
    monthly.download()
    monthly.close()
    
    if return_path:
        return monthly._local_bil_filename(monthly.dates[0])

def get_prism_normals(variable,
                      resolution,
                      months=None,
                      annual=False,
                      **kwargs):
    """Download 30 year normals PRISM data
    
    Parameters
    ----------
    variable : str
        Either tmean, tmax, tmin, or ppt
    
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
    """
    normals = PrismNormals(variable=variable,
                           resolution=resolution,
                           months=months,
                           annual=annual,
                           **kwargs)
    normals.download()
    normals.close()
