from collections import namedtuple
from fractions import Fraction
import av

# Tuples defined for storing regions to be cropped
Region = namedtuple("Region", ["xmin", "ymin", "xmax", "ymax"])

chimney_regions = {
    "smk1": [
        Region(593, 621, 721, 749),
        Region(739, 578, 803 + 64, 706),
        Region(722 + 64, 752, 850 + 64, 880),
        Region(874 + 64, 730, 1002 + 64, 858),
        Region(896 + 64, 605, 1024 + 64, 733),
        Region(941 + 64, 634, 1069 + 64, 762),
        Region(1179 + 64, 597, 1307 + 64, 725)
    ],
    "smk2": [
        Region(392 + 74, 492, 520 + 74, 620),
        Region(439 + 74, 602, 567 + 74, 730),
        Region(451 + 74, 601, 579 + 74, 729),
        Region(663 + 74, 563, 791 + 74, 691),
        Region(718 + 74, 591, 846 + 74, 719),
        Region(742 + 74, 675, 870 + 74, 803),
        Region(848 + 74, 666, 976 + 74, 794),
        Region(979 + 74, 673, 1107 + 74, 801),
        Region(1105 + 74, 625, 1233 + 74, 753),
        Region(1127 + 74, 612, 1255 + 74, 740),
        Region(1198 + 74, 614, 1326 + 74, 742),
        Region(1283 + 74, 757, 1411 + 74, 885),
        Region(1396 + 74, 767, 1524 + 74, 895)
    ],
    "ad1": [
        Region(382 + 74, 632, 510 + 74, 760),
        Region(452 + 84, 635, 580 + 84, 763),
        Region(1096 + 84, 574, 1224 + 84, 702)
    ],
    "ad3": [
        Region(499, 537, 627, 665),
        Region(906, 552, 1034, 680),
        Region(991, 559, 1119, 687)
    ],
    "ad4": [
        Region(43 + 20, 536 - 20, 171 + 20, 664 - 20),
        Region(560 + 20, 615 - 20, 688 + 20, 743 - 20),
        Region(659 + 20, 607 - 20, 787 + 20, 735 - 20)
    ],
    "jtc1": [
        Region(174 - 20, 572 + 20, 302 - 20, 700 + 20),
        Region(553 - 20, 367 + 20, 681 - 20, 495 + 20),
        Region(1197 - 20, 571 + 20, 1325 - 20, 699 + 20),
        Region(1299 - 20, 402 + 10, 1427 - 20, 530 + 10),
        Region(1535 - 20, 438 + 10, 1663 - 20, 566 + 10),
        Region(1600 - 20, 529 + 20, 1728 - 20, 657 + 20),
        Region(1662 - 20, 534 + 20, 1790 - 20, 662 + 20),
        Region(1779, 531 + 20, 1907, 659 + 20)
    ],
    "jtc2": [
        Region(128, 528, 256, 656),
        Region(275, 622, 403, 750),
        Region(400, 603, 528, 731),
        Region(417, 604, 545, 732),
        Region(577, 630, 705, 758),
        Region(679, 664, 807, 792),
        Region(696, 666, 824, 794),
        Region(1052, 530, 1180, 658),
        Region(1532, 535, 1660, 663),
        Region(1673, 540, 1801, 668),
        Region(1724, 494, 1852, 622)
    ],
    "jtc3": [
        Region(45, 577, 173, 705),
        Region(87, 690, 215, 818),
        Region(205, 724, 333, 852),
        Region(395, 583, 523, 711),
        Region(465, 746, 593, 874),
        Region(592, 651, 720, 779),
        Region(674, 674, 802, 802),
        Region(955, 677, 1083, 805),
        Region(1104, 677, 1232, 805),
        Region(1263, 727, 1391, 855),
        Region(1655, 658, 1783, 786),
        Region(1772, 542, 1900, 670)
    ],
    "jtc4": [
        Region(189, 534, 317, 662)
    ],
    "tb1": [
        Region(80, 487, 208, 615),
        Region(606, 737, 734, 865),
        Region(830, 733, 958, 861),
        Region(890, 699, 1018, 827),
        Region(919, 730, 1047, 858),
        Region(1033, 727, 1161, 855),
        Region(1219, 736, 1347, 864)
    ],
    "tb2": [
        Region(123, 719, 251, 847),
        Region(301, 712, 429, 840),
        Region(411, 498, 539, 626),
        Region(525, 440, 653, 568),
        Region(550, 499, 678, 627),
        Region(713, 598, 841, 726),
        Region(1005, 503, 1133, 631),
        Region(1030, 505, 1158, 633),
        Region(1205, 509, 1333, 637),
        Region(1269, 360, 1397, 488),
        Region(1419, 503, 1547, 631),
        Region(1671, 392, 1800, 520),
        Region(1745, 221, 1873, 349)
    ],
    "tb3": [
        Region(208, 832, 336, 960),
        Region(365, 824, 493, 952),
        Region(430, 893, 558, 1021),
        Region(446, 824, 574, 952),
        Region(525, 521, 653, 649),
        Region(988, 836, 1116, 964),
        Region(1056, 836, 1184, 964),
        Region(1089, 516, 1217, 644),
        Region(1546, 514, 1674, 642)
    ],
    "tb4": [
        Region(61 - 10, 774, 189 - 10, 902),
        Region(418 - 20, 638, 546 - 20, 766),
        Region(786 - 20, 980, 914 - 20, 1118),
        Region(995, 979, 1123, 1107),
        Region(1312, 870, 1440, 998),
        Region(1681, 683, 1809, 811)
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
    # Check if the camera_id is valid
    if not regions:
        raise ValueError(f"Invalid camera_id: {camera_id}. Valid IDs are: {list(chimney_regions.keys())}")
    for region in regions:
        xmin, ymin, xmax, ymax = region
        patch = image.crop((xmin, ymin, xmax, ymax))  # Use the crop method
        result.append(patch)
    return result