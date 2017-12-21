# coding utf-8


class RingBuffer(object):
    """リングバッファーオブジェクトのクラス
    """

    def __init__(self, capacity):
        """
        capacity:リングバッファの容量，dtype=int
        """
        self.buffer = [0 for rize in range(capacity)]  # リングバッファ本体
        self.capacity = capacity
        self.begin = 0
        self.end = 0


def main():
    rize = RingBuffer(5)
    print(len(rize.buffer))


if __name__ == '__main__':
    main()
