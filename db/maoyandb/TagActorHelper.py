# coding:utf-8
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, create_engine, VARCHAR,BIGINT,TIMESTAMP,BLOB,TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.maoyandb.ISqlHelper import ISqlHelper
import threading



BaseModel = declarative_base()


class TagActor(BaseModel):
    __tablename__ = 'tag_actor'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    tagid = Column(BIGINT, nullable=False)
    actorid = Column(BIGINT, nullable=False)


class TagActorHelper(ISqlHelper):
    params= {"tagid":None,"actorid":None}
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(TagActorHelper,"_instance"):
            with TagActorHelper._instance_lock:
                if not hasattr(TagActorHelper,"_instance"):
                    TagActorHelper._instance = object.__new__(cls)
        return TagActorHelper._instance

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
            tagactor = TagActor(tagid=value['tagid'],actorid=value['actorid'])
            self.session.add(tagactor)
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
                query = self.session.query(TagActor)
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
                query = self.session.query(TagActor)
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

            query = self.session.query(TagActor.id,TagActor.tagid,TagActor.actorid)
            if len(conditions) > 0 and count:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(TagActor.actorid.desc()).limit(count).all()
            elif count:
                return query.order_by(TagActor.actorid.desc()).limit(count).all()
            elif len(conditions) > 0:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(TagActor.actorid.desc()).all()
            else:
                return query.order_by(TagActor.actorid.desc()).all()
        except Exception as e:
            print(e)


    def close(self):
        pass


if __name__ == '__main__':
    sqlhelper = TagActorHelper()
    sqlhelper.init_db()
    actor = {"tagid":"2","actorid":"2"}

    sqlhelper.insert(actor)
    #sqlhelper.update({'name': '倚天屠龙'}, {'star': "10"})
    print(sqlhelper.select(1))
    #sqlhelper.delete({'tagid': '2'})
    #print(sqlhelper.select(1))

