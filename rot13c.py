import webapp2
import cgi
import string


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
	<br>
	<label>
		password
		<input type="password" name="password" value="%(password)s">
	</label>
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

	<br>
	<input type="submit"/>
</form>
"""


class UserSignUp(webapp2.RequestHandler):

	def serve_sign_up_form(self, username='', password='', verify='', email=''):
		self.response.out.write(user_sign_up_form %{
			"username" : username,
			"password" : password,
			"verify" : verify,
			"email" : email
			})

	def get(self):
		self.serve_sign_up_form()

	def post(self):
		username = self.response.get('username')
		password = self.response.get('password')
		verify = self.response.get('verify')
		email = self.response.email('email')

		if username and is_valid_name(username) and password and verify and verify == password:
			if email and is_valid_email(email):
					self.redirect('/signup/success' + '?username=' + username)
			else:
				error
			

		else:
			error





class SignUpSuccess(webapp2.RequestHandler):
	def get(self):
		pass






app = webapp2.WSGIApplication([('/', MainPage), ('/signup', UserSignUp), ('/signup/success', SignUpSuccess)], debug=True)