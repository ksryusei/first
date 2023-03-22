import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf


np.random.seed(0)
(X_train_base, labels_train_base), (test_x, test_y) = tf.keras.datasets.mnist.load_data()

train_x, valid_x, train_y, valid_y = train_test_split(X_train_base, labels_train_base, test_size = 0.2)

train_x = train_x.reshape((48000, 28, 28, 1))
valid_x = valid_x.reshape((12000, 28, 28, 1))
test_x = test_x.reshape((10000,28,28,1))


train_x = np.array(train_x).astype('float32')
valid_x = np.array(valid_x).astype('float32')
test_x = np.array(test_x).astype('float32')
train_x /= 255
valid_x /= 255
test_x /= 255

train_y = tf.keras.utils.to_categorical(train_y)
valid_y = tf.keras.utils.to_categorical(valid_y)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))

model.compile(optimizer=tf.optimizers.Adam(0.01), loss='categorical_crossentropy', metrics=['accuracy'])

log = model.fit(train_x, train_y, epochs=100, batch_size=10, verbose=True,
                callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_loss', 
                                                     min_delta=0, patience=10, 
                                                         verbose=1)],
                validation_data=(valid_x, valid_y))

model.save('model.h5')

pred_test = np.argmax(model.predict(test_x), axis=1)
sum(pred_test == test_y)/len(pred_test)