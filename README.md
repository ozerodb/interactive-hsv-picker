# interactive-hsv-picker

Little Python program to interactively find the best values for your HSV filter. Nothing new.

*Example: finding color green*<br>
![example](example.png)

>*All credit for the `hsv_reference.png` image goes to [Jacob Rus](https://en.wikipedia.org/wiki/User:Jacobolus), I simply found it on [this Wikipedia page](https://en.wikipedia.org/wiki/HSL_and_HSV).*

## Usage

The program accepts only one **optional** argument:

- `--source=<path_or_index>` : the path of the input image/video, or the index of the device (default 0 for webcam)

Once launched, you can play with the trackbars until you find an acceptable HSV range for your application.

Press q or Esc to quit.

### Examples

```bash
python3 interactive-hsv-picker.py   # uses the webcam
python3 interactive-hsv-picker.py --source='<device_idx>'    # uses the specified device
python3 interactive-hsv-picker.py --source='hsv_reference.png'   # uses the specified image
python3 interactive-hsv-picker.py --source='<input_video>.mp4'   # uses the specified video
```
