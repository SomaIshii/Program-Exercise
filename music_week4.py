import numpy as np
import pyaudio
import re


class Note(object):
    """一つの音符を表すクラス
    音符の長さと音名をもとに音符の波形を生成する
    """
    base_key_factor = {  # ラの音を基準にしたときの半音の隔たり
        'c': -9,
        'd': -7,
        'e': -5,
        'f': -4,
        'g': -2,
        'a': 0,
        'b': 2,
    }

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

        factor = self.__class__.base_key_factor[key]

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


class SimpleMusic(object):
    """簡単な音楽を鳴らすクラス"""

    volume = 0.1  # 音量
    channel_num = 1  # チャンネル数，今回はモノラルなので1

    def __init__(self, bpm, rate=44100):
        """
        bpm:曲のテンポ，一分間に4分音符が何回なるか，dtype=int
        rate:サンプルレート，dtype=int
        """
        self.bpm = bpm
        self.rate = rate
        self.note_list = []

    def append_note(self, note_obj):
        """Noteオブジェクトのインスタンスをリストに追加していくメソッド
        note_obj:Noteオブジェクト
        """
        self.note_list.append(note_obj)

    def play(self):
        """self.noteの波形を順番に生成，結合し，音を鳴らすメソッド"""
        # noteオブジェクトのメソッドで音符の波形を生成し，順番に取得
        music_wave = [note.generate_wave(self.bpm, self.rate)
                      for note in self.note_list]
        music_wave = np.concatenate(music_wave, axis=0)

        # 音量を変える
        music_wave *= self.__class__.volume

        # pyaudioのストリームを開く
        # streamへ波形を書き込みすると音が出る
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paFloat32,
                         channels=self.__class__.channel_num,
                         rate=self.rate, output=True, frames_per_buffer=1024)

        # 鳴らす
        # pyaudioでは波形を量子化ビット数32ビット，
        # 16進数表示でstreamに書き込むことで音を鳴らせる
        stream.write(music_wave.astype(np.float32).tostring())

    @classmethod
    def play_cdefgabc(cls, bpm):
        """ドレミファソラシドを鳴らすメソッド
        """
        note_list = [Note("c4"), Note("d4"), Note("e4"), Note("f4"),
                     Note("g4"), Note("a4"), Note("b4"), Note("c5")]
        cdefgabc = cls(bpm)
        for note in note_list:
            cdefgabc.append_note(note)

        cdefgabc.play()

    @classmethod
    def play_when_you_wish_upon_a_star(cls, bpm):
        """「星に願いを」を演奏するメソッド
        """
        note_list = [Note("g4"), Note("g5"), Note("f5"), Note("e5"),
                     Note("c#5"), Note("d5"), Note("a5", length=2),
                     Note("b4"), Note("b5"), Note("a5"), Note("g5"),
                     Note("f#5"), Note("g5"), Note("c6", length=2),
                     Note("d6"), Note("c6"), Note("b5"), Note("a5"),
                     Note("g5"), Note("f5"), Note("e5"), Note("d5"),
                     Note("c6", length=2), Note("c6", length=2),
                     Note("d6", length=4)]
        when_you_wish_upon_a_star = cls(bpm)
        for note in note_list:
            when_you_wish_upon_a_star.append_note(note)

        when_you_wish_upon_a_star.play()


def main():
    # ドレミファソラシドを鳴らす
    SimpleMusic.play_cdefgabc(bpm=100)
    # 試しに音量変えてみる
    SimpleMusic.volume = 0.5
    # 「星に願いを」を鳴らす
    SimpleMusic.play_when_you_wish_upon_a_star(bpm=500)


if __name__ == '__main__':
    main()
