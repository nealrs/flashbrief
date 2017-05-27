# -*- coding: utf-8 -*-

from flask import request, session, Flask, render_template, Response, redirect, url_for
from flask_cors import CORS, cross_origin
import requests
import json
import re
import random
from os import environ
import string
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import CompileError
from sqlalchemy.orm import sessionmaker, deferred
from sqlalchemy.ext.declarative import declarative_base

#from raven.contrib.f#lask import Sentry
#import logging

#####
# simple wrapper for logging to stdout on heroku
#def log(message):
    #print str(message)
    #sys.stdout.flush()
#####

## MySQL db config ##
dburl = environ['CLEARDB_DATABASE_URL']
db = create_engine(dburl, convert_unicode=True, pool_recycle=280, echo=False)
md = MetaData(bind=db)
Session = sessionmaker(bind=db)

Base = declarative_base()
class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    title = Column(String)
    audio = Column(String)
    text = Column(Text)
    url = Column(String)

# Initialize the Flask app ##
application = Flask(__name__)
application.config['PROPAGATE_EXCEPTIONS'] = True

## SENTRY CONFIG ##
#sentry = Sentry(application, dsn=environ['SENTRY_DSN'], logging=True, level=logging.ERROR)

@application.route('/')
def index():
  #return render_template('index.html')
  res = getNews()
  return json.dumps(res)

#####

def getNews():
  session = Session()
  # get today's date (month/day)
  #date = "sdf"
  rows = session.query(News).filter(Comment.date==date).order_by(Comment.id.desc()).limit(3)
  session.close()

  clist=[]
  for r in rows:
      clist.append({
        "uid": str(r.News.id),
        "updateDate": r.News.date, # do we need to mess with the date here?
        "titleText": r.News.title,
        "streamUrl": r.News.audio,
        "mainText": r.News.text,
        "redirectionURL": r.News.url})
  news = json.dumps(clist)

  #log(news)
  print news

  return news
#####

if __name__ == "__main__":
    application.run(debug=False)
