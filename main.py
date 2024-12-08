import os
import cv2
from ultralytics import YOLO
import numpy as np

# YOLOインスタンスと出力パス、フレームを受け取って、セグメンテーションした画像を出力パスへ生成する関数
def process_image(yolo, path2tdata, frame, num_frame):
    # YOLOv8でセグメンテーション
    results = yolo.track(frame, persist=True)

    frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    green_bg = np.full_like(frame_rgba, (0, 0, 0, 0), dtype=np.uint8)

    # セグメンテーションマスクの抽出
    current_masks = []
    for result in results:
        if result.masks is not None:
            for mask_data in result.masks:
                mask_contours = mask_data.xy[0]
                current_masks.append(mask_contours)

    # 検出されたセグメントを(0, 255, 0, 255)で塗りつぶす
    for contour in current_masks:
        contour_array = np.array(contour, dtype=np.int32)
        cv2.fillPoly(green_bg, [contour_array], (0, 255, 0, 255))

    # デバッグ用
    # cv2.imshow('green_bg', green_bg)

    # green_bgのうち、(0, 255, 0, 255)で塗りつぶされた部分をframe_rgba（つまり元画像）に置き換えて、出力
    output = np.where((green_bg == [0, 255, 0, 255]).all(axis=-1, keepdims=True), frame_rgba, green_bg)
    cv2.imshow('Processed Frame', output)
    file_name = f"frame_{num_frame}.png"
    save_path = os.path.join(path2tdata, file_name)
    cv2.imwrite(save_path, output)

# パスを受け取って、生成したデータをディレクトリ内に生成し、そのパスを返す関数
def gen_data(path2video):
    # パス関連
    # 存在しない場合のエラーハンドル
    if not os.path.isfile(path2video):
        raise FileNotFoundError(f"No video file found at {path2video}")

    base_dir = os.path.dirname(path2video)
    path2tdata = os.path.join(base_dir, "data/images")
    if not os.path.exists(path2tdata):
        os.makedirs(path2tdata)

    # 以下入力パスに存在するビデオの処理
    cap = cv2.VideoCapture(path2video)
    wait_secs = int(1000 / cap.get(cv2.CAP_PROP_FPS))
    yolo = YOLO("yolov8x-seg.pt")

    # 以下フレームごとの処理
    num_frame = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        process_image(yolo, path2tdata, frame, num_frame)

        cv2.waitKey(wait_secs)
        if cv2.waitKey(wait_secs) & 0xFF == ord('q'):
            break
        num_frame += 1

    cap.release()
    cv2.destroyAllWindows()

    return path2tdata

# パスを受け取って、受け取ったデータから（将来的に）3Dデータを返すmain関数
def main(path2video):
    path2tdata = gen_data(path2video)
    # train_nerf(path2tdata)

if __name__ == '__main__':
    main("test.mp4")
