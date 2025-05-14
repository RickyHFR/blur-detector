# import cv2
# import numpy as np
#
# def detect_blurriness_fft(region, threshold):
#     gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
#     f = np.fft.fft2(gray)
#     fshift = np.fft.fftshift(f)
#     magnitude_spectrum = np.abs(fshift)
#     high_freq_ratio = np.sum(magnitude_spectrum > 50) / magnitude_spectrum.size
#     is_blurry = high_freq_ratio < threshold
#     return is_blurry, high_freq_ratio
#
# def process_video_with_regions(input_video_path, output_video_path, regions, threshold):
#     cap = cv2.VideoCapture(input_video_path)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
#     frame_count = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         for region in regions:
#             xmin, ymin = region
#             xmax = xmin+128
#             ymax = ymin+128
#             cropped = frame[ymin:ymax, xmin:xmax]
#             is_blurry, high_freq_ratio = detect_blurriness_fft(cropped, threshold)
#             text = f"Blur: {high_freq_ratio:.2f} {'(Blurry)' if is_blurry else '(Clear)'}"
#             color = (0, 0, 255) if is_blurry else (0, 255, 0)
#             cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
#             cv2.putText(frame, text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
#         out.write(frame)
#         frame_count += 1
#     cap.release()
#     out.release()
# regions = [
#     (237, 330),
#     (812, 406),
#     (671, 436)
# ]
#
# input_video = "/media/peseyes/output/blur1.mp4"
# output_video = "/media/peseyes/output/blur1_test.mp4"
# blur_threshold = 0.7
# process_video_with_regions(input_video, output_video, regions, blur_threshold)
#15
# regions = [
#     (391, 367, 460, 450),
#     (456, 381, 510, 441),
#     (44, 330, 110, 399)
# ]
#14
# regions = [
#     (788, 350, 893, 477),
#     (520, 328, 642, 493),
#     (324, 323, 431, 472)
# ]
#7
# regions = [
#     (291, 196, 419, 324),
#     (226, 208, 354, 336)
# ]
#17
# regions = [
#     (319, 246, 436, 371),
#     (638, 280, 778, 412),
#     (901, 269, 1041, 404)
# ]
#21
#blur1
# regions = [
#     (237, 330),
#     (812, 406),
#     (671, 436)
# ]
# # regions = [
# #     (350, 300),
# #     (722, 220)
# # ]
# input_video = "/media/peseyes/output/blur1.mp4"
# output_video = "/media/peseyes/output/blur1_test.mp4"
# blur_threshold = 0.7
# process_video_with_regions(input_video, output_video, regions, blur_threshold)


import cv2
import numpy as np

# def detect_blurriness_fft(region, threshold):
#     gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
#     f = np.fft.fft2(gray)
#     fshift = np.fft.fftshift(f)
#     magnitude_spectrum = np.abs(fshift)
#     high_freq_ratio = np.sum(magnitude_spectrum > 100) / magnitude_spectrum.size
#     is_blurry = high_freq_ratio < threshold
#     return is_blurry, high_freq_ratio

def detect_blurriness_fft(region, threshold):
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.abs(fshift)

    sorted_magnitude = np.sort(magnitude_spectrum.flatten())
    cutoff_index = int(len(sorted_magnitude) * 0.9)
    cutoff_value = sorted_magnitude[cutoff_index]

    magnitude_spectrum[magnitude_spectrum > cutoff_value] = 0

    high_freq_ratio = np.sum(magnitude_spectrum > 100) / magnitude_spectrum.size

    is_blurry = high_freq_ratio < threshold
    return is_blurry, high_freq_ratio

def process_video_with_regions(input_video_path, output_video_path, regions, block_size, threshold):
    cap = cv2.VideoCapture(input_video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # for region in regions:
        #     xmin, ymin= region
        #     xmax = xmin+128
        #     ymax = ymin+128
        #     cropped = frame[ymin:ymax, xmin:xmax]
        #
        #     h, w = cropped.shape[:2]
        #     for y in range(0, h, block_size):
        #         for x in range(0, w, block_size):
        #             block_xmin = x
        #             block_ymin = y
        #             block_xmax = min(x + block_size, w)
        #             block_ymax = min(y + block_size, h)
        #             block = cropped[block_ymin:block_ymax, block_xmin:block_xmax]
        #
        #             is_blurry, high_freq_ratio = detect_blurriness_fft(block, threshold)
        #
        #             text = f"{high_freq_ratio:.2f} {'B' if is_blurry else 'C'}"
        #             color = (0, 0, 255) if is_blurry else (0, 255, 0)
        #             cv2.rectangle(cropped, (block_xmin, block_ymin), (block_xmax, block_ymax), color, 2)
        #             cv2.putText(cropped, text, (block_xmin + 5, block_ymin + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.1, color, 1, cv2.LINE_AA)
        #
        #     frame[ymin:ymax, xmin:xmax] = cropped
        for region in regions:
            xmin, ymin = region
            xmax = xmin + 128
            ymax = ymin + 128
            cropped = frame[ymin:ymax, xmin:xmax]

            is_blurry, high_freq_ratio = detect_blurriness_fft(cropped, threshold)

            text = f"{high_freq_ratio:.2f} {'B' if is_blurry else 'C'}"
            color = (0, 0, 255) if is_blurry else (0, 255, 0)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
            cv2.putText(frame, text, (xmin + 5, ymin + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

        out.write(frame)

        frame_count += 1
        print(f"Processed frame {frame_count}/{total_frames}", end='\r')

    cap.release()
    out.release()
    print("\nProcessing complete. Output saved to:", output_video_path)

regions = [
    (344, 422),
    (525, 348)
]

input_video = "/media/peseyes/output/blur5.mp4"
output_video = "/media/peseyes/output/blur5_test.mp4"
block_size = 128
blur_threshold = 0.7
process_video_with_regions(input_video, output_video, regions, block_size, blur_threshold)

def predict(image, threshold=0.1):
    # Convert PIL Image to numpy array
    region = np.array(image)
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.abs(fshift)

    sorted_magnitude = np.sort(magnitude_spectrum.flatten())
    cutoff_index = int(len(sorted_magnitude) * 0.9)
    cutoff_value = sorted_magnitude[cutoff_index]

    magnitude_spectrum[magnitude_spectrum > cutoff_value] = 0

    high_freq_ratio = np.sum(magnitude_spectrum > 100) / magnitude_spectrum.size

    is_blurry = high_freq_ratio < threshold
    return "blur" if is_blurry else "clear"