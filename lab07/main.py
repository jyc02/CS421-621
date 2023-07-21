import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask (__name__)

#set up database location and configure track modification settings so we dont have
#dont want to track every modification
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'datasqlite')
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False
db=SQLAlchemy(app)

class User(db.Model):
    __tablename__="user"

    id= db.Column(db.Integer, primary_key=True)
    user= db.Column(db.Text)
    pw=db.Column(db.Text)

    def __init__(self,user,pw):
        self.user = user
        self.pw = pw

    def __repr__(self):
        return f"user: {self.user} | pw: {self.pw}"
    
with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def index ():
    Logusername = request.args.get('Username')
    Logpassword = request.args.get('Password')
    message = ""
    for user in User.query.all():
        if user.user == Logusername:
            if user.pw == Logpassword:     
                return render_template('secretPage.html')
    return render_template('index.html', message = message)

@app.route('/secretPage')
def secretPage ():
    return render_template('secretPage.html')

@app.route('/signup')
def signup ():
    return render_template('signup.html')

@app.route('/thankyou')
def thankyou ():
    success = False
    user = request.args.get('Username')
    pw = request.args.get('Password')
    confirmpw = request.args.get('Confirmpassword')
    message = ""

    if pw != confirmpw or pw == "" or user =="":
        message =  "ERROR: Invalid Info"
    else:
        message = "thank you for signing up!"
        success = True

    if success:
        with app.app_context():
            newUser = User(user, pw)
            db.session.add(newUser)
            db.session.commit()
            all_users = User.query.all()
            print(all_users)
        
    return render_template('thankyou.html', message = message)

if __name__ == '__main__':
    app.run(debug=True)