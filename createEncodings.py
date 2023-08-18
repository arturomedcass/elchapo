import face_recognition
import os
import json

people_paths = os.listdir("people")
for i in range(len(people_paths)):
    people_paths[i] = os.path.join("people",people_paths[i])

file_path = "all_people.json"
with open(file_path) as open_file:
    # Load the JSON data from the file
    all_people = json.load(open_file)

for i in range(len(all_people["all_people"])):
    path = all_people["all_people"][i]["fileID"]

    path = os.path.join("people",path)

    image = face_recognition.load_image_file(path)

    all_people["all_people"][i]["encoding"] = list(face_recognition.face_encodings(image)[0])
    

print(all_people)

with open(file_path,"w") as open_file:
    # Load the JSON data from the file
    json.dump(all_people, open_file)