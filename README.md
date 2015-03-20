MozTrap CLI
===========

A command-line tool for downloading, editing and uploading test cases from/to MozTrap

# Usage
Download a test case as plaintext file:

```
python moztrap.py clone case <case_id>

```

Download a test suite as plaintext file: (you can find the suite id in a suite's shareable link)

```
python moztrap.py clone suite <suite_id>

```

Then, edit the downloaded file with your favorite text editor

See the diff between your version and the latest remote version

```
python moztrap.py diff case_<case_id>.txt
```

Push the test case back to MozTrap

```
python moztrap.py push --force -u <username> -k <api_key> case_<case_id>.txt
```

__Warning: this will force override the remote version__

#Known issue
* The default product is hardcoded to `Firefox OS v2.2` right now
* The default diff tool is hardcoded to `vimdiff` right now
* The test case title and description may fail to update.
