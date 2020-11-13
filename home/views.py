from django.shortcuts import render
import pyrebase
import matplotlib.pyplot as plt
import io
import base64, urllib
import pandas as pd

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

df = pd.DataFrame(db.child("data3").get().val())

print(type(db.child("data1").get().val()))

def renderMatplotlib(plot):
  fig = plot.gcf()
  buf = io.BytesIO()
  fig.savefig(buf, format='png')
  buf.seek(0)
  string = base64.b64encode(buf.read())
  return urllib.parse.quote(string)

# Create your views here.
def index(request):
  return render(request, 'pages/homePage.html')

def dataAnalysis(request):
  return render(request, 'pages/dataAnalysis.html')

def boxPlot():
  return df.boxplot(column='new_cases', vert=False)

def tanSo():
  return df.plot(x='date', y='new_cases', title="Biểu đồ tần số ca mắc mới theo thời gian", rot=20)

def tanSoTichLuyPlot():
  df['tanSoTichLuyNewCase'] = df['new_cases'].cumsum()
  return df.plot(x='date', y='tanSoTichLuyNewCase', rot=20, title="Biểu đồ tần số tích lũy ca mắc mới theo thời gian")

def tanXuatPlot():
  sum = df['new_cases'].sum()
  for i in range(len(df)):
    df.at[i, 'tanXuat'] = (df.at[i, 'new_cases']/sum)*100
  return df.plot(x='date', y='tanXuat', rot=20, title="Biểu đồ tần xuất các ca mắc mới theo thời gian")

def tanXuatTichLuyPlot():
  df['tanXuatTichLuy'] = df['tanXuat'].cumsum()
  return df.plot(x='date', y='tanXuatTichLuy', rot=20, title="Biểu đồ tần xuất tích lũy ca mắc mới theo thời gian")

def simpleChart(request):
  boxPlot()
  uri = renderMatplotlib(plt)

  tanSo()
  tanso = renderMatplotlib(plt)

  tanSoTichLuyPlot()
  tanSoTichLuy = renderMatplotlib(plt)

  tanXuatPlot()
  tanXuat = renderMatplotlib(plt)

  tanXuatTichLuyPlot()
  tanXuatTichLuy = renderMatplotlib(plt)

  describe = df['new_cases'].describe()

  data = {"uri": uri, "describe": describe, "tanso": tanso, "tanSoTichLuy": tanSoTichLuy, "tanXuat": tanXuat, "tanXuatTichLuy": tanXuatTichLuy}

  return render(request, 'components/newCase.html', {"data": data})
