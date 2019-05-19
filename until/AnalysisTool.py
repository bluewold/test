from pyecharts import Pie
from db.maoyandb.CommentsHelper import CommentHelper
from db.maoyandb.MovieHelper import MovieHelper
from pyecharts import Style
from pyecharts import Geo
import json
from pyecharts import Bar
from collections import Counter
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import matplotlib.pyplot as plt
import jieba
import numpy as np
from PIL import Image
import threading

class AnalysisTool(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(AnalysisTool, "_instance"):
            with AnalysisTool._instance_lock:
                if not hasattr(AnalysisTool, "_instance"):
                    AnalysisTool._instance = object.__new__(cls)
        return AnalysisTool._instance

    def get_star_radis(self,filmname):
        movieid = MovieHelper().select(1,{"name":filmname})
        if(movieid == None):
            return  False
        datalist = CommentHelper().select(conditions={"movieid":movieid})

        rates = []
        attr = ['五星', '四星', '三星', '二星', '一星']
        for data in datalist:
            rates.append(data[2])

        value=[rates.count(5)+rates.count(4.5),
               rates.count(4)+rates.count(3.5),
               rates.count(3)+rates.count(2.5),
               rates.count(2)+rates.count(1.5),
               rates.count(1)+rates.count(0.5)]

        pie = Pie('《流浪地球》评分星级比例', title_pos='center', width=900)
        pie.add('7-17', attr, value, center=[75, 50], is_random=True,
                radius=[30, 75], rosetype='area',
                is_legend_show=False, is_label_show=True)
        pie.render('评分.html')
        return True

    def get_fans_location(self,filmname):
        movieid = MovieHelper().select(1, {"name": filmname})
        if (movieid == None):
            return False
        datalist = CommentHelper().select(conditions={"movieid": movieid})
        citylist = []
        citydatalist=[]
        for data in datalist:
            citydatalist.append(data[3])

        citylist=citydatalist.copy()
        data = None
        with open(r"C:\Users\edwardlee\DeepML\Lib\site-packages\pyecharts\datasets\city_coordinates.json","r",
                  encoding="utf-8") as f:
            citydata =json.loads(f.read())
        new_city  = citydata.copy()


        for city in set(citylist):
            if city == '':
                while city in citylist:
                   citylist.remove(city)
                while city in citydatalist:
                    citydatalist.remove(city)

            count = 0
            for k in citydata.keys():
                count += 1
                if k == city:
                    break
                elif k.startswith(city):
                    new_city[city] = citydata[k]
                    break
                elif k.startswith(city[0:-1]) and len(city) >= 3:
                    new_city[city] = citydata[k]
                    break


            if len(citydata) == count:
                print(city)
                while city in citylist:
                    citylist.remove(city)
                while city in citydatalist:
                    citydatalist.remove(city)

        with open(r"C:\Users\edwardlee\DeepML\Lib\site-packages\pyecharts\datasets\city_coordinates.json", "w",
                 encoding="utf-8") as f:
            f.write(json.dumps(new_city,ensure_ascii=False))

        # 定义样式
        style = Style(
            title_color='#fff',
            title_pos='center',
            width=1200,
            height=600,
            background_color='#404a59'
        )

        data = Counter(citydatalist).most_common()
        print(data)
        # 根据城市数据生成地理坐标图
        geo = Geo('《流浪地球》粉丝位置分布', '数据来源：猫眼-汤小洋采集', **style.init_style)
        attr, value = geo.cast(data)
        geo.add('', attr, value, visual_range=[0, 3500],
                visual_text_color='#fff', symbol_size=15,
                is_visualmap=True, is_piecewise=True, visual_split_number=10)
        geo.render('粉丝位置分布-地理坐标图.html')

        # 根据城市数据生成柱状图
        data_top20 = Counter(citydatalist).most_common(20)  # 返回出现次数最多的20条
        bar = Bar("《流浪地球》粉丝来源排行TOP20", "数据来源：edwardlee采集", title_pos='center', width=1200, height=600)
        attr, value = bar.cast(data_top20)
        bar.add("", attr, value, is_visualmap=True, visual_range=[0, 3500], visual_text_color='#fff',
                is_more_utils=True,
                is_label_show=True)
        bar.render("粉丝来源排行-柱状图.html")

    def get_wordcloud(self,filmname):
        movieid = MovieHelper().select(1, {"name": filmname})
        if (movieid == None):
            return False
        datalist = CommentHelper().select(conditions={"movieid": movieid})
        commentlist = []
        for data in datalist:
            if data[1] != "" or data[1] != ",":
                commentlist.append(data[1])

        comments_after_split = jieba.cut(str(commentlist),cut_all=False)
        wordlist = "".join(comments_after_split)

        stopwords = STOPWORDS.copy()
        stopwords.add("电影")
        stopwords.add("一部")
        stopwords.add("一个")
        stopwords.add("没有")
        stopwords.add("什么")
        stopwords.add("有点")
        stopwords.add("这部")
        stopwords.add("这个")
        stopwords.add("不是")
        stopwords.add("真的")
        stopwords.add("感觉")
        stopwords.add("觉得")
        stopwords.add("还是")
        stopwords.add("但是")
        stopwords.add("就是")


        bg_image = np.array(Image.open( 'bg.jpg'))
        # 设置词云参数，参数分别表示：画布宽高、背景颜色、背景图形状、字体、屏蔽词、最大词的字体大小
        wc = WordCloud(width=2048, height=768, background_color='white', mask=bg_image, font_path='STKAITI.TTF',
                       stopwords=stopwords, max_font_size=800, random_state=50)

        wc.generate_from_text(wordlist)
        plt.imshow(wc)
        plt.axis("off")
        plt.show()

        wc.to_file("词云.jpg")

print(AnalysisTool().get_star_radis("流浪地球"))