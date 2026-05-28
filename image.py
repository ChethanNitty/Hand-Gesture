import cv2 as cv

cap = cv.VideoCapture(0)

while True:

    ret, frame = cap.read()

    blur = cv.blur(frame, (45,45))

    cv.imshow("Original", frame)
    cv.imshow("Smooth", blur)

    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()