# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 19:20:26 2018

@author: user2
"""

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import urllib
import ast


USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}



def fetch_results(trend_term):
    assert isinstance(trend_term, str), 'Trend term must be a string'
    escaped_trend_term = trend_term.replace(' ', '+')
    
    twitter_url =  'https://twitter.com/search?f=tweets&vertical=default&q={}&src=tren'.format(trend_term)
    response = requests.get(twitter_url, headers=USER_AGENT)
    response.raise_for_status()
    
    return trend_term, response.text

    
    
def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
    
    found_result = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'tweet'})
    
    for result in result_block:
        handle = result.find('span', attrs={'class': 'FullNameGroup'})
        tweet =  result.find('p', attrs={'class':'TweetTextSize'})
        if handle and tweet:
            handle = handle.get_text()
            tweet = tweet.get_text()
            if handle != '#':
                found_result.append({'handle': handle, 'rank': rank, 'tweet': tweet})
                rank += 1
    return found_result

 
    
def scrape(trend_term):
    try:
        keyword, html = fetch_results(trend_term)
        result = parse_results(html, keyword)
        return result
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")
        
neutral = 0
neg = 0
pos = 0       
if __name__ == '__main__':
    trends =['lazynigerianyouths']
    data = []
    
    for trend in trends:
        try:
            results = scrape(trend)
            for result in results:
                data.append(result)
        except Exception as e:
            print(e)
        finally:
            time.sleep(2)
    new_data = pd.DataFrame(data)
    #print(new_data)
    
    ana = new_data['tweet']
    print(type(ana))
    for tweets in ana:
        data = urllib.parse.urlencode({"text": tweets}).encode("utf-8")
        u = urllib.request.urlopen("http://text-processing.com/api/sentiment/", data)
        the_page = u.read()
        the_page = the_page.decode("utf-8")
        
        the_page = dict(ast.literal_eval(the_page))
        print(the_page['label'])
        outcome = the_page['label']
        
        if (outcome == 'neutral'):
            neutral += 1
        elif (outcome == 'pos'):
            pos += 1
        else:
            neg += 1
            
        #print(the_page['label'])
        
    #print(new_data['handle'])
print('Total negative is {}'.format(neg))        
print('Total positive is {}'.format(pos))        
print('Total neutral is {}'.format(neutral))        
    

    
    
    
    
    
    
    