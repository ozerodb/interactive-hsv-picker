import cv2
import argparse
import os.path
import numpy as np


def _nothing(x):
    pass


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="the path of the input image/video, or the index of the device (default 0 for webcam)",
    )
    return parser.parse_args()


def _main():
    # Parse arguments
    args = _get_args()

    supported_image_ext = [
        ".bmp",
        ".dib",
        ".jpeg",
        ".jpg",
        ".jpe",
        ".jp2",
        ".png",
        ".webp",
        ".pbm",
        ".pgm",
        ".ppm",
        ".pxm",
        ".pnm",
        ".pfm",
        ".sr",
        ".ras",
        ".tiff",
        ".tif",
        ".exr",
        ".hdr",
        ".pic",
    ]

    if not args.source:
        print("Source cannot be empty!")
        raise SystemExit

    is_image = False
    if args.source.isnumeric():
        args.source = int(args.source)
    elif os.path.splitext(args.source)[1] in supported_image_ext:
        is_image = True

    # Instantiate the capture object
    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print(f"Error while opening source {args.source}")
        raise SystemExit

    # Create a window
    window_name = "Interactive HSV picker"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 720)
    cv2.moveWindow(window_name, 100, 100)

    # Create trackbars
    cv2.createTrackbar("Show mask", window_name, 0, 1, _nothing)
    cv2.createTrackbar("Hmin", window_name, 0, 180, _nothing)
    cv2.createTrackbar("Smin", window_name, 0, 255, _nothing)
    cv2.createTrackbar("Vmin", window_name, 0, 255, _nothing)
    cv2.createTrackbar("hMAX", window_name, 0, 180, _nothing)
    cv2.createTrackbar("sMAX", window_name, 0, 255, _nothing)
    cv2.createTrackbar("vMAX", window_name, 0, 255, _nothing)

    # Set default value for max HSV trackbars
    cv2.setTrackbarPos("hMAX", window_name, 180)
    cv2.setTrackbarPos("sMAX", window_name, 255)
    cv2.setTrackbarPos("vMAX", window_name, 255)

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
        show_mask = cv2.getTrackbarPos("Show mask", window_name)
        Hmin = cv2.getTrackbarPos("Hmin", window_name)
        Smin = cv2.getTrackbarPos("Smin", window_name)
        Vmin = cv2.getTrackbarPos("Vmin", window_name)
        hMAX = cv2.getTrackbarPos("hMAX", window_name)
        sMAX = cv2.getTrackbarPos("sMAX", window_name)
        vMAX = cv2.getTrackbarPos("vMAX", window_name)

        # Set minimum and maximum HSV values to display
        lower = (Hmin, Smin, Vmin)
        upper = (hMAX, sMAX, vMAX)

        # Convert to HSV colorspace and perform thresholding
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Concatenate the input and output frames
        margin = np.ones((frame.shape[0], 5, 3), dtype="uint8") * 255

        if show_mask:
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
