from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import blog
from .. import db
from ..models import Permission,Role,User,Article,Comment,CategoryBlog

@blog.route('/')
def index():
    return render_template('index.html')

@blog.route('/user/<username>')
def user_index(username):
    user = User.query.filter_by(name=username).first()

    pass

def category(id):
    category = CategoryBlog.query.filter_by(id=id).first()



def article(id):
    article = Article.query.filter_by(id=id).first()

