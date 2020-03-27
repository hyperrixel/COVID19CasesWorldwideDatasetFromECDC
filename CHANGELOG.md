# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.0.0] - 2020-03-27
### Added
- Download the daily ' .xlsx ' file from [ECDC](https://www.ecdc.europa.eu/en)'s
server
- Load latest dataset into a variable on the end of process in the python version
- Use he software in script-mode and module-mode also
- Option to load the yesterday's data if error occurs during downloading the
actual dataset. If the script does not find the stored version of yesterday's
data, it download the missing dataset from ECDC
- Error handling when there is no data to download or to process
- File extension is hardcoded as ' .xlsx ', that means there is no additional
support for other filetypes
- Add trying limit into downloading part to balance between maximize the ability
to download the file and minimize the unneccesary loading of remote server
- Use printsummary function to give back a human-readable printed feedback
about working flow of software
- Create and support executable version
- Executable version support starting with argparser
- Start following [SemVer](https://semver.org/spec/v2.0.0.html)
- Start using CHANGELOG as CHANGELOG.md
- Start using README as README.md
- Start using REQUIREMENTS as requirements.txt
