from importlib.resources import contents
import requests 
from bs4 import BeautifulSoup
from urllib.request import urlretrieve 



    target_url = 'https://movies.yahoo.com.tw/movie_intheaters.html'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.release_movie_name a')):
        if index == 20:
            return content       
        title = data.text
        content += '{}\n'.format(title)
        print(content)
