#!/usr/bin/python
import re
import sys

f = open(sys.argv[1],'r+')  
fileread = f.read()

target = sys.argv[2]
result = re.sub(r'def '+target+r'([\W\w]*?)end',r'def '+target+r'\1 \n    '+sys.argv[3]+'\nend', fileread)
print result;

f.seek(0)
f.write(result);
f.truncate()
f.close();