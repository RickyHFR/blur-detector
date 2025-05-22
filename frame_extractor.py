from collections import namedtuple
from fractions import Fraction
import av

# Tuples defined for storing regions to be cropped
Region = namedtuple("Region", ["xmin", "ymin", "xmax", "ymax"])

chimney_regions = {
    "smk1": [
        Region(593 , 621 , 721  , 749 ),
        Region(739, 578 , (803 + 64)  , 706 ),
        Region(722 + 54 + 40  , 752 , (850 + 54 - 40)  , 880 - 80),
        Region((874 + 64 + 40)  , 730 , (1002 + 64 - 40)  , 858 - 80),
        Region((896 + 64)  , 605 , (1024 + 64)  , 733 ),
        Region((941 + 66)  , 634 , (1069 + 66)  , 762 ),
        Region((1179 + 54)  , 597 , (1307 + 54)  , 725 )
    ],
    "smk2": [
        Region((392 + 74)  , (492 + 25) , (520 + 74) - 30  , (620 + 25) ),
        Region((439 + 74) + 40  , (602 + 25) , (567 + 74)  , (730 + 25) ),
        Region((451 + 74) + 30 , (601 + 25) , (579 + 74)  , (729 + 25) ),
        Region((663 + 74)  , (563 + 25) , (791 + 74) - 20  , (691 + 25) ),
        Region((718 + 104)  , (591 + 25) , (846 + 84)  , (719 + 25) ),
        Region((742 + 79)  , (675 + 22) , (870 + 79)  , (803 + 22) - 20 ),
        Region((848 + 84)  , (666 + 22) , (976 + 84)  , (794 + 22) ),
        Region((979 + 81)  , (673 + 22) , (1107 + 81)  , (801 + 22) - 20 ),
        Region((1105 + 84)  , (625 + 22) , (1233 + 84)  , (753 + 22) ),
        Region((1127 + 82)  , (612 + 20) , (1255 + 82) - 10  , (740 + 20) ),
        Region((1198 + 84) + 20  , (614 + 30) , (1326 + 84)  , (742 + 30) ),
        Region((1283 + 84)  , (757 + 20) , (1411 + 84)  , (885 + 20) - 40 ),
        Region((1396 + 84)  , (767 + 22) , (1524 + 84) - 59 , (895 + 22) - 54)
    ],
    "ad1": [
        # Region((382 + 74)  , 632 , (510 + 74)  , 760 ),
        Region((452 + 84)  , 635 , (580 + 84)  , 763 ),
        Region((1096 + 80)  , (574 + 15) , (1224 + 80)  , (702 + 15) )
    ],
    "ad3": [
        Region((499 + 30 + 30)  , 537 , (627 + 30)  , 665 ),
        Region((906 + 30)  , 552 , (1034 + 30)  , 680 ),
        Region((991 + 30)  , 559 , (1119 + 30)  , 687 - 20 )
    ],
    "ad4": [
        Region((43 + 20)  , (536 - 20) , (171 + 20)  , (664 - 20) ), # TODO: unsure
        Region((560 + 20) + 40  , (615 - 20) , (688 + 20) - 45  , (743 - 20) - 90 ), # TODO: unsure
        Region((659 + 20) + 40  , (607 - 20) , (787 + 20) - 40  , (735 - 20) - 84 ) # TODO: unsure
    ],
    "jtc1": [
        Region((174 - 30) + 64  , (572 + 25) , (302 - 30) - 10  , (700 + 25) ),
        Region((553 - 35)  , (367 + 25) , (681 - 35)  , (495 + 25) + 10 ),
        Region((1197 - 35)  , (571 + 25) , (1325 - 35)  , (699 + 25) ), # TODO: unsure
        Region((1299 - 40)  , (402 + 10) , (1427 - 40)  , (530 + 10) ),
        Region((1535 - 25)  , (438 + 10) , (1663 - 25)  , (566 + 10) ),
        Region((1600 - 35) + 50  , (529 + 25) , (1728 - 35)  , (657 + 25) ),
        Region((1662 - 40) + 64  , (534 + 25) , (1790 - 40)  , (662 + 25) ),
        Region((1779 - 20) + 30  , (531 + 25) , (1907 - 20)  , (659 + 25) )
    ],
    "jtc2": [
        Region((128 - 5)  , (528 + 10) , (256 - 5)  , (656 + 10) - 10 ),
        Region((275 - 5)  , (622 + 8) , (403 - 5)  , (750 + 8) ),
        Region((400 - 2)  , (603 + 10) , (528 - 2)  , (731 + 10) ), # TODO: unsure
        Region((417 - 2)  , (604 + 10) , (545 - 2)  , (732 + 10) ), # TODO: unsure
        Region((577 - 3)  , (630 + 20) , (705 - 3)  , (758 + 20) ),
        Region((679 - 4)  , (664 + 10) , (807 - 4)  , (792 + 10) ),
        Region((696 - 2)  , (666 + 10) , (824 - 2)  , (794 + 10) ),
        Region(1052  , (530) , 1180  , (658) ),
        Region(1532 + 30 , (535 + 10) , 1660 - 50 , (663 + 10) ),
        Region(1673  , (540 + 10) , 1801 - 40  , (668 + 10) + 20 ),
        Region((1724 - 2) + 30  , (494 + 10) , (1852 - 2) - 30  , (622 + 10) )
    ], # until here
    "jtc3": [
        Region(45  , (577 + 5) , 173  , (705 + 5) ),
        Region(87  , (690 + 10) , 215  , (818 + 10) ),
        Region(205  , (724 + 10) , 333  , (852 + 10) ),
        Region(395  , (583 + 10) , 523  , (711 + 10) ),
        Region(465  , (746 + 10) , 593  , (874 + 10) ),
        Region(592  , (651 + 15) , 720  , (779 + 15) ),
        Region(674  , (674 + 10) , 802  , (802 + 10) ),
        Region(955  , (677 + 10) , 1083  , (805 + 10) ),
        Region(1104  , 677 , 1232  , 805 ),
        Region(1263  , (727 + 10) , 1391  , (855 + 10) ),
        Region(1655  , (658 + 10) , 1783  , (786 + 10) ),
        Region(1772  , (542 + 5) , 1900  , (670 + 5) )
    ],
    "jtc4": [
        Region((189 + 10)  , (534 + 5) , (317 + 10)  , (662 + 5) )
    ],
    "tb1": [
        Region(80  , (487 + 5) , 208  , (615 + 5) ),
        Region(606  , (737 + 5) , 734  , (865 + 5) ),
        Region(830  , (733 + 5) , 958  , (861 + 5) ),
        Region((890 - 3)  , (699 + 5) , (1018 - 3)  , (827 + 5) ),
        Region(919  , (730 + 5) , 1047  , (858 + 5) ),
        Region((1033 + 727)  , (855 + 3) , (1161 + 727)  , (855 + 3) ),
        Region((1219 - 5)  , (736 + 5) , (1347 - 5)  , (864 + 5) )
    ],
    "tb2": [
        Region((123 - 17)  , (719 + 10) , (251 - 17)  , (847 + 10) ),
        Region((301 - 17)  , (712 + 10) , (429 - 17)  , (840 + 10) ),
        Region((411 - 10)  , (498 + 10) , (539 - 10)  , (626 + 10) ),
        Region((525 - 10)  , (440 + 8) , (653 - 10)  , (568 + 8) ),
        Region((550 - 10)  , (499 + 10) , (678 - 10)  , (627 + 10) ),
        Region((713 - 10)  , (598 + 10) , (841 - 10)  , (726 + 10) ),
        Region((1005 - 10)  , (503 + 10) , (1133 - 10)  , (631 + 10) ),
        Region((1030 - 10)  , (505 + 10) , (1158 - 10)  , (633 + 10) ),
        Region((1205 - 7)  , (509 + 10) , (1333 - 7)  , (637 + 10) ),
        Region((1269 - 5)  , (360 + 10) , (1397 - 5)  , (488 + 10) ),
        Region(1419  , (503 + 10) , 1547  , (631 + 10) ),
        Region(1671  , (392 + 10) , 1800  , (520 + 10) ),
        Region(1745  , (221 + 10) , 1873  , (349 + 10) )
    ],
    "tb3": [
        Region((208 - 5)  , 832 , (336 - 5)  , 960 ),
        Region((365 - 3)  , 824 , (493 - 3)  , 952 ),
        Region((430 + 15)  , (893 + 20) , (558 + 15)  , (1021 + 20) ),
        Region((446 + 5)  , 824 , (574 + 5)  , 952 ),
        Region((525 + 5)  , 521 , (653 + 5)  , 649 ),
        Region(988  , 836 , 1116  , 964 ),
        Region(1056  , 836 , 1184  , 964 ),
        Region((1089 - 5)  , 516 , (1217 - 5)  , 644 ),
        Region((1546 - 2)  , 514 , (1674 - 2)  , 642 )
    ],
    "tb4": [
        Region((61 - 8)  , 774 , (189 - 8)  , 902 ),
        Region((418 - 20)  , 638 , (546 - 20)  , 766 ),
        Region((786 - 20)  , (980 + 3) , (914 - 20)  , (1118 + 3) ),
        Region((995 - 5)  , (979 + 5) , (1123 - 5)  , (1107 + 5) ),
        Region((1312 - 5)  , (870 + 3) , (1440 - 5)  , (998 + 3) ),
        Region((1681 - 5)  , (683 + 5) , (1809 - 5)  , (811 + 5) )
    ]
}

# Function to extract frames from a video
def ffmpeg_extract_interval(video_path, interval_sec=30.0):
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