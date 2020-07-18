# Info
Python based application to manage notes during phone interactions.

# Install
The main application can be installed using an automated setup script:

```
curl -IL https://raw.githubusercontent.com/am401/foneutil/master/setup.sh | bash
```

# Usage
The above setup script creates a VENV and installs the relevant requirements. To run the application, call the VENV Python application:

```
env/bin/python foneutil.py
```

The current main menu options available:

```
[R]ead file
[A]dd record
[D]elete record
[U]pdate record
[E]xit
```

# Change Log
All notable changes to this project will be documented in this section.

## [0.4.4] - 2020-06-26
### Added
- Edit functionality within the app, allowing user to edit existing records.

### Changed
- Changed menu text from `[A]dd a record` to `[A]dd record`

## [0.4.3] - 2020-06-02
### Changed
- Fix bug when creating dat.csv for first time with initial row being written on same line as the header.

## [0.4.2] - 2020-05-28
### Changed
- Fix bug where the dataframe was not properly called in the delete record function.

## [0.4.1] - 2020-05-24
### Changed
- Fix truncating of longer CSV files.
- Overhauled getData() to split it up in to smaller functions.

## [0.4] - 2020-05-12
### Added
- Add the option to delete records while in the script.
- Add checks when running script to check for data file's presence.


## [0.3] - 2020-04-20
### Changed
- Change Issue variable to Conundrum within input form to allow improved hot key combination.
- Updated some of the shortcut keys for


## [0.2] - 2020-04-08
### Added
- Added the ability to exit from the input form without saving the data.

### Changed
- Revamped user interface to remove numbers from menu options and input form.
- Banner now displays whenever moving back to main menu.

## [0.1] - 2020-04-01
### Added
- Add readline module in order to allow for user to edit existing text and move between fields.
- Add context manager to handle opening data file.

### Changed
- Improved main menu and user interface options.
