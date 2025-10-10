import time
import random

def main():
    print("---Bienvenido Al Cine MovieTime--")
    time.sleep(1)
    print("seleccione una opcion")
    time.sleep(1)
    print("---1.funciones disponibles---")
    print("---2.Boletos---")
    print("---3.salir---")  
    time.sleep(1)
    opcion = int(input("ingrese una opcion :"))
    if opcion == 1:
        funciones_disponibles()
    if opcion == 2:
        venta_boletos()
        numero_boleto()
        boletos_disponibles()
        calcular_dinero()
    elif opcion ==3:
        print("gracias por su visita")
        time.sleep(1)
        print("vuelva pronto")

def funciones_disponibles():
    print("Funciones disponibles:")
    funciones = [
        {"nombre": "Avengers: Endgame", "hora": "18:00", "sala": 1},
        {"nombre": "Inception", "hora": "20:00", "sala": 2},
        {"nombre": "The Dark Knight", "hora": "22:00", "sala": 3}
    ]
    for funcion in funciones:
        print(f"{funcion['nombre']} - {funcion['hora']} - Sala {funcion['sala']}")  

def agregar_funcion():
    print("Función para agregar una nueva función de cine")
    nombre = input("Ingrese el nombre de la función: ")
    hora = input("Ingrese la hora de la función (HH:MM): ")
    sala = input("Ingrese el número de sala: ")
    print(f"Función '{nombre}' agregada a las {hora} en la sala {sala}.")   

def venta_boletos():
    print("Bienvenido a la venta de boletos")
    nombre = input("Ingrese su nombre: ")
    cantidad = int(input("¿Cuántos boletos desea comprar?: "))
    funcion = print("seleccione la funcion que desa ver")
    precio_unitario = 10000  # Precio por boleto
    total = cantidad * precio_unitario
    print(f"{nombre}, el total a pagar por {cantidad} boletos es: ${total}")

def generar_numero_boleto():
    return random(1, 200)

def numero_boleto():
    numero_boleto = generar_numero_boleto()
    print(f'El numero de su boleto es: {numero_boleto}')
    return numero_boleto

def boletos_disponibles():
    total_boletos = 200
    boletos_vendidos = random.randint(1, 200)
    boletos_disponibles = total_boletos - boletos_vendidos
    print(f'boletos disponobles: {boletos_disponibles}')

def ventas_totales():
    total_ventas = 0
    venta_boletos = int(input("ingrese el total de boletos vendidos"))
    precio = 10000
    ventas_totales = venta_boletos * precio
    print(f'el total de ventas es:{ventas_totales}')

def calcular_dinero():
    total_dinero = 0
    boletos_vendidos = int(input("ingrese el total de boletos vendidos"))
    precio = 10000
    total_dinero = boletos_vendidos * precio
    print(f'el total de dinero es de:{total_dinero}')
    
if __name__ == "__main__":
    main()




