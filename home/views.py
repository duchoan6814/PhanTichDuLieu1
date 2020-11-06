from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'pages/homePage.html')

def dataAnalysis(request):
  return render(request, 'pages/dataAnalysis.html')

def simpleChart(request):
  return render(request, 'components/scatter.html')
