import cv2
import face_recognition as fr
import os
import numpy
from datetime import datetime

# Crear base de datos
ruta = 'data/estudiantes'
mis_imagenes = []
nombres_alumnos = []
lista_archivos = os.listdir(ruta)

for archivos in lista_archivos:
    imagen_actual = cv2.imread(f"{ruta}/{archivos}")
    mis_imagenes.append(imagen_actual)
    nombres_alumnos.append(os.path.splitext(archivos)[0])

print(nombres_alumnos)

#Codificar las imagenes
def codificar(imagenes):
    # Crear una lista nueva
    lista_codificada = []

    # Pasar todas las imagenes a RGB
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        # Codificar
        codificado = fr.face_encodings(imagen)[0]

        # Agregar a la lista
        lista_codificada.append(codificado)

    # Devolver lista codificada
    return lista_codificada

# Función para crear los registros
def registrar_evento(tipo, persona, carpeta="data/registros"):
    os.makedirs(f"{carpeta}/{tipo}", exist_ok=True)
    archivo = os.path.join(carpeta, f"{tipo}.csv")

    #crea el registro si no existe
    if not os.path.exists(archivo):
        with open(archivo,"w") as f:
            f.write("Nombre, Hora, Fecha\n")

    #si existe lo guarda
    with open(archivo, "a") as f:
        f.write(f"{persona},{datetime.now()},{datetime.now()}\n")


codigos_codificados = codificar(mis_imagenes)

def capturar_rostro(accion, guardar_imagen=False):
    # Tomar una imagen de camara web
    captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # Leer imagen de la camara
    exito, imagen = captura.read()

    #si no puede capturar
    if not exito:
        print("No se ha podido tomar la captura")

    # Reconocer cara en captura
    cara_captura = fr.face_locations(imagen)

    # Codificar cara capturada
    cara_captura_codificada = fr.face_encodings(imagen, cara_captura)

    # Buscar coincidencias | Doble loop
    for cara_codif, cara_ubic in zip(cara_captura_codificada, cara_captura):
        coincidencias = fr.compare_faces(lista_empleados_codificada, cara_codif)
        distancias = fr.face_distance(lista_empleados_codificada, cara_codif)

        print(distancias)

        indice_coincidencia = numpy.argmin(distancias)

        # Mostrar si existen coincidencias
        if distancias[indice_coincidencia] > 0.6:
            print("No coincide con ninguno de nuestro empleados")
        else:
            # Buscar el nombre del empleado encontrado
            nombre = nombres_empleados[indice_coincidencia]

            y1, x2, y2, x1 = cara_ubic
            cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(imagen, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(imagen, nombre, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            registrar_ingresos(nombre)

            # Mostrar la imagen obtenida
            cv2.imshow("Imagen web", imagen)

            # Mantener ventana abierta
            cv2.waitKey(3000)

            cv2.destroyAllWindows()


# registrar la asistencia del alumno clase
def control_asistencia():
    print("Control de asistencia iniciado...")
    detectar_rostro("asistencia")

# registrar la asistencia del alumno examen
def verificacion_examen():
    print("Verificación facial antes del examen...")
    detectar_rostro("examen", guardar_foto=True)

# Ingreso a la biblioteca
def acceso_biblioteca():
    print("Control de acceso a biblioteca/laboratorio...")
    detectar_rostro("acceso")

# Main
if __name__ == "__main__":
    print("=== ASISTENTE EDUCATIVO ===")
    print("1. Control de asistencia")
    print("2. Verificación de examen")
    print("3. Acceso a biblioteca/laboratorio")
    opcion = input("Selecciona opción (1-3): ")

    if opcion == "1":
        control_asistencia()
    elif opcion == "2":
        verificacion_examen()
    elif opcion == "3":
        acceso_biblioteca()
    else:
        print("Opción no válida.")