from flask import Flask, request, redirect, url_for ,render_template#import main Flask class and request object
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
import logging

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)


scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Calcutta'})
scheduler.start()

app = Flask(__name__,static_url_path='', static_folder='web/static',) #create the Flask app

def notify_at_time(msg,number):
    print("printing %s at %s" % (msg, datetime.now()))
    print(number)
    apiUrl = 'https://notification-call-text-api.herokuapp.com/nexmo'
    data = {'number':number,'message':msg,'channel':'phone'}
    res = requests.post(apiUrl,data = data)
    print(res.text)

@app.route('/acceptdata', methods=["POST"])
def acceptdata():
	print("Got Request")
	time = request.form['time']
	email = request.form['email']
	number = request.form['number']
	msg = request.form['msg']
	print(time)
	print(email)
	print(number)
	print(msg)
	number = "91" + str(number)
	msg = "This is test from R7. Your reminder is " + msg
	date_time = datetime.strptime(str(time), '%d-%m-%Y %H:%M %p')
	job = scheduler.add_job(notify_at_time, trigger='date', next_run_time=str(date_time), args=[msg,number])
#	return redirect(url_for('index'))
	return render_template('reminderSuccessfull.html',time = str(time))

# @app.route('/acceptdata', methods=["POST"])
# def query_example():
# 	print("Got Request")
# 	time = request.form['time']
# 	email = request.form['email']
# 	number = request.form['number']
# 	msg = request.form['msg']
# 	print(time)
# 	print(email)
# 	print(number)
# 	print(msg)
# 	date_time = datetime.strptime(str(time), '%d-%m-%Y %H:%M %p')
# 	job = scheduler.add_job(notify_at_time, trigger='date', next_run_time=str(date_time), args=[msg,number])
# 	return ("job details: %s" % job)

@app.route('/')
def index():
	return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run() #run app in debug mode on port 5000

