 
the image classifier
the introduction to the code
the statring of load_data

    
def load_data(train_dir,val_dir,
test_dir,img_size=IMG_SIZE,
              batch_size=BATCH_SIZE):
    datagen =
    ImageDataGeneration(rescale=1./255)

    train_data=
    datagen.flow_from_directory(
            train_dir,target_size=img_size, HEAD

        batch_size=batch_size,class_mode='categorical'
         test_data=
        datagen.flow_from_directory(
            test_dir,target_size=img_size,
            batch_size=batch_size,
            class_mode='categorical',shuffle = false)
            batch_size=batch_size,class_mode='categorical'

            val_data=
            datagen.flow_from_directory(
                val_dir,target_size=img_size,
                batch_size=batch_size,
                class_mode='categorical')

            return train_data,val_data,
            test_data_  
