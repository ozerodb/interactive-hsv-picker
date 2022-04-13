import cv2
import argparse
import numpy as np

def _nothing(x):
    pass

def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, help='the path of the input image, when not using webcam')
    parser.add_argument('--device', type=int, default=0, help='the index of the device to be used (default 0)')
    parser.add_argument('--show-mask', default=False, action='store_true', help='if specified, also display the binary mask')
    return parser.parse_args()

def _main():
    # Parse arguments
    args = _get_args()

    src = args.image if args.image else args.device
    is_image = True if args.image else False

    # Instantiate the capture object
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        print(f'Error while opening source {src}')
        raise SystemExit

    # Create a window
    window_name = 'Interactive HSV picker'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 720)
    cv2.moveWindow(window_name, 100, 100)

    # Create trackbars
    cv2.createTrackbar('Hmin', window_name, 0, 180, _nothing)
    cv2.createTrackbar('Smin', window_name, 0, 255, _nothing)
    cv2.createTrackbar('Vmin', window_name, 0, 255, _nothing)
    cv2.createTrackbar('hMax', window_name, 0, 180, _nothing)
    cv2.createTrackbar('sMax', window_name, 0, 255, _nothing)
    cv2.createTrackbar('vMax', window_name, 0, 255, _nothing)

    # Set default value for Max HSV trackbars
    cv2.setTrackbarPos('hMax', window_name, 180)
    cv2.setTrackbarPos('sMax', window_name, 255)
    cv2.setTrackbarPos('vMax', window_name, 255)

    frame = None
    while True:
        # Retrieve the frame (if need be)
        if is_image:
            if frame is None:
                ret, frame = cap.read()
        else:
            ret, frame = cap.read()
        if not ret:
            break

        # Get current positions of all trackbars
        Hmin = cv2.getTrackbarPos('Hmin', window_name)
        Smin = cv2.getTrackbarPos('Smin', window_name)
        Vmin = cv2.getTrackbarPos('Vmin', window_name)
        hMax = cv2.getTrackbarPos('hMax', window_name)
        sMax = cv2.getTrackbarPos('sMax', window_name)
        vMax = cv2.getTrackbarPos('vMax', window_name)

        # Set minimum and maximum HSV values to display
        lower = (Hmin, Smin, Vmin)
        upper = (hMax, sMax, vMax)

        # Convert to HSV colorspace and perform thresholding
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Concatenate the input and output frames
        margin = np.ones((frame.shape[0], 5, 3), dtype = "uint8")*255

        if args.show_mask:
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            output = cv2.hconcat([frame, margin, mask, margin, result])
        else:
            output = cv2.hconcat([frame, margin, result])

        # Display result image
        cv2.imshow(window_name, output)

        # Quit the program using q or Esc
        k = cv2.waitKey(1)
        if k == 27 or k == 113:
            break

if __name__ == "__main__":
    _main()