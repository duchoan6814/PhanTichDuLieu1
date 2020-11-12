from django.shortcuts import render
import pyrebase

config = {
    "apiKey": "AIzaSyDoY8ph7q_upbbRWsWQXnqt3y_hvr4_pzE",
    "authDomain": "hello-world-74dc5.firebaseapp.com",
    "databaseURL": "https://hello-world-74dc5.firebaseio.com",
    "projectId": "hello-world-74dc5",
    "storageBucket": "hello-world-74dc5.appspot.com",
    "messagingSenderId": "773753015853",
    "appId": "1:773753015853:web:ca91fc690ee905857232a4",
    "measurementId": "G-6JP2XGQWMN"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

print(type(db.child("data1").get().val()))
# Create your views here.
def index(request):
  return render(request, 'pages/homePage.html')

def dataAnalysis(request):
  return render(request, 'pages/dataAnalysis.html')

def simpleChart(request):
  return render(request, 'components/newCase.html', db.child("data1").get().val())
