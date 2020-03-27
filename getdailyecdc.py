"""
        _                 _
       (_)               | |
 _ __   _  __  __   ___  | |
| '__| | | \ \/ /  / _ \ | |
| |    | |  >  <  |  __/ | |
|_|    |_| /_/\_\  \___| |_|

COVID-19-data-from-ECDC
-----------------------

The goal of this project is to provide python based downloader and loader for
geographic distribution of COVID-19 cases worldwide dataset from ECDC's website.

Copyright rixel 2020
Distributed under the Boost Software License, Version 1.0.
See accompanying file LICENSE or a copy at https://www.boost.org/LICENSE_1_0.txt
"""



# Import section
# Imports from standard library
from argparse import ArgumentParser, SUPPRESS
from datetime import date, timedelta
import requests
from os.path import isfile



# Constant to set version [Major, Minor, Build, Release type]
VERSION = [1, 0, 0, 'beta']

# Constant to specify fallback behavior.
# If >0, tries to get data from count of previous days, 0 is for no fallback.
LOAD_LASTDATA_IF_DOWNLOAD_FAILS = 1

# Constant to set number of download tries.
TRYING_LIMIT = 3

# Constant to root link of ECDC website's download area.
LINK_CORE = 'https://www.ecdc.europa.eu/sites/default/files/documents/'

# Constant to set xlsx file prefix
FILENAME_CORE = 'COVID-19-geographic-disbtribution-worldwide-'



def generatelinkandname(day_minus=None):
    """
    Generates link and filename strings to given day
    ------------------------------------------------
    @Params: (int)      [optional] Count of day before today. If omitted today's
                        date will be used.
    @Return: (tuple)    Tuple of download-link and filename strings.
    """

    global args

    if day_minus == None:
        day = date.today().strftime("%Y-%m-%d")
    else:
        day = (date.today() - timedelta(days = day_minus)).strftime("%Y-%m-%d")
    link = '{}{}{}.xlsx'.format(args.root_link, args.prefix, day)
    name = './{}{}.xlsx'.format(args.prefix, day)
    return link, name



def getfile(link):
    """
    Gets file from link and prints the status of the process
    --------------------------------------------------------
    @Params: link (string)      Link to get the file from.
    @Return: (data|Nonetype)    Data in case of success else None.
    """

    global args

    file_data = None
    trying_count = 1
    print('')
    while file_data == None and trying_count <= args.try_limit:
        try:
            print('\rTrying to get {}... ({}/{})'
                  .format(link, trying_count, args.try_limit), end='')
            back_data = requests.get(link)
            if back_data.status_code == 200:
                file_data = back_data.content
        except:
            pass
        trying_count += 1
        if file_data == None:
            print(' FAILED!')
        else:
            print(' SUCCESS.')
    return file_data



def getversion():
    """
    Returns version variable as a string
    ------------------------------------
    @Return: (string)   Version string in format <Major>.<Minor>.<Build>.<Release-type>.
    """

    global VERSION

    if len(VERSION) == 3:
        return '{}.{}.{}'.format(VERSION[0], VERSION[1], VERSION[2])
    else:
        return '{}.{}.{}-{}'.format(VERSION[0], VERSION[1], VERSION[2], VERSION[3])



def printsummary(text):
    """
    Prints summary and text
    -----------------------
    @Params: text   (string)    Text to print after summary header.
    """

    print('Summary:')
    print('--------')
    print(text)



parser = ArgumentParser(description='Downloader for geographic distribution of COVID-19 cases worldwide dataset from ECDC\'s website', epilog='')
parser.add_argument('-f', '--fallback-days', default=LOAD_LASTDATA_IF_DOWNLOAD_FAILS,
                    help='set count of fallback days (default is {}, 0 is no fallback)'
                    .format(LOAD_LASTDATA_IF_DOWNLOAD_FAILS), metavar='DAYS', type=int)
parser.add_argument('-p', '--prefix', default=FILENAME_CORE,
                    help='set xlsx file prefix (default is "{}")'.format(FILENAME_CORE),
                    metavar='NAME')
parser.add_argument('-r', '--root-link', default=LINK_CORE,
                    help='set download link root (default is "{}")'.format(LINK_CORE),
                    metavar='NAME')
parser.add_argument('-t', '--try-limit', default=TRYING_LIMIT,
                    help='set count of download try-limits (default is 3)', metavar='TRIES', type=int)
parser.add_argument('-v', '--version', action='version', default=SUPPRESS, version=getversion())
args = parser.parse_args()

link, name = generatelinkandname()
if not isfile(name):
    data = getfile(link)
    if data != None:
        print('Saving data to {}...'.format(name), end='')
        with open(name, 'wb') as outstream:
            outstream.write(data)
        print(' DONE.')
        printsummary('Download finished successfully.\nYou can use the new file:\n{}'
                     .format(name))
    elif args.fallback_days > 0:
        no_result = True
        for i in range(1, args.fallback_days + 1):
            link, name = generatelinkandname(i)
            if isfile(name):
                printsummary('Failed to download daily file.\nYou can use nearest available file and data from here:\n{}'
                             .format(name))
                no_result = False
                break
            else:
                data = getfile(link)
                if data != None:
                    print('Saving data to {}...'.format(name), end='')
                    with open(name, 'wb') as outstream:
                        outstream.write(data)
                    print(' DONE.')
                    printsummary('Failed to download daily file.\nNo datasets before this day present but it is downloaded successfully.\n'
                                 + 'You can use file and data from here:\n{}'
                                 .format(name))
                    no_result = False
                    break
        if no_result:
            printsummary('Failed to download daily file.\nFallback to previous days also failed in given interval.\n'
                         + 'To solve this issue try to set higher fallback_days value.\n')
    else:
        printsummary('Failed to download daily file.\nNo fallback is set, nothing downloaded.\n' +
                     'Set fallback_days different than 0 to download data from previous day(s).')
else:
    printsummary('Today\'s data already downloaded.\nYou can use the file:\n{}'
                 .format(name))
