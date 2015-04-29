import logging

# For mtapi.py

productversion="v2.2" #FIXME: hardcoded
# productversion="0.8" #For local debug

mtorigin = "https://moztrap.mozilla.org" # production
# mtorigin = "http://127.0.0.1:8000"     # local
# mtorigin = "http://requestb.in/1b8n1md1" # API testing
#"http://requestb.in/1b8n1md1?inspect" # API testing

networktimeout = 15 #sec

# For diff.py
difftool="vimdiff"

#For create
defaultProduct = "Firefox OS"
defaultVersion = productversion

# Global logging setting
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
