import json

from src.image.table_line import extract_table_line


def extract_table_content(json_content, frame_path):

    rows, cols, grad = extract_table_line(frame_path=frame_path, json_content=json_content)
    init_x = cols[0]
    table_row_data = {}
    for i, row in enumerate(rows):
        if i == len(rows) - 1:
            break

        table_row_data["row_{}".format(i + 1)] = []
        for _json in json_content["textAnnotations"][1:]:
            _json_x = 0.5 * (_json["boundingPoly"]["vertices"][0]["x"] + _json["boundingPoly"]["vertices"][1]["x"])
            _json_y = 0.5 * (_json["boundingPoly"]["vertices"][0]["y"] + _json["boundingPoly"]["vertices"][3]["y"]) \
                      + (_json_x - init_x) * grad
            if row <= _json_y <= rows[i + 1]:
                tmp_dict = {"text": _json["description"], "x": _json_x, "col_add": False}
                table_row_data["row_{}".format(i + 1)].append(tmp_dict)

    table_data = {}
    for row_id in table_row_data.keys():
        table_data[row_id] = {}
        for i, col in enumerate(cols):
            if i == len(cols) - 1:
                break
            table_data[row_id]["col_{}".format(i + 1)] = ""
            for j, cell_data in enumerate(table_row_data[row_id]):
                if col <= cell_data["x"] <= cols[i + 1]:
                    table_data[row_id]["col_{}".format(i + 1)] += cell_data["text"] + " "
                    table_row_data[row_id][j]["col_add"] = True

        for cell_data in table_row_data[row_id]:
            tmp = ""
            if not cell_data["col_add"]:
                tmp += cell_data["text"] + " "
            if tmp != "":
                table_data[row_id]["col_{}".format(len(cols))] = tmp

    return table_data


if __name__ == '__main__':

    with open('') as f:
        json_content_ = json.load(f)
    extract_table_content(json_content=json_content_,
                          frame_path="")
