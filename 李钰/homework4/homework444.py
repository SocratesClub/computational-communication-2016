
# coding: utf-8

# In[1]:

import urllib2
from bs4 import BeautifulSoup


# In[2]:

url = 'file:///C:/Users/Administrator/Documents/GitHub/computational-communication-2016/data/test.html'
content = urllib2.urlopen(url).read() 
soup = BeautifulSoup(content, 'html.parser') 
soup


# In[3]:

print(soup.prettify())


# In[4]:

for tag in soup.find_all(True):
    print(tag.name)


# In[5]:

soup('head') # or soup.head


# In[6]:

soup('body') # or soup.body


# In[7]:

soup('title')  # or  soup.title


# In[8]:

soup('p')


# In[9]:

soup.p


# In[10]:

soup.title.name


# In[11]:

soup.title.string


# In[12]:

soup.title.text


# In[13]:

soup.title.parent.name


# In[14]:

soup.p


# In[15]:

soup.p['class']


# In[16]:

soup.find_all('p', {'class', 'title'})


# In[17]:

soup.find_all('p', class_= 'title')


# In[18]:

soup.find_all('p', {'class', 'story'})


# In[19]:

soup.find_all('p', {'class', 'story'})[0].find_all('a')


# In[20]:

soup.a


# In[21]:

soup('a')


# In[22]:

soup.find(id="link3")


# In[23]:

soup.find_all('a')


# In[24]:

soup.find_all('a', {'class', 'sister'}) # compare with soup.find_all('a')


# In[25]:

soup.find_all('a', {'class', 'sister'})[0]


# In[26]:

soup.find_all('a', {'class', 'sister'})[0].text


# In[27]:

soup.find_all('a', {'class', 'sister'})[0]['href']


# In[28]:

soup.find_all('a', {'class', 'sister'})[0]['id']


# In[29]:

soup.find_all(["a", "b"])


# In[30]:

print(soup.get_text())


# In[31]:

url = "http://mp.weixin.qq.com/s?__biz=MzA3MjQ5MTE3OA==&mid=206241627&idx=1&sn=471e59c6cf7c8dae452245dbea22c8f3&3rd=MzA3MDU4NTYzMw==&scene=6#rd"
content = urllib2.urlopen(url).read() #获取网页的html文本
soup = BeautifulSoup(content, 'html.parser') 
print soup.title.text
print soup.find('div', {'class', 'rich_media_meta_list'}).find(id = 'post-date').text
print soup.find('div', {'class', 'rich_media_content'}).get_text()


# In[32]:

from IPython.display import display_html, HTML
HTML('<iframe src=http://bbs.tianya.cn/list.jsp?item=free&nextid=%d&order=8&k=PX width=1000 height=500></iframe>')
# the webpage we would like to crawl


# In[33]:

page_num = 0
url = "http://bbs.tianya.cn/list.jsp?item=free&nextid=%d&order=8&k=PX" % page_num
content = urllib2.urlopen(url).read() #获取网页的html文本
soup = BeautifulSoup(content, "lxml") 
articles = soup.find_all('tr')


# In[34]:

print articles[0]


# In[35]:

print articles[1]


# In[36]:

len(articles[1:])


# In[37]:

for t in articles[1].find_all('td'): print t


# In[38]:

td = articles[1].find_all('td')


# In[39]:

print td[0]


# In[40]:

print td[0]


# In[41]:

print td[0].text


# In[42]:

print td[0].text.strip()


# In[43]:

print td[0].a['href']


# In[44]:

print td[1]


# In[45]:

print td[2]


# In[46]:

print td[3]


# In[47]:

print td[4]


# In[48]:

records = []
for i in articles[1:]:
    td = i.find_all('td')
    title = td[0].text.strip()
    title_url = td[0].a['href']
    author = td[1].text
    author_url = td[1].a['href']
    views = td[2].text
    replies = td[3].text
    date = td[4]['title']
    record = title + '\t' + title_url+ '\t' + author + '\t'+ author_url + '\t' + views+ '\t'  + replies+ '\t'+ date
    records.append(record)


# In[49]:

print records[2]


# In[50]:

def crawler(page_num, file_name):
    try:
        # open the browser
        url = "http://bbs.tianya.cn/list.jsp?item=free&nextid=%d&order=8&k=PX" % page_num
        content = urllib2.urlopen(url).read() #获取网页的html文本
        soup = BeautifulSoup(content, "lxml") 
        articles = soup.find_all('tr')
        # write down info
        for i in articles[1:]:
            td = i.find_all('td')
            title = td[0].text.strip()
            title_url = td[0].a['href']
            author = td[1].text
            author_url = td[1].a['href']
            views = td[2].text
            replies = td[3].text
            date = td[4]['title']
            record = title + '\t' + title_url+ '\t' + author + '\t'+                         author_url + '\t' + views+ '\t'  + replies+ '\t'+ date
            with open(file_name,'a') as p: # '''Note'''：Ａppend mode, run only once!
                        p.write(record.encode('utf-8')+"\n") ##!!encode here to utf-8 to avoid encoding

    except Exception, e:
        print e
        pass


# In[51]:

# crawl all pages
for page_num in range(10):
    print (page_num)
    crawler(page_num, 'C:/Users/Administrator/Documents/GitHub/computational-communication-2016/data/tianya_bbs_threads_list.txt') 


# In[52]:

import pandas as pd

df = pd.read_csv( 'C:/Users/Administrator/Documents/GitHub/computational-communication-2016/data/tianya_bbs_threads_list.txt', sep = "\t", header=None)
df[:2]


# In[53]:

len(df)


# In[54]:

df=df.rename(columns = {0:'title', 1:'link', 2:'author',3:'author_page', 4:'click', 5:'reply', 6:'time'})
df[:2]


# In[55]:

len(df.link)


# In[56]:

df.author_page[:5]


# In[57]:

def author_crawler(url, file_name):
    try:
        content = urllib2.urlopen(url).read() #获取网页的html文本
        soup = BeautifulSoup(content, "lxml")
        link_info = soup.find_all('div', {'class', 'link-box'})
        followed_num, fans_num = [i.a.text for i in link_info]
        try:
            activity = soup.find_all('span', {'class', 'subtitle'})
            post_num, reply_num = [j.text[2:] for i in activity[:1] for j in i('a')]
        except:
            post_num, reply_num = 1, 0
        record =  '\t'.join([url, followed_num, fans_num, post_num, reply_num])
        with open(file_name,'a') as p: # '''Note'''：Ａppend mode, run only once!
                    p.write(record.encode('utf-8')+"\n") ##!!encode here to utf-8 to avoid encoding

    except Exception, e:
        print e, url
        record =  '\t'.join([url, 'na', 'na', 'na', 'na'])
        with open(file_name,'a') as p: # '''Note'''：Ａppend mode, run only once!
                    p.write(record.encode('utf-8')+"\n") ##!!encode here to utf-8 to avoid encoding
        pass


# In[58]:

for k, url in enumerate(df.author_page):
    if k % 10==0:
        print k
    author_crawler(url, 'C:/Users/Administrator/Documents/GitHub/computational-communication-2016/data/tianya_bbs_threads_author_info.txt') 


# In[61]:

url = df.author_page[1]
content = urllib2.urlopen(url).read() #获取网页的html文本
soup1 = BeautifulSoup(content, "lxml") 


# In[63]:

user_info = soup.find('div',  {'class', 'userinfo'})('p')
area, nid, freq_use, last_login_time, reg_time = [i.get_text()[4:] for i in user_info]
print area, nid, freq_use, last_login_time, reg_time 

link_info = soup1.find_all('div',  {'class', 'link-box'})
followed_num, fans_num = [i.a.text for i in link_info]
print followed_num, fans_num


# In[64]:

activity = soup1.find_all('span', {'class', 'subtitle'})
post_num, reply_num = [j.text[2:] for i in activity[:1] for j in i('a')]
print post_num, reply_num


# In[65]:

print activity[2]


# In[66]:

link_info = soup.find_all('div', {'class', 'link-box'})
followed_num, fans_num = [i.a.text for i in link_info]
print followed_num, fans_num


# In[67]:

link_info[0].a.text


# In[68]:

df.link[2]
Out[13]:


# In[69]:

url = 'http://bbs.tianya.cn' + df.link[2]
url


# In[70]:

from IPython.display import display_html, HTML
HTML('<iframe src=http://bbs.tianya.cn/post-free-2848797-1.shtml width=1000 height=500></iframe>')
# the webpage we would like to crawl


# In[71]:

post = urllib2.urlopen(url).read() #获取网页的html文本
post_soup = BeautifulSoup(post, "lxml") 
#articles = soup.find_all('tr')


# In[72]:

print (post_soup.prettify())[:1000]


# In[73]:

pa = post_soup.find_all('div', {'class', 'atl-item'})
len(pa)


# In[74]:

print pa[0]


# In[75]:

print pa[1]


# In[76]:

print pa[89]


# In[77]:

print pa[0].find('div', {'class', 'bbs-content'}).text.strip()


# In[78]:

print pa[87].find('div', {'class', 'bbs-content'}).text.strip()


# In[79]:

pa[1].a


# In[80]:

print pa[0].find('a', class_ = 'reportme a-link')


# In[81]:

print pa[0].find('a', class_ = 'reportme a-link')['replytime']


# In[82]:

print pa[0].find('a', class_ = 'reportme a-link')['author']


# In[83]:

for i in pa[:10]:
    p_info = i.find('a', class_ = 'reportme a-link')
    p_time = p_info['replytime']
    p_author_id = p_info['authorid']
    p_author_name = p_info['author']
    p_content = i.find('div', {'class', 'bbs-content'}).text.strip()
    p_content = p_content.replace('\t', '')
    print p_time, '--->', p_author_id, '--->', p_author_name,'--->', p_content, '\n'


# In[84]:

post_soup.find('div', {'class', 'atl-pages'})#['onsubmit']


# In[85]:

post_pages = post_soup.find('div', {'class', 'atl-pages'})
post_pages = post_pages.form['onsubmit'].split(',')[-1].split(')')[0]
post_pages


# In[86]:

url = 'http://bbs.tianya.cn' + df.link[2]
url_base = ''.join(url.split('-')[:-1]) + '-%d.shtml'
url_base


# In[87]:

def parsePage(pa):
    records = []
    for i in pa:
        p_info = i.find('a', class_ = 'reportme a-link')
        p_time = p_info['replytime']
        p_author_id = p_info['authorid']
        p_author_name = p_info['author']
        p_content = i.find('div', {'class', 'bbs-content'}).text.strip()
        p_content = p_content.replace('\t', '').replace('\n', '')#.replace(' ', '')
        record = p_time + '\t' + p_author_id+ '\t' + p_author_name + '\t'+ p_content
        records.append(record)
    return records

import sys
def flushPrint(s):
    sys.stdout.write('\r')
    sys.stdout.write('%s' % s)
    sys.stdout.flush()


# In[88]:

url_1 = 'http://bbs.tianya.cn' + df.link[10]
content = urllib2.urlopen(url_1).read() #获取网页的html文本
post_soup = BeautifulSoup(content, "lxml") 
pa = post_soup.find_all('div', {'class', 'atl-item'})
b = post_soup.find('div', class_= 'atl-pages')
b


# In[89]:

url_1 = 'http://bbs.tianya.cn' + df.link[0]
content = urllib2.urlopen(url_1).read() #获取网页的html文本
post_soup = BeautifulSoup(content, "lxml") 
pa = post_soup.find_all('div', {'class', 'atl-item'})
a = post_soup.find('div', {'class', 'atl-pages'})
a


# In[90]:

a.form


# In[91]:

if b.form:
    print 'true'
else:
    print 'false'


# In[101]:

import random
import time

def crawler(url, file_name):
    try:
        # open the browser
        url_1 = 'http://bbs.tianya.cn' + url
        content = urllib2.urlopen(url_1).read() #获取网页的html文本
        post_soup = BeautifulSoup(content, "lxml") 
        # how many pages in a post
        post_form = post_soup.find('div', {'class', 'atl-pages'})
        if post_form.form:
            post_pages = post_form.form['onsubmit'].split(',')[-1].split(')')[0]
            post_pages = int(post_pages)
            url_base = '-'.join(url_1.split('-')[:-1]) + '-%d.shtml'
        else:
            post_pages = 1
        # for the first page
        pa = post_soup.find_all('div', {'class', 'atl-item'})
        records = parsePage(pa)
        with open(file_name,'a') as p: # '''Note'''：Ａppend mode, run only once!
            for record in records:    
                p.write('1'+ '\t' + url + '\t' + record.encode('utf-8')+"\n") 
        # for the 2nd+ pages
        if post_pages > 1:
            for page_num in range(2, post_pages+1):
                time.sleep(random.random())
                flushPrint(page_num)
                url2 =url_base  % page_num
                content = urllib2.urlopen(url2).read() #获取网页的html文本
                post_soup = BeautifulSoup(content, "lxml") 
                pa = post_soup.find_all('div', {'class', 'atl-item'})
                records = parsePage(pa)
                with open(file_name,'a') as p: # '''Note'''：Ａppend mode, run only once!
                    for record in records:    
                        p.write(str(page_num) + '\t' +url + '\t' + record.encode('utf-8')+"\n") 
        else:
            pass
    except Exception, e:
        print e
        pass


# In[102]:

url = 'http://bbs.tianya.cn' + df.link[2]
file_name = 'C:/Users/Administrator/Documents/GitHub/computational-communication-2016/data/tianya_bbs_threads_test.txt'
crawler(url, file_name)


# In[103]:

for k, link in enumerate(df.link):
    flushPrint(link)
    if k % 10== 0:
        print 'This it the post of : ' + str(k)
    file_name='C:/Users/Administrator/Documents/GitHub/computational-communication-2016/data/tianya_bbs_threads_test.txt'
    crawler(link, file_name)


# In[105]:

dtt = []
with open(='C:/Users/Administrator/Documents/GitHub/computational-communication-2016/data/tianya_bbs_threads_test.txt', 'r') as f:
    for line in f:
        pnum, link, time, author_id, author, content = line.replace('\n', '').split('\t')
        dtt.append([pnum, link, time, author_id, author, content])
len(dtt)


# In[107]:

dtt = []
with open('C:/Users/Administrator/Documents/GitHub/computational-communication-2016/data/tianya_bbs_threads_test.txt', 'r') as f:
    for line in f:
        pnum, link, time, author_id, author, content = line.replace('\n', '').split('\t')
        dtt.append([pnum, link, time, author_id, author, content])
len(dtt)


# In[108]:

dt = pd.DataFrame(dtt)
dt[:5]


# In[109]:

dt=dt.rename(columns = {0:'page_num', 1:'link', 2:'time', 3:'author',4:'author_name', 5:'reply'})
dt[:5]


# In[110]:

dt.reply[:100]

