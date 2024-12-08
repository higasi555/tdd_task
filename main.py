import os
import cv2

# YOLOインスタンスと出力パス、フレームを受け取って、セグメンテーションした画像を出力パスへ生成する関数
def process_image(yolo, path2tdata, frame, num_frame):
    None

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
    # 処理を後で追加

    return path2tdata

# パスを受け取って、受け取ったデータから（将来的に）3Dデータを返すmain関数
def main(path2video):
    path2tdata = gen_data(path2video)
    # train_nerf(path2tdata)

if __name__ == '__main__':
    main("test.mp4")
