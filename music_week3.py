import numpy as np
import pyaudio
import re

BASE_KEY_FACTOR = {  # ラの音を基準にしたときの半音の隔たり
    'c': -9,
    'd': -7,
    'e': -5,
    'f': -4,
    'g': -2,
    'a': 0,
    'b': 2,
}


class Note(object):
    """一つの音符を表すクラス
    音符の長さと音名をもとに音符の波形を生成する
    """

    def __init__(self, scale, length=1):
        """引数から音符の周波数と長さをセットする．
        scale:単一の音名，dtype=str
        length:音符の長さ(4分音符を1とする)，dtype=float
        """
        self.length = length

        # 単一の音名から周波数を取得する(sample.pyより拝借)
        # 正規表現で音階，変化記号，オクターブ番号を抽出
        match = re.match(r'([a-gA-G])([b#]?)([0-9]+)$', scale)
        key, accidental, octave_str = match.groups()
        octave = int(octave_str)

        factor = BASE_KEY_FACTOR[key]

        if accidental == '#':
            factor += 1
        elif accidental == 'b':
            factor -= 1

        self.freq = 440 * 2**((octave - 4) + factor / 12)

    def generate_wave(self, bpm, rate):
        """音符の波形を生成して返すメソッド
        bpm:曲のテンポ，一分間に4分音符が何回なるか，dtype=int
        rate:サンプルレート,dtype=int

        返り値:波形が記された1次元ndarray
        """
        # 音符の波形を表す配列の長さ
        wave_length = int(self.length * int((60 / bpm) * rate))
        factor = 2 * np.pi * self.freq / rate

        # 音符の音の波形,1次元ndarray
        note_wave = np.sin(factor * np.arange(wave_length))

        return note_wave


def main():
    note = Note('a4')

    print(note.generate_wave(bpm=120, rate=44100))


if __name__ == '__main__':
    main()
