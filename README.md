#Weather Parser

This utility downloads yearly weather data zip files from
[NOAA's Global Summary of the Day](https://www.ncdc.noaa.gov/cgi-bin/res40.pl).  It then parses and loads it into
either MongoDB, individual csvs or individual json files.

##Configuration
1. Ensure you have a Mongo instance running on your network
2. Edit the settings.py file to point at local directories, local database and other configuration settings.
```python
file_dir = The location to download / unzip GSOD files into
out_dir =  The output location for all JSON or CSV files
formats = {
       'json': False,   - True to output to JSON, or False to not
       'csv': False,    - True to output to JSON, or False to not
       'print': False,  - True to output to print to console, or False to not
       'mongo': True    - True to load into Mongo, or False to not
   }
mp = {
       'do_multiprocessing':True,   - True to use multiprocessing for parsing the weather files, or false to use a single process
       'pools':8                    - If multiprocessing is specified, this is the number of processes used
   }
timestamp = '2013-01-05' - You can set this to a date string like 'YYYY-MM-DD' to filter only newer records
                    Otherwise set to None to not filter```
mongo_info = {
       'hostname': 'localhost',     - Hostname of Mongo Instance
       'port': 27017,               - Port of Mongo Instance
       'database': 'weather',       - Database
       'collection': 'stations'     - Collection to load data into
   }
ftp_info = {
       'urlFTP': 'ftp.ncdc.noaa.gov',   - Base url of GSOD
       'fldRoot': 'pub/data/gsod'       - Subfolder containing GSOD zip files
   }
log_info = {
       'do_timestamp': True,    - True to create a log file, or False to not log
       'location':'/Users/christopherfricke/Source/Weather/GSOD_Parser/logs/gsod.log'   - Location of log file
   }
delete_temp = True   - True to delete temp data when done, or False to keep temp data (loooots of data)
years = range(1951,1961) - Define a year range to query data.
verbose = False  - True to print out more information, False to limit the amount of printouts to console
```
3. Execute parse_gsod.py
4. Enjoy