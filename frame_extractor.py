from collections import namedtuple
from fractions import Fraction
import av
from PIL import ImageDraw

# Tuples defined for storing regions to be cropped
Region = namedtuple("Region", ["xmin", "ymin", "xmax", "ymax"])

chimney_regions = {
    "smk1": [
        Region(593 , 621 - 56 , 721  , 749 - 56 ),
        Region(739, 578 - 57, 803 + 64  , 706 - 57 ),
        Region(722 + 104  , 752 , 850 + 54 - 30, 880 - 80),
        # Region(0, 0, 0, 0),
        Region(896 + 84  , 605 - 40, 1024 + 44  , 733 - 80 ),
        # Region(0, 0, 0, 0),
        Region(1179 + 54  , 557 , 1307 + 54  , 725 - 80)
    ],
    "smk2": [
        Region(392 + 74 + 10  , 492 + 25 - 80 , 520 + 74 - 20  , 620 + 25 - 80 ),
        Region(439 + 74 + 32, 602 + 25 - 40, 567 + 74, 730 + 25 - 90 ),
        # Region(0, 0, 0, 0),
        Region(663 + 74  , 563 + 25 - 30 , 791 + 74 - 30  , 635),
        Region(718 + 109  , 591, 846 + 84 - 45  , 719 + 25 - 90),
        # Region(0, 0, 0, 0),
        Region(848 + 84  , 650 , 976 + 54  , 740),
        Region(979 + 81  , 673 , 1107 + 55  , 801 + 22 - 80 ),
        Region(1105 + 94  , 600 , 1233 + 74  , 680 ),
        # Region(0, 0, 0, 0),
        Region(1198 + 84 + 20  , 614 , 1326 + 54  , 680 ),
        Region(1283 + 84, 757, 1411 + 54, 885 + 20 - 75),
        # Region(0, 0, 0, 0)
    ],
    "ad1": [
        # Region(0, 0, 0, 0),
        Region(452 + 84  , 635 , 580 + 84  , 700),
        Region(1096 + 80  , 550 , 1224 + 80  , 640)
    ],
    "ad3": [
        Region(499 + 25 + 30  , 490 , 627 + 30  , 605),
        Region(906 + 30  , 520 , 1034 + 20  , 620 ),
        Region(991 + 30  , 520 , 1119 + 30  , 687 - 60 )
    ],
    "ad4": [
        # Region(0, 0, 0, 0),
        Region(560 + 20  , 615 - 100 , 688 + 20  , 743 - 20 - 100 ),
        Region(659 + 20  , 607 - 90 , 787 + 20  , 735 - 20 - 84 )
    ],
    "jtc1": [
        Region(174 - 30  , 572 , 302 - 30  , 650 ),
        Region(553 - 35  , 367 , 681 - 35  , 455 ),
        # Region(0, 0, 0, 0),
        Region(1299 - 30  , 402 - 30 , 1427 - 50  , 470 ),
        Region(1535 - 25  , 420 , 1663 - 25  , 520 ),
        # Region(0, 0, 0, 0),
        Region(1662 - 40 + 10  , 510 , 1790 - 40  , 620 ),
        Region(1779 - 20 + 30  , 531 , 1907 - 70  , 659 )
    ],
    "jtc2": [
        Region(128 - 5  , 510 , 256 - 5  , 580),
        Region(275 - 5  , 600 , 403 - 15  , 670),
        Region(440  , 570 , 508 - 2  , 670),
        # Region(0, 0, 0, 0),
        Region(630  , 610 , 660  , 670),
        # Region(0, 0, 0, 0),
        # Region(0, 0, 0, 0),
        Region(1052, 530, 1180, 590),
        Region(1532 + 30, 510, 1660 - 10, 600),
        Region(1700, 520, 1801 - 30, 600),
        Region(1724 - 2 + 30, 470, 1852 - 20, 560)
    ],
    "jtc3": [
        Region(45  , 530 , 150  , 630 ),
        Region(117  , 670 , 160  , 750 ),
        # Region(0, 0, 0, 0),
        Region(395 + 30 , 550 , 523 - 20  , 650 ),
        Region(465 + 20 , 700 , 593 - 40  , 790 ),
        Region(592  , 600 , 720  , 710 ),
        # Region(0, 0, 0, 0),
        Region(975  , 650 , 1083  , 740 ),
        # Region(0, 0, 0, 0),
        # Region(0, 0, 0, 0),
        Region(1655, 620, 1740, 720),
        Region(1772, 480, 1850, 600)
    ],
    "jtc4": [
        Region(230, 500, 300, 590)
    ],
    "tb1": [
        Region(80, 430, 208, 560),
        Region(606, 700, 734, 810),
        Region(850, 700, 930, 790),
        Region(920, 650, 1015, 770),
        # Region(0, 0, 0, 0),
        # Region(0, 0, 0, 0),
        Region(1219 - 5, 700, 1347 - 5, 760)
    ],
    "tb2": [
        Region(123 - 17, 690, 220, 790),
        Region(301 - 17, 690, 429 - 17, 785),
        Region(400, 450, 495, 570),
        Region(515, 410, 643, 510),
        # Region(0, 0, 0, 0),
        Region(700, 570, 831, 670),
        Region(995, 450, 1123, 575),
        # Region(0, 0, 0, 0),
        Region(1205, 450, 1300, 580),
        Region(1290, 300, 1400, 430),
        Region(1419, 450, 1547, 570),
        Region(1671, 350, 1780, 460),
        # Region(0, 0, 0, 0)
    ],
    "tb3": [
        # Region(0, 0, 0, 0),
        # Region(0, 0, 0, 0),
        # Region(0, 0, 0, 0),
        # Region(0, 0, 0, 0),
        Region(525 + 5, 470, 653 + 5, 595),
        # Region(0, 0, 0, 0),
        # Region(0, 0, 0, 0),
        Region(1089 - 5, 470, 1217 - 5, 590),
        Region(1546 - 2, 470, 1674 - 2, 590)
    ],
    "tb4": [
        Region(61 - 8, 730, 189 - 8, 845),
        Region(418 - 20, 590, 546 - 20, 710),
        Region(786, 960, 914 - 20, 1045),
        Region(995 - 5, 950, 1123 - 5, 1045),
        # Region(0, 0, 0, 0),
        Region(1681 - 5, 630, 1809 - 5, 755)
    ]
}

# Function to extract frames from a video
def ffmpeg_extract_interval(video_path, interval_sec=1.0):
    """
    Extract frames from a video at a fixed interval and return them as in-memory objects.

    :param video_path: Path to MP4 video.
    :param interval_sec: Seconds between each output frame.
    :return: List of PIL.Image objects representing the frames.
    """
    container = av.open(video_path)
    stream = container.streams.video[0]
    tb = stream.time_base

    # How many pts‐units correspond to interval_sec?
    # interval_sec / time_base  => Fraction
    pts_per_interval = int((Fraction(interval_sec) / tb).limit_denominator())

    frames = []
    next_pts = 0

    for frame in container.decode(stream):
        # frame.pts is in units of tb
        if frame.pts is None:
            continue
        if frame.pts >= next_pts:
            frames.append(frame.to_image())
            next_pts += pts_per_interval

    return frames

def crop_chimney_regions(image, camera_id):
    """
    image       : PIL image
    camera_id   : ID of the camera

    Returns:
        list of cropped patches
    """
    result = []
    regions = chimney_regions.get(camera_id, [])
    width, height = image.size
    # Check if the camera_id is valid
    if not regions:
        raise ValueError(f"Invalid camera_id: {camera_id}. Valid IDs are: {list(chimney_regions.keys())}")
    for region in regions:
        xmin, ymin, xmax, ymax = region
        patch = image.crop((xmin / 1920 * width, ymin / 1080 * height, xmax / 1920 * width, ymax / 1080 * height))  # Use the crop method
        result.append(patch)
    return result

def label_regions(image, camera_id):
    """
    Label the regions in the image based on the camera_id.

    :param image: PIL image
    :param camera_id: ID of the camera
    :return: List of labeled regions
    """
    width, height = image.size
    regions = chimney_regions.get(camera_id, [])
    if not regions:
        raise ValueError(f"Invalid camera_id: {camera_id}. Valid IDs are: {list(chimney_regions.keys())}")
    for region in regions:
        xmin, ymin, xmax, ymax = region
        # Draw rectangle around the region
        draw = ImageDraw.Draw(image)
        draw.rectangle([xmin / 1920 * width, ymin / 1080 * height, xmax / 1920 * width, ymax / 1080 * height], outline="red", width=2)
    return image