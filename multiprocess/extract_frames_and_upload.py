import sys
import os
import urllib
import multiprocessing as mp
import argparse

from tos_client import upload_image

import logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()

fileHandler = logging.FileHandler("extract_frames.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.setLevel(logging.INFO)


def extract_frames_and_upload(video_queue, video_dir, frame_dir, fps, key_frame):
    while True:
        video = video_queue.get()
        if video is not None:
            video_path = os.path.join(video_dir, video)
            frame_sub_dir = os.path.join(frame_dir, video.replace(".mp4", ""))
            if not os.path.isdir(frame_sub_dir):
                os.mkdir(frame_sub_dir)
            if not key_frame:
                cmd = "ffmpeg -i {} -q:v 1 -vf fps={} {}/%5d.jpg".format(video_path, str(fps), frame_sub_dir)
            else:
                cmd = "ffmpeg -i {} -q:v 1 -force_key_frames 'expr:gte(t,n_forced*{})' -vsync vfr {}/%5d.jpg".format(video_path, str(fps), frame_sub_dir)
            os.system(cmd)

            frame_img_files = os.listdir(frame_sub_dir)
            flag_frame = 0
            for img in frame_img_files:
                try:
                    img_path = os.path.join(frame_sub_dir, img)
                    with open(img_path, 'r') as img_file:
                        image_data = img_file.read()
                        tos_uri = upload_image(image_data, "%s_%s" % (video.replace(".mp4", ""), img.replace(".jpg", "")))
                        logger.debug('$$Upload frame success: %s' % tos_uri)
                    cmd = "rm %s" % img_path
                    os.system(cmd)
                except Exception as ex:
                    logger.warn(str(ex) + '----' + img)
                    flag_frame += 1
                    pass
            logger.info("##Vid Completion: %s, error: %d" % (frame_sub_dir.split("/")[-1], flag_frame))
            if not flag_frame:
                os.system("rm -rf %s" % frame_sub_dir)
        else:
            return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_dir", required=True)
    parser.add_argument("--frame_dir", required=True)
    parser.add_argument("--fps", type=float, default=1)
    parser.add_argument("--num_processes", type=int, default=1)
    parser.add_argument("--key_frame", action="store_true")
    parser.add_argument("--vid_list", type=str)
    args = parser.parse_args()
    video_queue = mp.Queue()
    videos = os.listdir(args.video_dir)
    vid_completed = list()
    with open(args.vid_list, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if len(line) > 3:
                vid_completed.append(line.strip())
    videos = filter(lambda v: v not in vid_completed, videos)

    videos = videos[:1000]  # 10 for test, to be deleted

    for video in videos:
        video_queue.put(video)
    for i in xrange(args.num_processes):
        video_queue.put(None)

    processes = []
    for i in xrange(args.num_processes):
        p = mp.Process(
            target=extract_frames_and_upload, args=(video_queue, args.video_dir, args.frame_dir, args.fps, args.key_frame))
        p.daemon = True
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
