def load_data(train_dir,val_dir,
test_dir,img_size=IMG_SIZE,
              batch_size=BATCH_SIZE):
    datagen =
    ImageDataGeneration(rescale=1./255)

    train_data=
    datagen.flow_from_directory(
