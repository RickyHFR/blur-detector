from evaluate_folder import evaluate_folder

def main():
    folder_path = "NEA_data/blur_night"
    # evaluate_folder(folder_path, expected_label="clear", output_folder_path="annotated_results/"+folder_path)
    evaluate_folder(folder_path, expected_label='blur', output_folder_path="annotated_results/"+folder_path)

if __name__ == "__main__":
    main()
