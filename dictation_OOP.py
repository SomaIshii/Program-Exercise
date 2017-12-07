import math
import numpy as np
import pyaudio


class TonePlayer(object):
    """単音を鳴らすクラス"""

    def __init__(self, length=1, rate=44100):
        """length: 音の長さ(s)"""

        self.length = length
        self.rate = rate

    def generate_wave(self, freq_obj):
        """Frequencyオブジェクトを取ってsin波を作る

        freq_obj: Frequencyオブジェクト
        """
        step = (2 * math.pi) * freq_obj.freq / self.rate  # 2πf*(1/rate)
        # sin(2πft)
        wave = np.sin(step * np.arange(int(self.length * self.rate)))
        return wave

    def play(self, freq_obj):
        """Frequencyオブジェクトを取って音を鳴らす

        freq_obj: Frequencyオブジェクト
        """
        wave = self.generate_wave(freq_obj)
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paFloat32, channels=1,
                         rate=self.rate, output=True)
        stream.write(wave.astype(np.float32).tostring())


class Frequency(object):
    """周波数を表すクラス"""

    def __init__(self, scale):
        """scaleは"d2"などの音階を表す文字列．簡単化のため#,♭はなし"""

        key, octave = scale[0], int(scale[1])

        # 音階の処理
        scale_name = 'cxdxefxgxaxb'  # こそぴょんのパクリ
        key_index = scale_name.find(key)
        factor = key_index - 9

        self.freq = 55 * 2 ** ((octave - 1) + factor / 12)


freq_c4 = Frequency("c4")

player = TonePlayer(2)
player.play(freq_c4)  # ド 2秒
player.play(Frequency("d4"))  # レ 2秒
player.length = 3
player.play(Frequency("e4"))  # ミ 3秒
