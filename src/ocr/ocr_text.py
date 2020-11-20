import json
import os

from src.table.content import extract_table_content
from utils.folder_file_manager import save_file
from utils.google_api import GoogleVisionAPI
from settings import LOCAL, CUR_DIR

google_ocr = GoogleVisionAPI()


def process_ocr_text(frame_path):

    image_ocr_json = google_ocr.detect_text(img_path=frame_path)

    if LOCAL:
        json_file_path = os.path.join(CUR_DIR, 'temp', "temp.json")
        save_file(filename=json_file_path, content=json.dumps(image_ocr_json), method="w")

    content = extract_table_content(json_content=image_ocr_json, frame_path=frame_path)

    table_text = ""
    for row_id in content.keys():
        for col_id in content[row_id].keys():
            table_text += "'" + content[row_id][col_id] + "'" + ","
        table_text += "\n"

    return table_text


if __name__ == '__main__':

    process_ocr_text(frame_path="")
