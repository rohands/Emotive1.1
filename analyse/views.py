from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from analyse.models import User
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
import requests
import json


#Should be moved to another config file, exposing API key not a nest practice!
account_sid = "ACcb73e44e38653e08f174446161e4c276"
auth_token  = "6f60d9fffbac16025702d41d4d0f37b4"

SENTIMENT_ENDPOINT = "https://eastus2.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"
SENTIMENT_KEY = "89d6afcc5e9b477182a4e1700b4f0f54"


def index(request):
    return render(request, 'analyse/dashboard.html', {})

@csrf_exempt
def send_sms(request):

	#Updating DB
	user = User(phone=request.POST["phone"],name=request.POST["name"].replace("'","''"),
		first_message=request.POST["first"].replace("'","''"),pos_message=request.POST["pos"].replace("'","''"),
		neg_message=request.POST["neg"].replace("'","''"))
	user.save()

	#Sending message using Twilio
	try:
		client = Client(account_sid, auth_token)
		message = client.messages.create(to="+1"+request.POST["phone"], from_="+15412142354",body=request.POST["first"])
	except Exception as e:
		print e
		return HttpResponse("Hello, world. Message sending failed")
	return HttpResponse("Successfully sent messages")

@csrf_exempt
def receive_sms(request):
	#Gathering details of sender
	message_body = request.POST['Body']
	sender = request.POST['From']

	print "Message received from ", sender[2:]

	#Getting user information
	user = User.objects.get(phone=sender[2:])


	#Gathering sentiment from Microsoft APIs and sending follow-up message
	try:
		#Preparing the payload
		data = '''{"documents": [{"language": "en","id": "1","text": "%s"}]}''' % str(message_body)
		headers = { 'Ocp-Apim-Subscription-Key': SENTIMENT_KEY, 'Content-Type':'application/json','Accept':'application/json'}
		res = requests.post(url = SENTIMENT_ENDPOINT, data = data, headers = headers).text
		
		#Obtaining sentiment from response
		sentiment = json.loads(res)["documents"][0]["score"]
		resp = MessagingResponse()

		#Decide which message to send
		resp.message(user.neg_message) if sentiment < 0.5 else resp.message(user.pos_message)

		return HttpResponse(str(resp))
	except Exception as e:
		return HttpResponse("Failed to retrieve sentiment")

	return HttpResponse("Thank you Twilio!")
