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
        # self.beginとself.endの指し示す位置を変更させる
        self.end = 0 if self.end == self.max_index else self.end + 1
        if self.buffer[self.end - 1] is not None:
            self.begin = self.end

        self.buffer[self.end - 1] = item

    def get_list(self):
        """リングバッファのbeginからendまでの配列を表示するリスト
        """
        if self.buffer[self.begin] is None:
            print([])
            return

        if self.begin >= self.end:
            begin_to_capacity = self.buffer[self.begin:]
            zero_to_end = self.buffer[:self.end]
            buffer_list = begin_to_capacity + zero_to_end
            print(buffer_list)
        else:
            print(self.buffer[self.begin:self.end])


def main():
    rize = RingBuffer(6)
    rize.append_back(9)
    rize.append_back(23)
    rize.append_back(98)
    rize.append_front(78)
    rize.append_front(89)
    rize.append_back(33)
    rize.append_back(98)
    rize.append_front(3)
    rize.append_front(3)
    rize.append_front(3)
    rize.append_front(3)
    rize.get_list()


if __name__ == '__main__':
    main()
