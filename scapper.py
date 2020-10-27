# import the needed libraries
import requests
import pandas as pd
import time # for timing script
import xml.etree.ElementTree as ET # built in library

def clean_url(searched_item,data_filter):
    """
    OUTPUT : url to be fecthed for the searched_item and data_filter
     ---------------------------------------------------
    Parameters: 
    'today' - get headlines of the news that are released only in today 
    'this_week' - get headlines of the news that are released in this week 
    'this month' - news released in this month 
    'this_year' - news released in this year
    number : int/str input for number of days ago
    or '' blank to get all data
    """
    x =pd.datetime.today()
    today =str(x)[:10]
    yesterday = str(x + pd.Timedelta(days=-1))[:10]
    this_week = str(x + pd.Timedelta(days=-7))[:10]
    if data_filter == 'today':
        time = 'after%3A' + yesterday
    elif data_filter == 'this_week':
        time = 'after%3A'+ this_week + '+before%3A' + today
    elif data_filter == 'this_year':
        time = 'after%3A'+str(x.year -1)
    elif str(data_filter).isdigit():
        temp_time2= str(x + pd.Timedelta(days=-int(data_filter)))[:10]
        temp_time = str(x + pd.Timedelta(days=-int(data_filter)-90))[:10]
        print (temp_time)
        time =  'after%3A'+ temp_time + '+before%3A' + temp_time2
    else:
        time=''
    url = f'https://news.google.com/rss/search?q={search_term}+'+time+'&hl=en-US&gl=US&ceid=US%3Aen'
    print (url)
    return url

# clear the description
def get_text(x):
    start = x.find('<p>')+3
    end = x.find('</p>')
    return x[start:end]

def get_news(search_term, data_filter=None):
    """
    Search through Google News with the "search_term" and get the headlines 
     and the contents of the news that was released today, this week, this month, 
    or this year ("date_filter"). 
    """
    
    url = clean_url(search_term, data_filter)
    response = requests.get(url)
    # get the root directly as we have text file of string now
    root= ET.fromstring(response.text)
    #get the required data
    title = [i.text for i in root.findall('.//channel/item/title') ]
    link = [i.text for i in root.findall('.//channel/item/link') ]
    description = [i.text for i in root.findall('.//channel/item/description') ]
    pubDate = [i.text for i in root.findall('.//channel/item/pubDate') ]
    source = [i.text for i in root.findall('.//channel/item/source') ]
    # clear the description
    short_description = list(map(get_text,description))
    
    # set the data frame
    df = pd.DataFrame({'title':title, 'link':link, 'description':short_description,'date':pubDate,'source':source })
    # adjust the date column
    df.date = pd.to_datetime(df.date, unit='ns')
    # for saving purpose uncomment the below
    df.to_csv(f'scam/{search_term}_news.csv',mode ='a', encoding='utf-8-sig' , index=False)
    return df

if __name__ == "__main__":
    
    list_of_topics=['accused of scam','found guilty in scam','arrested for scam','accused of scam in india','found guilty in scam in india','arrested for scam in india']
    for search_term in list_of_topics:
        #search_term = str(input('Enter your search term here: '))
        print(search_term)
        start = time.time()
        for i in range(0,40):
            data = get_news(search_term, data_filter=(90*i))
        end = time.time()-start
        print("Execution time", end)

#get_news('scam in corporations','this_year')
#https://news.google.com/rss/search?q=scam%20in%20india+after%3A2016-10-18+before%3A2016-10-25&hl=en-US&gl=US&ceid=US%3Aen