import requests
import os
import json
import TwitterSecrets


bearer_token = TwitterSecrets.Bearer_Token

#search_url = "https://api.twitter.com/2/tweets/search/recent?query=covid&expansions=geo.place_id&tweet.fields=geo&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type"
# search_url = "https://api.twitter.com/2/tweets/search/recent?query=covid&expansions=geo.place_id,referenced_tweets.id&place.fields=country&tweet.fields=text,created_at"

#search_url = "https://api.twitter.com/2/tweets/search/recent?query=covid&expansions=referenced_tweets.id,geo.place_id&tweet.fields=text,created_at,geo&place.fields=geo,country&end_time=2022-04-30T19:05:33Z"
search_url = "https://api.twitter.com/2/tweets/search/recent?expansions=author_id&tweet.fields=text,created_at,lang,source&user.fields=location&max_results=10"

#query_params = {'query': 'covid','max_results':10,'user.fields':'description','tweet.fields':'created_at','expansions':'geo.place_id','place.fields':'country'}



def getParam(date):
    starttime = date+ 'T00:00:00Z'
    endtime = date + 'T23:59:59Z'
    query_params = {'query':'covid','start_time':starttime,'end_time':endtime}
    return query_params
    

#From each source, also need to capture at least 100 records 
# (for CSV/JSON sources you need to capture at least 1000), and each record must have at least 5 “fields” associated with it.
#query_params = {'query': 'covid','tweet.fields':'text','max_results':10,'expansions':'author_id','user.fields':'location'}


# 'query':''




#For data from APIs or web pages you must cache the raw results 
# (JSON or HTML) you fetch from the source. You will need to demonstrate your use of caching for the Data Checkpoint milestone.


def saveCaching(data, filename):
    '''
    input 
    json data:the data using api
    file name:using the year get from the page as the cache file name
    '''
    # filename = 'cache/'+date +'.json'
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)
    
        
        
def loadCaching(date):
    '''
    
    '''
    pass
    

    
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    
    # set the date needed yyyy-mm-dd
    date = '2022-4-28'
    filename = 'cache/'+date +'.json'
    #see if in the cache if in use the cache if not get the json data using api
    
    try:
        with open(filename,'r',encoding='utf-8') as json_file:    
  
            json_data = json.load(json_file)
        print('load cache successfully')
    except:
        query_params = getParam(date)
        json_data = connect_to_endpoint(search_url, query_params)
        saveCaching(json_data, filename)
        print("write json file success!")
    
    json_indent = json.dumps(json_data, indent=4, sort_keys=True)
        
    
    print(json_indent)
    


if __name__ == "__main__":
    main()