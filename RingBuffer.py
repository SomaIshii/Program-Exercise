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

    def move_cursor_to_left(self, cursor):
        """begin or endのカーソルを左に動かすメソッド
        cursor:左に動かしたいカーソルの現在指し示しているインデックス
        """
        cursor = self.max_index if cursor == 0 else cursor - 1
        return cursor

    def move_cursor_to_right(self, cursor):
        """begin or endのカーソルを右に動かすメソッド
        cursor:右に動かしたいカーソルの現在指し示しているインデックス
        """
        cursor = 0 if cursor == self.max_index else cursor + 1
        return cursor

    def append_front(self, item):
        """リングバッファの先頭にitemを追加するメソッド
        item:追加したい要素
        """
        # self.beginとself.endの指し示す位置を変更させる
        self.begin = self.move_cursor_to_left(self.begin)
        if self.buffer[self.begin] is not None:
            self.end = self.begin
        self.buffer[self.begin] = item

    def append_back(self, item):
        """リングバッファの先頭にitemを追加するメソッド
        item:追加したい要素
        """
        # self.beginとself.endの指し示す位置を変更させる
        self.end = self.move_cursor_to_right(self.end)
        if self.buffer[self.end - 1] is not None:
            self.begin = self.end
        self.buffer[self.end - 1] = item

    def pop_front(self):
        """先頭のitemを削除してそのitemを返すメソッド
        """
        popping_item = self.buffer[self.begin]
        self.buffer[self.begin] = None
        if popping_item is not None:
            self.begin = self.move_cursor_to_right(self.begin)
        return popping_item

    def pop_back(self):
        """最後尾のitemを削除してそのitemを返すメソッド
        """
        popping_item = self.buffer[self.end - 1]
        self.buffer[self.end - 1] = None
        if popping_item is not None:
            self.end = self.move_cursor_to_left(self.end)
        return popping_item

    def get_list(self):
        """リングバッファのbeginからendまでの配列を表示するリスト
        """
        if self.buffer[self.begin] is None:
            buffer_list = []
        elif self.begin >= self.end:
            begin_to_capacity = self.buffer[self.begin:]
            zero_to_end = self.buffer[:self.end]
            buffer_list = begin_to_capacity + zero_to_end
        else:
            buffer_list = self.buffer[self.begin:self.end]
        print(buffer_list)

    @classmethod
    def do_exercise(cls):
        """課題を実行するクラスメソッド
        """
        ring_buffer = RingBuffer(capacity=5)
        ring_buffer.append_front(1)
        ring_buffer.append_front(2)
        ring_buffer.append_front(3)
        ring_buffer.get_list()
        ring_buffer.append_back(4)
        ring_buffer.append_back(5)
        ring_buffer.append_back(6)
        ring_buffer.append_back(7)
        ring_buffer.get_list()
        ring_buffer.pop_front()
        ring_buffer.pop_front()
        ring_buffer.get_list()
        ring_buffer.pop_back()
        ring_buffer.get_list()
        ring_buffer.append_front(8)
        ring_buffer.get_list()


def main():
    RingBuffer.do_exercise()


if __name__ == '__main__':
    main()
