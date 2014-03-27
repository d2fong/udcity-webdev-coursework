from google.appengine.ext import db


class Post(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(requrired = True)
	created = db.DateTimeProperty(auto_now_add = True)
