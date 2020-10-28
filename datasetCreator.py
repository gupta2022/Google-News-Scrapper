import requests
import glob
import pandas as pd
import csv

msgLocation="/home/aditya/Google-News-Scrapper/"
list_labels=["fraud","bribery","defamation","corruption","scam" ,"defaulter"]
for x in list_labels:
    files=glob.glob(msgLocation+x+"/*.csv")
    for fl in files:
        data = pd.read_csv(fl)
        print(data)