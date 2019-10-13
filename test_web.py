from app.py import *
from bs4 import BeautifulSoup
import requests, unittest

# UNITTEST all tests must start with test**
# LEVERAGE assert -> self.assertTrue()

WORDLIST = "wordlist.txt"
SITE = "http://localhost:5000/"

class TESTWebFunctions(unittest.TestCase):
	def test_UserStandardRegistration():
	#User Login With Registration
	.\curl -d "uname=username&password=password&phoneNum=11111111111" -X POST http://localhost:5000/register
	RESPONSE should be : 
	<title>Redirecting...</title>
	<h1>Redirecting...</h1>
	<p>You should be redirected automatically to target URL: <a href="/login">/login</a>.  If not click the link.
	.\curl -d "uname=username&password=password&phoneNum=11111111111" -X POST http://localhost:5000/login
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
	<title>Redirecting...</title>
	<h1>Redirecting...</h1>
	<p>You should be redirected automatically to target URL: <a href="/home">/home</a>.  If not click the link.
	
	def test_UserStandardLogin():
	# User standard login from successful registration
	
	
	def test_RegisterUserTwiceWithDifferentMFA():
	#register same user twice with different mfa
	.\curl -j -b cookies.txt -d "uname=username&password=password&phoneNum=22222222222" -X POST http://localhost:5000/register
	User Already Exists
	
	def test_userAttemptRegisterWithExistingUsername():
	# User Attempting To Register Again Using The Same Username:
	.\curl -d "uname=username&password=password&phoneNum=11111111111" -X POST http://localhost:5000/register
	RESPONSE should be : User Already Exists
	
	def test_RegisterExistingUserWithDifferentPassword():
	# register same user with different password
	.\curl -j -b cookies.txt -d "uname=username&password=password1&phoneNum=11111111111" -X POST http://localhost:5000/register
	User Already Exists
		
	def test_AccessLoginWithoutRegistration():
	# User access login without registration

	def test_AccessSpellCheckerWithoutRegistration():
	# attempt to access spell checker without registration
	
	def test_AccessSpellCheckerWithoutLogin():
	# attempt to access spell checker without login
	.\curl -X GET http://localhost:5000/spell_check
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
	<title>Redirecting...</title>
	<h1>Redirecting...</h1>
	<p>You should be redirected automatically to target URL: <a href="/login">/login</a>.  If not click the link.
	
	
	def test_LogoutWithoutLogin():
	# attempt to logout without login
	
	
r = requests.get("http://localhost:5000/")
assert(r.status_code == 200)
soup = BeautifulSoup(r.text, "html.parser")
links = soup.find_all('a')
for link in links:
	print(link['href'])
	requests.get(link['href'])
	
successLinks = soup.find_all('p', id='success')

requests.post('http://localhost:5000/login')

SESSION = requests.Session()
session.get("localhost:5000/login")
session.post("localhost:5000/login")

print(soup.prettify())

# python3 test_web.py

if __name__=='__main__':
	unittest.main()
	
python unittest package 
subprocess execute curl .> beautiful soup to check output
and use options to save off and resend session cookies. I then pull out the csrf token value and resend as part of the post. 

