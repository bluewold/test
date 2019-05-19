import datetime
import json
import re
import time
from datetime import timedelta
import lxml
import requests
from lxml import html
from db.maoyandb.CommentsHelper import CommentHelper
from db.maoyandb.MovieHelper import MovieHelper
from db.maoyandb.TagHelper import TagHelper
from db.maoyandb.ActorHelper import  ActorHelper
from db.maoyandb.TagMovieHelper import TagMovieHelper
from db.maoyandb.TagActorHelper import TagActorHelper
from db.maoyandb.MovieActorHelper import MovieActorHelper
from until.BloomFilter import BloomFilter
from until.helptool import HelpTool
import threading
import gevent
import gevent.monkey

#gevent.monkey.patch_all()

class maoyan:

    '''def get_comment(self,urllist,filmid):
        commentlist = []
        for url in urllist:
            if not BloomFilter().contains(url):
                try:
                    time.sleep(1)
                    response = requests.get(url,headers=HelpTool().get_header()).content.decode("utf-8","ignore")
                    jsonObj = json.loads(response)
                    datas = jsonObj["data"]
                    data_comments = datas["comments"]


                    for data_comment in data_comments:
                        localTime = time.localtime(data_comment['time'] / 1000)
                        strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
                        commentinfo = {"movieid":filmid,"nick":data_comment['nick'],"content":data_comment['content']
                                       ,"score":data_comment['score'],"time":strTime,"pictureurl":data_comment['avatarUrl']}
                        print(commentinfo)
                        CommentHelper().insert(commentinfo)
                except Exception as e:
                    print(e)
    '''
    def get_comment_time(self,goodtime,filmid,movieid):
        endtime = datetime.datetime.strptime(goodtime, '%Y-%m-%d')
        endtime = endtime.strftime('%Y-%m-%d %H:%M:%S')
        starttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        while starttime > endtime:
            url = 'http://m.maoyan.com/mmdb/comments/movie/'+str(filmid)+'.json?_v_=yes&offset=0&startTime=' + starttime.replace(' ', '%20')
            print(url)
            if not BloomFilter().contains(url):
                try:
                    time.sleep(1.5)
                    response = requests.get(url,headers=HelpTool().get_header(),timeout=5).content.decode("utf-8","ignore")
                    jsonObj = json.loads(response)
                    data_comments = jsonObj["cmts"]
                    if(len(jsonObj["cmts"]) == 0):
                        print("filmid:" + filmid + "获取评论结束")
                        return

                    commentinfolist = []
                    for data_comment in data_comments:
                        #localTime = time.localtime(data_comment['time'] / 1000)
                        #strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
                        try:

                            commentinfo = {"movieid":movieid,"nick":data_comment['nick'],"content":data_comment['content']
                                           ,"score":data_comment['score'],"city":data_comment['cityName'],"time":data_comment['startTime'],"pictureurl":data_comment['avatarurl']}
                            commentinfolist.append(commentinfo)
                            print(commentinfo)
                        except:
                            continue


                    CommentHelper().insert(commentinfolist)



                    start_time = data_comments[len(data_comments)-1]['startTime']  # 获得末尾评论的时间
                    if(datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') == starttime):
                        return
                    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(
                        seconds=-1)  # 转换为datetime类型，减1秒，避免获取到重复数据
                    starttime = datetime.datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')  # 转换为str
                    print(starttime)
                except Exception as e:
                    start_time = data_comments[len(data_comments) - 1]['startTime']  # 获得末尾评论的时间
                    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(
                        seconds=-10)  # 转换为datetime类型，减1秒，避免获取到重复数据
                    starttime = datetime.datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')  # 转换为str
                    print(e)
            else:
                starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S')+ timedelta(seconds=-30)  # 转换为datetime类型，减1秒，避免获取到重复数据
                starttime = datetime.datetime.strftime(starttime, '%Y-%m-%d %H:%M:%S')
        print("filmid:"+filmid+"获取评论结束")

    def get_actorpage(self,urlset,filmid):
        while True:
            url = urlset.pop()
            if not url:
                break
            if not BloomFilter().contains(url):
                try:
                    response = requests.get(url).content.decode("utf-8", "ignore")

                    font_file = re.findall("vfile\.meituan\.net/colorstone/(\w+\.woff)", response)[0]

                    font = HelpTool().download_font(font_file)

                    etree = lxml.html.fromstring(response)

                    try:
                        fans = re.findall(r'<p class="index-num followCount">\s+<span class="stonefont">(.*?)</span>\s+</p>',
                                   response, re.S)[0]
                        fans = HelpTool().getdata(fans, font)
                    except:
                        fans = "0"

                    try:
                        data = \
                        re.findall('<p class="index-num">\s+<span class="stonefont">(.*?)</span>\s+</p>', response, re.S)[0]
                        data = data.split('<')
                        data = HelpTool().getdata(data[0], font)
                        unit = etree.xpath("//p[@class=\"index-num\"]//span[@class=\"unit\"]/text()")[0]
                        money = data[0] + unit
                        # money = getdata(data[0], font)
                        # money = money + data[1]
                    except:
                        money = "暂无"

                    name = etree.xpath("//div[@class=\"shortInfo\"]/p[1]/text()")[0]

                    try:
                        tag = etree.xpath("//span[@class=\"profession\"]/text()")[0]
                        taglist = tag.split(" | ")
                    except:
                        taglist = []

                    try:
                        birthday = etree.xpath("//span[@class=\"birthday\"]/text()")[0]
                    except:
                        birthday = "1900-01-01"

                    try:
                        height = etree.xpath("//span[@class=\"height\"]/text()")[0]
                    except:
                        height = "暂无"

                    titleleftlist = etree.xpath("//dl[@class=\"dl-left\"]//dt//text()")
                    titlerightlist = etree.xpath("//dl[@class=\"right\"]//dt//text()")
                    titlelist = []
                    for title in titleleftlist:
                        titlelist.append(title.encode("utf-8", "ignore").decode("utf-8", "ignore").replace("", ""))
                    for title in titlerightlist:
                        titlelist.append(title.replace("xa0", ""))

                    infoleftlist = etree.xpath("//dl[@class=\"dl-left\"]//dd//text()")
                    inforightlist = etree.xpath("//dl[@class=\"right\"]//dd//text()")
                    infolist = []
                    for info in infoleftlist:
                        infolist.append(info.strip())
                    for info in inforightlist:
                        infolist.append(info.strip())

                    constel = "暂无"
                    birthplace = "暂无"
                    nation = "暂无"
                    gender = "暂无"
                    school = "暂无"
                    blood = "暂无"
                    for index in range(len(titlelist)):
                        try:
                            if titlelist[index].find('星') != -1:
                                constel = infolist[index]
                            elif titlelist[index] == '出生地':
                                birthplace = infolist[index]
                            elif titlelist[index].find("国") != -1:
                                nation = infolist[index]
                            elif titlelist[index].find("性") != -1:
                                gender = infolist[index]
                            elif titlelist[index] == "毕业学校":
                                school = infolist[index]
                            elif titlelist[index].find("血") != -1:
                                blood = infolist[index]
                        except:
                            pass

                    try:
                        introduce = etree.xpath("//p[@class=\"cele-desc\"]/text()")[0]
                    except:
                        introduce = "暂无"

                    pictureurl = etree.xpath("//div[@class=\"avatar-shadow\"]/img/@src")[0]

                    actorinfo = {"name":name,"birthday":birthday,"money":money,"fans":fans,
                                 "introduce":introduce,"pictureurl":pictureurl,"height":height,
                                 "gender":gender,"school":school,"constel":constel,"birthplace":birthplace,
                                 "nation":nation,"blood":blood}



                    ActorHelper().insert(actorinfo)
                    actorid  = ActorHelper().select(1,{"name":name})[0][0]
                    print(actorinfo)

                    movieactorinfo = {"movieid":filmid,"actorid":actorid}
                    MovieActorHelper().insert(movieactorinfo)
                    print(movieactorinfo)

                    tag = etree.xpath("//[span[@class=\"profession\"]/text()")
                    taglist = tag.split(" | ")
                    for tag in taglist:
                        taginfo = {"name":tag}
                        TagHelper().insert(taginfo)
                        tagid =TagHelper().select(1,conditions={"name":tag})[0][0]
                        tagactorinfo = {"tagid":tagid,"actorid":actorid}
                        print(tagactorinfo)
                        TagActorHelper().insert(tagactorinfo)
                except Exception as e:
                    print(e)

    def get_filmPage(self,urllist):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,             like Gecko) Chrome/70.0.3538.110 Safari/537.36"}

        for url in urllist:
            if not BloomFilter().contains(url):
                print("------"+url+"---------")
                try:
                    time.sleep(1)
                    response = requests.get(url, headers=headers).content.decode("utf-8", "ignore")
                    font_file = re.findall("vfile\.meituan\.net/colorstone/(\w+\.woff)", response)[0]

                    font = HelpTool().download_font(font_file)

                    try:
                        star = re.findall(r'<span class="index-left info-num ">\s+<span class="stonefont">(.*?)</span>\s+</span>',
                                      response)[0]

                        star = HelpTool().getdata(star, font)
                    except:
                        star = "暂无"

                    try:
                        audience = re.findall(r'<span class=".*?score-num.*?">(.*?)</span>', response, re.S)[0]
                        unit = audience.split(";")[-1]
                        audience = HelpTool().getdata(audience, font)
                        audience = audience + unit
                        print(audience)
                    except:
                        audience = "暂无"

                    try:
                        money = re.findall(
                            r'<div class="movie-index-content box">\s+<span class="stonefont">(.*?)</span><span class="unit">(.*?)</span>\s+</div>',
                            response)[0]
                        money = HelpTool().getdata(money[0], font)
                    except:
                        money = "暂无"

                    response = lxml.html.fromstring(response)
                    try:
                        name = response.xpath("//div[@class=\"movie-brief-container\"]/h3/text()")[0]
                    except:
                        continue


                    tag = response.xpath("//div[@class=\"movie-brief-container\"]/ul/li[1]/text()")[0]
                    taglist = tag.split(",")


                    try:
                        datalist = response.xpath("//div[@class=\"movie-brief-container\"]/ul/li[2]/text()")[0]
                        datalist = datalist.split("/")
                        zone = datalist[0].strip()
                        length = datalist[1].strip()
                    except:
                        zone = "暂无"
                        length = "暂无"

                    try:
                        startdate = response.xpath("//div[@class=\"movie-brief-container\"]/ul/li[3]/text()")[0]
                        startdate = startdate[0:10]
                    except:
                        startdate = "暂无"

                    try:
                        content = response.xpath("//span[@class=\"dra\"]/text()")[0]
                    except:
                        content = "暂无"

                    try:
                        pictureurl = response.xpath("//div[@class=\"avatar-shadow\"]/img/@src")[0]
                    except:
                        continue

                    directorurllist = response.xpath(
                        "//ul[@class=\"celebrity-list clearfix\"]/li[@class=\"celebrity \"]/a/@href")
                    actorurllist = response.xpath("//li[@class=\"celebrity actor\"]/a/@href")
                    urlset = set()
                    url_pre = "https://maoyan.com"
                    for directorurl in directorurllist:
                        urlset.add(url_pre + directorurl)
                    for actorurl in actorurllist:
                        urlset.add(url_pre + actorurl)

                    movieinfo ={"name":name,"zone":zone,"length":length,"startdate":startdate,
                                "pictureurl":pictureurl,"star":star,"money":money,"audience":audience
                                ,"content":content}
                    print(movieinfo)
                    MovieHelper().insert(movieinfo)
                    movieid = MovieHelper().select(1,{"name":name})[0][0]

                    for tag in taglist:
                        taginfo = {"name":tag}
                        TagHelper().insert(taginfo)
                        tagid =TagHelper().select(1,conditions={"name":tag})[0][0]
                        print(tag)
                        print(tagid)
                        tagmovieinfo = {"tagid":tagid,"movieid":movieid}
                        print(tagmovieinfo)
                        TagMovieHelper().insert(tagmovieinfo)

                    '''commentresponse = requests.get(url,headers=HelpTool().headers).content.decode("utf-8","ignore")
                    commentetree = lxml.html.fromstring(commentresponse)
                    commentnum = commentetree.xpath("//a[@class=\"link link-more comments-link\"]//h4//span[2]/text()")[0]
                    commentnum = eval(commentnum)'''


                    filmid = url.split("/")[-1]
                    '''commentlist=[]
                    if(commentnum // 15 == 0):
                        commentnum = commentnum//15
                    else:
                        commentnum = commentnum//15 + 1
                    for i in range(0,commentnum):
                        url = "http://m.maoyan.com/review/v2/comments.json?movieId=248906&userId=-1&offset="+str(i*15)+"&limit=15&ts=0&type=3"
                        commentlist.append(url)
                    print(startdate)'''
                    gevent.joinall([
                        gevent.spawn(self.get_comment_time(startdate,filmid,movieid)),
                        gevent.spawn(self.get_actorpage(urlset,movieid)),
                    ])
                except Exception as e:
                    print(e)

    def get_filmurllist(self,num):
        urllist = []
        commentlist = []
        for index in range(num):
            url = "https://maoyan.com/films?showType=3&offset=" + str(index * 30)
            if not BloomFilter().contains(url):
                response = requests.get(url).content.decode("utf-8", "ignore")
                response = lxml.html.fromstring(response)

                movielist = response.xpath("//div[@class=\"movie-item\"]/a/@href")
                for movie in movielist:
                    urllist.append("https://maoyan.com" + movie)
                time.sleep(1)
        return urllist

    def get_pagenum(self):
        url = "https://maoyan.com/films?showType=3"
        response = requests.get(url).content.decode('utf-8', "ignore")
        response = lxml.html.fromstring(response)

        #pagenum = response.xpath("//ul[@class=\"list-pager\"]//li[last()-1]/a/text()")[0]
        #pagenum="67"
        pagenum="1"
        return self.get_filmurllist(eval(pagenum))

    def cuturllist(self,urllist):
        N = 6
        moreurllist = [[], [], [], [], [],[]]
        for index in range(len(urllist)):
            moreurllist[index % N].append(urllist[index])
        return moreurllist

    def crawl(self):
        #urllist = self.get_pagenum()
        #cuturllist = self.cuturllist(urllist)
        threadlist = []
        cuturllist=[['https://maoyan.com/films/248906']]
        for cuturl in cuturllist:
            thread = threading.Thread(target=self.get_filmPage, args=(cuturl,))
            threadlist.append(thread)
            thread.start()


        for thd in threadlist:
           thd.join()


maoyanUtil = maoyan()
maoyanUtil.crawl()