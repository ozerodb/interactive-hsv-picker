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


def _print_hsv_values(window_name):
    Hmin = cv2.getTrackbarPos("Hmin", window_name)
    Smin = cv2.getTrackbarPos("Smin", window_name)
    Vmin = cv2.getTrackbarPos("Vmin", window_name)
    Hmax = cv2.getTrackbarPos("Hmax", window_name)
    Smax = cv2.getTrackbarPos("Smax", window_name)
    Vmax = cv2.getTrackbarPos("Vmax", window_name)
    print(f"HSV range -> lower: ({Hmin}, {Smin}, {Vmin})  upper: ({Hmax}, {Smax}, {Vmax})")


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
    # Try to parse source as a device index (supports negative indices too)
    try:
        args.source = int(args.source)
    except ValueError:
        ext = os.path.splitext(args.source)[1].lower()
        if ext in supported_image_ext:
            is_image = True
        # Check that the file actually exists before attempting to open it
        if not os.path.isfile(args.source):
            print(f"Error: file not found: {args.source}")
            raise SystemExit

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
    cv2.createTrackbar("Hmax", window_name, 0, 180, _nothing)
    cv2.createTrackbar("Smax", window_name, 0, 255, _nothing)
    cv2.createTrackbar("Vmax", window_name, 0, 255, _nothing)

    # Set default value for max HSV trackbars
    cv2.setTrackbarPos("Hmax", window_name, 180)
    cv2.setTrackbarPos("Smax", window_name, 255)
    cv2.setTrackbarPos("Vmax", window_name, 255)

    print("Controls: 'q' or Esc to quit, 's' to print current HSV values")

    frame = None
    while True:
        # Retrieve the frame (if need be)
        if is_image:
            if frame is None:
                ret, frame = cap.read()
        else:
            ret, frame = cap.read()
        if not ret:
            if frame is None:
                print("Error: failed to read frame from source.")
            break

        # Get current positions of all trackbars
        show_mask = cv2.getTrackbarPos("Show mask", window_name)
        Hmin = cv2.getTrackbarPos("Hmin", window_name)
        Smin = cv2.getTrackbarPos("Smin", window_name)
        Vmin = cv2.getTrackbarPos("Vmin", window_name)
        Hmax = cv2.getTrackbarPos("Hmax", window_name)
        Smax = cv2.getTrackbarPos("Smax", window_name)
        Vmax = cv2.getTrackbarPos("Vmax", window_name)

        # Set minimum and maximum HSV values to display
        lower = (Hmin, Smin, Vmin)
        upper = (Hmax, Smax, Vmax)

        # Convert to HSV colorspace and perform thresholding
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Concatenate the input and output frames
        margin = np.ones((frame.shape[0], 5, 3), dtype="uint8") * 255

        if show_mask:
            mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            output = cv2.hconcat([frame, margin, mask_bgr, margin, result])
        else:
            output = cv2.hconcat([frame, margin, result])

        # Display result image
        cv2.imshow(window_name, output)

        # Quit with q or Esc; print current values with s
        k = cv2.waitKey(1)
        if k == 27 or k == ord('q'):
            _print_hsv_values(window_name)
            break
        elif k == ord('s'):
            _print_hsv_values(window_name)


if __name__ == "__main__":
    _main()
