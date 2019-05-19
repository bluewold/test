from until.config import TEST_IP,DB_CONFIG

class Test_URL_Fail(Exception):
    def __str__(self):
        str = "访问%s失败，请检查网络连接" % TEST_IP
        return str


class Con_DB_Fail(Exception):
    def __str__(self):
        str = "使用DB_CONNECT_STRING:%s--连接数据库失败" % DB_CONFIG
        return str
