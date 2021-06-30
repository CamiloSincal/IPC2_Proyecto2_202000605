from os import truncate
from django.shortcuts import render,redirect
from django.utils import encoding
import requests as req
from xml.etree import ElementTree as ET
from xml.dom import minidom
from .models import Profile
import random
import re
from django.contrib import messages

dic = {}
class listaJuegos:
    def __init__(self,nombre,stock,estado):
        self.nombre = nombre
        self.stock = stock
        self.estado = estado

class cumpleData:
    def __init__(self,nombreC,fechaC) :
        self.nombreC = nombreC
        self.fechaC = fechaC
        
# Create your views here.
def principal(request):
    
    #Arreglos locales para almacenamiento de datos
    nombresMejoresClientes = []
    montosGastados = []
    barColors = []

    nombresDeJuegos = []
    copiasVendidas = []
    pieColors = []

    tiposClasificacion = []
    cantidadPClasificacion = []
    coloresBar2 = []

    nombresCump = []
    apellidosCump = []
    fechasCump = []
    totalCump = []

    nombreTodosJuegos = []
    stockJuegos = []
    estadoJuegos = []
    todosJuegos =[]
    global dic
    xmltext = req.get('http://localhost:5000/getxml')
    stringXML = xmltext.text
    #Recorrido de nuevo XML
    doc = minidom.parseString(stringXML)
    #Busco los juegos más vendidos
    juegosV =  doc.getElementsByTagName('juegosMasVendidos')
    for juego in juegosV:
        nombresJuegos = juego.getElementsByTagName('nombre')
        copiasV = juego.getElementsByTagName('copiasVendidas')
        for nombre in nombresJuegos:
            nombresDeJuegos.append(nombre.firstChild.data)
        
        for copia in copiasV:
            copiasVendidas.append(int(copia.firstChild.data))
        #Agrego un conjunto de colores para la gráfica
        for i in range(len(nombresJuegos)):
            r = int(random.randint(0,255))
            g = int(random.randint(0,255))
            b = int(random.randint(0,255))
            color = 'rgb('+str(r)+','+str(g)+','+str(b)+')'
            pieColors.append(color)
    #Busco a los mejores Clientes
    mjClientes = doc.getElementsByTagName('mejoresClientes')
    for client in mjClientes:
        #Busco los atributos para la gráfica
        nombresClt = client.getElementsByTagName('nombre')
        montos = client.getElementsByTagName('monto')
        for nomb in nombresClt:
            nombresMejoresClientes.append(nomb.firstChild.data)
        for mont in montos:
            montosGastados.append(mont.firstChild.data)
        #Agrego un conjunto de colores para la gráfica
        for j in range(len(nombresClt)):
            r = int(random.randint(0,255))
            g = int(random.randint(0,255))
            b = int(random.randint(0,255))
            color = 'rgb('+str(r)+','+str(g)+','+str(b)+')'
            barColors.append(color)
        #Busco la etiqueta para clasificaciones
        clasificaciones = doc.getElementsByTagName('clasificaciones')
        for clasificaicon in clasificaciones:
            #Busco los atributos:
            tipos = clasificaicon.getElementsByTagName('tipo')
            cantidad = clasificaicon.getElementsByTagName('cantidad')
            for tipo in tipos:
                tiposClasificacion.append(tipo.firstChild.data)
            for cnt in cantidad:
                cantidadPClasificacion.append(cnt.firstChild.data)
        #Genero colores para cada barra
        for k in range(len(tiposClasificacion)):
            r = int(random.randint(0,255))
            g = int(random.randint(0,255))
            b = int(random.randint(0,255))
            color = 'rgb('+str(r)+','+str(g)+','+str(b)+')'
            coloresBar2.append(color)
    #Busco el tag de los cumpleaños
    cumpleanios = doc.getElementsByTagName('cumpleaños')
    for cump in cumpleanios:
        #Busco los atributos
        nombreCum = cump.getElementsByTagName('nombre')
        apellidoCum = cump.getElementsByTagName('apellido')
        fechaCum = cump.getElementsByTagName('fecha')
        for nmCum in nombreCum:
            nombresCump.append(nmCum.firstChild.data)
        for apell in apellidoCum:
            apellidosCump.append(apell.firstChild.data)
        for fechCum in fechaCum:
            fechasCump.append(fechCum.firstChild.data)
    #Almaceno los datos en un nuevo arreglo
    for j in range(len(nombresCump)):
        newCumpleanio = cumpleData(nombresCump[j]+' '+apellidosCump[j],fechasCump[j])
        totalCump.append(newCumpleanio)
    #Busco el tag para todos los juegos
    tJuegos = doc.getElementsByTagName('listaJuegos')
    for jueg in tJuegos:
        #Busco los Atributos
        nombreJuego = jueg.getElementsByTagName('nombre')
        stockJuego = jueg.getElementsByTagName('stock')
        #Recorro los atributos y almaceno valores
        for nmJuego in nombreJuego:
            nombreTodosJuegos.append(nmJuego.firstChild.data)
        for stock in stockJuego:
            stockJuegos.append(stock.firstChild.data)
            #Determino el valor del stock para verificar si es mayor a 10 y establecer el estado
            if int(stock.firstChild.data) < 10:
                estadoJuegos.append('rojo')
            else:
                estadoJuegos.append('normal')
    #Almaceno los datos en un arreglo de clases
    for k in range(len(nombreTodosJuegos)):
        newReg = listaJuegos(nombreTodosJuegos[k],stockJuegos[k],estadoJuegos[k])
        todosJuegos.append(newReg)
    
    dic['dataJuegos'] = todosJuegos
    dic['dataCum'] = totalCump
    dic['fechasCum'] = fechasCump
    dic['content'] = stringXML
    dic['namesGames'] = nombresDeJuegos
    dic['copias'] = copiasVendidas
    dic['namesC'] = nombresMejoresClientes
    dic['gasto'] = montosGastados
    dic['Clasificacion'] = tiposClasificacion
    dic['numClas'] = cantidadPClasificacion
    dic['colores'] = pieColors
    dic['barColores'] = barColors
    dic['clasColors'] = coloresBar2
    return render(request,'index.html',dic)

def csvProcess(request):
    #Variables de regex para verificar los CSV
    patronEdad = "^[0-9]{2}$"
    patronNombre = "(^[A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙ]+\s*$|^[A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙ]+\s[A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙ]+$)"
    patronFecha = "(^[0-2]{1}[0-9]{1}(/|-)[0]{1}[0-9]{1}(/|-)[0-9]{4}$|^[0-2]{1}[0-9]{1}(/|-)[1]{1}[0-2]{1}(/|-)[0-9]{4}$|^[3]{1}[0-1]{1}(/|-)[1]{1}[0-2]{1}(/|-)[0-9]{4}$|^[3]{1}[0-1]{1}(/|-)[0]{1}[0-9]{1}(/|-)[0-9]{4}$)"
    patronanio = "^[0-9]{4}$"
    patronCantidad = "^[0-9]*$"
    patronDecimal = "^[0-9]*\.+[0-9]+$"
    patronClas = "(^E{1}$|^T{1}$|^M{1}$)"
    patronPlataforma = "(^[A-Za-z0-9]+\s*$|^[A-Za-z0-9]+\s[A-Za-z0-9]+$)"
    #Variable que indica si se procede a la creacion del XML o no
    convertirXML = True
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
        #----------------------------Verificacion de contenidos---------------------------------------------
        #=====================================Clientes======================================================
        for filaEnClientes in range(len(clientes)-1):
        #--------------Nombres
            if not re.match(patronNombre,clientes[filaEnClientes+1][0]):
                convertirXML = False
                messages.error(request,"Se encontró "+str(clientes[filaEnClientes+1][0])+" en el archivo de Clientes, el cual no es un valor valido para los nombres.")
                break
        #--------------Apellidos
            if not re.match(patronNombre,clientes[filaEnClientes+1][1]):
                    convertirXML = False
                    messages.error(request,"Se encontró "+str(clientes[filaEnClientes+1][1])+" en el archivo de Clientes, el cual no es un valor valido para los apellidos.")
                    break
        #--------------Edades
            if not re.match(patronEdad,clientes[filaEnClientes+1][2]):
                    convertirXML = False
                    messages.error(request,"Se encontró "+str(clientes[filaEnClientes+1][2])+" en el archivo de Clientes, el cual no es un valor valido para la edad.")
                    break
        #------------Fecha Nacimiento
            if not re.match(patronFecha,clientes[filaEnClientes+1][3]):
                    convertirXML = False
                    messages.error(request,"Se encontró "+str(clientes[filaEnClientes+1][3])+" en el archivo de Clientes, el cual no es un valor valido para la fecha de nacimiento.")
                    break
        #------------Primera Compra
            if not re.match(patronFecha,clientes[filaEnClientes+1][4]):
                    convertirXML = False
                    messages.error(request,"Se encontró "+str(clientes[filaEnClientes+1][4])+" en el archivo de Clientes, el cual no es un valor valido para la fecha de la primera compra.")
                    break
        #=====================================Mejores Clientes======================================================
        for cadaFilaMjCliente in range(len(mejoresClientes)-1):
        #----------Verifico el nombre
            if not re.match(patronNombre,mejoresClientes[cadaFilaMjCliente+1][0]):
                convertirXML = False
                messages.error(request,"Se encontró "+str(mejoresClientes[cadaFilaMjCliente+1][0])+" en el archivo de Mejores Clientes, el cual no es un valor valido para el nombre.")
                break
        #----------Verifico la Fecha de la Ultima compra------------------------
            if not re.match(patronFecha,mejoresClientes[cadaFilaMjCliente+1][1]):
                convertirXML = False
                messages.error(request,"Se encontró "+str(mejoresClientes[cadaFilaMjCliente+1][1])+" en el archivo de Mejores Clientes, el cual no es un valor valido para la fecha de la ultima compra.")
                break
        #-----------Verifico la cantidad Comprada-------------------------------
            if not re.match(patronCantidad,mejoresClientes[cadaFilaMjCliente+1][2]):
                convertirXML = False
                messages.error(request,"Se encontró "+str(mejoresClientes[cadaFilaMjCliente+1][2])+" en el archivo de Mejores Clientes, el cual no es un valor valido para la cantidad de compra.")
                break
        #-----------Verifico la cantidad Gastada por cliente---------------------
            if not re.match(patronDecimal,mejoresClientes[cadaFilaMjCliente+1][3]) and convertirXML == True:
                if re.match(patronCantidad,mejoresClientes[cadaFilaMjCliente+1][3]):
                    mejoresClientes[cadaFilaMjCliente+1][3] = str(mejoresClientes[cadaFilaMjCliente+1][3])+'.00'
                else:
                    convertirXML = False
                    messages.error(request,"Se encontró "+str(mejoresClientes[cadaFilaMjCliente+1][3])+" en el archivo de Mejores Clientes, el cual no es un valor valido para la cantidad Gastada.")
                    break
        #===============================Juegos Mas vendidos======================================================
        for cadaFilaJuegoMV in range(len(juegosMasVendidos)-1):
        #----------------Dado que los juegos pueden tener carácteres extraños no los verifico-----------------
        #-------------Verifico la Ultima Compra------------------
            if not re.match(patronFecha,juegosMasVendidos[cadaFilaJuegoMV+1][1]):
                convertirXML = False
                messages.error(request,"Se encontró "+str(juegosMasVendidos[cadaFilaJuegoMV+1][1])+" en el archivo de Juegos más Vendidos, el cual no es un valor valido para la fecha de la ultima compra.")
                break
        #------------Verifico las copias vendidas------------------
            if not re.match(patronCantidad,juegosMasVendidos[cadaFilaJuegoMV+1][2]):
                convertirXML = False
                messages.error(request,"Se encontró "+str(juegosMasVendidos[cadaFilaJuegoMV+1][2])+" en el archivo de Juegos más Vendidos, el cual no es un valor valido para las copias vendidas.")
                break
        #------------Verifico el stock---------------------
            if not re.match(patronCantidad,juegosMasVendidos[cadaFilaJuegoMV+1][3]):
                convertirXML = False
                messages.error(request,"Se encontró "+str(juegosMasVendidos[cadaFilaJuegoMV+1][3])+" en el archivo de Juegos más Vendidos, el cual no es un valor valido para el stock.")
                break
        #=======================Todos los juegos-------------------------
        for cadaFilaJuego in range(len(juegos)-1):
        #----------------Dado que los juegos pueden tener carácteres extraños no los verifico-----------------
        #----------------------Verifico el nombre de la plataforma--------------
            if not re.match(patronPlataforma,juegos[cadaFilaJuego+1][1]):
                convertirXML = False
                messages.error(request,"Se encontró "+str(juegos[cadaFilaJuego+1][1])+" en el archivo de juegos, el cual no es un valor valido para el nombre de la plataforma.")
                break
        #-----------------------------Verifico el año------------------
            if not re.match(patronanio,juegos[cadaFilaJuego+1][2]):
                convertirXML = False
                messages.error(request,"Se encontró "+str(juegos[cadaFilaJuego+1][2])+" en el archivo de juegos, el cual no es un valor valido para el año de publicación.")
                break
        #--------------------Verifico la clasificación-----------------
            if not re.match(patronClas,juegos[cadaFilaJuego+1][3]):
                convertirXML = False
                messages.error(request,"Se encontró "+str(juegos[cadaFilaJuego+1][3])+" en el archivo de juegos, el cual no es un valor valido para las clasificaciones.")
                break
        #------------------Verifico el stock---------------------
            if not re.match(patronCantidad,juegos[cadaFilaJuego+1][4]):
                convertirXML = False
                messages.error(request,"Se encontró "+str(juegos[cadaFilaJuego+1][4])+" en el archivo de juegos, el cual no es un valor valido para el stock.")
                break
        #----------------------------------Creación de XML--------------------------------------------------
        if convertirXML:
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
            #req.post('http://localhost:5000/xml',xmlText)
            dic['XML'] = finalXMLText.toprettyxml(indent="\t")
        convertirXML = True
        
    return redirect('index')

def sendXML(request):
    if request.method == 'POST':
        xmldata = request.POST.get('out')
        data = xmldata.encode('utf-8')
        req.post('http://localhost:5000/xml',data)
    return redirect('index')