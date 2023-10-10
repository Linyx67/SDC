import cv2
import numpy as np

def topView(image, corners):
    """
    image   : The input image.
    corners : A tuple of 4 corners giving the region of interest.
    The corners are given clockwise from the top left corner
    1_____________2

    |             |
    |             |
    |             |
    4_____________3
    """
    # Get the Height and Width of the image
    (H, W) = image.shape[:2]
    # Convert the input tuple of corners to a numpy float32 matrix
    corners = np.float32(corners)
    # The input corners are mapped to these output corners
    outputCorners = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
    # Apply OpenCV's perspective transform
    transform = cv2.getPerspectiveTransform(corners, outputCorners)
    warped = cv2.warpPerspective(image, transform, (W, H))
    return warped, transform

def transformPoints(points, transform):
    """
    Apply a perspective transform to a set of points on an image.
    Return the new points on the transformed image.
    """
    # Convert the points to a numpy float32 matrix
    points = np.float32(points)
    points = points.reshape(-1, 1, 2)
    # Apply the perspective transform and return a list of the new points
    transformed = cv2.perspectiveTransform(points, transform)
    transformedPoints = []
    for i in range(points.shape[0]):
        transformedPoints.append((int(transformed[i][0][0]),
                                   int(transformed[i][0][1])))
    return transformedPoints

def highlightView(image, corners):
    """
    Draw lines showing the region of interest specificed by the 4 corners given.
    """
    # Highlight the Corners
    for corner in corners:
        cv2.circle(image, corner, 10, (0, 255, 0), -1)
    # Draw a box around the region
    cv2.line(image, corners[0], corners[1], (0, 255, 0), 2)
    cv2.line(image, corners[1], corners[2], (0, 255, 0), 2)
    cv2.line(image, corners[2], corners[3], (0, 255, 0), 2)
    cv2.line(image, corners[3], corners[0], (0, 255, 0), 2)


def testChessboard2():
    image = cv2.imread("resources/chessboard-2.jpg")    
    image = cv2.resize(image, (1008, 756))
    cboard2 = ((125, 55), (855, 60), (970, 725), (16, 720))    
    view, transform = topView(image, cboard2)
    highlightView(image, cboard2)
    cv2.imshow("Input", image)
    cv2.imshow("Output", view)
    while True:
        if cv2.waitKey(1) == ord('q'):
            break

def testChessboard4():
    image = cv2.imread("resources/chessboard-4.jpg")    
    image = cv2.resize(image, (479, 369))
    cboard4 = ((212, 24), (448, 136), (295, 344), (34, 192))
    view, transform = topView(image, cboard4)
    highlightView(image, cboard4)
    cv2.imshow("Input", image)
    cv2.imshow("Output", view)
    while True:
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()

def testVideo(filepath):
    cap = cv2.VideoCapture(filepath)
    region = ((299, 115), (748, 225), (512, 456), (52, 269))
    success, frame = cap.read()
    while success:
        view, transform = topView(frame, region)
        highlightView(frame, region)
        cv2.imshow("Input", frame)
        cv2.imshow("Output", view)
        success, frame = cap.read()

        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()

def testVideo1():
    cap = cv2.VideoCapture("resources/vtest.avi")
    region = ((299, 115), (748, 225), (512, 456), (52, 269))
    success, frame = cap.read()
    while success:
        view, transform = topView(frame, region)
        highlightView(frame, region)
        cv2.imshow("Input", frame)
        cv2.imshow("Output", view)
        success, frame = cap.read()

        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()

def testVideo2():
    cap = cv2.VideoCapture("resources/pedestrians.mkv")
    region = ((463, 72), (929, 153), (713, 536), (64, 296))
    success, frame = cap.read()
    while success:
        frame = cv2.resize(frame, (960, 540))
        view, transform = topView(frame, region)
        highlightView(frame, region)
        cv2.imshow("Input", frame)
        cv2.imshow("Output", view)
        success, frame = cap.read()

        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()

def testTransformPoints1():
    image = cv2.imread("resources/chessboard-2.jpg")    
    image = cv2.resize(image, (1008, 756))
    cboard2 = ((125, 55), (855, 60), (970, 725), (16, 720))    
    # Points to transform
    testPoints = ((408, 278), (737, 216), (725, 531), (145, 570))
    view, transform = topView(image, cboard2)
    transformedPoints = transformPoints(testPoints, transform)
    # Draw circles at the original points and their transformations
    for point in testPoints:
        cv2.circle(image, point, 10, (0, 255, 0), -1)
    for point in transformedPoints:
        cv2.circle(view, point, 10, (0, 255, 0), -1)
    highlightView(image, cboard2)
    cv2.imshow("Input", image)
    cv2.imshow("Output", view)
    while True:
        if cv2.waitKey(1) == ord('q'):
            break

def testTransformPoints2():
    cap = cv2.VideoCapture("resources/vtest.avi")
    region = ((299, 115), (748, 225), (512, 456), (52, 269))
    testPoints = ((300, 200), (300, 300))
    success, frame = cap.read()
    while success:
        frame = cv2.resize(frame, (960, 540))
        view, transform = topView(frame, region)
        transformedPoints = transformPoints(testPoints, transform)
        highlightView(frame, region)

        for point in testPoints:
            cv2.circle(frame, point, 10, (0, 255, 0), -1)
        for point in transformedPoints:
            cv2.circle(view, point, 10, (0, 255, 0), -1)

        cv2.imshow("Input", frame)
        cv2.imshow("Output", view)
        success, frame = cap.read()

        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()

# Uncomment to run some demos
# testChessboard2()
# testChessboard4()
# testVideo1()
# testVideo2()
# testTransformPoints1()
# testTransformPoints2()