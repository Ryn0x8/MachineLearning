import tensorflow as tf
from tensorflow import keras
from keras import layers, models
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) =  tf.keras.datasets.mnist.load_data()

x_train, x_test = x_train/255.0, x_test/255.0

x_train = x_train[..., tf.newaxis]
x_test = x_test[..., tf.newaxis]

data_augemtation = keras.Sequential(
    [
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        layers.RandomTranslation(0.1, 0.1),
    ]
)


model = models.Sequential([
    layers.Flatten(input_shape = (28,28)),
    layers.Dense(128, activation = "relu"),
    layers.Dense(10, activation = "softmax")
])

model.compile(
            optimizer = "rmsprop", 
            loss = "sparse_categorical_crossentropy", 
            metrics = ["accuracy"]
            )

history = model.fit(x_train, y_train, epochs = 5, validation_split=0.1)

test_loss, test_acc = model.evaluate(x_test, y_test)
print('\nTest accuracy:', test_acc)

predictions = model.predict(x_test)

plt.figure(figsize=(4,4))
plt.imshow(x_test[0].reshape(28,28), cmap="gray")
plt.title(f"Predicted: {predictions[0].argmax()}")
plt.axis("off")
plt.show()

plt.plot(history.history['accuracy'], label="Train Accuracy")
plt.plot(history.history['val_accuracy'], label="Validation Accuracy")
plt.legend()
plt.title("Accuracy Curve")
plt.show()

plt.plot(history.history['loss'], label="Train Loss")
plt.plot(history.history['val_loss'], label="Validation Loss")
plt.legend()
plt.title("Loss Curve")
plt.show()
