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



# Special constants for modul style use.
__author__ = 'rixel'
__copyright__ = "Copyright 2020, COVID-19-data-from-ECDC Project"
__credits__ = ['rixel']
__license__ = 'BOOST 1.0'
__version__ = '1.0'
__status__ = 'Beta'



# Import section
# Imports from standard library
from datetime import date, timedelta
import requests
from os.path import isfile

# Imports of external libraries
import pandas as pd



# Constant to specify fallback behavior.
# If True, tries to get data from yesterday.
LOAD_LASTDATA_IF_DOWNLOAD_FAILS = True

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

    global LINK_CORE
    global FILENAME_CORE

    if day_minus == None:
        day = date.today().strftime("%Y-%m-%d")
    else:
        day = (date.today() - timedelta(days = day_minus)).strftime("%Y-%m-%d")
    link = '{}{}{}.xlsx'.format(LINK_CORE, FILENAME_CORE, day)
    name = './{}{}.xlsx'.format(FILENAME_CORE, day)
    return link, name



def getfile(link):
    """
    Gets file from link and prints the status of the process
    --------------------------------------------------------
    @Params: link (string)      Link to get the file from.
    @Return: (data|Nonetype)    Data in case of success else None.
    """

    global TRYING_LIMIT

    file_data = None
    trying_count = 1
    print('')
    while file_data == None and trying_count <= TRYING_LIMIT:
        try:
            print('\rTrying to get {}... ({}/{})'
                  .format(link, trying_count, TRYING_LIMIT), end='')
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



def printsummary(text):
    """
    Prints summary and text
    -----------------------
    @Params: text   (string)    Text to print after summary header.
    """

    print('Summary:')
    print('--------')
    print(text)



def simpleget(minus_day=None):
    """
    Downloads data and generates link and filename strings to given day
    -------------------------------------------------------------------
    @Params: (int)      [optional] Count of day before today. If omitted today's
                        date will be used.
    @Return: (tuple)    Tuple of downloaded data, download-link and filename.
    """

    link, name = generatelinkandname(minus_day)
    data = getfile(link)
    return data, link, name



link, name = generatelinkandname()
if not isfile(name):
    data = getfile(link)
    if data != None:
        print('Saving data to {}...'.format(name), end='')
        with open(name, 'wb') as outstream:
            outstream.write(data)
        print(' DONE.')
        dataset = pd.read_excel(name)
        printsummary('Download finished successfully.\nYou can use the new file:\n{}'
                     .format(name))
    elif LOAD_LASTDATA_IF_DOWNLOAD_FAILS:
        link, name = generatelinkandname(1)
        if isfile(name):
            dataset = pd.read_excel(name)
            printsummary('Failed to download daily file.\nYou can use file and data from yesterday:\n{}'
                         .format(name))
        else:
            data = getfile(link)
            if data != None:
                print('Saving data to {}...'.format(name), end='')
                with open(name, 'wb') as outstream:
                    outstream.write(data)
                print(' DONE.')
                dataset = pd.read_excel(name)
                printsummary('Failed to download daily file.\nNo dataset from yesterday present but it is downloaded successfully.\n'
                             + 'You can use file and data from yesterday:\n{}'
                             .format(name))
            else:
                printsummary('Failed to download daily file.\nFallback to yesterday wasn\'t successful too.\n'
                             + 'To solve this issue try simpleget(minus_day) function with more than 1 minus day parameter.\n')
    else:
        printsummary('Failed to download daily file.\nNo fallback is set, nothing downloaded.\n' +
                     'Set LOAD_LASTDATA_IF_DOWNLOAD_FAILS to True to download data from yesterday.')
else:
    dataset = pd.read_excel(name)
    printsummary('Today\'s data already downloaded.\nYou can use the file:\n{}'
                 .format(name))
