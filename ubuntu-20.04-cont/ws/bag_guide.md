sudo apt install python3.8-venv
python3 -m venv bagvenv
pip install rosbags
rosbags-convert straight_test_slow
