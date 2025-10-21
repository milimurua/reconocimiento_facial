# Reconocimiento Facial

## Descripción
Este proyecto implementa un sistema de **reconocimiento facial con cámara web** para gestionar:
- Control de asistencia  
- Verificación de examen  
- Acceso a biblioteca o laboratorio  

Usa la librería `face_recognition` (basada en *dlib*) y **OpenCV** para detectar rostros en tiempo real, registrando los eventos en archivos `.csv`.

---

## Estructura del proyecto

Crea las carpetas con esta estructura:

```

reconocimiento_facial/
│
├── asistente_educativo.py         # Script principal
├── reconocimiento_facial.py       
├── README.md
├── .gitignore
│
├── data/
│   ├── estudiantes/               # Imágenes de estudiantes (rostros base)
│   │   └── NombreApellido.jpg
│   │
│   └── registros/                 # Se generan automáticamente los CSV
│       ├── asistencia.csv
│       └── examen.csv
│
└── .venv/                         # Entorno virtual (no se sube al repo)

````

---

## Configuración del entorno

### Crear entorno virtual
Desde PyCharm o la terminal:

```bash
python -m venv .venv
````

Activa el entorno:

**Windows (PowerShell):**

```bash
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### Instalar dependencias

Ejecuta dentro del entorno:

```bash
pip install cmake
pip install dlib-bin
pip install face_recognition
pip install Pillow
pip install opencv-python
```

## Agregar imágenes de estudiantes

Guarda en `data/estudiantes/` una foto **frontal**.

Ejemplo:

```
data/estudiantes/
│
├── Juan_Perez.jpg
└── Ana_Sosa.png
```

> No uses espacios ni caracteres especiales en los nombres.

---

## Ejecución

Verás el menú:

```
=== ASISTENTE EDUCATIVO ===
1. Control de asistencia
2. Verificación de examen
3. Acceso a biblioteca/laboratorio
Selecciona opción (1-3):
```

Selecciona una opción y la cámara se abrirá.
El sistema:

* Detecta tu rostro.
* Verifica si coincide con los registrados.
* Registra el evento en `data/registros/<tipo>.csv`.

> Presiona **`q`** para cerrar la cámara.

---

## Archivos de registro

Cada acción genera un archivo `.csv` en `data/registros/`, con formato:

```
Nombre,Hora,Fecha
Juab_Perez,09:42:18,2025-10-21
```

---

## Problemas comunes

| Error                                        | Causa                              | Solución                                                                  |
| -------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'PIL'` | Falta Pillow                       | `pip install Pillow`                                                      |
| `CMake is not installed`                     | Falta CMake real                   | Instalar desde [cmake.org](https://cmake.org/download/) y agregar al PATH |
| `No se detectó ningún rostro`                | Mala iluminación o cámara sin foco | Repetir la captura con mejor luz                                          |
| `Cannot find 'git'`                          | Git no instalado                   | Instalar desde [git-scm.com](https://git-scm.com/download/win)            |

