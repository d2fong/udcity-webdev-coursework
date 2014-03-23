import webapp2
import cgi
import string
import re


def escape_html(s):
	return cgi.escape(s, quote = True)


def encrypt_rotc13(text):
	lowercase = "abcdefghijklmnopqrstuvwxyz"
	uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	encrpyted_text = []
	for word in text.split():
		new_word = []
		for char in word:
			if char in lowercase:
				char_index = (lowercase.index(char) + 13) % 26
				new_word.append(lowercase[char_index])
			elif char in uppercase:
				char_index = (uppercase.index(char) + 13) % 26
				new_word.append(uppercase[char_index])
			else:
				new_word.append(char)
		encrpyted_text.append("".join(new_word))
	return " ".join(encrpyted_text)




rotc13_form = """
<form method="post">
	Enter your text to encrypt:
	<br>
	<textarea name="text">%(result)s</textarea>
	<br>
	<input type="submit"/>
</form>
"""
class MainPage(webapp2.RequestHandler):

	def write_form(self, text=''):
		self.response.out.write(rotc13_form%{"result": escape_html(text)})

	def get(self):
		self.write_form()

	def post(self):
		raw_text = self.request.get('text')
		rotc13_text = encrypt_rotc13(raw_text)
		self.write_form(rotc13_text)


user_sign_up_form = """
<form method="post">
	Sign Up
	<br>
	<label>
		username
		<input type="text" name="username" value="%(username)s">
	</label>
	%(username_error)s
	<br>
	<label>
		password
		<input type="password" name="password" value="%(password)s">
	</label>
	%(password_error)s
	<br>
	<label>
		verify
		<input type="password" name="verify" value="%(verify)s">
	</label>
	<br>
	<label>
		email
		<input type="text" name="email" value="%(email)s"/>
	</label>
	%(email_error)s
	<br>
	<input type="submit"/>
</form>
"""


class UserSignUp(webapp2.RequestHandler):
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	PASSWORD_RE = re.compile("^.{3,20}$")
	EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")

	def serve_sign_up_form(self, username='', password='', verify='', email='', username_error='', password_error='',email_error=''):
		self.response.out.write(user_sign_up_form %{
			"username" : username,
			"password" : password,
			"verify" : verify,
			"email" : email,
			"username_error" : username_error,
			"password_error" : password_error,
			"email_error" : email_error
			})

	def get(self):
		self.serve_sign_up_form()
	def is_valid_name(self, username):
		return UserSignUp.USER_RE.match(username)
	def is_valid_password(self, password):
		return UserSignUp.PASSWORD_RE.match(password)
	def is_valid_email(self, email):
		return UserSignUp.EMAIL_RE.match(email)

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')



		input_is_valid = True
		email_error = ''
		username_error = ''
		password_error = ''
		email_error = ''

		if  not self.is_valid_name(username):
			username_error = "Invalid Username"
			input_is_valid = False

		if not(self.is_valid_email(email)):
			email_error = "Invalid Email"
			input_is_valid = False

		if not self.is_valid_password(password) or password != verify:
			password_error = "Your passwords do not match or are invalid"
			input_is_valid = False

		if input_is_valid:
			self.redirect('/welcome' + '?username=' + escape_html(username))
		else:
			self.serve_sign_up_form(username, '', '', email, username_error, password_error, email_error)





class SignUpSuccess(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		self.response.write("welcome," + username)






app = webapp2.WSGIApplication([('/', MainPage), ('/signup', UserSignUp), ('/welcome', SignUpSuccess)], debug=True)