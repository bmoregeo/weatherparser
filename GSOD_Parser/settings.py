__author__ = 'christopherfricke'

file_dir = '/Users/christopherfricke/Source/Weather/data/downloads'
out_dir =  '/Users/christopherfricke/Source/Weather/data/out'

formats = {
    'json': False,
    'csv': False,
    'print': False,
    'mongo': True
}

mp = {
    'do_multiprocessing':True,
    'pools':8
}

timestamp = None


mongo_info = {
    'hostname': 'localhost',
    'port': 27017,
    'database': 'weather',
    'collection': 'stations'
}


ftp_info = {
    'urlFTP': 'ftp.ncdc.noaa.gov',
    'fldRoot': 'pub/data/gsod'
}

log_info = {
    'do_timestamp': True,
    'location':'/Users/christopherfricke/Source/Weather/GSOD_Parser/logs/gsod.log'
}

delete_temp = True


years = range(1951,1961)
verbose = False
do_download = False