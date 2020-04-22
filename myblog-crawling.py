# pip install bs4 # For BeautifulSoup
# https://assaeunji.github.io/
# https://assaeunji.github.io/page2/
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

#%%
# 하나만 긁어보기
req = requests.get("https://assaeunji.github.io/")
html = req.text
soup = BeautifulSoup(html, "html.parser") # BeautifulSoup으로 htlml소스를 python 객체로 변환
my_titles = soup.select("article > header > h1 > a ") #posts > article:nth-child(1) > header > h1 > a


#%%
# 1. Max page 출력
# page number 구조
# CSS selector: content > nav > a:nth-child(4)
# <a class="page-number" href="/page2">2</a>
maxpage = int(soup.findAll("a",{"page-number"})[len(soup.findAll("a",{"page-number"}))-1].string)
print(maxpage)


#%%
#------------------------------------------------------------------
# http://www.hanbit.co.kr/channel/category/category_view.html?cms_code=CMS6168044195
# titles 구조 -> BeautifulSoup.select

# categories 구조 -> BeautifulSoup.findAll
# <span itemprop="name">AWS</span>

# wordcounts 구조
# <span title="Words count in article">4420 </span>

# 생성일 구조
# <time title="Post created" itemprop="dateCreated datePublished" datetime="2020-03-30T00:00:00+00:00">
#                 2020-03-30
#               </time>
#------------------------------------------------------------------
whole_source = ""
my_categories = []
my_titles     = []
my_wordcounts = []
my_times      = []

for pagenum in range(maxpage):
    if pagenum > 0:
        URL  = "https://assaeunji.github.io/"+"page"+str(pagenum+1)+"/"
    else:
        URL  = "https://assaeunji.github.io/"
    raw  = requests.get(URL)
    whole_source = whole_source + raw.text

soup = BeautifulSoup(whole_source,'html.parser')
find_categories = soup.findAll("span",{"itemprop":"name"})
find_titles     = soup.select("article > header > h1 > a ")
find_wordcounts = soup.findAll("span",{"title":"Words count in article"})
find_times      = soup.findAll("time",{"title":"Post created"})

for category in find_categories:
    my_categories.append(category.text.strip())

for title in find_titles:
    my_titles.append(title.text.strip())

for wordcount in find_wordcounts:
    my_wordcounts.append(int(wordcount.text.strip()))

for time in find_times:
    my_times.append(time.text.strip())


#%%
col_names = ['categories','titles','wordcounts','times']
blog_stat = pd.DataFrame(np.array([my_categories,my_titles,my_wordcounts,my_times]).T, columns=col_names)
blog_stat.head(3)
blog_stat.info()
blog_stat['wordcounts'] = pd.to_numeric(blog_stat['wordcounts'])
blog_stat['times']     = blog_stat['times'].apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"))

#%%
#------------------------------------------------------------------
# 누적 통계량
print("누적 카테고리수:{}".format(blog_stat['categories'].value_counts().shape[0]))
print("누적 포스팅수: {}".format(blog_stat.shape[0]))
print("누적 단어수: {}".format(np.sum(blog_stat['wordcounts'])))

#%%
time_labels=list(blog_stat['times'].apply(lambda x: x.strftime("%y-%m-%d")))

plt.subplot(2,1,1)
plt.bar(blog_stat['categories'].value_counts().index,blog_stat['categories'].value_counts(),
alpha=.5,color="red")
plt.yticks(range(6))
plt.title("Number of Posts by Categories")
plt.subplot(2,1,2)
plt.bar(time_labels,my_wordcounts,alpha=.5)
plt.title("Word Counts by Days")
plt.xticks(rotation=300)
plt.yticks(np.linspace(0,10000,11))
plt.vlines(x=13.5,ymin=0,ymax=11000,linestyles="--")
plt.subplots_adjust(hspace = 0.5, wspace = 0.3)
# plt.savefig("../assaeunji.github.io/images/march-blog-stat.png")

#%%
#------------------------------------------------------------------
# 이번 달만 추출
THIS_MONTH = 3

cond1 = blog_stat['times'].apply(lambda x: x.year) == 2020 
cond2 = blog_stat['times'].apply(lambda x: x.month)== THIS_MONTH
THIS_MONTH_blog_stat = blog_stat[cond1&cond2]
#%%
#------------------------------------------------------------------
# 이번달 통계량
THIS_MONTH_labels     = list(THIS_MONTH_blog_stat['times'].apply(lambda x: x.strftime("%m-%d")))
THIS_MONTH_wordcounts = list(THIS_MONTH_blog_stat['wordcounts'])

print(str(THIS_MONTH)+"월 카테고리수:{}".format(THIS_MONTH_blog_stat['categories'].value_counts().shape[0]))
print(str(THIS_MONTH)+"월 포스팅수: {}".format(THIS_MONTH_blog_stat.shape[0]))
print(str(THIS_MONTH)+"월 단어수: {}".format(np.sum(THIS_MONTH_blog_stat['wordcounts'])))

#%%
plt.subplot(2,1,1)
plt.bar(THIS_MONTH_blog_stat['categories'].value_counts().index,THIS_MONTH_blog_stat['categories'].value_counts(),
alpha=.5,color="red")
plt.yticks(range(6))
plt.title("Number of Posts by Categories")
plt.subplot(2,1,2)
plt.bar(THIS_MONTH_labels,THIS_MONTH_wordcounts,alpha=.5)
plt.title("Word Counts by Days")
plt.xticks(rotation=300)
plt.yticks(np.linspace(0,10000,11))
plt.subplots_adjust(hspace = 0.5, wspace = 0.3)

TODAY_MONTH=datetime.datetime.strftime(datetime.datetime.now(), "%b").lower()
plt.savefig("../assaeunji.github.io/images/"+TODAY_MONTH+"-blog-stat.png")
