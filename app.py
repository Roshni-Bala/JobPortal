from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)

# ======================================= LOGIN =====================================================
app.secret_key = 'roshnisSecretKEY!'

# Configure the MongoDB URI for the database
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Users'

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
        name = user['Name']
        return render_template('homepage.html', name=name)
    else:
        return 'Invalid email or password'

#-------------------------------- LOGIN DONE ----------------------------------

@app.route('/homepage')
@login_required
def homepage():
    user = mongo.db.Users.find_one({'Email': current_user.id})
    name = user['Name']
    return render_template('homepage.html', name=name)

@app.route('/hiring', methods=['POST', 'GET'])
def hiring():
    if request.method == 'POST':
        company_name = request.form.get('CompanyName')
        job_domain = request.form.get('JobDomain')
        primary_skill = request.form.get('PSkill')
        secondary_skill = request.form.get('SSkill')
        role = request.form.get('Role')
        experience = request.form.get('YoE')
        salary = request.form.get('Salary')

        hiring_data = {
            'CompanyName': company_name,
            'JobDomain': job_domain,
            'PSkill': primary_skill,
            'SSkill': secondary_skill,
            'Role': role,
            'YoE': experience,
            'Salary': salary
        }

        # Access the 'JobPortal' collection within the same database
        mongo.db.JobPortal.insert_one(hiring_data)
        return redirect(url_for('homepage'))

    return render_template('hiring.html')

@app.route('/apply', methods=['GET'])
@login_required
def apply():
    search_query = request.args.get('search_query', '')
    jobs = []
    if search_query:
        jobs = mongo.db.JobPortal.find({'$text': {'$search': search_query}})

    return render_template('apply.html', jobs=jobs)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'

if __name__ == '__main__':
    app.run(debug=True)
