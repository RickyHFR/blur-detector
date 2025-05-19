from collections import namedtuple
from fractions import Fraction
import av

# Tuples defined for storing regions to be cropped
Region = namedtuple("Region", ["xmin", "ymin", "xmax", "ymax"])

chimney_regions = {
    "smk1": [
        Region(529 + 64, 621, 657 + 64, 749),
        Region(675 + 64, 578, 803 + 64, 706),
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

# # Example usage:
# frames = ffmpeg_extract_interval("test_videos/test_vid1.mp4", interval_sec=0.5)
# for i, frame in enumerate(frames):
#     # display each frame
#     frame.show(title=f"Frame {i+1}")

# chimney_regions = {
#     "smk1": [
#         Region(593 - 64, 621, 721 - 64, 749),
#         Region(739 - 64, 578, 867 - 64, 706),
#         Region(786 - 64, 752, 914 - 64, 880),
#         Region(938 - 64, 730, 1066 - 64, 858),
#         Region(960 - 64, 605, 1088 - 64, 733),
#         Region(1005 - 64, 634, 1133 - 64, 762),
#         Region(1243 - 64, 597, 1371 - 64, 725)
#     ],
#     "smk2": [
#         Region(456 - 64, 492, 584 - 64, 620),
#         Region(503 - 64, 602, 631 - 64, 730),
#         Region(515 - 64, 601, 643 - 64, 729),
#         Region(727 - 64, 563, 855 - 64, 691),
#         Region(782 - 64, 591, 910 - 64, 719),
#         Region(806 - 64, 675, 934 - 64, 803),
#         Region(912 - 64, 666, 1040 - 64, 794),
#         Region(1043 - 64, 673, 1171 - 64, 801),
#         Region(1169 - 64, 625, 1297 - 64, 753),
#         Region(1191 - 64, 612, 1319 - 64, 740),
#         Region(1262 - 64, 614, 1390 - 64, 742),
#         Region(1347 - 64, 757, 1475 - 64, 885),
#         Region(1460 - 64, 767, 1588 - 64, 895)
#     ],
#     "ad1": [
#         Region(446 - 64, 632, 574 - 64, 760),
#         Region(516 - 64, 635, 644 - 64, 763),
#         Region(1160 - 64, 574, 1288 - 64, 702) 
#     ],
#     "ad3": [
#         Region(563 - 64, 537, 691 - 64, 665),
#         Region(970 - 64, 552, 1098 - 64, 680),
#         Region(1055 - 64, 559, 1183 - 64, 687)
#     ],
#     "ad4": [ # Invalid region due to obstruction
#         Region(107 - 64, 536, 235 - 64, 664),
#         Region(624 - 64, 615, 752 - 64, 743),
#         Region(723 - 64, 607, 851 - 64, 735) 
#     ],
#     "jtc1": [
#         Region(222 - 48, 597 - 25, 350 - 48, 725 - 25),
#         Region(601 - 48, 387 - 20, 729 - 48, 515 - 20),
#         Region(1245 - 48, 591 - 20, 1373 - 48, 719 - 20),
#         Region(1347 - 48, 402, 1475 - 48, 530),
#         Region(1599 - 64, 448 - 10, 1727 - 64, 576 - 10),
#         Region(1648 - 48, 544 - 15, 1776 - 48, 672 - 15),
#         Region(1710 - 48, 549 - 15, 1838 - 48, 677 - 15),
#         Region(1843 - 48, 546 - 15, 1971 - 48, 674 - 15)
#     ],
#     "jtc2": [
#         Region(176 - 48, 518 + 10, 304 - 48, 646 + 10),
#         Region(323 - 48, 612 + 10, 451 - 48, 740 + 10),
#         Region(448 - 48, 593 + 10, 576 - 48, 721 + 10),
#         Region(465 - 48, 594 + 10, 593 - 48, 722 + 10),
#         Region(625 - 48, 620 + 10, 753 - 48, 748 + 10),
#         Region(727 - 48, 654 + 10, 855 - 48, 782 + 10),
#         Region(744 - 48, 656 + 10, 872 - 48, 784 + 10),
#         Region(1100 - 48, 520 + 10, 1228 - 48, 648 + 10),
#         Region(1580 - 48, 525 + 10, 1708 - 48, 653 + 10),
#         Region(1721 - 48, 530 + 10, 1849 - 48, 658 + 10),
#         Region(1772 - 48, 484 + 10, 1900 - 48, 612 + 10)
#     ],
#     "jtc3": [
#         Region(93 - 48, 567 + 10, 221 - 48, 695 + 10),
#         Region(135 - 48, 680 + 10, 263 - 48, 808 + 10),
#         Region(253 - 48, 714 + 10, 381 - 48, 842 + 10),
#         Region(443 - 48, 573 + 10, 571 - 48, 701 + 10),
#         Region(513 - 48, 736 + 10, 641 - 48, 864 + 10),
#         Region(640 - 48, 641 + 10, 768 - 48, 769 + 10),
#         Region(722 - 48, 664 + 10, 850 - 48, 792 + 10),
#         Region(1003 - 48, 667 + 10, 1131 - 48, 795 + 10),
#         Region(1152 - 48, 667 + 10, 1280 - 48, 795 + 10),
#         Region(1311 - 48, 717 + 10, 1439 - 48, 845 + 10),
#         Region(1703 - 48, 648 + 10, 1831 - 48, 776 + 10),
#         Region(1820 - 48, 532 + 10, 1948 - 48, 660 + 10) 
#     ],
#     "jtc4": [
#         Region(237 - 48, 524 + 10, 365 - 48, 652 + 10) 
#     ],
#     "tb1": [
#         Region(128 - 48, 487, 256 - 48, 615),
#         Region(654 - 48, 737, 782 - 48, 865),
#         Region(878 - 48, 733, 1006 - 48, 861),
#         Region(938 - 48, 699, 1066 - 48, 827),
#         Region(967 - 48, 730, 1095 - 48, 858),
#         Region(1081 - 48, 727, 1209 - 48, 855),
#         Region(1267 - 48, 736, 1395 - 48, 864)
#     ],
#     "tb2": [
#         Region(163 - 40, 719, 291 - 40, 847),
#         Region(341 - 40, 712, 469 - 40, 840),
#         Region(451 - 40, 498, 579 - 40, 626),
#         Region(565 - 40, 440, 693 - 40, 568),
#         Region(590 - 40, 499, 718 - 40, 627),
#         Region(753 - 40, 598, 881 - 40, 726),
#         Region(1045 - 40, 503, 1173 - 40, 631),
#         Region(1070 - 40, 505, 1198 - 40, 633),
#         Region(1245 - 40, 509, 1373 - 40, 637),
#         Region(1309 - 40, 360, 1437 - 40, 488),
#         Region(1459 - 40, 503, 1587 - 40, 631),
#         Region(1711 - 30, 392, 1840 - 30, 520),
#         Region(1785 - 30, 221, 1913 - 30, 349)
#     ],
#     "tb3": [
#         Region(256 - 48, 832, 384 - 48, 960),
#         Region(413 - 58, 824, 541 - 58, 952),
#         Region(488 - 58, 893, 616 - 58, 1021),
#         Region(504 - 58, 824, 632 - 58, 952),
#         Region(583 - 58, 521, 711 - 58, 649),
#         Region(1036 - 58, 836, 1164 - 58, 964),
#         Region(1104 - 58, 836, 1232 - 58, 964),
#         Region(1137 - 58, 516, 1265 - 58, 644),
#         Region(1594 - 58, 514, 1722 - 58, 642)
#     ],
#     "tb4": [
#         Region(115 - 54, 774, 243 - 54, 902),
#         Region(466 - 54, 638, 594 - 54, 766),
#         Region(834 - 54, 980, 962 - 54, 1118),
#         Region(1049 - 54, 979, 1177 - 54, 1107),
#         Region(1366 - 54, 870, 1494 - 54, 998),
#         Region(1735 - 54, 683, 1863 - 54, 811)
#     ]
# }