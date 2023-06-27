import argparse


class MyParser:

    def __init__(self, name):
        self.name = name

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--path', type=str,
                            help='путь к файлу с кэшем', default='cache')
        parser.add_argument('--server', type=str,
                            help='авторитетный сервер',
                            default='213.180.193.1')
        return parser.parse_args()
