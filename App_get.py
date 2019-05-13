# coding=UTF-8

import requests
import re
from wordcloud import WordCloud
from wordcloud import WordCloud,ImageColorGenerator
import jieba
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import misc
import imageio

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        #r.encoding = r.apparent_encoding
        r.encoding
        return r.text
    except:
        return ''

def printAPPName(html):
    try:
        pattern = re.compile(r'{"im:name":{"label":(.*?)}, "rights"', re.S)
        APPName = re.findall(pattern, str(html))
        return 'APPName:' + str(APPName)
    except:
        return ''

def fillUnivlist(titles, comments, stars, html):
    try:
        pattern = re.compile(r'"title":{"label":(.*?)}, "content"', re.S) #提取标题
        nbaInfo = re.findall(pattern, str(html)) #提取title

        # findStr = '"title":{"label":'
        # nbaInfo = nbaInfo1[nbaInfo1.find(findStr)+len(findStr):]
        patternFloor = re.compile(r'"content":{"label":(.*?), "attributes":{"type":"text"}}', re.S) #提取content
        floorText = re.findall(patternFloor, str(html))

        patternStar = re.compile(r'"im:rating":{"label":(.*?)}, "id"', re.S)  # 提取星级
        star = re.findall(patternStar, str(html))

        number = len(nbaInfo)
        print(number)
        for i in range(number):
            Info = nbaInfo[i] #利用Tools类移除不想要的格式字符
            if i==0:Info = Info[Info.find('"title":{"label":')+len('"title":{"label":'):]
            Info1 = floorText[i]
            Info2 = star[i]
            titles.append('title:' + Info)
            comments.append('content:' + Info1)
            stars.append('star:' + Info2)
    except:
        return ''

def writeText(titleText, fpath):
    try:
        with open(fpath, 'a', encoding='utf-8') as f:
            f.write(str(titleText)+'\n')
            f.write('\n')
            f.close()
    except:
        return ''

def writeUnivlist(titles, comments, stars, fpath, num):
    with open(fpath, 'a', encoding='utf-8') as f:
        for i in range(num):
            f.write(str(stars[i]) + '\n')
            f.write('*' * 10 + '\n')
            f.write(str(titles[i]) + '\n')
            f.write('*' * 50 + '\n') #输入一行*号
            f.write(str(comments[i]) + '\n')
            f.write('*' * 100 + '\n')
        f.close()

def word_cloud():
    f_comment = open("./Allpick.txt", 'rb')
    words = []
    for line in f_comment.readlines():
        if (len(line)) == 12:
            continue
        A = jieba.cut(line)
        words.append(" ".join(A))
    #print(words)

    #print(final)
    #bk = imread()

    stopwords = ['APPName','[ ]','.',' ','1','3','*','content','star','title',':','"','APPName : [ ] \n','\n','title : \n','* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * \n']
    new_words = []
    for sent in words:
        word_in = sent.split()
        new_word_in = []
        for word in word_in:
            if word in stopwords:
                continue
            else:
                new_word_in.append(word)
        #print(new_word_in)
        new_sent = " ".join(new_word_in)
        new_words.append(new_sent)

    final_words = []
    for sent in new_words:
        sent = sent.split(' ')
        final_words += sent
    final_words_flt = []
    for word in final_words:
        if word == ' ':
            continue
        else:
            final_words_flt.append(word)

    text = " ".join(final_words_flt)

    bk = imageio.imread('./version.png')
    word_pic = WordCloud(font_path='/System/Library/Fonts/PingFang.ttc',mask=bk,width=2000,height=4000,margin=2).generate_from_text(text.lower())
    image_colors = ImageColorGenerator(bk)
    plt.imshow(word_pic.recolor(color_func=image_colors))
    plt.axis('off')
    plt.figure()
    plt.imshow(bk, cmap=plt.cm.gray)
    plt.axis("off")
    word_pic.to_file('./test.png')
    plt.show()



def main():
    count = 0
    url = 'https://itunes.apple.com/rss/customerreviews/page=1/id=587800848/sortby=mostrecent/json?l=en&&cc=cn' #要访问的网址
    output_file = './Allpick.txt' #最终文本输出的文件
    html = getHTMLText(url) #获取HTML
    APPName = printAPPName(html)
    writeText(APPName, output_file)
    for i in range(10):
        i = i + 1
        titles = []
        comments = []
        stars = []
        url = 'https://itunes.apple.com/rss/customerreviews/page=' + str(i) + '/id=587800848/sortby=mostrecent/json?l=en&&cc=cn'
        html = getHTMLText(url)
        fillUnivlist(titles, comments, stars, html)
        writeUnivlist(titles, comments, stars, output_file, len(titles))
        count = count + 1
        print("\r当前进度: {:.2f}%".format(count * 100 / 10), end="")
    word_cloud()

if __name__ == '__main__':
    main()