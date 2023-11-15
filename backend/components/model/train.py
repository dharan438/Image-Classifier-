from keras import backend
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense

width, height = 150, 150

train_data = "../dataset/cb"
validation_data = "../dataset/cb"
train_samples = 2000
validation_samples = 800
epochs = 50
batch_size = 16
model_name = "model.h5"

if backend.image_data_format() == "channels_first":
    input_shape = (3, width, height)
else:
    input_shape = (width, height, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation("sigmoid"))

model.compile(
    loss="binary_crossentropy",
    optimizer="rmsprop",
    metrics=["accuracy"],
)

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1.0 / 255)

train_generator = train_datagen.flow_from_directory(
    train_data,
    target_size=(width, height),
    batch_size=batch_size,
    class_mode="binary",
)

validation_generator = test_datagen.flow_from_directory(
    validation_data,
    target_size=(width, height),
    batch_size=batch_size,
    class_mode="binary",
)

model.fit(
    train_generator,
    steps_per_epoch=train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_samples // batch_size,
)

model.save(model_name)
