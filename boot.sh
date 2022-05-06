sleep 15

cd /home/pi/Documents/project2
python ./server.py &
sleep 35
python ./bouton.py &
python ./classes/VolumeControl.py &
python ./classes/ModeControl.py &
play ./audio/systemAudio/soundChanged.ogg