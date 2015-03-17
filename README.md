MozTrap CLI
===========

A command-line tool for downloading, editing and uploading test cases from/to MozTrap

# Usage
Download a test case as plaintext file:

```
python moztrap.py clone caseversion <case id>

```

Download a test suite as plaintext file:

```
python moztrap.py clone suite <suite id>

```

Then, edit the downloaded file with your favorite text editor

See the diff between your version and the latest remote version

```
python moztrap.py diff caseversion_<case id>.txt
```

Push the test case back to MozTrap

```
python moztrap.py push --force caseversion_<case id>.txt
```

__Warning: this will force override the remote version__

#Known issue
* The default product is hardcoded to `Firefox OS v2.2` right now
* The default diff tool is hardcoded to `vimdiff` right now
* Pushing a suite to MozTrap has not been implemented yet.

