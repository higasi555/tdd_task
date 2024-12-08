import unittest
import os
import sys
sys.path.append(os.pardir)
from main import gen_data, main

class TestVideoProcessing(unittest.TestCase):

    # ディレクトリが正しく作られるかどうか
    def test_directory_creation(self):
        test_path = "temp/test.mp4"
        expected_directory = "temp/data/images"

        # 作った関数の実行
        result_path = gen_data(test_path)

        self.assertTrue(os.path.exists(expected_directory))
        self.assertEqual(result_path, expected_directory)

    # パスが間違ってる時、notfoundとなるかどうか
    def test_error_handling_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            # 作った関数の実行
            gen_data("non_existent_path.mp4")

    # 一時的に作成したディレクトリを消去
    def tearDown(self):
        try:
            os.rmdir("temp/data/images")
            os.rmdir("temp/data")
            os.rmdir("temp")
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()