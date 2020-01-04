from bs4 import BeautifulSoup as bs
import requests
import json

target = 'https://enews.epa.gov.tw/Page/B514A5023133ED27'
source = 'https://enews.epa.gov.tw/'

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

if __name__ == "__main__":
    print(get_list())