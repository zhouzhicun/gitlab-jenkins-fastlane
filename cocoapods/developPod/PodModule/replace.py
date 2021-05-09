#!/usr/bin/python
import re
import sys

f = open(sys.argv[1],'r+')  
fileread = f.read()

target = sys.argv[2]
result = re.sub(r''+target+r'',sys.argv[3], fileread)

f.seek(0)
f.write(result);
f.truncate()
f.close();