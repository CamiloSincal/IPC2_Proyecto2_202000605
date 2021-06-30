from django.shortcuts import render,redirect
from django.utils import encoding
import requests as req
from xml.etree import ElementTree as ET
from xml.dom import minidom
import codecs
dic = {}
# Create your views here.
def principal(request):
    global dic
    xmltext = req.get('http://localhost:5000/getxml')
    stringXML = xmltext.text
    dic['content'] = stringXML
    return render(request,'index.html',dic)

def csvProcess(request):
    global dic
    if request.method == 'POST':
        #------------------------------------Lectura de archivos-------------------------------------------
        #Lectura de la parte de clientes
        archivo = request.FILES.get('clientesdata')
        dataclientes = archivo.read().decode(encoding='UTF-8')
        filasClientes = dataclientes.splitlines()
        clientes = []
        for filaCliente in filasClientes:
            clientes.append(filaCliente.split(';'))
        #Lectura de los mejores Clientes
        archivo2 = request.FILES.get('mejoresdata')
        datamejores = archivo2.read().decode(encoding='UTF-8')
        filasmejores = datamejores.splitlines()
        mejoresClientes = []
        for fmClientes in filasmejores:
            mejoresClientes.append(fmClientes.split(';'))
        #Lectura de los juegos más vendidos
        archivo3 = request.FILES.get('juegosvendidosdata')
        datajuegosv = archivo3.read().decode(encoding='UTF-8')
        filasjuegosvendidos = datajuegosv.splitlines()
        juegosMasVendidos = []
        for fjuegosV in filasjuegosvendidos:
            juegosMasVendidos.append(fjuegosV.split(';'))
        #Lectura del archivo de juegos
        archivo4 = request.FILES.get('juegosdata')
        datajuegos = archivo4.read().decode(encoding='UTF-8')
        filasjuegos = datajuegos.splitlines()
        juegos = []
        for filaJ in filasjuegos:
            juegos.append(filaJ.split(';'))
        #----------------------------------Creación de XML--------------------------------------------------
        title = ET.Element('Chet')
        #Agregado de clientes al XML
        clientesTitle = ET.SubElement(title,'clientes')
        for fClientes in range(len(clientes)-1):
            nombre = ET.SubElement(clientesTitle,'nombre')
            apellido = ET.SubElement(clientesTitle,'apellido')
            edad = ET.SubElement(clientesTitle,'edad')
            fechaCump = ET.SubElement(clientesTitle,'fechaCumpleaños')
            fechaPC = ET.SubElement(clientesTitle,'fechaPrimeraCompra')
            nombre.text = clientes[fClientes+1][0]
            apellido.text = clientes[fClientes+1][1]
            edad.text = clientes[fClientes+1][2]
            fechaCump.text = clientes[fClientes+1][3]
            fechaPC.text = clientes[fClientes+1][4]
        #Agrego los mejores CLientes
        mejoresTitle = ET.SubElement(title,'mejoresClientes')
        for fmejoresClientes in range(len(mejoresClientes)-1):
            nomb = ET.SubElement(mejoresTitle,'nombre')
            fechaUC = ET.SubElement(mejoresTitle,'fechaUltimaCompra')
            cantidadC = ET.SubElement(mejoresTitle,'cantidadComprada')
            cantidadg = ET.SubElement(mejoresTitle,'cantidadGastada')
            nomb.text = mejoresClientes[fmejoresClientes+1][0]
            fechaUC.text = mejoresClientes[fmejoresClientes+1][1]
            cantidadC.text = mejoresClientes[fmejoresClientes+1][2]
            cantidadg.text = mejoresClientes[fmejoresClientes+1][3]
        #Agrego los juegos más vendidos
        vendidosTitle = ET.SubElement(title,'juegosMasVendidos')
        for fvendidos in range(len(juegosMasVendidos)-1):
            nombjuego = ET.SubElement(vendidosTitle,'nombre')
            fechULC = ET.SubElement(vendidosTitle,'fechaUltimaCompra')
            copiasV = ET.SubElement(vendidosTitle,'copiasVendidas')
            stock = ET.SubElement(vendidosTitle,'stock')
            nombjuego.text = juegosMasVendidos[fvendidos+1][0]
            fechULC.text = juegosMasVendidos[fvendidos+1][1]
            copiasV.text = juegosMasVendidos[fvendidos+1][2]
            stock.text = juegosMasVendidos[fvendidos+1][3]
        #Agrego todos los juegos
        juegosTitle = ET.SubElement(title,'juegos')
        for gamef in range(len(juegos)-1):
            nomJuego = ET.SubElement(juegosTitle,'nombre')
            plataforma = ET.SubElement(juegosTitle,'plataforma')
            anioL = ET.SubElement(juegosTitle,'añoLanzamiento')
            clas = ET.SubElement(juegosTitle,'clasificacion')
            stockJ = ET.SubElement(juegosTitle,'stock')
            nomJuego.text = juegos[gamef+1][0]
            plataforma.text = juegos[gamef+1][1]
            anioL.text = juegos[gamef+1][2]
            clas.text = juegos[gamef+1][3]
            stockJ.text = juegos[gamef+1][4]
        xmlText = ET.tostring(title,encoding='utf-8')
        finalXMLText = minidom.parseString(xmlText)
        req.post('http://localhost:5000/xml',xmlText)
        dic['XML'] = finalXMLText.toprettyxml(indent="\t")
        
        
        #Creacion de clientes

    return redirect('index')
