import glob
import cv2
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf

#これは日本絵画の識別をするAIです
#データ準備
files = glob.glob('C:/Users/ironr/Documents/Nishika/data/train/train/*.jpg')
files = sorted(files)
df_label = pd.read_csv("C:/Users/ironr/Documents/Nishika/data/train.csv")

file_list = []
for file in files:
  file = cv2.imread(file)
  file_list.append(file)

#画素値を正規化
file_list = [file.astype(float)/255 for file in file_list] 
train_x, valid_x, train_y, valid_y = train_test_split(file_list, df_label, test_size=0.2)

# train_y, valid_y をダミー変数化
train_y = tf.keras.utils.to_categorical(train_y["gender_status"])
valid_y = tf.keras.utils.to_categorical(valid_y["gender_status"])

# リスト型を配列型に
train_x = np.array(train_x)
valid_x = np.array(valid_x)

#層の定義
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)))
model.add(tf.keras.layers.Conv2D(32,(3,3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
model.add(tf.keras.layers.Dropout(0.3)) 
model.add(tf.keras.layers.Conv2D(64,(3,3), padding="same", activation='relu'))
model.add(tf.keras.layers.Conv2D(64,(3,3), activation='relu'))  
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))  
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(8, activation='softmax'))

# モデルを構築
model.compile(optimizer=tf.optimizers.Adam(0.01), loss='categorical_crossentropy', metrics=['accuracy'])

# Early stoppingを適用してフィッティング
log = model.fit(train_x, train_y, epochs=100, batch_size=10, verbose=True,
                callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_loss', 
                                                     min_delta=0, patience=10, 
                                                         verbose=1)],
                validation_data=(valid_x, valid_y))

test_loss, test_acc = model.evaluate(valid_x, valid_y, verbose=0)
print(test_loss)
print(test_acc)


model.save('日本絵画識別AI.h5')