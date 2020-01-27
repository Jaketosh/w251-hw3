# README - Homework 3 Internet of Things 101
By Jacob Tosh

The purpose of this homework was to combine MQTT, Docker, Python, and S3 Buckets to create an IoT system that begins by having a camera identify a face and ends with the face being written into an S3 bucket. The pipeline between the beginning and the ending points consists of MQTT brokers and messaging systems.

## Docker Images

The Docker images used in this project were Dockerfile.faceDetector, Dockerfile.broker, Dockerfile.forwarder, and Dockerfile. writer. FaceDetector was used for the container that utilized the camera and the images to the local broker. Both the local broker and the remote broker used the Dockerfile.broker image. The Dockerfile.forwarder image was used by the local forwarder that picked up the messages from the local broker and sent them to the remote broker. The final image used is the Dockerfile.writer image. This image was used on the remote machine to pick up the messages sent to the remote broker and write the messages to the s3 bucket.

## Building the Images

__To build the images run the following commands:__
Local - 
docker build -t facedetect -f Dockerfile.faceDetector .
docker build -t broker -f Dockerfile.broker .
docker build -t forwarder -f Dockerfile.forwarder .

Remote -
docker build -t remotebroker -f Dockerfile.broker .
docker build -t writer -f Dockerfile.writer .

## Setting up the local containers to run the project
__Spinning up each container and connecting them in a network:__
docker network create --driver bridge hw03
docker run --name broker --network hw03 -p 1883:1883 -dit broker
docker run --name forwarder --network hw03 -dit forwarder
docker run --name facedetect --network hw03 --device /dev/video1 -dit facedetect

__Setting up broker:__
docker attach broker
run /usr/sbin/mosquitto

__Setting up forwarder:__
docker attach forwarder
Now copy msgForwarder.py into the forwarder container
python msgForwarder.py

__Setting up facedetect:__
docker attach facedetect
Now copy faceDetect.py into the facedetect container
python faceDetect.py

## Setting up the remote containers to run the project
ssh into the remote machine
Copy Dockerfile.broker and Dockerfile.writer onto the remote machine

__Spinning up each container and connecting them in a network:__
docker network create --driver bridge hw03
docker run --name remotebroker --network hw03 -p 1883:1883 -dit broker
docker run --name writer --network hw03 -dit writer

__Setting up writer on the remote machine:__
docker attach writer
create your .s3cfg file that will allow you to communicate with your s3bucket
Now copy imgProcessor.py into the writer container and adjust the s3 bucket sync command to match your s3 bucket
python imgProcessor.py

## Python files
__faceDetect.py__
faceDetect.py connects to the local broker and then begins accessing the camera to identify faces. Once a face is identified, the face is cropped into a new image and is then turned into a byte array. This byte array is then sent to the local broker in a message.

__msgForwarder.py__
msgForwarder.py subscribes to the local broker and etablishes a connection with the remote broker. The forwarder then waits until a message is received. Once a message is received, the message forwarder acquires the message and then publishes that message to the remote broker.

__imgProcessor.py__
imgProcessor.py is run on the remote machine in the writer container. This code establishes a connection between the remote broker and the writer container. When the remote broker receives a connection, the writer container reads in the message and then writes the byte array payload to a file in the container. Once the file is written, the code syncs the directory containing the face images with the desired s3 bucket. 

## MQTT Topics and QoS
The MQTT topic used was called "faces". I chose this name because I thought it accurately represented the data that we were transferring. The QoS used was 0. My understanding of QoS is that as the QoS number increases, so does the reliability of the message arriving at its intended destination and the latency associated with sending the message. Since this project was for homework, I felt like QoS 0 worked fine, but if you were instead capturing faces with the intent of identifying criminals, you would probably want to increase your QoS to better ensure that your messages arrive reliably.
