# ffmpeg / mkv2avi.py
This script allows you to convert MKV to AVI video, using H.264,
likely to be compatible with TV where H265 is not available.

## Installation / Usage
Use the script mkv2avi.py

```bash
python3 mkv2avi.py path_video_folder
```

Specify the path where the videos are. The output will be in the same folder
You can use -o as an option to define how you want the output files to be named
For example, if you used -o "Reign-" the output files will become "Reign-S01E01.avi" where "S01E01" will be extracted from the source file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
