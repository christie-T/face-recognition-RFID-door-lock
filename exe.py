from picamera2 import Picamera2
import cv2
import face_recognition
import imutils
import pickle
import time
import RPi.GPIO as GPIO
import pigpio
from mfrc522 import SimpleMFRC522

# initializing RFID module
reader = SimpleMFRC522()

# initializing Servo Motor
servo = 18  
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency(servo, 50)

# initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

time.sleep(2)  # let the camera warm up
known_faces, known_names = pickle.loads(open('face_encodings.pickle', "rb").read())
print('Processing...')

# small function for RFID authentication
def authenticate_rfid():
        print("Waiting for RFID tag...")
        while True:
                id, text = reader.read()
                print(id)
                if id == int("603358394745"):  # Replace id with allowed ids, can switch out for array or smth idk
                    print("RFID authenticated!")
                    return True
                else:
                    print("Invalid RFID. Try again.")
                    time.sleep(4)

# auth the RFID before proceeding
if not authenticate_rfid():
        print("Authentication failed. Exiting...")
        exit()

while True:
    try:
        # capture frame from picam2
        frame = picam2.capture_array()

        # resize for faster processing!
        frame = imutils.resize(frame, width=344)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # display the frame 
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # detecting face locations
        locations = face_recognition.face_locations(frame, model='hog')
        encodings = face_recognition.face_encodings(frame, locations)

        print(f"Found {len(encodings)} face(s)")

        for face_encoding, face_location in zip(encodings, locations):
            results = face_recognition.compare_faces(known_faces, face_encoding, 0.4)
            match = None

            if True in results:
                match = known_names[results.index(True)]
                print(f"Match found: {match}")

                # rectangle around face with person's name !
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, match, (left, bottom + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if match:  # check if a valid match is found
                    pwm.set_servo_pulsewidth(servo, 500) # servo logic
                    time.sleep(1)
                    pwm.set_servo_pulsewidth(servo, 1500)
                    print("Face recognized, servo will spin!")  
       

    except KeyboardInterrupt:
        break

cv2.destroyAllWindows()
picam2.stop()