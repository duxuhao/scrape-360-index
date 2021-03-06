#!/bin/env python
#encoding:utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import codecs
import time

total = []
Brand = pd.read_csv('serach_dic.csv',encoding = 'utf-8',header = None)
p = re.compile('<tspan dy="3.5">')
Index_file = codecs.open('Brand_serach_index_360.csv','a','utf-8')
Index_file.write('Brand')
for i in range(12):
	month = '20150' + str(i+1)
	Index_file.write(',')
	Index_file.write(month)
Index_file.write('\n')
month_dates = [31,28,31,30,31,30,31,31,30,31,30,31]
month_range = [0,31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]

for keyword in Brand[0][:]:
	try:
		print 'Downloading --- ' + keyword + ' ---'
		URL = u'http://index.so.com/#trend?q=' + keyword + u'&t=201501|201512'
		driver = webdriver.Firefox()
		driver.get(URL)
		time.sleep(3)
		a = driver.find_element_by_tag_name("body").get_attribute("innerHTML")
		
		t = a.find('</path><path stroke-width="2" d="')
		num = re.sub(r'.*M20', 'M20', a[t:t+15000]).split('"')[0]
		data = [map(float, xy.split(',')) for xy in re.split('[ML]', num)[1:]]
		print '-- trend obtain --'
		it = re.finditer(p,a)
		Index_file.write(keyword)
		Index_file.write(',')
		axis_range=[]
		for i, match in enumerate(it):
			if (i > 15) & (i  < 23):
				t = match.span()[1]
				Myrange = re.sub(r'.*3.5"<', '', a[t:t+100]).split('<')[0].replace(",","")
				if Myrange.isdigit():
					axis_range.append(int(Myrange))
		
		print '-- range obtain --'
		numrange = np.reshape(data,365*2)[1::2]
		axis_max = max(axis_range)
		axis_min = min(axis_range)
		top = 194
		bottom = 38
		k = (axis_max-axis_min)/(top - bottom)
		print '-- slope obtain --'
		for i in range(12):
			mm = np.min(numrange[month_range[i]:month_range[i+1]])
			Index_file.write(str(k * (top-mm) + axis_min))
			Index_file.write(',')
		driver.quit()
		Index_file.write('\n')
		print '-- trend complete--'
	except:
		driver.quit()
		Index_file.write('\n')
		print   '--- download encounter some problem --- '

Index_file.close()

