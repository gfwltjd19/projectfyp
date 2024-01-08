from flask import Flask, render_template, request, jsonify
from chat import get_response
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/')
def index_get():
    return render_template('About.html')

@app.route('/templates/About.html')
def about_page():
    return render_template('About.html')

@app.route('/templates/Services.html')
def services_page():
    return render_template('Services.html')

@app.route('/templates/Appointment.html')
def appointment_page():
    return render_template('Appointment.html')

@app.route('/templates/Contact.html')
def contact_page():
    return render_template('Contact.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


# Configuring MySQL  
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = 'fyp_data'

mysql = MySQL(app)

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if request.method == 'POST':
        try:
            # Extract form data for appointment booking
            name = request.form['full-name']
            phone = request.form['phone']
            email = request.form['email']
            services = request.form['services']
            date = request.form['date']
            time = request.form['time']

            # Create a cursor and execute the SQL query
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO appointments (name, phone, email, services, date, time) VALUES (%s, %s, %s, %s, %s, %s)", (name, phone, email, services, date, time))
            
            # Commit changes and close the cursor
            mysql.connection.commit()
            cur.close()

            return jsonify({'success': True})

        except Exception as e:
            app.logger.error(str(e))
            return jsonify({'success': False, 'error': str(e)})

    return render_template('appointment.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form['full-name']
            email = request.form['email']
            phone = request.form['phone']
            message = request.form['message']

            # Create a cursor and execute the SQL query
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO contact_messages(name, email, phone, message) VALUES (%s, %s, %s, %s)", (name, email, phone, message))

            # Commit changes and close the cursor
            mysql.connection.commit()
            cur.close()

            return jsonify({'success': True})

        except Exception as e:
            app.logger.error(str(e))
            return jsonify({'success': False, 'error': str(e)})

    return render_template('contact.html')

#if __name__ == '__main__':
 #   app.run(debug=True)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8082)
