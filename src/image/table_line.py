import cv2
import numpy as np

from settings import IMAGE_MARGIN, LINE_SPACING


def extract_table_line(frame_path, json_content):

    left = json_content["textAnnotations"][0]["boundingPoly"]["vertices"][0]["x"]
    right = json_content["textAnnotations"][0]["boundingPoly"]["vertices"][1]["x"]
    top = json_content["textAnnotations"][0]["boundingPoly"]["vertices"][0]["y"]
    bottom = json_content["textAnnotations"][0]["boundingPoly"]["vertices"][3]["y"]

    frame = cv2.imread(frame_path)
    for _json in json_content["textAnnotations"][1:]:
        t_left = _json["boundingPoly"]["vertices"][0]["x"]
        t_top = _json["boundingPoly"]["vertices"][0]["y"]
        t_right = _json["boundingPoly"]["vertices"][1]["x"]
        t_bottom = _json["boundingPoly"]["vertices"][2]["y"]
        frame[t_top:t_bottom, t_left:t_right] = 255

    # cv2.imshow("origin frame", cv2.resize(frame, (800, 600)))
    # cv2.waitKey()
    if top - IMAGE_MARGIN < 0:
        f_top = 0
    else:
        f_top = top - IMAGE_MARGIN
    if left - IMAGE_MARGIN < 0:
        f_left = 0
    else:
        f_left = left - IMAGE_MARGIN
    if bottom + IMAGE_MARGIN > frame.shape[0]:
        f_bottom = frame.shape[0]
    else:
        f_bottom = bottom + IMAGE_MARGIN
    if right + IMAGE_MARGIN > frame.shape[1]:
        f_right = frame.shape[1]
    else:
        f_right = right + IMAGE_MARGIN
    crop_frame = frame[f_top:f_bottom, f_left:f_right]
    gray_frame = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray frame", cv2.resize(gray_frame, (800, 600)))
    _, thresh_frame = cv2.threshold(gray_frame, 200, 255, cv2.THRESH_BINARY)
    dilate_frame = cv2.erode(thresh_frame, np.ones((2, 2), np.uint8), iterations=2)
    # dilate_frame = cv2.morphologyEx(gray_frame, cv2.MORPH_CLOSE, np.ones((4, 4), np.uint8), iterations=1)
    # cv2.imshow("dilate frame", cv2.resize(dilate_frame, (800, 600)))
    # cv2.imshow("dilate frame", thresh_frame)
    # cv2.waitKey()
    dilate_frame_inv = cv2.bitwise_not(dilate_frame)
    min_line_length = crop_frame.shape[0] * 0.2
    max_line_gap = 20
    lines = cv2.HoughLinesP(dilate_frame_inv, 1, np.pi / 180, 100, minLineLength=min_line_length,
                            maxLineGap=max_line_gap)
    row_lines = []
    col_lines = []
    row_grads = 0
    grad_cnt = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(x1 - x2) > abs(y1 - y2):
            grad = (y1 - y2) / abs(x1 - x2)
            if grad > 0.1:
                continue
            row_lines.append([y1, y2])
            row_grads += grad
            grad_cnt += 1
        else:
            col_lines.append([int(0.5 * (x1 + x2))])

        cv2.line(crop_frame, (x1, y1), (x2, y2), (0, 0, 255), 10)

    row_grad = row_grads / grad_cnt

    # cv2.imshow("line frame", cv2.resize(crop_frame, (800, 600)))
    # cv2.waitKey()
    # cv2.imwrite('tmp.jpg', crop_frame)
    sorted_row_lines = sort_lines(lines=row_lines, axis=1)
    sorted_col_lines = sort_lines(lines=col_lines, axis=0)

    rows = []
    for row_line in sorted_row_lines:
        row_min = max(row_line, key=lambda i: i[0])
        rows.append(row_min[0] + top - IMAGE_MARGIN)
    cols = []
    for col_line in sorted_col_lines:
        col = np.average(col_line)
        cols.append(col + left - IMAGE_MARGIN)

    return rows, cols, row_grad


def sort_lines(lines, axis):

    sorted_lines = sorted(lines, key=lambda k: k[axis])
    sorted_values = []
    init_value = sorted_lines[0][axis]
    tmp_line_value = []

    for line in sorted_lines:
        if abs(init_value - line[axis]) < LINE_SPACING:
            tmp_line_value.append(line)

        else:
            sorted_values.append(tmp_line_value[:])
            tmp_line_value.clear()
            tmp_line_value.append(line)
            init_value = line[axis]

    sorted_values.append(tmp_line_value[:])

    return sorted_values


if __name__ == '__main__':
    extract_table_line(frame_path="", json_content="")
