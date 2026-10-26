# Reconocedor de dígitos con TensorFlow, OpenCV y Flask

Este proyecto entrena un modelo CNN sobre el dataset MNIST y luego lo usa para reconocer dígitos en tiempo real desde la cámara del equipo. La aplicación muestra una vista en vivo con el número detectado en un navegador web.

## Características

- Entrenamiento de un modelo CNN con TensorFlow/Keras.
- Carga del modelo entrenado desde `modelo_mnist.h5`.
- Captura de video desde la cámara con OpenCV.
- Reconocimiento del dígito en una zona central del frame.
- Visualización web en Flask en `http://127.0.0.1:5000`.

## Estructura del proyecto

- `entrenar_modelo.py` - Entrena el modelo MNIST y guarda el archivo `.h5`.
- `preconocer_numeros.py` - Carga el modelo y ejecuta la app web con reconocimiento en tiempo real.
- `modelo_mnist.h5` - Modelo entrenado generado por `entrenar_modelo.py`.
- `requirements.txt` - Dependencias del proyecto.

## Requisitos

- Python 3.10 o 3.11 recomendado
- Cámara web disponible
- Git

## Instalación

1. Clona el repositorio:

```bash
git clone <url-del-repositorio>
cd Reconocedor
```

2. Crea y activa un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instala las dependencias:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Entrenar el modelo

Si aún no existe el archivo `modelo_mnist.h5`, ejecuta:

```bash
python3 entrenar_modelo.py
```

Este script:

- descarga el dataset MNIST,
- entrena la red neuronal,
- guarda el modelo como `modelo_mnist.h5`.

> El entrenamiento puede tardar unos minutos dependiendo de la máquina y de la velocidad de GPU/CPU.

## Ejecutar la aplicación

Una vez que el modelo esté listo, inicia la app:

```bash
python3 preconocer_numeros.py
```

Luego abre en tu navegador:

```text
http://127.0.0.1:5000
```

La aplicación mostrará:

- la transmisión de la cámara en vivo,
- un recuadro verde alrededor del área analizada,
- el número detectado en la pantalla.

## Capturas del proyecto

### 1. Entrenamiento del modelo

![Entrenamiento del modelo](assets/Captura%20desde%202026-10-25%2021-15-25.png)

Esta captura muestra la fase de entrenamiento del modelo CNN sobre el conjunto MNIST. En la consola se observa cómo la pérdida disminuye y la precisión aumenta a medida que avanzan las épocas, lo que confirma que el modelo está aprendiendo a clasificar dígitos correctamente.

### 2. Interfaz principal de la aplicación

![Interfaz web](assets/Captura%20desde%202026-10-25%2021-18-16.png)

Aquí se ve la interfaz web desarrollada con Flask. La parte izquierda muestra la cámara en vivo y el recuadro verde que marca la zona de análisis, mientras que la parte derecha presenta el número detectado por el modelo. Esta vista permite al usuario ver el proceso en tiempo real de forma clara y simple.

### 3. Reconocimiento en tiempo real

![Reconocimiento del número](assets/Captura%20desde%202026-10-25%2021-18-34.png)

En esta imagen se aprecia el sistema analizando un número escrito en papel. El modelo reconoce la figura dentro del rectángulo verde y la muestra en el panel lateral, demostrando que la clasificación funciona en un caso real con cámara en vivo.

## Nota sobre la cámara

La aplicación usa la cámara por defecto del sistema (`cv2.VideoCapture(0)`). Si tu equipo tiene más de una cámara, es posible que necesites cambiar el índice `0` dentro de `preconocer_numeros.py`.

## Solución de problemas

### Error al abrir la cámara

Asegúrate de que:

- la webcam esté conectada,
- no esté siendo usada por otra app,
- permisos de cámara estén habilitados.

### Error con TensorFlow

Si aparece un problema de compatibilidad con TensorFlow, prueba con una versión de Python 3.10 o 3.11 y vuelve a instalar las dependencias:

```bash
pip install -r requirements.txt
```

### El modelo no existe

Ejecuta antes:

```bash
python3 entrenar_modelo.py
```

## Licencia

Este proyecto se comparte con fines educativos y de aprendizaje.

## Autor

Proyecto desarrollado para reconocimiento de dígitos en tiempo real con visión artificial.
