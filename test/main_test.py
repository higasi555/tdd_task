import unittest
from unittest.mock import Mock
import os
import sys
sys.path.append(os.pardir)
from main import gen_data, main, process_image

import numpy as np

class TestVideoProcessing(unittest.TestCase):

    def setUp(self):
        # process_imageをテストするときに必要な各種変数
        self.yolo = Mock()
        self.path2tdata = 'temp/data/images'
        self.frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
        self.num_frame = 0

    # ディレクトリが正しく作られるかどうか
    def test_directory_creation(self):
        test_path = "../temp/test.mp4"
        expected_directory = "../temp/data/images"

        # 作った関数の実行
        result_path = gen_data(test_path)

        self.assertTrue(os.path.exists(expected_directory))
        self.assertEqual(os.path.normpath(result_path), os.path.normpath(expected_directory))

    # パスが間違ってる時、notfoundとなるかどうか
    def test_error_handling_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            # 作った関数の実行
            gen_data("non_existent_path.mp4")

    def test_process_image_basic(self):
        # 仮のトラッキング結果
        self.yolo.track.return_value = Mock(masks=[{'xy': [(10, 10), (100, 100)]}])

        # 作った関数の実行
        process_image(self.yolo, self.path2tdata, self.frame, self.num_frame)

        # 生成された画像ファイルを確認
        self.assertTrue(os.path.exists(f'{self.path2tdata}/frame_0.png'))

    # 一時的に作成したディレクトリを消去
    def tearDown(self):
        try:
            os.rmdir("../temp/data/images")
            os.rmdir("../temp/data")
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()