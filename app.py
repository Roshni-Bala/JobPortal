from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Users'


# ======================================= LOGIN =====================================================
app.secret_key = 'roshnisSecretKEY!'

mongo = PyMongo(app)
login_manager = LoginManager(app)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login_submit():
    email = request.form.get('Email')
    password = request.form.get('Password')
    user = mongo.db.Users.find_one({'Email': email})

    if user and user['Password'] == password:
        user_obj = User(email)
        login_user(user_obj)
        return 'Login successful'
    else:
        return 'Invalid email or password'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'

if __name__ == '__main__':
    app.run(debug=True)
