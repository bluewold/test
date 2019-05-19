# coding:utf-8
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, create_engine, VARCHAR,BIGINT,TIMESTAMP,BLOB,TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.maoyandb.ISqlHelper import ISqlHelper
import threading



BaseModel = declarative_base()


class Movie(BaseModel):
    __tablename__ = 'movie'
    movieid = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(256), nullable=False)
    zone = Column(VARCHAR(128), nullable=True)
    length = Column(VARCHAR(128), nullable=True)
    startdate = Column(DateTime, nullable=True)
    pictureurl = Column(VARCHAR(512), nullable=True)
    star = Column(VARCHAR(16), nullable=True)
    money = Column(VARCHAR(128))
    audience = Column(VARCHAR(128))
    content = Column(TEXT)


class MovieHelper(ISqlHelper):
    params = {"name": None, "zone": None, "length": None, "startdate": None, "pictureurl": None, "star": None
        , "money": None, "audience": None, "content": None}
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(MovieHelper,"_instance"):
            with MovieHelper._instance_lock:
                if not hasattr(MovieHelper,"_instance"):
                    MovieHelper._instance = object.__new__(cls)
        return MovieHelper._instance

    def __init__(self):
        self.engine = create_engine("mysql+pymysql://root:@localhost:3306/maoyan?charset=utf8", echo=False)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()

    def init_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)


    def insert(self,value=None):
        try:
            movie = Movie(name=value['name'].encode("utf-8","ignore"), zone=value['zone'].encode("utf-8","ignore"), length=value['length'].encode("utf-8","ignore"), startdate=value['startdate'].encode("utf-8","ignore"),
                          pictureurl=value['pictureurl'].encode("utf-8","ignore"),star=value['star'].encode("utf-8","ignore"), money=value['money'].encode("utf-8","ignore")
                          ,audience=value['audience'].encode("utf-8","ignore"), content=value['content'].encode("utf-8","ignore"))

            self.session.add(movie)
            self.session.commit()
        except Exception as e:
            print(e)


    def delete(self, conditions=None):
        try:
            if conditions:
                conditon_list = []
                for key in list(conditions.keys()):
                    if self.params.get(key, None):
                        conditon_list.append(self.params.get(key) == conditions.get(key))
                conditions = conditon_list
                query = self.session.query(Movie)
                for condition in conditions:
                    query = query.filter(condition)
                deleteNum = query.delete()
                self.session.commit()
            else:
                deleteNum = 0
            return ('deleteNum', deleteNum)
        except Exception as e:
            print(e)


    def update(self, conditions=None, value=None):
        '''
        conditions的格式是个字典。类似self.params
        :param conditions:
        :param value:也是个字典：{'ip':192.168.0.1}
        :return:
        '''
        try:
            if conditions and value:
                conditon_list = []
                for key in list(conditions.keys()):
                    if self.params.get(key,None) == None:
                        print(key)
                        conditon_list.append(key + " == "+ conditions.get(key))
                conditions = conditon_list
                print(conditions)
                query = self.session.query(Movie)
                for condition in conditions:
                    query = query.filter(condition)
                updatevalue = {}
                for key in list(value.keys()):
                    if self.params.get(key, None) == None:
                        updatevalue[key] = value.get(key)
                updateNum = query.update(updatevalue)
                self.session.commit()
            else:
                updateNum = 0
            return {'updateNum': updateNum}
        except Exception as e:
            print(e)


    def select(self, count=None, conditions=None):
        '''
        conditions的格式是个字典。类似self.params
        :param count:
        :param conditions:
        :return:
        '''
        try:
            if conditions:
                conditon_list = []
                for key in list(conditions.keys()):
                    if self.params.get(key, None) == None:
                        conditon_list.append(key + " = '"+ conditions.get(key) + "'")
                conditions = conditon_list
            else:
                conditions = []

            query = self.session.query(Movie.movieid,Movie.movieid,Movie.name, Movie.zone,Movie.length,Movie.startdate,
                                       Movie.pictureurl,Movie.star,Movie.money,Movie.audience,Movie.content)
            if len(conditions) > 0 and count:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(Movie.money.desc()).limit(count).all()
            elif count:
                return query.order_by(Movie.money.desc()).limit(count).all()
            elif len(conditions) > 0:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(Movie.money.desc()).all()
            else:
                return query.order_by(Movie.money.desc()).all()
        except Exception as e:
            print(e)


    def close(self):
        pass


if __name__ == '__main__':
    sqlhelper = MovieHelper()
    movie = {"name":"倚天屠龙","zone":"中国大陆","length":"128分钟","startdate":"2019-03-20 23:43:00",
             "pictureurl":"11233","star":"9.9","money":"128亿","audience":"12万","content":"敏敏郡主好好看"}

    #sqlhelper.insert(movie)
    #sqlhelper.update({'name': '倚天屠龙'}, {'star': "10"})
    print(sqlhelper.select(1))
    #sqlhelper.delete({'name': '倚天屠龙'})
    #print(sqlhelper.select(1))

