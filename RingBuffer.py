# coding utf-8


class RingBuffer(object):
    """リングバッファーオブジェクトのクラス
    """

    def __init__(self, capacity):
        """
        capacity:リングバッファの容量，dtype=int
        """
        self.buffer = [None for rize in range(capacity)]  # リングバッファ本体
        self.max_index = capacity - 1  # self.bufferのインデックスの最大値
        self.begin = 0
        self.end = 0

    def append_front(self, item):
        """リングバッファの先頭にitemを追加するメソッド
        item:追加したい要素
        """
        # self.beginとself.endの指し示す位置を変更させる
        self.begin = self.max_index if self.begin == 0 else self.begin - 1
        if self.buffer[self.begin] is not None:
            self.end = self.begin

        self.buffer[self.begin] = item

    def append_back(self, item):
        """リングバッファの先頭にitemを追加するメソッド
        item:追加したい要素
        """


def main():
    rize = RingBuffer(6)
    rize.append_front(8)
    rize.append_front(3)
    rize.append_front(5)
    rize.append_front(5)
    rize.append_front(2)
    rize.append_front(189)
    rize.append_front(98)
    rize.append_front(98)
    rize.append_front(98)
    rize.append_front(98)
    print(rize.buffer)
    print(rize.begin)
    print(rize.end)


if __name__ == '__main__':
    main()
