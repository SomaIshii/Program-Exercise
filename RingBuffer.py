# coding utf-8


class RingBuffer(object):
    """リングバッファーオブジェクトのクラス
    """

    def __init__(self, capacity):
        """
        capacity:リングバッファの容量，dtype=int
        """
        self.buffer = [0 for rize in range(capacity)]  # リングバッファ本体
        self.max_index = capacity - 1  # self.bufferのインデックスの最大値
        self.begin = 0
        self.end = 0

    def append_front(self, item):
        """リングバッファの先頭にitemを追加するメソッド
        item:追加したい要素
        """
        # beginとendの指し示す位置を変更する
        self.begin = self.max_index if self.begin == 0 else self.begin - 1
        self.end = self.begin if self.end < self.begin else self.end

        self.buffer[self.begin] = item


def main():
    rize = RingBuffer(5)
    rize.append_front(9)
    rize.append_front(1)
    rize.append_front(2)
    rize.append_front(7)
    rize.append_front(3)
    rize.append_front(4)
    print(rize.buffer)
    print(rize.begin)
    print(rize.end)


if __name__ == '__main__':
    main()
