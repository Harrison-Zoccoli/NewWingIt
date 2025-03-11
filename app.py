from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import os
from datetime import datetime
from matching import UserData, find_matches, send_match_email

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['STATIC_URL_PATH'] = '/static'

# Store travelers in memory (replace with database in production)
travelers = []

@app.route('/')
def index():
    return render_template('index.html', travelers=travelers)

@app.route('/add_traveler', methods=['GET', 'POST'])
def add_traveler():
    if request.method == 'POST':
        try:
            email = request.form['email']
            name = request.form['name']
            date_str = request.form['date']
            time_str = request.form['time']

            # Convert string inputs to date and time objects
            date_value = datetime.strptime(date_str, '%Y-%m-%d').date()
            time_value = datetime.strptime(time_str, '%H:%M').time()

            new_traveler = UserData(email, name, date_value, time_value)
            travelers.append(new_traveler)
            
            flash('Traveler added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding traveler: {str(e)}', 'error')
    
    return render_template('add_traveler.html')

@app.route('/find_matches')
def find_all_matches():
    all_matches = []
    for traveler in travelers:
        matches = find_matches(traveler, travelers)
        if matches:
            all_matches.extend(matches)
    
    return render_template('matches.html', matches=all_matches)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 