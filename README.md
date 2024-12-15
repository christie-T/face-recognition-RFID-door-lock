# Raspberry Pi Door Lock Project

## 🛠 set-up

# 1. install Raspbian onto Raspberry Pi 3

# 2. Open Terminal and run

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install git cmake
```

# 3. Face Recognition Library:
```bash
sudo pip3 install face_recognition
```

This might take a while. PLEASE increase swapfile memory (I used 1024mb) for installation, or the installations gonna brick. Guide here: 

https://akashrajpurohit.com/blog/increase-swap-memory-on-raspberry-pi/#:~:text=Swap%20file%20is%20a%20file,with%20limited%20amount%20of%20RAM.


# 4. Extra Libraries
```bash
sudo pip3 install imutils pypickle
raspi-config
```
Then, enable the camera in config.


## Running the program

Put images of the face you want recognized in 'faces' directory

Then, run:

```bash
python3 encode_faces.py
python3 exe.py
```
