# coding:utf-8
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, create_engine, VARCHAR,BIGINT,TIMESTAMP,BLOB,TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
from db.maoyandb.ISqlHelper import ISqlHelper
import threading



BaseModel = declarative_base()


class Comment(BaseModel):
    __tablename__ = 'comments'
    commentid = Column(BIGINT, primary_key=True, autoincrement=True)
    movieid = Column(BIGINT, nullable=False)
    nick= Column(VARCHAR(1024), nullable=False)
    content = Column(VARCHAR(1024), nullable=True)
    score = Column(Integer, nullable=True)
    city = Column(VARCHAR(32),nullable=True)
    time = Column(DateTime, nullable=True)
    pictureurl = Column(VARCHAR(512), nullable=True)



class CommentHelper(ISqlHelper):
    params = {"movieid": None, "nick": None, "content": None, "score": None,"city":None, "time": None, "pictureurl": None}

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(CommentHelper,"_instance"):
            with CommentHelper._instance_lock:
                if not hasattr(CommentHelper,"_instance"):
                    CommentHelper._instance = object.__new__(cls)
        return CommentHelper._instance

    def __init__(self):
        self.engine = create_engine("mysql+pymysql://root:@localhost:3306/maoyan?charset=utf8", echo=False)
        DB_Session = scoped_session(sessionmaker(bind=self.engine))
        self.session = DB_Session()
        BaseModel.metadata.create_all(self.engine)

    def init_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)


    def insert(self,valuelist=None):
        try:
            for value in valuelist:

                comment = Comment(movieid=value['movieid'], nick=value['nick'], content=value['content'], score=value['score'],
                              city=value["city"],time=value['time'],pictureurl=value['pictureurl'])
                self.session.add(comment)
                self.session.commit()
                self.session.flush()
        except Exception as e:
            self.session.rollback()


    def delete(self, conditions=None):
        try:
            if conditions:
                conditon_list = []
                for key in list(conditions.keys()):
                    if self.params.get(key, None):
                        conditon_list.append(self.params.get(key) == conditions.get(key))
                conditions = conditon_list
                query = self.session.query(Comment)
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
                query = self.session.query(Comment)
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

            query = self.session.query(Comment.nick,Comment.content,Comment.score,
                                       Comment.city,Comment.time,Comment.pictureurl)
            if len(conditions) > 0 and count:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(Comment.score.desc()).limit(count).all()
            elif count:
                return query.order_by(Comment.score.desc()).limit(count).all()
            elif len(conditions) > 0:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(Comment.score.desc()).all()
            else:
                return query.order_by(Comment.score.desc()).all()
        except Exception as e:
            print(e)


    def close(self):
        pass


if __name__ == '__main__':
    sqlhelper = CommentHelper()
    sqlhelper.init_db()
    comment = {"movieid":"1","nick":"青青大笨蛋","content":"一脸懵逼","score":"9.5","city":"荆州","time":"2018-04-06",
             "pictureurl":"11233"}
    comment1 = {"movieid": "1", "nick": "青青小笨蛋", "content": "一脸懵逼", "score": "9.5", "city":"鹰潭","time": "2018-04-06",
               "pictureurl": "11233"}
    #sqlhelper.insert(comment)
    #sqlhelper.insert(comment1)
    #sqlhelper.update({'name': '倚天屠龙'}, {'star': "10"})
    print(sqlhelper.select(1,{'nick':"青青大笨蛋"}))
    #sqlhelper.delete({'name': '倚天屠龙'})
    #print(sqlhelper.select(1))

