# coding:utf-8
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, create_engine, VARCHAR,BIGINT,TIMESTAMP,BLOB,TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.maoyandb.ISqlHelper import ISqlHelper
import threading



BaseModel = declarative_base()


class Actor(BaseModel):
    __tablename__ = 'actor'
    actorid = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(256), nullable=False)
    birthday = Column(DateTime, nullable=True)
    money = Column(VARCHAR(128), nullable=True)
    fans = Column(Integer, nullable=True)
    introduce = Column(TEXT, nullable=True)
    pictureurl = Column(VARCHAR(512), nullable=True)
    height = Column(VARCHAR(256))
    gender = Column(VARCHAR(2))
    school = Column(VARCHAR(256))
    constel = Column(VARCHAR(16))
    birthplace = Column(VARCHAR(256))
    nation = Column(VARCHAR(16))
    blood = Column(VARCHAR(16))


class ActorHelper(ISqlHelper):
    params= {"name": None, "birthday": None, "money": None, "fans": None, "introduce": None, "pictureurl": None
        , "height": None, "gender": None, "school": None, "constel": None, "birthplace": None,
             "nation": None, "blood": None}
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(ActorHelper,"_instance"):
            with ActorHelper._instance_lock:
                if not hasattr(ActorHelper,"_instance"):
                    ActorHelper._instance = object.__new__(cls)
        return ActorHelper._instance

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
            actor = Actor(name=value['name'].encode("utf-8","ignore"), birthday=value['birthday'].encode("utf-8","ignore"), money=value['money'].encode("utf-8","ignore"), fans=value['fans'],
                          introduce=value['introduce'].encode("utf-8","ignore"),pictureurl=value['pictureurl'].encode("utf-8","ignore"), height=value['height'].encode("utf-8","ignore")
                          ,gender=value['gender'].encode("utf-8","ignore"), school=value['school'].encode("utf-8","ignore"),constel=value['constel'].encode("utf-8","ignore"),birthplace=value['birthplace'].encode("utf-8","ignore")
                          ,nation=value['nation'].encode("utf-8","ignore"),blood=value['blood'].encode("utf-8","ignore"))

            self.session.add(actor)
            self.session.commit()
        except Exception as e:
            print(e)


    def delete(self, conditions=None):
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(Actor)
            for condition in conditions:
                query = query.filter(condition)
            deleteNum = query.delete()
            self.session.commit()
        else:
            deleteNum = 0
        return ('deleteNum', deleteNum)


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
                query = self.session.query(Actor)
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

            query = self.session.query(Actor.actorid,Actor.name,Actor.birthday, Actor.money,Actor.fans,
                                       Actor.introduce,Actor.pictureurl,Actor.height,Actor.gender,Actor.school,
                                       Actor.constel,Actor.birthplace,Actor.nation,Actor.blood)
            if len(conditions) > 0 and count:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(Actor.money.desc()).limit(count).all()
            elif count:
                return query.order_by(Actor.money.desc()).limit(count).all()
            elif len(conditions) > 0:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(Actor.money.desc()).all()
            else:
                return query.order_by(Actor.money.desc()).all()
        except Exception as e:
            print(e)


    def close(self):
        pass


if __name__ == '__main__':
    sqlhelper = ActorHelper()
    sqlhelper.init_db()
    actor = {"name":"小青","birthday":"2019-03-20","money":"1000亿","fans":"666666","introduce":"你真棒",
             "pictureurl":"11233","height":"165cm","gender":"女","school":"你猜","constel":"巨蟹",
             "birthplace":"荆州","nation":"中国","blood":"o型"}

    #sqlhelper.insert(actor)
    #sqlhelper.update({'name': '倚天屠龙'}, {'star': "10"})
    print(sqlhelper.select(1))
    #sqlhelper.delete({'name': '倚天屠龙'})
    #print(sqlhelper.select(1))

