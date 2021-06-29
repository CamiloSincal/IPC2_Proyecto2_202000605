from os import truncate
from re import findall
from typing import Sized
from flask import Flask, request
from xml.etree import ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app,resources={r"/*": {"origin": "*"}})
#Clase para almacenar y controlar los datos de los mejores clientes del xml de retorno
class mejoresClientes:
    def __init__(self,nombre,monto):
        self.nombre = nombre
        self.monto = monto

#Clase para almacenar y controlar datos de los juegos mas vendidos
class juegosConMayorVenta:
    def __init__(self,nombre,ventas,fechaDeLanzamiento):
        self.nombre = nombre
        self.ventas = ventas
        self.fechaDeLanzamiento = fechaDeLanzamiento

class totalClasificaciones:
    def __init__(self,tipo,total):
        self.tipo = tipo
        self.total = total
class cumpleanio:
    def __init__(self,nombre,apellido,fecha):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha = fecha

class juegosChet:
    def __init__(self,nombre,stock):
        self.nombre = nombre
        self.stock = stock

mjClientes = []
juegosMasVendidos = []
totalClas = []
cumpleanios = []
totalG = []
@app.route("/xml",methods=['POST'])
def xmldata():
    #Importado de los arreglos de datos globales
    global mjClientes
    global juegosMasVendidos
    global totalClas
    global cumpleanios
    global totalG
    #Rquest del XML
    xmlString = request.data.decode('utf-8')
    doc = minidom.parseString(xmlString)
    #--------------------------------Obtención para mejores Clientes--------------------------------
    #Arreglos locasles para los datos
    nommjclientes = []
    montomjClientes = []
    #Ingreso al tag de mejores Clientes
    mejoresClt = doc.getElementsByTagName('mejoresClientes')
    #Recorro los mejores clientes para poder obtener el valor de los datos para la clase
    for mejorCliente in mejoresClt:
        #Obtengo los nombres
        nombre = mejorCliente.getElementsByTagName('nombre')
        for nom in nombre:
            nommjclientes.append(nom.firstChild.data)
        #Obtengo el monto Gastado
        monto = mejorCliente.getElementsByTagName('cantidadGastada')
        for nom in monto:
            montomjClientes.append(nom.firstChild.data)
    #Agrego los valores de los arreglos a una clase nueva y luego al arreglo general
    for i in range(len(nommjclientes)):
        newMejorCliente = mejoresClientes(nommjclientes[i],montomjClientes[i])
        mjClientes.append(newMejorCliente)
    #--------------------------------Obtención para juegos más vendidos-------------------------------
    #Ingreso al tag de juegos más vendidos
    juegosVendidos = doc.getElementsByTagName('juegosMasVendidos')
    #Arreglos locasles para los datos
    nomJuego = []
    copiasV = []
    fechasLanz = []
    #Recorro los juegos más vendidos para obtener los datos
    for juegos in juegosVendidos:
        #Obtengo los nombres:
        nombre = juegos.getElementsByTagName('nombre')
        for nom in nombre:
            nomJuego.append(nom.firstChild.data)
        #Obtengo las CopiasVenidas:
        copias = juegos.getElementsByTagName('copiasVendidas')
        for cop in copias:
            copiasV.append(cop.firstChild.data)
    #Ingreso al tag de juegos para buscar las fechas de publicación
    juegoGeneral = doc.getElementsByTagName('juegos')
    #Arreglos para las fechas y nombres correspondientes
    fechasLanzamiento = []
    nomjuegoFechas = []
    for juego in juegoGeneral:
        #Obtengo las fechas
        fecha = juego.getElementsByTagName('añoLanzamiento')
        for f in fecha:
            fechasLanzamiento.append(f.firstChild.data)
        nombreFechas = juego.getElementsByTagName('nombre')
        for n in nombreFechas:
            nomjuegoFechas.append(n.firstChild.data)
    #Comparo los nombres almacenados con los anteriores para verificar si existe información para la fecha
    for indice in range(len(nomJuego)):
        for indice2 in range(len(nomjuegoFechas)):
            if nomjuegoFechas[indice2] == nomJuego[indice]:
                fechasLanz.append(fechasLanzamiento[indice2])
                break
        fechasLanz.append('Sin datos')
    #Agrego los valores de los arreglos a una clase nueva y luego al arreglo general    
    for j in range(len(nomJuego)):
        newJuegoVendido = juegosConMayorVenta(nomJuego[j],copiasV[j],fechasLanz[j])
        juegosMasVendidos.append(newJuegoVendido)
    #--------------------------------Obtención para clasificacion-------------------------------
    #Ingreso al tag de juegos
    totalJuegos = doc.getElementsByTagName('juegos')
    #Arreglo para los datos
    tipoClasificacion = []
    for games in totalJuegos:
        clasificacion = games.getElementsByTagName('clasificacion')
        for clas in clasificacion:
            tipoClasificacion.append(clas.firstChild.data)
    #Remuevo clasificaciones repetidas
    tipoClasificacion = list(dict.fromkeys(tipoClasificacion))
    size = [0] * len(tipoClasificacion)
    #Recorro el arreglo de clasificaciones para determinar el numero de cada uno de estos
    for clf in clasificacion:
        pos = 0
        while pos < len(tipoClasificacion):
            if str(clf.firstChild.data) == tipoClasificacion[pos]:
                size[pos]+=1
            pos+=1
    #Agrego los valores a una clase y luego a un arreglo de estas
    for k in range(len(tipoClasificacion)):
        newClasQ = totalClasificaciones(tipoClasificacion[k],size[k])
        totalClas.append(newClasQ)
    #-------------------------------Obtencion de cumpleaños--------------------------------------
    #Ingreso al tag de clientes
    clientes = doc.getElementsByTagName('clientes')
    for cliente in clientes:
        fechasC = cliente.getElementsByTagName('fechaCumpleaños')
        nombres = cliente.getElementsByTagName('nombre')
        apellidos = cliente.getElementsByTagName('apellido')
    #Arreglo para los cumpleaños
    fechas = []
    nombresF = []
    apellidosF = []
    #Almaceno las fechas
    for fechaCump in fechasC:
        fechas.append(datetime.strptime(fechaCump.firstChild.data,'%d/%m/%Y').date())
    #Almaceno los nombres
    for nomb in nombres:
        nombresF.append(nomb.firstChild.data)
    #Almaceno los apellidos
    for apellido in apellidos:
        apellidosF.append(apellido.firstChild.data)
    #Realizo un ordenamiento burbuja para en base a los meses para tener las fechas en el orden adecuado
    finish = False
    while finish == False:
        finish = True
        for posi in range(len(fechas)-1):
            if fechas[posi].month > fechas[posi+1].month:
                #Cambio de fechas
                aux = fechas[posi]
                fechas[posi] = fechas[posi+1]
                fechas[posi+1] = aux
                #Cambio de nombres
                aux2 = nombresF[posi]
                nombresF[posi] = nombresF[posi+1]
                nombresF[posi+1] = aux2
                #Cambio de apellidos
                aux3 = apellidosF[posi]
                apellidosF[posi] = apellidosF[posi+1]
                apellidosF[posi+1] = aux3
                finish = False
    #Agregado de valores a clase y arreglo
    for l in range(len(fechas)):
        newCump = cumpleanio(nombresF[l],apellidosF[l],str(fechas[l]))
        cumpleanios.append(newCump)
    #------------------------------Obtención de listado de juegos--------------------------------------------
    #Reutilizo la variable que ingreso al tag juegos
    #Obtengo los datos necesarios
    for jg in juegoGeneral:
        nombreJuego = jg.getElementsByTagName('nombre')
        stockJuego = jg.getElementsByTagName('stock')
    #Arreglos locales para lamacenar la informacion
    nombresJuegos = []
    stockDeJuegos = []
    #Almaceno los datos
    for nombreJg in nombreJuego:
        nombresJuegos.append(nombreJg.firstChild.data)
    
    for stockJg in stockJuego:
        stockDeJuegos.append(stockJg.firstChild.data)
    #Instancias y agregado a los arreglos
    for m in range(len(nombresJuegos)):
        newGame = juegosChet(nombresJuegos[m],stockDeJuegos[m])
        totalG.append(newGame)
    return ''
    
@app.route("/getxml",methods=['GET'])
def getxml():
    #Importo los arreglos globales
    global mjClientes
    global juegosMasVendidos
    global totalClas
    global cumpleanios
    global totalG
    #Inicio la creacion del XML de retorno
    title = ET.Element('data')
    #Agregado de los mejoresClientes
    mjClienteTitle = ET.SubElement(title,'mejoresClientes')
    for i in range(len(mjClientes)):
        nombre = ET.SubElement(mjClienteTitle,'nombre')
        monto = ET.SubElement(mjClienteTitle,'monto')
        nombre.text = mjClientes[i].nombre
        monto.text = mjClientes[i].monto
    #Agregado de los juegos mas vendidos
    jMasVendidosTitle = ET.SubElement(title,'juegosMasVendidos')
    for j in range(len(juegosMasVendidos)):
        nombrej = ET.SubElement(jMasVendidosTitle,'nombre')
        copiasVendidas = ET.SubElement(jMasVendidosTitle,'copiasVendidas')
        fechasL = ET.SubElement(jMasVendidosTitle,'añoLanzamiento')
        nombrej.text = juegosMasVendidos[j].nombre
        copiasVendidas.text = juegosMasVendidos[j].ventas
        fechasL.text = juegosMasVendidos[j].fechaDeLanzamiento
    #Agrego las clasificaciones
    jClasificacionTitle = ET.SubElement(title,'clasificaciones')
    for k in range(len(totalClas)):
        tipoClas = ET.SubElement(jClasificacionTitle,'tipo')
        cantidad = ET.SubElement(jClasificacionTitle,'cantidad')
        tipoClas.text = totalClas[k].tipo
        cantidad.text = str(totalClas[k].total)
    #Agrego las fechas de cumpleaños
    cumpleanioTitle = ET.SubElement(title,'cumpleaños')
    for l in range(len(cumpleanios)):
        nom = ET.SubElement(cumpleanioTitle,'nombre')
        apell = ET.SubElement(cumpleanioTitle,'apellido')
        fecha = ET.SubElement(cumpleanioTitle,'fecha')
        nom.text = cumpleanios[l].nombre
        apell.text = cumpleanios[l].apellido
        fecha.text = cumpleanios[l].fecha
    #Agrego las lista de juegos
    juegosTitle = ET.SubElement(title, 'listaJuegos')
    for m in range(len(totalG)):
        nombreJuego = ET.SubElement(juegosTitle,'nombre')
        stockJuego = ET.SubElement(juegosTitle,'stock')
        nombreJuego.text = totalG[m].nombre
        stockJuego.text = totalG[m].stock

    doc = ET.tostring(title,encoding='utf-8')
    return doc

if __name__=="__main__":
    app.run(debug=True)