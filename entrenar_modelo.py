import tensorflow as tf
from tensorflow.keras import datasets, layers, models

# Cargar dataset MNIST
(x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()

# Normalizar
x_train = x_train / 255.0
x_test = x_test / 255.0

# Ajustar forma
x_train = x_train.reshape(-1,28,28,1)
x_test = x_test.reshape(-1,28,28,1)

# Crear modelo CNN
model = models.Sequential([
    layers.Conv2D(32,(3,3),activation='relu',input_shape=(28,28,1)),
    layers.MaxPooling2D((2,2)),

    layers.Conv2D(64,(3,3),activation='relu'),
    layers.MaxPooling2D((2,2)),

    layers.Flatten(),
    layers.Dense(64,activation='relu'),
    layers.Dense(10,activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenar
model.fit(x_train,y_train,epochs=5)

# Guardar modelo
model.save("modelo_mnist.h5")

print("Modelo guardado correctamente")