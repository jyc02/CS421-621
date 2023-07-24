import os
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'datasqlite')
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False
db=SQLAlchemy(app)

app.config['SECRET_KEY'] = 'oursecretkey'


class MyForm(FlaskForm):
    username = StringField('Username: ')
    email = StringField('Email: ')
    password = StringField ('Password: ')
    confirmPw = StringField ('Confirm Password: ')
    submit = SubmitField("Login")

class SignUpForm(MyForm):
    submit = SubmitField("Sign Up")

#USER MODEL IN FLASK
class User(db.Model):
    __tablename__="user"

    id= db.Column(db.Integer, primary_key=True)
    user= db.Column(db.Text)
    pw= db.Column(db.Text)
    email = db.Column(db.Text)

    def __init__(self,user,pw,email):
        self.user = user
        self.pw = pw
        self.email = email

    def __repr__(self):
        return f"user: {self.user} | pw: {self.pw} | email: {self.email}"
    

with app.app_context():
    db.create_all()
    db.session.commit()
    

@app.route('/', methods=['GET', 'POST'])
def login():
    username = False
    form = MyForm()
    logUser = "Username: "
    logPw = "Password: "
    userError = ""
    pwError = ""
    message = ""
    success = False
    if form.validate_on_submit():
        user = form.username.data
        pw = form.password.data
        if user != "":
            pass
        else:
            userError = "user is empty"
            if pw == "":
                pwError = "pw is empty"
            return render_template('login.html', form = form, logUser = logUser, logPw = logPw, userError = userError, pwError = pwError, message=message)
        if pw != "":
            pass
        else:
            pwError = "pw is empty"
            return render_template('login.html', form = form, logUser = logUser, logPw = logPw, userError = userError, pwError = pwError, message=message)
        
        for login in User.query.all():
            if login.user == user:
                if login.pw == pw:  
                    return redirect(url_for('secretPage'))
                    # return render_template('secretPage.html')
        message = "Incorrect login info!"
        return render_template('login.html', form = form, logUser = logUser, logPw = logPw, userError = userError, pwError = pwError, message=message)
        # form.username.data=''
        # form.password.data=''

    return render_template('login.html', form = form, logUser = logUser, logPw = logPw)

def verifyPw(pw):
    upperFlag = False
    lowerFlag = False
    numFlag = False
    message = ""
    error_list = []
    if len(pw)>0:
        if pw[-1].isnumeric():
            numFlag = True
        
        for char in pw:
            if char.isupper():
                upperFlag = True
                
            if char.islower():
                lowerFlag = True
                
        if numFlag == False:
            message = "password is missing number at the end"
            error_list.append(message)
        if lowerFlag == False:
            message = "password is missing lowercase character"
            error_list.append(message)
        if upperFlag == False:
            message = "password is missing uppercase character"
            error_list.append(message)

    return error_list




@app.route('/signup', methods=['GET', 'POST'])
def signup ():
    form = SignUpForm()
    userError = ""
    pwError = ""
    emailError = ""
    logUser = "Username: "
    logPw = "Password: "
    logEmail = "Email: "
    user = ""
    pw = ""
    email = ""
    if form.validate_on_submit():
        user = form.username.data
        pw = form.password.data
        email = form.email.data
        error_list = verifyPw(form.password.data)
        if user != "":
            pass
        else:
            userError = "user is empty"
            if pw == "":
                pwError = "password is empty"
            elif pw != form.confirmPw.data:
                pwError = "passwords do not match!"
            if email == "":
                emailError = "email is empty"
            elif not "@" in email:
                emailError = "invalid email, missing @"
            return render_template('signup.html', form = form, logUser = logUser, logPw = logPw, logEmail = logEmail, userError = userError, pwError = pwError, emailError=emailError, error_list = error_list)
        

        if pw != "":
            pass
        else:
            if email == "":
                emailError = "email is empty"
            elif not "@" in email:
                emailError = "invalid email, missing @"
            if pw == "":
                pwError ="password is empty"
            if pw != form.confirmPw.data:
                pwError = "passwords do not match!"
            return render_template('signup.html', form = form, logUser = logUser, logPw = logPw, logEmail = logEmail, userError = userError, pwError = pwError, emailError=emailError, error_list = error_list)
        
        if email == "":
            emailError = "email is empty"
            if pw == "":
                pwError = "pw is empty"
            elif pw != form.confirmPw.data:
                pwError = "passwords do not match!"
            error_list = verifyPw(pw)
            return render_template('signup.html', form = form, logUser = logUser, logPw = logPw, logEmail = logEmail, userError = userError, pwError = pwError, emailError=emailError, error_list = error_list)
        elif not "@" in email:
            emailError = "invalid email, missing @"
            if pw == "":
                pwError = "pw is empty"
            elif pw != form.confirmPw.data:
                pwError = "passwords do not match!"
            return render_template('signup.html', form = form, logUser = logUser, logPw = logPw, logEmail = logEmail, userError = userError, pwError = pwError, emailError=emailError, error_list = error_list)

    
        if pw != form.confirmPw.data:
            pwError = "Passwords do not match!"
            return render_template('signup.html', form = form, logUser = logUser, logPw = logPw, logEmail = logEmail, userError = userError, pwError = pwError, emailError=emailError, error_list=error_list)


        for userInfo in User.query.all():
            if userInfo.email == email:
                emailError = "Email address already in use"
                return render_template('signup.html', form = form, logUser = logUser, logPw = logPw, logEmail = logEmail, userError = userError, pwError = pwError, emailError=emailError, error_list = error_list)

        if len(error_list) > 0:
            return render_template('signup.html', form = form, logUser = logUser, logPw = logPw, logEmail = logEmail, userError = userError, pwError = pwError, emailError=emailError, error_list = error_list)


        with app.app_context():
            newUser = User(user, pw, email)
            db.session.add(newUser)
            db.session.commit()
            all_users = User.query.all()
            print(all_users)
        return redirect(url_for('thankyou'))
    return render_template('signup.html', form = form, logUser = logUser, logPw = logPw, logEmail = logEmail, userError = userError, pwError = pwError, emailError=emailError)

@app.route('/secretPage')
def secretPage():
    return render_template('secretPage.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)