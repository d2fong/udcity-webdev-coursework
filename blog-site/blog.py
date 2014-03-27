import os
import webapp2
import jinja2
from models import Post
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
		self.render("index.html")

class NewPost(Handler):
	def get(self):
		self.render("new_post.html")

	def post(self):
		subject = self.request.get('subject')
		content = self.request.get('content')

		if content and subject:
			post = Post(subject = subject, content = content)
			key = post.put()
			self.redirect("/" + str(key.id())
		else:
			re render the template with title/content and a error message

class AboutPage(Handler):
	def get(self):
		self.render("index.html")

class PortfolioPage(Handler):
	def get(self):
		self.render("index.html")

class BlogPost(Handler):

	def get(self, blog_id):
		
		posts = Blog.get_by_id(blog_id())
		self.render("index.html", posts=[s])

app = webapp2.WSGIApplication([(r'/posts/(\d+)', BlogPost), (r'/about', AboutPage), (r'/portfolio', PortfolioPage), (r'/', MainPage), (r'/newpost', NewPost)], debug=True)