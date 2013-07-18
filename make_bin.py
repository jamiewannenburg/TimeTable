import os
import subprocess
import zipfile
import shutil
import re

# run py2exe install (installs to /dist)
subprocess.call("python setup.py install py2exe")

# get new version number
p = os.path.relpath('binaries/windows')
filename = 'TimeTable_v0-001.zip'
if os.path.exists(os.path.join(p,'TimeTable_v0-001.zip')):
    count = 0
    for f in os.listdir(p):
        if re.search(r'TimeTable_v0-\d{3}.zip',f).group(0):
            candidate = int(re.search(r'\d{3}',f).group(0))
            if candidate > count:
                count = candidate
            
    filename = 'TimeTable_v0-%.3d.zip'% (count+1)

# copy new assets and text directories into dist folder
#if os.path.exists(os.path.join('dist','assets')):
#    shutil.rmtree('dist/assets')
#if os.path.exists(os.path.join('dist','text')):
#    shutil.rmtree('dist/text')

#shutil.copytree('assets','dist/assets')
#shutil.copytree('text','dist/text')

# zip contents of dist folder into a new binary version
with zipfile.ZipFile(os.path.join(p,filename),'w') as myzip:
    for root, dirs, files in os.walk('dist'):
        for file in files:
            myzip.write(os.path.join(root, file))

