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
    mfa = StringField('Phone Number', [validators.DataRequired(message="Enter 10 Digit Phone Number"),validators.Length(min=11,max=11,message="Enter 11 Digit Phone Number")], id='2fa')

class wordForm(Form):
    textbox = TextAreaField('textbox', [validators.DataRequired(message="Enter Words to Check"),validators.Length(max=20000)])
    
# 3 forms with each function for processing (register & login & spellinput)
@app.route('/')
def index():
    return "Welcome to Joe Gumke JDG597 - Spell Checker Web Application!!!"

# Form for register 
@app.route('/register', methods=['POST','GET'])
def register():
    result='success'
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate() and not session.get('logged_in'):
        uname = (form.uname.data)
        pword = (form.pword.data)
        mfa = (form.mfa.data)

        if uname in userDict.keys():
            result='failure'
            return redirect('/register')

        if uname not in userDict.keys():
            userDict[uname] = [[pword],[mfa]]
            result='success'
            return redirect('/login')
    if request.method == 'GET' and session.get('logged_in'):
        result='success'
        return redirect('/login')
    else:
        result=''
        return render_template('register.html', form=form, result=result)

# Form for login
@app.route('/login', methods=['POST','GET'])
def login():
    form = RegistrationForm(request.form)

    if request.method == ('GET' or 'POST') and session.get('logged_in'):
        result='success'
        return redirect('/home')

    if request.method == 'POST' and form.validate(): 
        uname = (form.uname.data)
        pword = (form.pword.data)
        mfa = (form.mfa.data)
        if uname in userDict.keys() and pword in userDict[uname][0] and mfa in userDict[uname][1]:
            session['logged_in'] = True
            result='success'
            return redirect('/home')
        if session.get('logged_in'):
            result='success'
            return redirect('/home')
        else:
            result='failure'
            return redirect('/register')
    if request.method == ('GET' or 'POST') and not session.get('logged_in') and request.referrer =='http://localhost:5000/register' :
        result='success'
    else:
        result=''

    return render_template('login.html', form=form, result=result)

@app.route('/home', methods=['POST','GET'])
def home():
    #form = wordForm(request.form)
    if session.get('logged_in') and request.method =='GET':
        result='success'
        return render_template('home.html', result=result)
    
    if session.get('logged_in') and request.method =='POST' and request.form['submit_button'] =='Log Out':
        session.pop('logged_in', None)
        result=''
        return redirect('/login')

    if session.get('logged_in') and request.method =='POST' and request.form['submit_button'] =='Spell Checker':
        return redirect('/spell_check')
    else:
        result='failure'
        return redirect('/login')

# Text Submission && Result Retrieval 
@app.route('/spell_check', methods=['POST','GET'])
def spell_check():
    form = wordForm(request.form)
    misspelled =[]

    if session.get('logged_in') and request.method == 'GET':
        return render_template('spell_check.html', form=form)

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

    else:
        return redirect('/login')

    return render_template('spell_check.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
	
