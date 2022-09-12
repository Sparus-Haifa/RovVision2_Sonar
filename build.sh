docker build -t blue_rov --build-arg VARIANT=ubuntu-20.04 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) . && \
cd hw/sonar_docker && ./build.sh && cd ../.. && \
docker save -o ros_sonar.dockerimage ros_sonar && \
rsync -auAXv ros_sonar.dockerimage $REMOTE_SUB:/home/nanosub/nir --info=progress2 && \
docker pull osrf/ros:melodic-desktop-full && \
ssh -t $REMOTE_SUB "docker rm ros_sonar || true && cd /home/nanosub/nir && docker load -i ros_sonar.dockerimage"