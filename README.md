# Object_Detection_Indian_driving_dataset

The readme is all about the tensor flow object detection API on the Indian Driving Dataset. Though the COCO detection API installation and training are straight forward 
as described [here](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html) i would like to walk you through the data preparation part and the difficulties I faced. The results of the model are shared towards the end. 
In case you are curious to work on the dataset and give a try yourself before going through the blog the dataset can be found [here](https://idd.insaan.iiit.ac.in/).


the dataset is approximately 23GB and contains 15 different classes of objects to be detected. The folder structure is as below once extracted. Images which should be 
part of train, test and validation sets are shared in the form of 3 text files.

![unzipped](https://user-images.githubusercontent.com/94750531/184939134-d436365b-348a-41bf-b319-7e52877a883d.JPG)


As always; it's a good practice to get to know the data before we train our model. I have written a short script to check for the number of files within each category
[Images and respective XML files] and below are the results.

Annotations : 41858 files

JPEGImages : 46659 files

There are few missing files in annotations test files . Another short script was written to only move the files common to both train and validation files to a separate folder and then prepare the tf record files.

Ideally the new folder should be having (41858*2) files as we would expect but only around (14k) files were initially present in the new folder.

After a lot of meddling around and trying different scripts to move the files around it was noticed the file names were repeated. A short script was written to find the 
unique file names from each given train, validation and test set of text files and the results are as following.

(4955, 3450, 1509)

Even though the images are different the names are repeated and hence all the (41858*2) files couldn't be moved to the common folder.
Just as a insight into one of the directory [Images/XML] we have 6 different camera angles as below.

![camera_angles](https://user-images.githubusercontent.com/94750531/184939204-08b43235-29cf-450f-8798-82d6713df754.JPG)


I have decided to train the model on one of the camera angle; but apart from the duplicate file names there is also the possibility of missing details for the 
object(as the object perspective changes with the camera angle).

Also few images are repetitive; as in the case when the vehicle is struck in traffic behind a bus; there would be a series of images of the same bus almost entirely 
for the folder and in particular cases where the entire stretch of the road is empty which i believe won't be of much help to our model.

Manual selection of data, though possible is very tedious job.

So i decided to go ahead and prepare the train tf record for the 14k images and their respective xml files [as described above] and then create a partial subset for 
preparing the test tf record; but the problems still persisted with the below error.

tensorflow.python.framework.errors_impl.NotFoundError: NewRandomAccessFile failed to Create/Open: (path_to_folder)\images\train\0014730.jpg : The system cannot find 
the file specified.; No such file or directory

Even though files were present in the folder the error was persistent. I tried deleting the respective image and xml files manually for the file in error message but 
still the error would persist , at times i tried finding the missing file and then copying into the folder manually and then the same error would pop up for the another
filename and is very difficult to follow the process manually.

Upon observing the data the problem was found to be associated with the filenames ending with "_r".

The file names were mainly of 2 categories:
1) 0026505.jpg and its corresponding 0026505.xml file
2) 000006_r.jpg and its corresponding 000006_r.xml file.

since not much description is given about the data I'm not sure of the significance of the naming convention followed for "_r" files. They are of same shape for few 
random samples i checked but the problem is with the xml files which point to different image file and is the cause of above issue where the files are missing for the 
tf record to be created.

An example can be seen below where the actual XML file is 000240_r.xml but the annotations are for totally different image. There is a possibility of even assigning 
the wrong labels and bounding boxes in this scenario.

![normal](https://user-images.githubusercontent.com/94750531/184939414-4db137be-f519-4a9f-b7f6-0487249d3c38.JPG)

![_r](https://user-images.githubusercontent.com/94750531/184939447-af37bbcc-2749-4828-bc4e-d7cf7f69f9c0.JPG)


but is not with the case of filenames which do not have the "_r" extension.

so i have modified the script slightly to not move the files with "_r" extension. There were a total of app. 12k [including xml and jpg ] files used to create the train tf record file successfully.

For the preparation of label_map.pbtxt file the class names were taken from the official website where the distribution of classes in each of the sets is given.

Now that the data is sorted its time we train the model on our custom dataset. I have trained the model on Google Colab.
All the steps for [installation](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html) and [training](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/training.html)
are very well documented. The only error which can be difficult during installation (if occurred) is with the C++ build tools. In that case i request
you to follow this [short video](https://www.youtube.com/watch?v=rcI1_e38BWs) for remediation as almost everything on the forums or discussion didn't work for me. 
It would save you time surfing the web for resolution. Any other errors which are encountered are straight forward or seems to work with the resolution provided on
the forums or discussion threads.

The model was trained on SSD ResNet 50. Feel free to experiment with various models [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md)

Initially i trained the model on partial data and low epochs .The results, as expected are very bad :p. Either there were no bounding boxes at all or i would get bouding box which covers almost the entire image :D

So i trained the model on the entire data for 2000 epochs and bounding boxes now are better than before. Though cars are being detected fine our model has falsely detected auto as car.


![download (3)](https://user-images.githubusercontent.com/94750531/184938272-22a62d73-66c6-474e-a323-0dfee2f15ce2.png)


I have selected the below images from web specially to see how well the model performs as our model has not seen the images in rainy condition and it performed considerably.

![semma](https://user-images.githubusercontent.com/94750531/184938337-44917b5f-962c-406a-a232-bb7ff6d1a13b.png)

![download (2)](https://user-images.githubusercontent.com/94750531/184938386-d1722975-6d8e-4343-91d0-565f94a7b80c.png)


Couple of observations is our model is good at detecting the card and bikes which i assume can be attributed to the distribution of the data. The below [image](https://idd.insaan.iiit.ac.in/dataset/details/)
taken from the IDD website where the data was downloaded shows the representation of the data split across the 3 different dataset and since only part of the data 
was used for training the model. with more data our model would surely perform well.

![label_hierarchy](https://user-images.githubusercontent.com/94750531/184939641-ad17fed9-ff0b-4f18-b986-bc667be77286.png)


Any suggestions or improvements are welcome :)
Thank you.
