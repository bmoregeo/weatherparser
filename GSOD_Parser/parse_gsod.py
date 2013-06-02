__author__ = 'christopherfricke'

#- System Libraries
import logging
import datetime
from os.path import basename, dirname, join

#- Package Libraries
import utilities as u
import settings

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

if __name__ == '__main__':
    log_file = settings.log_info['location']
    if settings.log_info['do_timestamp']:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
        log_file = join(dirname(log_file), "%s_%s" % (timestamp, basename(log_file)))

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename=log_file,
                        filemode='w')

    # Chunk this by 5 so that we do not totally fill up the HD with large downloads!
    year_groups = chunks(settings.years, 5)

    for years in year_groups:
        u.make_message('Starting...')

        if settings.do_download:
            whole_years = u.download(years)
            unzipped_years = u.expand(whole_years)
        else:

            unzipped_years = [join(settings.file_dir, str(year)) for year in years]

        u.parse_years(unzipped_years)
        u.make_message('Finished...')
