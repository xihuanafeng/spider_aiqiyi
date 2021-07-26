# -*- coding: UTF-8 -*-
# @Time : 2021/7/26 10:06
# @Author : xihuanafeng
# @File : aiqiyi_comments.py
# @Software : PyCharm

import requests
import re
import time
import random
import jieba
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import matplotlib.font_manager as font_manager
from PIL import Image
from wordcloud import WordCloud


comments = []
# 模型安装

'''
 *  name:  not_empty:数据筛选
 *  para:   NONE
 *  return: 
 *  return_lx : 
 *  writer: xihuanafeng
 *  function: 定义筛选规则，去除空, :和开头的，
 *  time:   2021/7/25
'''


def not_empty(s):
    return s and s.strip() and s.strip(':') and s.strip(',')


'''
 *  name:  comment_clear:数据整理函数
 *  para:  评论数据
 *  return: 整理好的评论数据
 *  return_lx : str
 *  writer: xihuanafeng
 *  function: 去除评论中的字母表情之类的数据
 *  time:   2021/7/25
'''


def comment_clear(content):
    comment_clear_list = re.sub(r"</?(.+?)>|&nbsp;|\t|\r", "", content)
    comment_clear_list = re.sub(r"\n", " ", comment_clear_list)
    clear_comment = re.sub('[^\u4e00-\u9fa5^a-z^A-Z^0-9]', '', comment_clear_list)
    return clear_comment


'''
 *  name:  分词函数
 *  para:  需要分词的句子或文本：str
 *  return: 分词后的数据
 *  return_lx : list
 *  writer: xihuanafeng
 *  function: 分词
 *  time:   2021/7/25
'''


def fenci(text):
    '''
    利用jieba进行分词
    参数 text:需要分词的句子或文本
    return：分词结果
    '''

    jieba.load_userdict('add_words.txt')    # 添加自定义字典
    # seg = jieba.lcut(text, cut_all=False)
    seg = jieba.lcut(text, cut_all=False)  # 直接返回list
    return seg


'''
 *  name:  停用分词
 *  para:  
 *  return: 
 *  return_lx : 
 *  writer: xihuanafeng
 *  function: 
 *  time:   2021/7/25
'''


def stopwordslist(file_path):
    stopwords = [line.strip() for line in open(file_path, encoding='UTF-8').readlines()]
    return stopwords


'''
 *  name:  去除停用词
 *  para:  
 *  return: 
 *  return_lx : 
 *  writer: xihuanafeng
 *  function: 
 *  time:   2021/7/25
'''


def movestopwords(sentence, stopwords, counts):
    '''
    去除停用词,统计词频
    参数 file_path:停用词文本路径 stopwords:停用词list counts: 词频统计结果
    return：None
    '''
    out = []
    for word in sentence:
        if word not in stopwords:
            if len(word) != 1:
                counts[word] = counts.get(word, 0) + 1
    return None


'''
 *  name:  绘制词频统计表
 *  para:  counts: 词频统计结果 num:绘制topN
 *  return: None
 *  return_lx : None
 *  writer: xihuanafeng
 *  function: 
 *  time:   2021/7/25
'''


def drawcounts(counts, num):
    '''
    绘制词频统计表
    参数 counts: 词频统计结果 num:绘制topN
    return：none
    '''
    x_aixs = []
    y_aixs = []
    c_order = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    # print(c_order)
    for c in c_order[:num]:
        x_aixs.append(c[0])
        y_aixs.append(c[1])

    # 设置显示中文
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    plt.bar(x_aixs, y_aixs)
    plt.title('词频统计结果')
    plt.show()


'''
 *  name:  根据词频绘制词云图
 *  para:  参数 word_f:统计出的词频结果
 *  return: None
 *  return_lx : None
 *  writer: xihuanafeng
 *  function: 
 *  time:   2021/7/25
'''

def drawcloud(word_f):

    # 加载背景图片
    cloud_mask = np.array(Image.open('cloud.png'))
    # 忽略显示的词
    st = {"东西", "这是"}
    # 生成wordcloud对象
    wc = WordCloud(background_color='white',
                   mask=cloud_mask,
                   max_words=150,
                   font_path='simhei.ttf',
                   min_font_size=10,
                   max_font_size=100,
                   width=400,
                   relative_scaling=0.3,
                   stopwords=st)
    wc.fit_words(word_f)
    wc.to_file('pic.png')

'''
 *  name:  使用hub对评论进行内容分析
 *  para:  参数 word_f:统计出的词频结果
 *  return: None
 *  return_lx : None
 *  writer: xihuanafeng
 *  function: 
 *  time:   2021/7/25
'''

if __name__=='__main__':
    all_page = 5
    for page in range(1, all_page):
        base_url = f'https://sns-comment.iqiyi.com/v3/comment/get_comments.action?agent_type=118&agent_version=9.11.5&authcookie=b3YOhPajFgcajWm1pRZnX5IKGWSA006JVVqm1Y9DVNFvTM9zm17t9ee5a61JpgV2TYcsg59&business_type=17&channel_id=6&content_id=16099208800&page_size=40&types=time&page={page}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',
            'Referer': 'https://www.iqiyi.com/v_19ry9w7eh8.html',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site'
        }
        # 为实时加载出来的一般为json数据
        request = requests.get(base_url, headers=headers)
        response = request.json()
        time.sleep(random.random() * 2)
        # 获取评论数据，根据page_size 得，一次获得40条，page_size中40,comments=40条,只要第一页是10条
        all_comments_list = response['data']['comments']
        if page == 1:
            for i in range(10):
                comments.append(all_comments_list[i]['content'])
                # print(all_comments_list[i]['content'])
        else:
            for j in range(39):
                # 因为存在有几个是没有content的情况，所以需要判断一下
                if 'content' in all_comments_list[j]:
                    comments.append(all_comments_list[j]['content'])
                    # print(all_comments_list[j]['content'])
                else:
                    comments.append(' ')
    # 去除列表中一些异常的数据
    comments = list(filter(not_empty, comments))
    print('共爬取了%d条数据' % (len(comments)))
    with open('aiqiyi.text', 'w', encoding='utf-8') as f:
        for item in comments:
            over_clear = comment_clear(item)
            f.write(over_clear + '\n')
    print('保存数据完毕')
    file_comment = open('aiqiyi.text', 'r', encoding='utf-8')
    counts = {}
    for line in file_comment:
        words = fenci(line)
        stopwords = stopwordslist('cn_stopwords.txt')
        movestopwords(words, stopwords, counts)
    drawcounts(counts, 10)  # 绘制top10 高频词
    drawcloud(counts)   # 绘制词云
    f.close()
    print('完毕')
    file_path = 'aiqiyi.text'
