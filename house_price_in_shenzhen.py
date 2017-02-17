#!/usr/bin/python
#-*- coding:utf-8 -*-

"""
=========================================================
Linear Regression for house price of shenzhen
=========================================================

"""


import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import json
import string
import time

import sqlite3

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

print 'start'

#get data
_db=sqlite3.connect("lianjia_sz.db")
_db.text_factory=str
cu = _db.cursor()

sql = 'select a.room,a.size,strftime(\'%s\', a.deal_date),a.floors,a.build_time,a.unit_price,b.economic_circle from chengjiao a join xiaoqu b where a.name=b.name and a.name in ( select name from xiaoqu where district in (\'南山区\', \'罗湖区\', \'福田区\') ) and a.build_time!=0;'

cu.execute(sql)
tuple_data = cu.fetchall()


'''
华侨城 0 
莲塘 1 
东门 2 
梅林 3 
香蜜湖 4 
新秀 5 
石厦 6 
华强南 7 
南山中心 8 
南头 9 
前海 10 
大学城 11 
洪湖 12 
科技园 13 
景田 14 
春风路 15 
黄贝岭 16 
上下沙 17 
布心 18 
后海 19 
莲花 20 
蛇口 21 
银湖 22 
竹子林 23 
皇岗 24 
八卦岭 25 
西丽 26 
福田中心 27 
'''
eco_circle_num=0
eco_circle_dict={}
for i in tuple_data:
	if not (i[6] in eco_circle_dict.keys()):
		eco_circle_dict[i[6]] = eco_circle_num
		print 'eco_circle %s %d \n' %(i[6], eco_circle_num)
		eco_circle_num+=1

target_x = []

###multi variable



for i in tuple_data:
	tmp = []
	k=0
	for j in i:
		k+=1
		if k==6:
			continue
		if k==7:
			tmp.append(eco_circle_dict[j])
			continue
		if isinstance(j,basestring):
			j=string.atoi(j,10)
		tmp.append(j)
	target_x.append(tmp)



###single variable
'''
for i in tuple_data:
	tmp=[]
	#tmp.append(i[0])  #按 room 训练
	tmp.append(i[4])  #按 build_time
	#tmp.append(eco_circle_dict[i[6]])  #按 economic_circle

	#tmp.append(string.atoi(i[2]))
	target_x.append(tmp)
#target_x = target_x[:, np.newaxis]
'''

target_y = []
for i in tuple_data:
	target_y.append(i[5])

#target_x = target_x[:, np.newaxis, 2]

#split data
x_train = target_x[:-400]
x_test = target_x[-400:]

y_train = target_y[:-400]
y_test = target_y[-400:]

#print target_x[0:20]

#train
regr = linear_model.LinearRegression()
regr.fit(x_train, y_train)

print('Coefficients: \n', regr.coef_)

print("Mean squared error: %.2f"
      % np.mean((regr.predict(x_test) - y_test) ** 2))

print('Variance score: %.2f' % regr.score(x_test, y_test))

####self predict
#build_time
'''
x_x=[]
for i in range(1980,2016):
	x_x.append(i)

x_predict=[]
for i in range(1980,2016):
	tmp=[2,60,1485878400,25,8]
	tmp.insert(4,i)
	x_predict.append(tmp)
'''

#floors
'''
x_x=[]
for i in range(6,40):
	x_x.append(i)

x_predict=[]
for i in range(6,40):
	tmp=[2,60,1485878400,2008,8]
	tmp.insert(3,i)
	x_predict.append(tmp)
'''

#deal_date

x_x=[]
for i in range(1420041600,1506787200,86400*7):
	x_x.append(i)

x_predict=[]
for i in range(1420041600,1506787200,86400*7):
	tmp=[2,60,25,2008,8]
	tmp.insert(2,i)
	x_predict.append(tmp)

#size
'''
x_x=[]
for i in range(50,90):
	x_x.append(i)

x_predict=[]
for i in range(50,90):
	tmp=[2,1485878400,25,2008,8]
	tmp.insert(1,i)
	x_predict.append(tmp)
'''

#x_predict=[[2,60,1496246400,30,2005,8]] #64893

###multi-train show

x_predict_price=regr.predict(x_predict)
print 'predict %u' %x_predict_price

#plt.plot(x_x, x_predict_price, color='blue',
#         linewidth=3)
#plt.xticks(())
#plt.yticks(())

#plt.show()


#self predict plot


###single-train show
#plot
'''
plt.scatter(x_test, y_test,  color='black')
plt.plot(x_test, regr.predict(x_test), color='blue',
         linewidth=3)


plt.show()
'''