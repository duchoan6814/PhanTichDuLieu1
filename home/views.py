from django.shortcuts import render
import pyrebase
import matplotlib.pyplot as plt
import io
import base64, urllib
import pandas as pd
from datetime import datetime
from html import unescape
from numpy.random import seed
from numpy.random import randn
from statsmodels.graphics.gofplots import qqplot

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

for i in range(len(df)):
    df.at[i, 'month'] = datetime.strptime(df.at[i, 'date'], '%Y-%m-%d').month

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

def boxPlot(str):
  return df.boxplot(column=str, vert=False)

def tanSo(x, y, title, rot):
  return df.plot(x=x, y=y, title=title, rot=rot)

def tanSoTichLuyPlot(tenCotTichLuyMoi, tenCotTanSo, x, y, rot, title):
  df[tenCotTichLuyMoi] = df[tenCotTanSo].cumsum()
  return df.plot(x=x, y=y, rot=rot, title=title)

def tanXuatPlot(cotCanTinh, cotMoi, x, y, rot, title):
  sum = df[cotCanTinh].sum()
  for i in range(len(df)):
    df.at[i, cotMoi] = (df.at[i, cotCanTinh]/sum)*100
  return df.plot(x=x, y=y, rot=20, title=title)

def tanXuatTichLuyPlot(cotMoi, cotCanTinh, x, y, rot, title):
  df[cotMoi] = df[cotCanTinh].cumsum()
  return df.plot(x=x, y=y, rot=rot, title=title)

def interquartile_range(column):
  Q1 = df[column].quantile(0.25)
  Q3 = df[column].quantile(0.75)
  IQR = Q3 - Q1
  return IQR


  # ===================================================================

def simpleChart(request):
  plt.clf()

  boxPlot('new_cases')
  uri = renderMatplotlib(plt)

  describe = df['new_cases'].describe()
  describes = {
    "count": describe['count'],
    "mean": describe['mean'],
    "std": describe['std'],
    "min": describe['min'],
    "haiNam": describe['25%'],
    "namMuoi": describe['50%'],
    "bayNam": describe['75%'],
    "max": describe['max'],
    "median": df['new_cases'].median(),
    "mode": df['new_cases'].mode()
  }

  doPhanTan = {
    "IQR": interquartile_range('new_cases'),
    "var": df['new_cases'].var(),
    "std": df['new_cases'].std(),
  }

  mucDo = {
    "knewness": df['new_cases'].skew(),
    "kurtosis": df['new_cases'].kurtosis()
  }

  plt.clf()
  fig, ax = plt.subplots()
  df['new_cases'].plot.kde(ax=ax, legend=False, title='Histogram new_cases')
  df['new_cases'].plot.hist(density=True, ax=ax,color ='red')
  ax.set_ylabel('new_cases')
  ax.grid(axis='y')
  ax.set_facecolor('#d8dcd0')
  hist = renderMatplotlib(plt)

  plt.clf()
  x= df['new_cases']
  data=  randn(len(x))
  qqplot(data,line ='s')
  plt.title('Biểu đồ phân phối chuẩn của new_cases')
  kiemDinh = renderMatplotlib(plt)

  data = {"uri": uri, "describe": describes, "doPhanTan": doPhanTan, "mucDo": mucDo, "hist": hist, "kiemDinh": kiemDinh}

  return render(request, 'components/newCase.html', {"data": data})

def newDeathsBoxPlot():
  return df.boxplot(column='new_deaths', vert=False)

def newDeath(request):
  plt.clf()

  boxPlot('new_deaths')
  uri = renderMatplotlib(plt)

  describe = df['new_deaths'].describe()
  describes = {
    "count": describe['count'],
    "mean": describe['mean'],
    "std": describe['std'],
    "min": describe['min'],
    "haiNam": describe['25%'],
    "namMuoi": describe['50%'],
    "bayNam": describe['75%'],
    "max": describe['max'],
    "median": df['new_deaths'].median(),
    "mode": df['new_deaths'].mode()
  }

  doPhanTan = {
    "IQR": interquartile_range('new_deaths'),
    "var": df['new_deaths'].var(),
    "std": df['new_deaths'].std(),
  }

  mucDo = {
    "knewness": df['new_deaths'].skew(),
    "kurtosis": df['new_deaths'].kurtosis()
  }

  plt.clf()
  fig, ax = plt.subplots()
  df['new_deaths'].plot.kde(ax=ax, legend=False, title='Histogram new_deaths')
  df['new_deaths'].plot.hist(density=True, ax=ax,color ='red')
  ax.set_ylabel('new_deaths')
  ax.grid(axis='y')
  ax.set_facecolor('#d8dcd0')
  hist = renderMatplotlib(plt)

  plt.clf()
  x= df['new_deaths']
  data=  randn(len(x))
  qqplot(data,line ='s')
  plt.title('Biểu đồ phân phối chuẩn của new_deaths')
  kiemDinh = renderMatplotlib(plt)

  data = {"uri": uri, "describe": describes, "doPhanTan": doPhanTan, "mucDo": mucDo, "hist": hist, "kiemDinh": kiemDinh}
  return render(request, 'components/newDead.html', {"data": data})

def tileCaseWithDeath(request):
  plt.clf()
  plt.pie([df['new_cases'].sum(), df['new_deaths'].sum()], labels=["Số ca mắc", "Tử vong"], autopct='%1.1f%%', colors=[ "#21bf73", "#fd5e53"])
  plt.title("Biểu đồ tỉ lệ ca mắc mới và tử vong do COVID-19 tại các bang ở Mỹ")
  tileCaMacVaChet = renderMatplotlib(plt)
  data = {"tileCaMacVaChet": tileCaMacVaChet}
  return render(request, 'components/tiLeCasesAndDeaths.html', {"data": data})

def macVaChetTheoThang(request):
  plt.clf()
  
  a = df.groupby('month')['new_cases', 'new_deaths'].sum().reset_index()
  plt.plot(a['month'].tolist(), a['new_cases'].tolist())
  plt.plot(a['month'].tolist(), a['new_deaths'].tolist())
  plt.title("Tổng số lượng người chết và mắc bệnh theo tháng")
  plt.xlabel("Tháng")
  plt.ylabel("Số ca")
  macVaChetTheoThang = renderMatplotlib(plt)
  data = {"macVaChetTheoThang": macVaChetTheoThang}
  return render(request, 'components/macVaChetTheoThang.html', {"data": data})