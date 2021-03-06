# -*- coding: utf-8 -*-

import time
import random
import couchdb
import json

#Reference from: https://www.opensourceforu.com/2015/07/interfacing-couchdb-with-python-2/
class Couch:
    # Connection Establishment with database
    def __init__(self,ip,dbname_list):
        couchserver=couchdb.Server(url=ip)
        couchserver.resource.credentials=('admin','admin')
        # Variable to store database objects
        self.db=[]
        # database required at starting
        present_database=['apikey','subregion']
        
        ip_file=open("ip.txt", "r")
        # Reading master node ip address
        while True:
            couchdb_master_ip=ip_file.readline().rstrip()
            if couchdb_master_ip != '':         #checking to not get an empty string
                break
        couchdb_master_login_url='http://admin:admin@'+couchdb_master_ip+':5984/'

        # Reading other node ip to enable replication in our system
        db_child=ip_file.readlines()
        ip_file.close()

        # Creating or loading db
        for dbname in present_database:
            self.db = self.db + [self.createdb(couchserver,dbname)]
            for child in db_child:
                couchserver.replicate(couchdb_master_login_url+dbname,'http://admin:admin@'+child.rstrip()+':5984/'+dbname,create_target=True,continuous=True)


        for dbname in dbname_list:
            self.db = self.db + [self.createdb(couchserver,dbname)]
            for child in db_child:
                couchserver.replicate(couchdb_master_login_url+dbname,'http://admin:admin@'+child.rstrip()+':5984/'+dbname,create_target=True,continuous=True)
        # Adding required static data to db
        self.create_static()
        
#Reference from: https://www.opensourceforu.com/2015/07/interfacing-couchdb-with-python-2/
    # Creating database if it does not exist, else loading it
    def createdb(self,couchserver,dbname):
        if dbname in couchserver:
            return couchserver[dbname]
        else:
            return couchserver.create(dbname)

    

    # Pushing scraped tweets along with their subjecitivity and polarity to tweet databse on couchDB
    def pushdata(self,data,dbname):

        flag=0
        for i in self.db:
            if dbname==i._name:
                flag=0
                i.save(data)
                
                break
            else:
                flag=1
        if flag==1:
            print(dbname+" does not exist")




     # Adding static data to db needed by harvestor
    def create_static(self):

        f=open('apikey.json')
        for i in f.readlines():
            c=json.loads(i)
            try:
                self.pushdata(c,'apikey')
            except:
                pass
        f=open('subregion.json')
        for i in f.readlines():
            d=json.loads(i)
            try:
                self.pushdata(d,'subregion')
            except:
                pass       

    # Getting the data and setting lock or flag on that item so that it is not accessed by other.
    def getdata(self,dbname):
        while True:
            for i in self.db:
                if dbname==i._name:
                        # Randomly reading data item.Each item is read aproximately equal number of times
                        data = str(random.randint(1,4))
                        extracted =i.get(data)
                        if extracted['flag']==0:
                            try:
                                extracted['flag']=1
                                count=extracted['count']
                                count+=1
                                extracted['count']=count
                                i.save(extracted)
                                print("id: ",data,i._name)
                                return extracted
                            except:
                                print("id: ",data," wait: 30 second sleep")
                                time.sleep(30)
                                pass

    # Releasing the lock or flag after operation on that item is over
    def resetflag(self,column,value,dbname):
        for i in self.db:
            if dbname==i._name:
                for j in i:
                    aim=i.get(j)
                    if aim[column]==value:
                        aim['flag']=0
                        i.save(aim)
