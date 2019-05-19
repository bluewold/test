# coding:utf-8

class ISqlHelper(object):
    params = {'ip': None, 'port': None, 'types': None, 'protocol': None, 'country': None, 'area': None}
    actor_params={"name":None,"birthday":None,"money":None,"fans":None,"introduce":None,"picture":None
                  ,"height":None,"gender":None,"school":None,"constel":None,"birthplace":None,
                  "nation":None,"blood":None}
    movie_params={"name":None,"zone":None,"length":None,"startdate":None,"picture":None,"star":None
                  ,"money":None,"audience":None,"content":None}
    comment_params={"movieid":None,"nick":None,"content":None,"score":None,"time":None,"picture":None}
    tag_params={"name":None}
    movie_actor_params={"movieid":None,"actorid":None}
    tag_actor_params={"tagid":None,"actorid":None}
    tag_movie_params={"tagid":None,"movieid":None}
    actor_actor_params={"from_actorid":None,"to_actorid":None,"relation_desc":None}


    def init_db(self):
        raise NotImplemented

    def drop_db(self):
        raise NotImplemented

    def insert(self, value=None):
        raise NotImplemented

    def delete(self, conditions=None):
        raise NotImplemented

    def update(self, conditions=None, value=None):
        raise NotImplemented

    def select(self, count=None, conditions=None):
        raise NotImplemented


