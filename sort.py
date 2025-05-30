import os
import shutil

def sort_files_by_number(src_folder, dst_folder):
    os.makedirs(dst_folder, exist_ok=True)
    files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]
    def extract_number(filename):
        # Assumes the last underscore-separated part is the float number (before extension)
        base = os.path.splitext(filename)[0]
        num_str = base.split('_')[-1]
        try:
            return float(num_str)
        except ValueError:
            return float('inf')  # Put files without a valid number at the end
    files_sorted = sorted(files, key=extract_number)
    for f in files_sorted:
        shutil.copy(os.path.join(src_folder, f), os.path.join(dst_folder, f))
    print(f"Sorted {len(files_sorted)} files from {src_folder} to {dst_folder}.")

# Example usage:
sort_files_by_number('test_vid_in_progress/results', 'test_vid_in_progress/results_sorted')
