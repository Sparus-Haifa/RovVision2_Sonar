#!/bin/bash
source run_common.sh

tmux kill-ser


PROJECT_PATH=/home/host/projects/RovVision2/
#PYTHON=${1:-/miniconda/bin/python}

#[ $USER == 'uav' ] && export RESIZE_VIEWER=1500
[ $USER == 'uav' ] && export RESIZE_VIEWER=2300

if [ ! -v SIM ]
then
tmux kill-session -t dronelab
tmux new-session -d -s dronelab
PYTHON=/bin/python3
PROJECT_PATH=../
else
tmux new-window
fi 

viewer_arg=""

if [ "$1" = "local" ]; then
    echo "local"
    cmd="./run_ground_control.sh"
    viewer_arg="-r"
fi


new_4_win


if [ "$1" != "local" ]; then
    runShell 0 scripts ./ssh_route.sh
fi
sleep 1
runLoop 1 ground_control joy_rov.py
#run 2 ground_control "viewer.py --pub_data --udp"
tmux select-pane -t 2
tmux send-keys "./setProfile.sh" ENTER
run 2 ground_control "rovViewer.py $viewer_arg"
#run 2 web "--version && FLASK_APP=server.py flask run"
#run 3 web "--version && sleep 3 && firefox http://127.0.0.1:5000/static/html/ropedive.html --new-window  --new-tab -url http://127.0.0.1:5000/static/html/checklists.html"

if [ "$1" != "local" ]; then
    sleep 8
    runShell 3 scripts ./run_sonar_reconfigure_docker.sh
fi



tmux att
