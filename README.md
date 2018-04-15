# RetinaNetDocker-
A Nvidia docker container environment for training and executing [RetinaNet with tensorflow](https://github.com/fizyr/keras-retinanet).


# To Use Run the following commands

 - sudo nvidia-docker build -f Dockerfile -t retinanet .
 - sudo nvidia-docker run -it -d -p 0.0.0.0:6006:6006 -p 0.0.0.0:8888:8888 -v {data path}:/data/ retinanet
 - nvidia-docker exec -it {docker id} bash
 - keras_retinanet/bin/train.py pascal {/data/path to data}