'''
定义规则 urls:url列表
         type：解析方式,取值 regular(正则表达式),xpath(xpath解析),module(自定义第三方模块解析)
         patten：可以是正则表达式,可以是xpath语句不过要和上面的相对应
'''
import os

'''
ip，端口，类型(0高匿名，1透明)，protocol(0 http,1 https),country(国家),area(省市),updatetime(更新时间)
 speed(连接速度)
'''
parserList = [

    {
        'urls': ['http://www.xicidaili.com/%s/%s' % (m, n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 8)],
        'type': 'xpath',
        'pattern': ".//*[@id='ip_list']/tr[position()>1]",
        'position': {'ip': './td[2]', 'port': './td[3]', 'type': './td[5]', 'protocol': './td[6]'}
    }
]
'''
数据库的配置
'''
DB_CONFIG = {

    'DB_CONNECT_TYPE': 'sqlalchemy',  # 'pymongo'sqlalchemy;redis
    # 'DB_CONNECT_STRING':'mongodb://localhost:27017/'
    #'DB_CONNECT_STRING': 'sqlite:///' + os.path.dirname(__file__) + '/data/proxy.db'
    'DB_CONNECT_STRING' : 'mysql+mysqldb://root:@localhost/proxy?charset=utf8mb4'

    # 'DB_CONNECT_TYPE': 'redis',  # 'pymongo'sqlalchemy;redis
    # 'DB_CONNECT_STRING': 'redis://localhost:6379/8',

}
CHINA_AREA = ['河北', '山东', '辽宁', '黑龙江', '吉林'
    , '甘肃', '青海', '河南', '江苏', '湖北', '湖南',
              '江西', '浙江', '广东', '云南', '福建',
              '台湾', '海南', '山西', '四川', '陕西',
              '贵州', '安徽', '重庆', '北京', '上海', '天津', '广西', '内蒙', '西藏', '新疆', '宁夏', '香港', '澳门']
QQWRY_PATH = os.path.dirname(__file__) + "\\data\\qqwry.dat"
THREADNUM = 5
API_PORT = 8000
'''
爬虫爬取和检测ip的设置条件
不需要检测ip是否已经存在，因为会定时清理
'''
UPDATE_TIME = 30 * 60  # 每半个小时检测一次是否有代理ip失效
MINNUM = 50  # 当有效的ip值小于一个时 需要启动爬虫进行爬取

TIMEOUT = 5  # socket延时
'''
反爬虫的设置
'''
'''
重试次数
'''
RETRY_TIME = 3

#默认给抓取的ip分配20分,每次连接失败,减一分,直到分数全部扣完从数据库中删除
DEFAULT_SCORE=10

TEST_URL = 'http://ip.chinaz.com/getip.aspx'
TEST_IP = 'http://httpbin.org/ip'
TEST_HTTP_HEADER = 'http://httpbin.org/get'
TEST_HTTPS_HEADER = 'https://httpbin.org/get'
#CHECK_PROXY变量是为了用户自定义检测代理的函数
#现在使用检测的网址是httpbin.org,但是即使ip通过了验证和检测
#也只能说明通过此代理ip可以到达httpbin.org,但是不一定能到达用户爬取的网址
#因此在这个地方用户可以自己添加检测函数,我以百度为访问网址尝试一下
#大家可以看一下Validator.py文件中的baidu_check函数和detect_proxy函数就会明白

CHECK_PROXY={'function':'checkProxy'}#{'function':'baidu_check'}

#下面配置squid,现在还没实现
#SQUID={'path':None,'confpath':'C:/squid/etc/squid.conf'}

MAX_CHECK_PROCESS = 2 # CHECK_PROXY最大进程数
MAX_CHECK_CONCURRENT_PER_PROCESS = 30 # CHECK_PROXY时每个进程的最大并发
TASK_QUEUE_SIZE = 50 # 任务队列SIZE
MAX_DOWNLOAD_CONCURRENT = 3 # 从免费代理网站下载时的最大并发 
CHECK_WATI_TIME = 1#进程数达到上限时的等待时间