from . import db
from flask.ext.login import UserMixin, AnonymousUserMixin
from datetime import datetime

# login
class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE_AUTHOR_COMMENTS = 8
    MODERATE_ALL_COMMENTS = 16
    ADMIN = 32

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    pw_hash = db.Column(db.String(128))

    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))
    articles = db.relationship('Article',backref='user',lazy='dynamic')
    comments = db.relationship('Comment',backref='user',lazy='dynamic')

    def __init__(self, **kwargs):
        super(User,self).__init__(**kwargs)
        if self.role == None:
            self.role = Role.query.filter_by(default=True).first()
    
    def can(self, permissions):
        return self.role is not None and \
                (self.role.permissions&permissions)==permissions

    def is_administrator(self):
        return self.can(Permission.ADMIN)

class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False
    
    def is_administrator(self):
        return False



class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynameic')
    default = db.Column(db.Boolean,default=False,index=True)

    @staticmethod
    def insert_roles():
        roles={
                'User':(Permission.FOLLOW |
                    Permission.COMMENT |
                    Permission.WRITE |
                    MODERATE_AUTHOER_COMMENTS,True),
                'Moderator':(Permission.FOLLOW |
                    Permission.COMMENT |
                    Permission.WRITE |
                    Permission.MODERATE_AUTHOER_COMMENTS |
                    Permission.MODERATE_ALL_COMMENTS,False),

                'Admin':(Permission.FOLLOW |
                    Permission.COMMENT |
                    Permission.WRITE |
                    Permission.MODERATE_AUTHOER_COMMENTS |
                    Permission.MODERATE_ALL_COMMENTS,False)
                }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        de.session.commit()



# blog
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(512))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    categoryb_id = db.Column(db.Integer,db.ForeignKey('categoryb.id'))
    comments = db.relationship('Comment',backref='article',lazy='dynamic')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer,db.ForeignKey('article.id'))

class CategoryBlog(db.Model):
    __tablename__ = 'categoryb'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    articles = db.relationship('Article',backref='categoryb',lazy='dynamic')


'''
class TagBlog(db.Model):
    __tablename__ = 'tagb'
    id = db.Column(db.Integer,primary_key=True)

# novel
class Novel(db.Model):
    __tablename__ = 'novel'
    id = db.Column(db.Integer,primary_key=True)

class CategoryNovel(db.Model):
    __tablename__ = 'categoryn'
'''
