from bs4 import BeautifulSoup as bs
import requests
import json
import ast

target = 'https://enews.epa.gov.tw/Page/B514A5023133ED27'
source = 'https://enews.epa.gov.tw/'

help_target = 'https://www.cwb.gov.tw/V8/C/W/W50_index.html'

def get_list():
    r = requests.get(url=target)
    soup = bs(r.text,'html.parser')
    
    date_tags = soup.find_all('span', class_="date")
    classify_tags = soup.find_all('span', class_="classify")
    title_tags = soup.find_all('h3', class_="ellipsis-item")
    content_tags = soup.find_all('p', class_="ellipsis-item")
    news_list = []
    print(len(date_tags),len(classify_tags),len(title_tags),len(content_tags))
    for a,b,c,d in zip(date_tags[1:],classify_tags[1:],title_tags,content_tags[1:]):
        news_list.append(
            {
                "url": soup.find_all('a', attrs={"title":c.text})[0]['href'],
                "url_title":soup.find_all('a', attrs={"title":c.text})[0]['title'],
                "date":a.text,
                "classify":b.text,
                "title":c.text,
                "content":d.text
            }
        )
    #print(news_list)
    return news_list

def get_help():
    r = requests.get(url='https://www.cwb.gov.tw/Data/js/fcst/W50_Data.js?')
    r.encoding = 'utf-8'
    helper = r.text.replace('var W50_County=','')
    helper_dict = ast.literal_eval(helper)['W50']
    
    content = "\n\n".join(helper_dict["Content"])
    content = "*{}* \n\n".format(helper_dict["Title"]) + content
    content = content + " \n\n更新時間：" + helper_dict["DataTime"]

    #print(helper_dict['Title'])
    #print(helper_dict['Content'])
    
    return content

if __name__ == "__main__":
    print(get_help())