
# coding: utf-8

# In[1]:

import urllib2
from bs4 import BeautifulSoup


# In[2]:

url = "http://mp.weixin.qq.com/s?src=3&timestamp=1461155424&ver=1&signature=wpcGObnqIVC5ogRAr6rbCFGCy15HUuSglcAwd52fUzU7K4oYgvKdvpR512DQ1X4fY-TL8VT7r-mfvtcjcQYlKlk13NwwUYN9ZrV00Me7rh6kGY2IenJ7yeQFVGYgtVO8NO-cSHa3LbPF5UmJRY3ZSA=="
content = urllib2.urlopen(url).read() #获取网页的html文本
soup = BeautifulSoup(content, 'html.parser') 


# In[3]:

print soup.title.text
print soup.find('div', {'class', 'rich_media_meta_list'}).find(id = 'post-date').text
print soup.find('div', {'class', 'rich_media_content'}).get_text()

