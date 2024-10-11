#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    #  getting all the articles from the server
    article = [article.to_dict() for article in Article.query.all()]
    # creting and returning a response
    response = make_response(article, 200)
    return response


@app.route('/articles/<int:id>')
def show_article(id):
    #  setting the session["page_views"] to 0 if the user has never viewed an article
    session["page_views"] = 0 if not session.get("page_views") else session.get("page_views")
    # incrementing the session["page_views"] by 1
    session["page_views"] +=1

    # creating an if else ststement to check whether the user had viewed more than 3 pages
    if session["page_views"] <=3:
        # show the article in accordance to the  id
        article = Article.query.filter(Article.id == id).first()
        #  making the article to a dictionary 
        article_dict = article.to_dict()
        # creating and returning a response
        response = make_response(article_dict, 200)
        return response
    else:
        # create and return a response with a response body
        response_body = {'message': 'Maximum pageview limit reached'}
        response = make_response(response_body, 401)
        return response


if __name__ == '__main__':
    app.run(port=5555)
