import argparse
import cv2
import random
from collections import defaultdict as dd
import time
#read file
# read marked video
# go frame by frame
# wait one s per frame
# wait for key
# space for pause. back and forth with b and n, w wrong.
#first run through all the marked ones
# then run through unmarked ones.
#save the labbeled ones.
#python3 label.py -v '/Users/maj/repos/tracker/OP_analysis/Visibility_analysis_trimmed_videos/ASD_ductus_tracked.mp4' -l '/Users/maj/repos/tracker/OP_analysis/Visibility_analysis_trimmed_videos/ASD_ductus_visibility_log.txt' -r /Users/maj/repos/tracker/OP_analysis/Visibility_analysis_trimmed_videos/visbility_labels.txt

labels = dd(int)

NOT_VISIBLE = 1
VISIBLE = 2
NOT_VISIBLE_INCORRECTLY = -NOT_VISIBLE
VISIBLE_INCORRECTLY = -VISIBLE

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', required=True, action='store', default='.', help="video file")
    parser.add_argument('-l', '--log', required=True, action='store', default='.', help="log file")
    parser.add_argument('-r', '--labels', required=True, action='store', default='.', help="label file to save to")
    
    return parser.parse_args()

def read(cap, frameno):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frameno-1)
    ret, frame = cap.read()
    return frame

def check(cap, frames, title, default_label):
    SPACE = 32
    for frameno in frames:
        if labels[frameno] == 0:
            labels[frameno] = default_label

    tot = len(frames)
    index = 0
    while index < tot:
        print(f'{index}/{tot}')
        frameno = frames[index]
        frame = read(cap, frameno)
        cv2.imshow(title, frame)
        waittime = 1000 if index < tot -1 else 10000
        k = cv2.waitKey(waittime) #ms

        if k == ord('q'): exit()
        if k == SPACE:
            print('Paused')
            paused = True
            while paused:
                frameno = frames[max(0, index)]
                frame = read(cap, frameno)
                cv2.imshow(title, frame)
                k = cv2.waitKey(0)

                if k == SPACE:
                    print('Unpaused')
                    paused = False
                if k == ord('b'):
                    index -= 1
                if k == ord('n'):
                    index += 1
                if k == ord('w'):
                    labels[frameno] = -default_label
                if k == ord('c'):
                    labels[frameno] = default_label
                if k == ord('q'):
                    exit()

                
        else:
            index += 1
    
    

def write_labels(label_log):
    with open(label_log, 'w+') as lf:
        for frame, label in labels.items():
            lf.write(f'{frame} {label}\n')
    


def label(video, visibility_log, label_log):
    def convert(n): return int(n)
    visible = list(map(convert, open(visibility_log, 'r').readlines()))
    
    cap = cv2.VideoCapture(video)
    frametot = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)+ 0.5)
    K = 1000
    random.seed(1234)
    sample = random.sample(range(1, frametot + 1), K)
    vis_sample = []
    not_vis_sample = []
    for frame in sorted(sample):
        if frame in visible:
            vis_sample.append(frame)
        else:
            not_vis_sample.append(frame)
    
    print(len(vis_sample))
    print(len(not_vis_sample))
    time.sleep(3)
    print('Starting')

    check(cap, vis_sample, 'CLASSIFIED: SEEN', VISIBLE)
    #write labels
    print('Done with seen')
    
    check(cap, not_vis_sample, 'CLASSIFIED: NOT SEEN', NOT_VISIBLE)

    print('Done with unseen')
    write_labels(label_log)
    
    




def main():
    args = get_args()
    
    video = args.video
    visibility_log = args.log
    label_log = args.labels
    label(video, visibility_log, label_log)


if __name__ == '__main__':
    
    main()
