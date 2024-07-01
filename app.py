import numpy as np
import model
from flask import Flask, request, render_template, redirect, url_for, session, flash, Response
import pickle

app = Flask(__name__, template_folder="templates")
model = pickle.load(open('model.pkl', 'rb'))

# Mock user database for demonstration purposes
users = {
    'admin': 'admin_password'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate user credentials
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            # Redirect back to the page the user was trying to access
            next_url = request.args.get('next') or url_for('index')
            return redirect(next_url)
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if not session.get('logged_in'):
        flash('Please login first.', 'warning')
        return redirect(url_for('login', next=request.url))
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not session.get('logged_in'):
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Perform prediction and display results
        gender = request.form['gender']
        stream = request.form['stream']
        internship = request.form['internship']
        cgpa = request.form['cgpa']
        backlogs = request.form['backlogs']
        arr = np.array([gender, stream, internship, cgpa, backlogs])
        brr = np.asarray(arr, dtype=float)
        output = model.predict([brr])
        if output == 1:
            out = 'You have high chances of getting placed!!!'
        else:
            out = 'You have low chances of getting placed. All the best.'
        return render_template('out.html', output=out)
    # Render the predict.html template for GET requests
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
