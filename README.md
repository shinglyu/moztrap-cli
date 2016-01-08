MozTrap CLI
===========

A command-line tool for downloading, editing and uploading test cases from/to MozTrap

# Usage

* Install dependencies by `bash install.sh`
* Download a test suite as Excel file (xlsx): (you can find the suite id in a suite's shareable link)

```
python moztrap.py clone suite <suite_id>

```

* Upload the Excel file to google spreadsheet
* Edit the test cases as you like
* Use [MozIlluminate](https://github.com/MozIlluminate/mozilluminate-demo) to sync the cases back to MozTrap

> Warning: MozIlluminate-demo only pushes to moztrap-dev server right now. Please send an email to us to support MozIlluminate to go on production.

#Configuration
Edit the `config.py` file to change:
* Default product version
* Diff tool
* etc.


#Known issue
* The default product is hardcoded to `Firefox OS v2.2` right now
* The default diff tool is hardcoded to `vimdiff` right now
* The test case title and description may fail to update.
