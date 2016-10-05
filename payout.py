#!/usr/bin/env python
from __future__ import division
import mysql.connector
import time

times=str(time.time())
date=time.strftime("%Y/%m/%d")
time=time.strftime("%H:%M:%S")
datetime=str(date)+' '+str(time)
cnx = mysql.connector.connect(user=[YOUR DATABASE USERNAME], password=[YOUR DATABASE PASSWORD],
                              host=[YOUR HOST IP ADDRESS],
                              database=[YOUR DATABASE NAME])
cursor = cnx.cursor()

query_btc=(" SELECT * FROM wp_usermeta WHERE meta_key= 'shares' ")
cursor.execute(query_btc)#find
dat=cursor.fetchall ()

query_btc=(" SELECT * FROM wp_usermeta WHERE meta_key= 'bitcoin' ")
cursor.execute(query_btc)#find
dat2=cursor.fetchall ()

tot_pay=[]
payout=[PAYOUT RATE]

for i in dat:
	for row in dat2:
		if i[1]==row[1]:
			if int(float(i[3]))>=2:#WE PROCESS THE PAYOUT IF THE USER OWN MORE THAN 1 SHARE
				value=float(i[3])*payout
				tot_pay.append(value)
				interest=float(row[3])+float(value)
				print i[1],row[1],i[3],format(value,'.8f'),row[3],interest
				query3=(""" UPDATE wp_usermeta SET meta_value= %s WHERE umeta_id= %s """)#update
				data3=(interest,str(row[0]))#update
				cursor.execute(query3,data3)#update
				query4=("INSERT INTO wp_myCRED_log""(ref_id,user_id,creds,ctype,time,entry)""VALUES (%s,%s,%s,%s,%s,%s)")#add new LOG				
				data4=('0',str(row[1]),value,'bitcoin',str(times),'%plural% daily interest rate payment')#add new LOG
				cursor.execute(query4,data4)

print sum(tot_pay)
cursor.close#all
cnx.close()
