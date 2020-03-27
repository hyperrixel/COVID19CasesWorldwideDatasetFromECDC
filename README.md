# COVID-19 Cases Worldwide Dataset from ECDC

## What is this?

The goal of this project is to provide downloader and loader for geographic distribution of COVID-19 cases worldwide dataset from [ECDC's website](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide).

*We highly recommend to use this or similar script or module instead of downloading the dataset each time from the server of ECDC to spare data usage and keep bandwidth for other researchers and developers as well.* Both solutions here checks whether today's data is downloaded yet or not and downloads only in case if it is needed.

## Parts of the project

### Python script to use as downloader or as a module

The file ` ecdcloader.py ` is a python script designed to be used as a module or as a downloader at the same time.

#### As module

Simpla paste the file ` ecdcloader.py ` into your working directory and add ` import ecdcloader ` line to your code. After importing the module, the variable ` dataset ` will contain the actual data in the form of ` pandas.DataFrame() `.

#### As script

Simply run ` ecdcloader.py ` and you'll get the newest file.

#### Fine tuning

If you want to use different settings

- ` LOAD_LASTDATA_IF_DOWNLOAD_FAILS ` Constant to specify fallback behavior. If True, tries to get data from yesterday. (Default value: *True*)
- ` TRYING_LIMIT ` Number of trying if error occurs during download. (Default value: *3*)
- ` LINK_CORE ` Root link of ECDC website's download area. (Default value: *https://www.ecdc.europa.eu/sites/default/files/documents/*)
- ` FILENAME_CORE ` Set xlsx file prefix (Default value: *COVID-19-geographic-disbtribution-worldwide-*)

### Python script and its binary to use as executable

The windows executable ` getdailyecdc.exe ` is built from ` getdailyecdc.py ` you can check it's virus-free status at [jotty's page](https://virusscan.jotti.org/en-US/filescanjob/1xzi4o68p0) or you can check the result of the query [here](https://github.com/hyperrixel/COVID19CasesWorldwideDatasetFromECDC/blob/master/virus_free_proof.jpg).

The executable accepts comand-line parameters.

#### Command-line parameters

- ` -h ` ` --help ` Displays help screen.
- ` -f DAYS ` ` --fallback-days DAYS ` Sets count of fallback days. Default is ` 1 `. To pass fallback set it to ` 0 `.
- ` -p NAME ` ` --prefix NAME ` Sets xlsx file prefix. Default is "COVID-19-geographic-disbtribution-worldwide-".
- ` -r NAME ` ` --root-link NAME ` Sets download link root. Default is "https://www.ecdc.europa.eu/sites/default/files/documents/".
- ` -t TRIES ` ` --try-limit TRIES ` Sets count of download try-limits Default is ` 3 `. Use higher value in case of very bad connection circumstances.
- ` -v ` ` --version ` Shows program's version number and exits

## Future plans

Support of other filetypes: ` csv ` ` xml ` ` json `
