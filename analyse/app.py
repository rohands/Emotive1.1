from flask import Flask, flash, redirect, render_template, request, session, abort
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
# from flask_cors import CORS
import psycopg2
import requests
import json
import re
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/emotive'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    phone = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    first_message = db.Column(db.String(255), unique=True)
    pos_message = db.Column(db.String(255), unique=True)
    neg_message = db.Column(db.String(255), unique=True)

    def __init__(self, email):
        self.phone = phone
        self.name = name
        self.first_message = first_message
        self.pos_message = pos_message
        self.neg_message = neg_message


    def __repr__(self):
        return '<Phone %d>' % self.phone
# CORS(app)

first_session = True
account_sid = "ACcb73e44e38653e08f174446161e4c276"
auth_token  = "6f60d9fffbac16025702d41d4d0f37b4"

SENTIMENT_ENDPOINT = "https://eastus2.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"
SENTIMENT_KEY = "89d6afcc5e9b477182a4e1700b4f0f54"



try:
    connection = psycopg2.connect(user = "rohands",password = "rohan",host = "127.0.0.1",
                                  port = "5432",database = "emotive")
    cursor = connection.cursor()
    connection.autocommit = True
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)

@app.route('/', methods=['GET'])
def load():
	return render_template('dashboard.html')



@app.route('/sms/', methods=['POST','GET'])
def receive_sms():
	if request.method == 'GET':
		return 'Receiving URL'
	else:
		message_body = request.form['Body']
		sender = request.form['From']
		print message_body,sender[2:]

		try:
			cursor.execute("SELECT pos_message,neg_message FROM users WHERE phone = %s;" % (sender[2:]))
			rows = cursor.fetchone()
		except Exception as e:
			# reconnect_db()
			return "Failed to retrieve data about the phone number"

		try:
			data = '''{"documents": [{"language": "en","id": "1","text": "%s"}]}''' % str(message_body)
			print data

			headers = { 'Ocp-Apim-Subscription-Key': SENTIMENT_KEY, 'Content-Type':'application/json','Accept':'application/json'}
			res = requests.post(url = SENTIMENT_ENDPOINT, data = data, headers = headers).text
			print res
			sentiment = json.loads(res)["documents"][0]["score"]
			resp = MessagingResponse()
			resp.message(rows[1]) if sentiment < 0.5 else resp.message(rows[0])
			return str(resp)
		except Exception as e:
			return "Failed to retrieve sentiment"

		

@app.route('/send/', methods=['POST','GET'])
def send_sms():
	if request.method == 'GET':
		return 'Sending URL'
	else:
		try:
			cursor.execute("BEGIN;INSERT INTO users values ('%s','%s','%s','%s','%s'); COMMIT;" % 
				(request.form["phone"],request.form["name"].replace("'","''"),request.form["first"].replace("'","''"),
					request.form["pos"].replace("'","''"),request.form["neg"].replace("'","''")))

		except (Exception, psycopg2.Error) as error:
			cursor.execute("ROLLBACK;");
			print "Error while connecting to PostgreSQL", error
			# reconnect_db()
			return "Database updation failed",error


		try:
			client = Client(account_sid, auth_token)
			message = client.messages.create(to="+1"+request.form["phone"], 
			    from_="+15412142354",body=request.form["first"])
			print(message.sid)
		except Exception as e:
			print e
			return "Message sending failed"

		return "Success!"

def reconnect_db():
	global connection
	global cursor
	if connection:
		cursor.close()
		connection.close()
		print("PostgreSQL connection is closed")

	try:
	    connection = psycopg2.connect(user = "rohands",password = "rohan",host = "127.0.0.1",
	                                  port = "5432",database = "emotive")
	    cursor = connection.cursor()
	except (Exception, psycopg2.Error) as error :
	    print ("Error while connecting to PostgreSQL", error)



if __name__ == "__main__":
    app.run(debug=True)