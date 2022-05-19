sleep 25

cd /home/pi/Documents/project2
play ./audio/systemAudio/soundChanged.ogg
python ./server.py &
sleep 40
python ./bouton.py &
python ./classes/VolumeControl.py &
play ./audio/systemAudio/soundChanged.ogg