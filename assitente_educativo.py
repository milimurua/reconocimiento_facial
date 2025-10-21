import cv2
import face_recognition as fr
import os
import numpy as np
from datetime import datetime

# Crear base de datos
ruta = 'data/estudiantes'
mis_imagenes = []
nombres_alumnos = []
lista_archivos = os.listdir(ruta)

for archivo in lista_archivos:
    imagen_actual = cv2.imread(f"{ruta}/{archivo}")
    if imagen_actual is None:
        print(f"No se pudo leer {archivo}, se omitirá.")
        continue
    mis_imagenes.append(imagen_actual)
    nombres_alumnos.append(os.path.splitext(archivo)[0])

print(f"Estudiantes cargados:{nombres_alumnos}")

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
    os.makedirs(f"{carpeta}", exist_ok=True)
    archivo = os.path.join(carpeta, f"{tipo}.csv")

    #crea el registro si no existe
    if not os.path.exists(archivo):
        with open(archivo,"w") as f:
            f.write("Nombre, Hora, Fecha\n")

    #si existe lo guarda
    with open(archivo, "a") as f:
        f.write(f"{persona},{datetime.now()},{datetime.now()}\n")


codigos_codificados = codificar(mis_imagenes)

def capturar_rostro(accion, lista_codificada, nombres):
    print(f"Iniciando reconocimiento facial para {accion}:")

    camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not camara.isOpened():
        print("No se pudo acceder a la cámara.")
        return

    while True:
        exito, frame = camara.read()
        if not exito:
            print("No se pudo leer el video.")
            break

        # Reducir tamaño para acelerar
        pequeño = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(pequeño, cv2.COLOR_BGR2RGB)

        # Detección y codificación
        caras = fr.face_locations(rgb)
        codigos = fr.face_encodings(rgb, caras)

        for (top, right, bottom, left), cara_codif in zip(caras, codigos):
            distancias = fr.face_distance(lista_codificada, cara_codif)
            if len(distancias) == 0:
                continue

            indice = np.argmin(distancias)
            nombre = "Desconocido"
            color = (0, 0, 255)

            if distancias[indice] < 0.6:
                nombre = nombres[indice]
                color = (0, 255, 0)
                registrar_evento(accion, nombre)

            # Escalar coordenadas
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Dibujar recuadro y nombre
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, nombre, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)

        cv2.imshow("Asistente Educativo - Presiona 'q' para salir", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camara.release()
    cv2.destroyAllWindows()


# registrar la asistencia del alumno clase
def control_asistencia():
    print("Control de asistencia iniciado...")
    capturar_rostro("asistencia", codigos_codificados, nombres_alumnos)

def verificacion_examen():
    print("Verificación facial antes del examen...")
    capturar_rostro("examen", codigos_codificados, nombres_alumnos)

def acceso_biblioteca():
    print("Control de acceso a biblioteca/laboratorio...")
    capturar_rostro("acceso", codigos_codificados, nombres_alumnos)

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