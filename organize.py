import os.path
from datetime import datetime, date
import json
from PIL import Image, ExifTags
Image.MAX_IMAGE_PIXELS = None
from stat import *

import numpy as np
import matplotlib.pyplot as plt

# years = []
# files = os.listdir(os.getcwd())
# for filename in files:
# 	if os.path.isdir(filename): continue
# 	st = os.stat(filename)
# 	y = datetime.datetime.fromtimestamp(st[ST_MTIME]).year
# 	if y not in years: 
# 		years.append(y) 
# 		atlas[y]=[]
# 		if not str(y) in files:
# 			os.mkdir(str(y))
# 	newname = str(y)+"/"+filename
# 	os.rename(filename, newname)
# 	print newname
i=0
T = []
for folder in os.listdir(os.getcwd()):
	if not os.path.isdir(folder): continue
	for file in os.listdir(os.getcwd()+"/%s"%folder):
		f = os.getcwd()+"/%s"%(folder)+"/%s"%(file)
		if os.path.isdir(f): continue
		st = os.stat(f)
		#
		T.append(datetime.fromtimestamp(st[ST_MTIME]))
		#
		# try: fh=Image.open(f)
		# except IOError: continue			
		# try: exif = { ExifTags.TAGS[k]: v for k, v in fh._getexif().items() if k in ExifTags.TAGS}
		# except AttributeError: continue
		# if "DateTimeOriginal" in exif.keys():	
		# 	print f + "   " + exif["DateTimeOriginal"]
		# 	T.append(datetime.strptime('{}'.format(exif["DateTimeOriginal"]),'%Y:%m:%d %H:%M:%S'))
		# 	i=i+1
		# 	print i
dates = {}
for t in T:
	y = t.year; m = t.month; d = t.day
	if y not in dates.keys(): dates[y] = {}
	if m not in dates[y].keys(): dates[y][m] = {}
	if d not in dates[y][m].keys(): dates[y][m][d] = []
	dates[y][m][d].append("%s"%t)

json.dump(dates, open('dates.json', 'w'), sort_keys=True, indent=4)
dates = json.load(open('dates.json'))

Xm = []
Ym = []
Xy = []
Yy = []
for y in dates:
	i=0
	for i in range(1,13):
		Xm.append(date(int(y),i,1))
		if u'%s'%i in dates[y].keys(): Ym.append(len(dates[y][u'%s'%i]))
		else: Ym.append(0)
		i=i+1
	print y, i
for i in range(2012, 2019):
	Xy.append(date(i,7,1))
	if u'%s'%i in dates.keys(): Yy.append(sum([len(dates[u'%s'%i][u'%s'%k]) if u'%s'%k in dates[u'%s'%i].keys() else 0 for k in range(1,13)]))
	else: Yy.append(0)

Xm,Ym = zip(*sorted(zip(Xm,Ym)))
Xy,Yy = zip(*sorted(zip(Xy,Yy)))
ax = plt.subplot(111)
ax.plot(Xm, Ym, ls='-')
ax.bar(Xy, Yy, width=200, alpha=0.5, color='red')
ax.xaxis_date()
plt.grid(True)
plt.show()

