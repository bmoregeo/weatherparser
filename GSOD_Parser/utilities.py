__author__ = 'christopherfricke'
#- System Libraries
from os.path import basename, dirname, join, exists, splitext, getsize
from os import listdir, makedirs, remove
import logging
import shutil
import sys

#- Package Libraries
import settings
from station import station


def make_message(message, status = 1):
    """
    :param message: A message to print and log
    :type message: str
    :param status: A message priority, 1 = Normal; 2 = Print only if verbose; 3 = Warning; 5 = Error
    :type status: int
    :return:
    """
    if status == 1:
        print message
        logging.info(message)
    elif status == 2 and settings.verbose:
        print message
    elif status == 3:
        logging.warning(message)
    elif status == 5:
        logging.error(message)



def parse_years(folders):
    for folder in folders:
        year = basename(folder)

        try:
            station_files = [join(folder, f) for f in listdir(folder)]
            make_message("Parsing %s" % year)
            make_message('Processing %s stations' % "{:,}".format(len(station_files)))

            if settings.mp['do_multiprocessing']:
                multi_parse(station_files)
            else:
                sgl_parse(station_files)
        except OSError, e:
            make_message(e, 3)
            pass

        # Remove Temp Download
        #if settings.delete_temp:
        #    shutil.rmtree(folder)

def parse_the_file(station_file):
    try:
        make_message('\tParsing %s' % basename(station_file), 2)
        year = basename(dirname(station_file))
        output_dir = join(settings.out_dir, year)
        if not exists(output_dir):
            makedirs(output_dir)


        s = station(station_file)
        s.output_location = output_dir
        s.formats = settings.formats
        s.unzip()
        s.filter(settings.timestamp)
        s.export()

        make_message('\t\tDone...', 2)
    except IOError, e:
        make_message(e, 5)

def multi_parse(station_files):
    """
    Loop through a list of zipped gsod files in multiple processes.  Parse and export/load the data.

    :param station_files: A list of zipped GSOD files
    :type station_files: list
    :return:
    """
    import multiprocessing
    p = multiprocessing.Pool(settings.mp['pools'])
    p.map(parse_the_file, station_files)

def sgl_parse(station_files):
    """
    Loop through a list of zipped gsod files in a single process.  Parse and export/load the data.

    :param station_files: A list of zipped GSOD files
    :type station_files: list
    :return:
    """
    map(parse_the_file, station_files)




def download(years):
    """ Download the file from the FTP site.
    """
    import ftplib
    output_files = []

    for year in years:
        ftp = ftplib.FTP()
        fileToDownload = "%s/gsod_%s.tar" % (year, year)
        fileDownloaded = join(settings.file_dir, '%s.tar' % year)
        output_files.append(fileDownloaded)
        count = 0

        make_message('\tDownloading file for %s' % year)

        ftp.connect(settings.ftp_info['urlFTP'])
        ftp.login()
        ftp.cwd(settings.ftp_info['fldRoot'])
        ftp.voidcmd("TYPE I")

        datasock, estsize = ftp.ntransfercmd("RETR %s" % fileToDownload)
        transbytes = 0


        # Try to download the file five times, other wise raise error
        while not exists(fileDownloaded) or count >= 5:
            with open(fileDownloaded, "wb") as lF:
                while 1:
                    buf = datasock.recv(2048)

                    if not len(buf):
                        break
                    lF.write(buf)
                    transbytes += len(buf)
                    if estsize:
                        update_progress(float(transbytes) / float(estsize))

            # If file is blank, re download
            if getsize(fileDownloaded) < 2:
                remove(fileDownloaded)
                count += 1
            del lF
            #if os.path.getsize(self.fileTar) < 2:
            #    raise ValueError('The file %s could not be downloaded.' % self.fileTar)


        ftp.close()

    return output_files



def expand(year_tars):
    """ Extract a tar file into an output folder and extract out all the files
    """
    import tarfile
    output_folders = []
    for year_tar in year_tars:
        out_dir = splitext(year_tar)[0]
        output_folders.append(out_dir)
        make_message('\tExtracting file for %s' % basename(out_dir))
        tF = tarfile.open(year_tar)
        tF.extractall(out_dir)
        del tF

        # Remove Temp Download
        if settings.delete_temp:
            remove(year_tar)

    return output_folders


# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    """
    via: http://stackoverflow.com/questions/3160699/python-progress-bar/15860757#15860757
    :param progress:
    :return:
    """
    barLength = 100 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\r\t\t[{0}] {1:.2f}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()