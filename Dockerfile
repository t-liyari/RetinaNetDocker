# Todo Add flags for training and evaluation

FROM tensorflow/tensorflow:1.7.0-devel-gpu

EXPOSE 6006

RUN apt-get update && apt-get install python-opencv -y && apt-get clean -y
WORKDIR /tensorflow/tensorflow/examples/
RUN git clone https://github.com/fizyr/keras-retinanet.git
RUN cd keras-retinanet
RUN pip install Pillow h5py opencv-python --user
RUN pip install . --user
RUN python setup.py build_ext --inplace

WORKDIR keras-retinanet

