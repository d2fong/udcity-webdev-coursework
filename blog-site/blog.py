import os
import webapp2
import jinja2
from models import Post
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)




class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))



class MainPage(Handler):
	def get(self):
		posts = posts = Post.all().order('-created').run(limit=10)
		self.render("index.html", posts=posts)

class NewPost(Handler):
	def get(self):
		self.render("new_post.html")

	def post(self):
		subject = self.request.get('subject')
		content = self.request.get('content')

		if content and subject:
			post = Post(subject=subject, content=content)
			key = post.put()
			self.redirect("/posts/%d" %  + key.id())
		else:
			self.render("new_post.html", subject = subject, 
				content = content, 
				error="A subject title and content is required")


class AboutPage(Handler):
	def get(self):
		self.render("index.html")

class PortfolioPage(Handler):
	def get(self):
		self.render("index.html")

class SinglePagePost(Handler):

	def get(self, post_id):
		
		post = Post.get_by_id(int(post_id))
		self.render("index.html", posts = [post])

app = webapp2.WSGIApplication([(r'/posts/(\d+)', SinglePagePost), 
								(r'/about', AboutPage), 
								(r'PortfolioPage', PortfolioPage),
								(r'/', MainPage),
								(r'/newpost', NewPost)], debug=True)