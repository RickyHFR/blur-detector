from collections import namedtuple
from fractions import Fraction
import av
from PIL import ImageDraw, ImageFont

# Tuples defined for storing regions to be cropped
Region = namedtuple("Region", ["xmin", "ymin", "xmax", "ymax"])

chimney_regions = {
    "smk1": [
        Region(593, 565, 721, 693),
        Region(739, 521, 867, 649),
        Region(826, 752, 874, 800),
        # Region(0, 0, 0, 0),
        Region(980, 565, 1068, 653),
        # Region(0, 0, 0, 0),
        Region(1233, 557, 1361, 645)
        ],
        "smk2": [
        Region(476, 437, 574, 565),
        Region(545, 587, 641, 665),
        # Region(0, 0, 0, 0),
        Region(737, 558, 835, 635),
        Region(827, 591, 915, 654),
        # Region(0, 0, 0, 0),
        Region(932, 650, 1030, 740),
        Region(1060, 615, 1167, 743),
        Region(1199, 600, 1307, 680),
        # Region(0, 0, 0, 0),
        Region(1302, 614, 1400, 680),
        Region(1367, 702, 1465, 830),
        # Region(0, 0, 0, 0)
        ],
        "ad1": [
        # Region(0, 0, 0, 0),
        Region(536, 635, 664, 700),
        Region(1176, 550, 1304, 640)
        ],
        "ad3": [
        Region(554, 490, 657, 605),
        Region(936, 520, 1054, 620),
        Region(1021, 520, 1149, 627)
        ],
        "ad4": [
        # Region(0, 0, 0, 0),
        Region(580, 515, 708, 680),
        Region(679, 517, 807, 680)
        ],
        "jtc1": [
        Region(144, 572, 272, 650),
        Region(518, 367, 646, 455),
        # Region(0, 0, 0, 0),
        Region(1269, 372, 1377, 470),
        Region(1510, 420, 1638, 520),
        # Region(0, 0, 0, 0),
        Region(1632, 510, 1750, 620),
        Region(1789, 561, 1837, 589)
        ],
        "jtc2": [
        Region(123, 510, 251, 580),
        Region(270, 600, 388, 670),
        Region(440, 570, 506, 670),
        # Region(0, 0, 0, 0),
        Region(630, 610, 660, 670),
        # Region(0, 0, 0, 0),
        # Region(0, 0, 0, 0),
        Region(1052, 530, 1180, 590),
        Region(1562, 510, 1650, 600),
        # Region(1700, 520, 1771, 600),
        Region(1752, 470, 1832, 560)
        ],
        "jtc3": [
        Region(45, 530, 150, 630),
        Region(117, 670, 160, 750),
        # Region(0, 0, 0, 0),
        Region(425, 550, 503, 650),
        Region(485, 700, 553, 790),
        Region(592, 600, 720, 710),
        # Region(0, 0, 0, 0),
        Region(975, 650, 1083, 740),
        # Region(0, 0, 0, 0),
        # Region(0, 0, 0, 0),
        Region(1655, 620, 1740, 720),
        Region(1772, 480, 1850, 600)
        ],
        "jtc4": [
        Region(222, 500, 292, 590)
        ],
        "tb1": [
        Region(80, 430, 208, 560),
        Region(606, 700, 734, 810),
        Region(850, 700, 930, 790),
        Region(920, 650, 1015, 770),
        # Region(0, 0, 0, 0),
        # Region(0, 0, 0, 0),
        Region(1214, 700, 1342, 760)
        ],
        "tb2": [
        Region(106, 690, 220, 790),
        Region(284, 690, 412, 785),
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
        Region(530, 470, 658, 595),
        # Region(0, 0, 0, 0),
        # Region(0, 0, 0, 0),
        Region(1084, 470, 1212, 590),
        Region(1544, 470, 1672, 590)
        ],
        "tb4": [
        Region(53, 730, 181, 845),
        Region(398, 590, 526, 710),
        Region(786, 960, 894, 1045),
        Region(990, 950, 1118, 1045),
        # Region(0, 0, 0, 0),
        Region(1676, 630, 1804, 755)
        ]
    }

def ffmpeg_extract_interval(video_path, interval_sec=1.0):
    """
    Extract frames from a video at a fixed interval and return them as in-memory objects.
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
    Crop the chimney regions from the image based on the camera_id.
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

def label_regions(image, camera_id, scores=None, threshold=10.0):
    """
    Label the regions in the image based on the camera_id.
    """
    width, height = image.size
    regions = chimney_regions.get(camera_id, [])
    if not regions:
        raise ValueError(f"Invalid camera_id: {camera_id}. Valid IDs are: {list(chimney_regions.keys())}")
    draw = ImageDraw.Draw(image)
    try:
        font_bottom = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)  # Use a common large font on Linux
        font_score = ImageFont.truetype("DejaVuSans-Bold.ttf", 16)  # Smaller font for scores
    except Exception as e:
        print(f"Warning: Could not load DejaVuSans-Bold.ttf, using default font. Text may be small. ({e})")
        font_bottom = ImageFont.load_default()
        font_score = ImageFont.load_default()
    # Define a list of colors to cycle through for boxes and scores
    box_colors = [
        "red", "green", "blue", "orange", "purple", "magenta", "cyan", "lime", "yellow", "aqua", "fuchsia", "teal"
    ]
    for idx, region in enumerate(regions):
        xmin, ymin, xmax, ymax = region
        # Draw rectangle around the region
        box = [xmin / 1920 * width, ymin / 1080 * height, xmax / 1920 * width, ymax / 1080 * height]
        color = box_colors[idx % len(box_colors)]
        draw.rectangle(box, outline=color, width=2)
        # Draw score if provided
        if scores is not None and idx < len(scores):
            score_text = f"{scores[idx]:.2f}"
            text_x = box[0]
            text_y = box[1] - 10 - font_score.size
            if text_y < 0:
                text_y = 0
            draw.text((text_x, text_y), score_text, fill=color, font=font_score)
    # Draw average score and prediction at the bottom
    avg_score = sum(scores) / len(scores) if scores else 0
    pred = 'blur' if avg_score < threshold else 'clear'
    bottom_text = f"Avg: {avg_score:.2f} | Pred: {pred} | Threshold: {threshold:.2f} | Camera ID: {camera_id}"
    text_width, text_height = draw.textsize(bottom_text, font=font_bottom)
    bottom_x = (width - text_width) // 2
    bottom_y = height - text_height - 10
    draw.text((bottom_x, bottom_y), bottom_text, fill="cyan", font=font_bottom)
    return image, pred