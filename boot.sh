sleep 15

cd /home/pi/Documents/project2
python ./server.py &
sleep 5
python ./bouton.py &
python classes/Tensorflow.py &
sleep 15
python ./classes/ModeControl.py &
python ./classes/VolumeControl.py &
python startSound.py &