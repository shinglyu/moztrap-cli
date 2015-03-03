Command Specification
========================

moztrap -h  
  help

moztrap clone [resource] [id] 
  download the resource as a file
  e.g. moztrap clone caseversion 123 => download api/v1/caseversion/123 as caseversion__123.txt

moztrap clone [url] 
  download the MozTrap share URL (?)

moztrap diff [filename]
  diff the file with the latest remote version 

moztrap push -f [filename] -u [username] -k [api key]
  force override the remote version with the file content
  

