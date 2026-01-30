import tensorflow as tf
from model.noise import apply_noise

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train_1 = apply_noise(x_train)
x_train_2 = apply_noise(x_train)
x_train_3 = apply_noise(x_train)

x_train_1 = tf.keras.utils.normalize(x_train_1, axis=1)
x_train_2 = tf.keras.utils.normalize(x_train_2, axis=1)
x_train_3 = tf.keras.utils.normalize(x_train_3, axis=1)

x_test = tf.keras.utils.normalize(x_test, axis=1)

# extensions
# add noise to data e.g rotation, scaling, noise
# use full dataset including the test set

model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
model.add(tf.keras.layers.Dense(512, activation='relu'))
model.add(tf.keras.layers.Dense(512, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(x_train_1, y_train, epochs=5)
model.fit(x_train_2, y_train, epochs=5)
model.fit(x_train_3, y_train, epochs=5)


loss, accuracy = model.evaluate(x_test, y_test)

print(f"From test data: accuracy: {accuracy}, loss: {loss}")

model.save('./model/numberreader.h5')