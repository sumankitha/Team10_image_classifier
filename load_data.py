def load_data(train_dir,val_dir,
test_dir,img_size=IMG_SIZE,
              batch_size=BATCH_SIZE):
    datagen =
    ImageDataGeneration(rescale=1./255)

    train_data=
    datagen.flow_from_directory(
            train_dir,target_size=img_size,
            batch_size=batch_size,class_mode='categorical'

            val_data=
            datagen.flow_from_directory(
                val_dir,target
