# Todo Add flags for training and evaluation

FROM tensorflow/tensorflow:1.7.0-devel-gpu

EXPOSE 6006

RUN apt-get update && apt-get install python-opencv -y && apt-get clean -y
WORKDIR /tensorflow/tensorflow/examples/
RUN git clone https://github.com/admatis/keras-retinanet.git
WORKDIR keras-retinanet
RUN pip install Pillow h5py opencv-python --user
RUN pip install . --user
RUN python setup.py build_ext --inplace

# from here
RUN pip install flask

ENV LISTEN_PORT=8008
EXPOSE 8008

COPY /app ./app
#CMD python /app/main.py