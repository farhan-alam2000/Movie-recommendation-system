from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')

password = os.getenv("PASSWORD")
app.secret_key = os.getenv("APP_SECRET_KEY")

app.config['MONGO_URI'] = 'mongodb+srv://alaammfarhan:'+password+'@cluster0.xlweciy.mongodb.net/test'

mongo = PyMongo(app)

@app.route("/home", methods=['GET', 'POST'])
def home():
    # Fetch movie data and store it in a list
    movie_data = [
        {"title": "Batman", "poster_path": "/static/images/batman.jpeg"},
        {"title": "The Avengers", "poster_path": "/static/images/avengers.jpeg"}
    ]
    
    # Render the home.html template and pass in the movie data
    return render_template("home.html", movie_data=movie_data)





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        # Hash the password
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # Check if user already exists
        user = mongo.db.users.find_one({'email': email})
        if user:
            return 'Email already exists'

        # Add the user to the database
        mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password
        })

        return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        user = mongo.db.users.find_one({'email': email})
        print(user)
        if user:
            # Verify password
            if bcrypt.checkpw(password, user['password']):
                session['email'] = email
                print(email)
                return redirect(url_for('home'))
            else:
                error = 'Invalid password'
                return render_template('login.html', error = error)
        else:
            error = 'Email not found'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)

