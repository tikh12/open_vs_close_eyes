import cv2
import time, numpy as np

def def_web (width, height):
    webcam = cv2.VideoCapture(0)
    webcam.set(3,width)
    webcam.set(4,height)
    return webcam

if __name__ == '__main__':
    webcam = def_web(1280,720)

    listOfDur = []
    maxLenght = 100


    while True:
        timeStart = time.time()
        ret, frame = webcam.read()

        if not ret:
            break

        cv2.imshow('Frame name', frame)

        workTime = time.time() - timeStart
        if (len(listOfDur) > maxLenght):
            listOfDur.remove(listOfDur[0])
        listOfDur.append(workTime)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(f'Время: {round(np.mean(listOfDur)*1000,2)} мс')
    webcam.release()
    cv2.destroyAllWindows()