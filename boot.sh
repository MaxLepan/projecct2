sleep 25

cd /home/pi/Documents/project2
python ./server.py &
sleep 40
python ./bouton.py &
python ./classes/VolumeControl.py &
python ./startSound.py &