# coding:utf-8
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, create_engine, VARCHAR,BIGINT,TIMESTAMP,BLOB,TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.maoyandb.ISqlHelper import ISqlHelper
import threading



BaseModel = declarative_base()


class MovieActor(BaseModel):
    __tablename__ = 'movie_actor'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    movieid = Column(BIGINT, nullable=False)
    actorid = Column(BIGINT, nullable=False)


class MovieActorHelper(ISqlHelper):
    params= {"movieid":None,"actorid":None}
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(MovieActorHelper,"_instance"):
            with MovieActorHelper._instance_lock:
                if not hasattr(MovieActorHelper,"_instance"):
                    MovieActorHelper._instance = object.__new__(cls)
        return MovieActorHelper._instance

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
            movieactor = MovieActor(movieid=value['movieid'],actorid=value['actorid'])
            self.session.add(movieactor)
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
                query = self.session.query(MovieActor)
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
                query = self.session.query(MovieActor)
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
                    if self.params.get(key, None):
                        conditon_list.append(self.params.get(key) == conditions.get(key))
                conditions = conditon_list
            else:
                conditions = []

            query = self.session.query(MovieActor.id,MovieActor.movieid,MovieActor.actorid)
            if len(conditions) > 0 and count:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(MovieActor.actorid.desc()).limit(count).all()
            elif count:
                return query.order_by(MovieActor.actorid.desc()).limit(count).all()
            elif len(conditions) > 0:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(MovieActor.actorid.desc()).all()
            else:
                return query.order_by(MovieActor.actorid.desc()).all()
        except Exception as e:
            print(e)


    def close(self):
        pass


if __name__ == '__main__':
    sqlhelper = MovieActorHelper()
    sqlhelper.init_db()
    movieactor= {"movieid":"25","actorid":"2"}

    sqlhelper.insert(movieactor)
    #sqlhelper.update({'name': '倚天屠龙'}, {'star': "10"})
    print(sqlhelper.select(1))
    #sqlhelper.delete({'tagid': '2'})
    #print(sqlhelper.select(1))

