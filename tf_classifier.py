
import os

start_venv = os.system(". /home/pi/myenv/bin/activate")
print("`cd ~` ran with exit code %d" % start_venv)
home_dir = os.system("cd ~/Desktop/mlproject/")
print("`cd ~` ran with exit code %d" % home_dir)
label_image = os.system("python label_image.py image1.jpg")
print("`cd ~` ran with exit code %d" % label_image)
deac_venv = os.system("/home/pi/myenv/bin/deactivate")
print("`cd ~` ran with exit code %d" % deac_venv)