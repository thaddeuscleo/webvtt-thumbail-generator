import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime


def __concat_vh(list_2d):
    return cv2.vconcat([cv2.hconcat(list_h) for list_h in list_2d])


def __cvt_video_to_frames(video_filename, num_of_frames):
    cap = cv2.VideoCapture(video_filename)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) * 0.94)
    frames = []
    duration = 0
    if cap.isOpened() and total_frames > 0:

        seconds = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
        video_time = str(datetime.timedelta(seconds=seconds))

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, image = cap.read()
        for i in range(1, num_of_frames + 1):
            cap.set(cv2.CAP_PROP_POS_FRAMES, round(
                total_frames * i / num_of_frames))
            success, image = cap.retrieve()
            if not success:
                break
            frames.append(image)
    return frames, video_time


def generate_thumbnail(video_path, shape=(4, 4), image_format=".jpg", skip_exist=True, flat_dir=False, output_dir='Thumbnails'):
    output_path = os.path.splitext(video_path)[0] + image_format
    # Check in output file exists
    if os.path.isfile(output_path) and skip_exist:
        print(f'[INFO]: skip {output_path}, file already exist')
        return

    # Check video file is readable
    if not os.path.isfile(video_path):
        print(f'[INFO]: skip {video_path}, fail to read file')
        return

    print(f'[INFO]: processing {video_path}')

    frames, video_time = __cvt_video_to_frames(video_path, shape[0] * shape[1])
    thumbnail_shape = [shape, frames[0].shape]
    thumbnail_shape = [i for sub in thumbnail_shape for i in sub]
    frames = np.reshape(frames, thumbnail_shape)

    # Generate and save combined thumbnail
    thumbnail = __concat_vh(frames)
    thumbnail_size = (frames[0][0].shape[1], frames[0][0].shape[0])
    thumbnail = cv2.resize(thumbnail, thumbnail_size,
                           interpolation=cv2.INTER_AREA)

    if not flat_dir:
        final_path = f"{os.path.join(output_dir, output_path)}"
    else:
        final_path = f"{os.path.join(output_dir, output_path.split('/')[-1])}"
    final_dir = os.path.join(*final_path.split('/')[:-1])
    label = f"""
        Title: {final_path.split('/')[-1].split('.')[0]} \n
        Production: {output_path.split('/')[0]} \n
        Duration: {video_time}
    """

    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    plt.figure(figsize=(10,10))
    ax = plt.axes(frameon=False, xticks=[],yticks=[])
    ax.set_title(label, loc='left', fontsize=8, fontweight='bold')
    ax.imshow(cv2.cvtColor(thumbnail, cv2.COLOR_BGR2RGB))
    plt.savefig(final_path, bbox_inches='tight', pad_inches=0.1)
    print(
        f'[INFO]: thumb saved at {final_path}')

