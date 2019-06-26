#!/bin/bash
UNREAL_PROXY_PATH=/home/host/projects/RovVision2/sim/unreal_proxy
ENTRY_POINT=unreal_proxy
ENTRY_PATH=$UNREAL_PROXY_PATH/
DRONESIMLAB_PATH=../../DroneSimLab

#game defenitions
#GAME_PATH=/DroneLab/baked_games/Ocean1_packed/LinuxNoEditor/
GAME_PATH=/project_files/Ocean1_packed/LinuxNoEditor/
PACKED_NAME=Oceantest1


kill-session -t dronelab
source common.sh
kill_images python_dev

if [ `docker ps | grep -v unreal_engine |wc -l` -gt 1 ]; then 
    echo "ERROR: Make sure no other docker images other then unreal_engine are running (counting on sequencial IP addresses)";
    echo "use docker rm and docker ps to remove other docker containers"
    exit 0
fi

function init_rov {
tmux send-keys "cd ../../dockers/python3_dev && ./run_image.sh" ENTER
}

function pub_fdm {
tmux send-keys "cd ../../dockers/python3_dev && ./run_image.sh" ENTER
tmux send-keys "export PATH=/miniconda/bin/:\$PATH" ENTER 
}

function image_bridge {
tmux send-keys "cd ../../dockers/python3_dev && ./run_image.sh" ENTER
}




function run_game {
#tmux send-keys "cd $DRONESIMLAB_PATH/dockers/python3_dev && PROJECT_FILES_DIR=$PROJECT_FILES_DIR ./run_image.sh" ENTER
tmux send-keys "cd $DRONESIMLAB_PATH/dockers/python3_dev && ./run_image.sh" ENTER
tmux send-keys "export PATH=/miniconda/bin:\$PATH" ENTER
tmux send-keys "cd ${DEMO_PATH}" ENTER
tmux send-keys "python /DroneLab/UE4PyhtonBridge/set_path.py --entry_point $ENTRY_POINT --entry_path $ENTRY_PATH --packed_game_name $PACKED_NAME --packed_game_path $GAME_PATH" ENTER
tmux send-keys "cd ${GAME_PATH}" ENTER
tmux send-keys "INITIAL_DRONE_POS=$INITIAL_DRONE_POS CAMERA_RIG_PITCH=$CAMERA_RIG_PITCH DISPLAY=:0.0 ./run.sh" ENTER
}
#cleanning prev run

tmux new-session -d -s dronelab
#tmux send-keys "python drone_main.py" ENTER

#tmux send-keys "cd ../../dockers/unreal_engine_4 && ./attach.sh" ENTER
run_game

tmux new-window 
tmux split-window -h
tmux select-pane -t 0
tmux split-window -v
tmux select-pane -t 2
tmux split-window -v

tmux select-pane -t 0
pub_fdm 
tmux select-pane -t 1
init_rov 
tmux select-pane -t 2
image_bridge



#tmux send-keys "./run.sh" ENTER 
#tmux select-window -t 0
#tmux set -g mouse on
tmux att

