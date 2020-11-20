from src.ocr.ocr_text import process_ocr_text
from utils.folder_file_manager import save_file
from settings import RESULT_FILE_PATH, INPUT_IMAGE_PATH


if __name__ == '__main__':

    result = process_ocr_text(frame_path=INPUT_IMAGE_PATH)
    save_file(content=result, filename=RESULT_FILE_PATH, method='w')
    print("Successfully saved in {}".format(RESULT_FILE_PATH))
