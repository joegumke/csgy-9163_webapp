#app.py -- contains basics of python code. to start web service. 
	
from flask import Flask, request, url_for, redirect,render_template,flash,session
from flask_login import LoginManager, current_user, login_user
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField
import subprocess

#from wtforms.validators import ValidationError,DataRequired,Email
#from flask_wtf import FlaskForm

app = Flask(__name__)
app.secret_key = '1234567891234567893242341230498120348719035192038471902873491283510981834712039847124123940812903752903847129038471290835710289675413864310867135'
login_manager = LoginManager()
login_manager.init_app(app)

userDict = dict()

class RegistrationForm(Form):
    username = StringField('Username', [validators.DataRequired(),validators.Length(min=6, max=20)])
    email = StringField('Email Address', [validators.DataRequired(),validators.Email(),validators.Length(min=6, max=20)])
    password = PasswordField('Password', [validators.DataRequired(),validators.Length(min=6, max=20)])

class wordForm(Form):
    textbox = TextAreaField('textbox', [validators.DataRequired(),validators.Length(max=200)])


# 3 forms with each function for processing (register & login & spellinput)
@app.route('/')
def index():
    return "Welcome to Joe Gumke JDG597 - Spell Checker Web Application!!!"
    
	
# Form for register 
@app.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate() and not session.get('logged_in'):
        uname = (form.username.data)
        pword = (form.password.data)
        mfa = (form.email.data)

        if uname in userDict.keys():
            #flash("User Already Exists")
            return "User Already Exists"

        if uname not in userDict.keys():
            userDict[uname] = [[pword],[mfa]]
            #return redirect(url_for('login'))
            return redirect('/login')
            #flash("User Successfully Registered")

    if request.method == 'GET' and session.get('logged_in'):
        return redirect('/home')

    else:
        return render_template('register.html', form=form)

# Form for login
@app.route('/login', methods=['POST','GET'])
def login():
    form = RegistrationForm(request.form)

    if request.method == 'GET' and session.get('logged_in'):
        return redirect('/home')
        # return render_template('home.html')

    if request.method == 'POST' and form.validate(): 
        uname = (form.username.data)
        pword = (form.password.data)
        mfa = (form.email.data)
            #return 'Key:%s-- Value:%s ' % (key, value)
            #return 'result[pword]: %s' % (userDict[result['uname']][0])
            #return 'result[2fa]: %s' % (userDict[result['uname']][1])
            #return result['2fa']
        if uname in userDict.keys() and pword in userDict[pword][0] and mfa in userDict[mfa][0]:
            #### LAST SPOT #### get the indices properly working *****
            session['logged_in'] = True
            return render_template('home.html')
        else:
            #return "%s" % (pword)
            return "Unsuccessful Authentication"

    return render_template('login.html', form=form)

@app.route('/home', methods=['POST','GET'])
def home():
    form = wordForm(request.form)
    if session.get('logged_in') and request.method =='GET':
        return render_template('home.html')
    
    if session.get('logged_in') and request.method =='POST' and request.form['submit_button'] =='Log Out':
        session.pop('logged_in',None)
        return 'logout'

    if session.get('logged_in') and request.method =='POST' and request.form['submit_button'] =='Spell Checker':
        return redirect('/spell_check')
        #return render_template('spell_check.html', form=form)
    
    else:
        return 'You Must Login, Only Logged In Users Can Access...'

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
        #return redirect(url_for('login'))

    return render_template('spell_check.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
	
