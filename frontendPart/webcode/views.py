from django.shortcuts import render,redirect
import requests as req

# Create your views here.
def principal(request):
    xmltext = req.get('http://localhost:5000/getxml')
    stringXML = xmltext.text
    dic = {'content':stringXML}
    return render(request,'index.html',dic)

def xmldata(request):
    if request.method == 'POST':
        archivo = request.FILES['xmldata']
        data = archivo.read()
        
        req.post('http://localhost:5000/xml',data)
        
    return redirect('index')
