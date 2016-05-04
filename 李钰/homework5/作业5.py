
# coding: utf-8

# In[1]:

import urllib2
from bs4 import BeautifulSoup
import sys


# In[2]:

url = "http://www.hprc.org.cn/wxzl/wxysl/lczf/" 
content = urllib2.urlopen(url).read() 
soup = BeautifulSoup(content, 'html.parser') 
links = soup.find_all('td', {'class', 'bl'})


# In[3]:

links = soup.find_all('td', class_='bl') 
print len(links)


# In[4]:

hyperlinks = [url + i.a['href'].split('./')[1] for i in links]


# In[5]:

hyperlinks


# In[6]:

def crawler(url_i):
    content = urllib2.urlopen(url_i).read().decode('gb18030')  
    soup = BeautifulSoup(content, 'html.parser') 
    year = soup.find('span', {'class', 'huang16c'}).text[:4]
    year = int(year)
    report = ''.join(s.text for s in soup('p'))
    scripts = soup.find_all('script')
    countPage = int(''.join(scripts[1]).split('countPage = ')[1].split('//')[0])
    if countPage == 1:
        pass
    else:
        for i in range(1, countPage):
            url_child = url_i.split('.html')[0] +'_'+str(i)+'.html'
            content = urllib2.urlopen(url_child).read().decode('gb18030') 
            soup = BeautifulSoup(content) 
            report_child = ''.join(s.text for s in soup('p'))
            report = report + report_child
    return year, report


# In[7]:

reports = {}
for link in hyperlinks:
    year, report = crawler(link)
    print year
    reports[year] = report 


# In[8]:

url2016 = 'http://news.xinhuanet.com/fortune/2016-03/05/c_128775704.htm'
content = urllib2.urlopen(url2016).read()
soup = BeautifulSoup(content, 'html.parser') 
report2016 = ''.join(s.text for s in soup('p'))


# In[18]:

with open('D:/anacoda/gov_reports1954-2016.txt', 'wb') as f:
    for r in reports:
        line = str(r)+'\t'+reports[r].replace('\n', '\t') +'\n'
        f.write(line.encode('utf-8'))

