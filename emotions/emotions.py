from cv2 import VideoCapture, destroyAllWindows
from fer import FER

how_many = 50


def find_top_emotion(data,threshold=0):
    emotions = list(data.keys())
    top_emotion = None
    top_value = 0
    for emotion in emotions:
        if data[emotion] > top_value:
            top_emotion = emotion
            top_value = data[emotion]
    if top_value < threshold:
        top_value = None
        top_emotion = None
    return top_emotion,top_value

cap = VideoCapture(0)
counter = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    emo_detector = FER()
    
        
    captured_emotions = emo_detector.detect_emotions(frame)
    # print(captured_emotions)
    print("\nFaces found: " + str(len(captured_emotions)))
    face_counter = 1
    for face in captured_emotions:
        print("\tFace number: " + str(face_counter))
        top_emotion, value = find_top_emotion(face["emotions"],threshold = 0.0)
        print("\t" + str(top_emotion))
        print("\t" + str(value))

        face_counter +=1
    
    

    
    counter += 1
    if counter > how_many:
        break
cap.release()



