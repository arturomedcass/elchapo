import face_recognition
import cv2
import numpy as np
import os
import json

def addNewFace(all_people,face_encoding,name="No name",role="n-a",fileID="n-a"):
    temp = all_people["all_people"]
    temp.append(
        {
            "fileID" : fileID,
            "name" : name,
            "role" : role,
            "encoding" : list(face_encoding)
        }
    )
    
    all_people["all_people"] = temp

    return all_people

def saveAllFaces(all_people,path= "all_people.json"):
    with open(path,"w") as open_file:
    # Load the JSON data from the file
        json.dump(all_people, open_file)

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)



file_path = "all_people.json"
with open(file_path) as open_file:
    # Load the JSON data from the file
    all_people = json.load(open_file)



peeps = all_people.keys()

known_face_encodings = []
known_face_names = []
for i in range(len(all_people["all_people"])):
    known_face_encodings.append(np.array(all_people["all_people"][i]["encoding"]))
    known_face_names.append(all_people["all_people"][i]["name"])
    



# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Only process every "n" frame of video to save time
n = 10
frame_num = n # analyse the first frame
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    
    if frame_num >= n:
        frame_num = 0
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_ind in range(len(face_encodings)):
            face_encoding = face_encodings[face_ind]
            face_location = face_locations[face_ind]


            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            

            
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            else:
                # (top, right, bottom, left) = face_location
                # top *= 4
                # right *= 4
                # bottom *= 4
                # left *= 4

                # # Draw a box around the face
                # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # # Draw a label with a name below the face
                # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                # font = cv2.FONT_HERSHEY_DUPLEX
                # cv2.putText(frame, "Face to be saved", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                # cv2.imshow('Video', frame)

                saveYN = input("Do you want to save it? (Y/N) ")
                if saveYN == "Y":
                    # Propmt user for name
                    new_name = input("What is your name? ")
                    
                    # Add new person to all_people object
                    all_people = addNewFace(all_people,face_encoding,name=new_name)
                    saveAllFaces(all_people)

                    # Add encoding and name to known_face_encodings and known_face_names (no need to reload)
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(new_name)

                

            face_names.append(name)

    frame_num += 1


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()