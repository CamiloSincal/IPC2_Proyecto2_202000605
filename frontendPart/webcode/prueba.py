
class cumple():
    def __init__(self,nombre,apellido):
        self.nombre = nombre
        self.apellido = apellido
us = []
for i in range(2):
    newC = cumple(i,i+1)
    us.append(newC)

for j in us:
    print(j.nombre)