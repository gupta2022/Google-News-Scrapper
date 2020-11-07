import requests
import random
import glob
import pandas as pd
import csv
msgLocation="/home/aditya/Google-News-Scrapper/"
list_labels=["fraud","bribery","defamation","corruption","scam"]
df = pd.DataFrame(columns = ['url', 'tag'])
for x in list_labels:
    files=glob.glob(msgLocation+x+"/*.csv")
    links=[]
    for fl in files:
        data = pd.read_csv(fl)
        for index in data.index:
            t=data["title"][index].lower()
            link=data["link"][index]
            if t.find(x)!=-1 :
                if t.find("accus")!=-1:
                    links.append(link)
                elif t.find("guilty")!=-1:
                    links.append(link)
                elif t.find("arrested")!=-1:
                    links.append(link)
                elif t.find("charged")!=-1:
                    links.append(link)
                elif t.find("file")!=-1:
                    links.append(link)
                elif t.find("court")!=-1:
                    links.append(link)
        #print(data["link"])
    mylist = list(dict.fromkeys(links))
    mylist=random.sample(mylist,k=1772)
    for y in mylist:
        df=df.append({'url':y,'tag':x}, ignore_index = True)
    print(len(mylist))
df.to_csv('urlSet.csv', index=False )
