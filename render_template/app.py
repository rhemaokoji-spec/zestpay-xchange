from flask import Flask, render_template, request
import random
import smtplib
from email.message import EmailMessage
from flask import session

app = Flask(__name__)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        code = random.randint(100000, 999999)

        msg = EmailMessage()
        msg['Subject'] = 'ZestPay Password Recovery'
        msg['From'] = 'your-email@gmail.com'
        msg['To'] = email
        msg.set_content(f'Your verification code is: {code}')

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('your-email@gmail.com', 'your-app-password')
                smtp.send_message(msg)
            message = "Verification code has been sent to your email."
        except Exception as e:
            message = f"Error: {e}"

    return render_template('forgot_password.html', message=message)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        gender = request.form['gender']
        password = request.form['password']
        #confirm password = request.form['confirm password']
        # Save to DB here...
        return render_template('login.html', message="You have successfully created an account. Please log in.")
    return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        # Check DB
        user = get_user_by_phone(phone)
        if user and user['password'] == password:   



           session['user'] = user  # Store user in session
            return redirect('/dashboard')
        else:
            return render_template('login.html', message="Invalid credentials.")
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect('/login')
    return render_template('dashboard.html', user=user)



@app.route('/manage-account')
def manage_account():
    user = session.get('user')
    if not user:
        return redirect('/login')
    return render_template('manage_account.html', user=user)
     

if __name__ == "_main_":
  app.run(debug=True)
