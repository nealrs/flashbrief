# -*- coding: utf-8 -*-

from flask import request, session, Flask, render_template, Response, redirect, url_for
import requests
import json
import re
from os import environ
import string
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import CompileError
from sqlalchemy.orm import sessionmaker, deferred
from sqlalchemy.ext.declarative import declarative_base

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


@application.route('/')
def index():
  # This method should return a json object of up to 3 items, matching today's date with either text/audio components.
  res = getNews()
  return json.dumps(res)

def getNews():
  session = Session()
  # get today's date (month/day)
  #date = "sdf"
  #rows = session.query(News).filter(Comment.date==date).order_by(Comment.id.desc()).limit(3) #latest 3 stories on THIS DAY
  #rows = session.query(News).order_by(News.id.desc()).limit(3) #just latest 3


  for u in session.query(News).order_by(News.id.desc()).limit(3):
    print u.__dict__



  session.close()

  print "hi"
  #print rows
  print "end hi"

  clist=[]
  for r in rows:
      print "running rows loop"
      # do we need to mess with the date here? to match formats
      #odate = r.News.date
      #ndate = "sdf" #"2017-05-23T12:00:00.0Z"

      clist.append({
        "uid": str(r.News.id),
        "updateDate": r.News.date,
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
