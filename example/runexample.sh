#!/bin/bash
echo "Running log_in_video.py with short.mp4 and min 2 visible sides"
python3 ../log_in_video.py -v ./video/short.mp4 -cd data_sony.yaml -o ./tracked/short_tracked.mp4 -m 1 -l log.txt


echo "Running plot_pos.py with 100 frames interval (4 s)."
python3 ../plot_pos.py  -l /Users/maj/repos/3d_tracking/example/log.txt --interval_size=100