#app.py -- contains basics of python code. to start web service. 

from flask import Flask, request, redirect,render_template, session
from flask_login import LoginManager, current_user, login_user
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField, HiddenField
from flask_wtf import CSRFProtect
import subprocess

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = '1234567891234567893242341230498120348719035192038471902873491283510981834712039847124123940812903752903847129038471290835710289675413864310867135'
csrf = CSRFProtect()
csrf.init_app(app)

userDict = dict()
result = ''

class RegistrationForm(Form):
    uname = StringField('Username', [validators.DataRequired(message="Enter UserName"),validators.Length(min=6, max=20)])
    pword = PasswordField('Password', [validators.DataRequired(message="Enter Password"),validators.Length(min=6, max=20)])
    mfa = StringField('2FA', [validators.DataRequired(message="Enter 10 Digit Phone Number"),validators.Length(min=11,max=11,message="Enter 11 Digit Phone Number")], id='2fa')

class wordForm(Form):
    textbox = TextAreaField('textbox', [validators.DataRequired(message="Enter Words to Check"),validators.Length(max=20000)])
    

# 3 forms with each function for processing (register & login & spellinput)
@app.route('/')
def index():
    return "Welcome to Joe Gumke JDG597 - Spell Checker Web Application!!!"

# Form for register 
@app.route('/register', methods=['POST','GET'])
def register():
    registrationform = RegistrationForm(request.form)

    if request.method == 'POST' and registrationform.validate():
        uname = (registrationform.uname.data)
        pword = (registrationform.pword.data)
        mfa = (registrationform.mfa.data)
        result = ''

        if uname in userDict.keys():
            result='failure'
            error='User Already Exists, Please Login Or Register New Username'
            return render_template('register.html', form=registrationform, result=result,error=error)

        if uname not in userDict.keys():
            userDict[uname] = [[pword],[mfa]]
            result='success'
            error="Successful Registration Please Login"
            return render_template('register.html', form=registrationform, result=result,error=error)
 
    if request.method == 'GET' and not session.get('logged_in'):
        error='Not Logged In, Please Register or Login'
        result='failure'
        return render_template('register.html', form=registrationform, result=result,error=error)

    else:
        result=''
        error='hit else'
        return render_template('register.html', form=registrationform, result=result,error=error)

# Form for login
@app.route('/login', methods=['POST','GET'])
def login():
    loginform = RegistrationForm(request.form)

    if session.get('logged_in'):
        result='result'
        error='Already Logged In'
        return render_template('login.html', form=loginform, result=result,error=error)

    if request.method == 'POST' and loginform.validate() and not session.get('logged_in'): 
        uname = (loginform.uname.data)
        pword = (loginform.pword.data)
        mfa = (loginform.mfa.data)
        if uname in userDict.keys() and pword in userDict[uname][0] and mfa in userDict[uname][1]:
            session['logged_in'] = True
            result='result'
            error="Successful Authentication"
            return render_template('login.html', form=loginform, result=result,error=error)

        else:
            result='failure'
            error='Invalid Username, Please Login or Register'
            return render_template('login.html', form=loginform, result=result,error=error)

    if request.method == 'GET' and loginform.validate() and not session.get('logged_in'): 
        result=''
        error='GET LOGIN'
        return render_template('login.html', form=loginform, result=result,error=error)

    else:
        result=''
        error='login else statement'
        return render_template('login.html', form=loginform, result=result,error=error)


@app.route('/home', methods=['POST','GET'])
def home():
    if session.get('logged_in') and request.method =='GET':
        result='success'
        error = 'Authenticated User '
        return render_template('home.html', result=result, error=error)
    
    if not session.get('logged_in') and request.method == ('GET' or 'POST'):
        result='failure'
        error = 'Please Login to Access Home '
        return render_template('home.html', result=result, error=error)

    if session.get('logged_in') and request.method =='POST' and request.form['submit_button'] =='Log Out':
        error='Logged Out'
        result='success'
        session.pop('logged_in', None)
        return render_template('home.html', result=result, error=error)

    if session.get('logged_in') and request.method =='POST' and request.form['submit_button'] =='Spell Checker':
        result='success'
        error='Successful Request to Spell Checker'
        return render_template('home.html', result=result, error=error)

    else:
        result=''
        error='home else statement'
        return render_template('home.html', result=result, error=error)

# Text Submission && Result Retrieval 
@app.route('/spell_check', methods=['POST','GET'])
def spell_check():
    form = wordForm(request.form)
    misspelled =[]

    if session.get('logged_in') and request.method == 'GET':
        result='success'
        error='Successful Request to Spell Checker'
        return render_template('spell_check.html', form=form,result=result, error=error)

    if session.get('logged_in') and request.method == 'POST' and request.form['submit_button'] == 'Check Spelling':
        data = (form.textbox.data)
        tempFile = open("temp.txt","w")
        tempFile.write(data)
        tempFile.close()
        testsub = subprocess.Popen(["./a.out", "temp.txt", "wordlist.txt"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = testsub.stdout.read().strip()
        testsub.terminate()
        for line in output.decode('utf-8').split('\n'):
            misspelled.append(line.strip())
        return render_template('results.html', misspelled=misspelled)
        #except:
        #    return "errors"
        #return render_template('spell_check.html', form=form)

    if not session.get('logged_in'):
        result='failure'
        error='Login Before Accessing Spell Checker'
        return render_template('spell_check.html', form=form,result=result, error=error)

    else:
        error='spellCheck else statement'
        result=''
        return render_template('spell_check.html', form=form, result=result, error=error)
        #return redirect('/login')

    #return render_template('spell_check.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
	
