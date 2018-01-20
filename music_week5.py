from collections import deque
import matplotlib.animation as anm
import matplotlib.pyplot as plt
import numpy as np
import pyaudio

#
# 音の取得
#


class AudioInputSample(object):

    # PyAudioとNumpyののフォーマット．同じデータ型にしておく
    FORMAT_PA = pyaudio.paFloat32
    FORMAT_NP = np.float32

    # CHUNK / RATE が UPDATE_M_SECONDを超えると
    # （他の処理の計算量によっては近づくと）
    # 取得しきれないデータが発生してうまくコンスタレーションが
    # 計算できなくなるので注意
    RATE = 44100  # サンプルレート
    CHUNK = 2048  # 一度の読み込みで入ってくる音のサンプル数
    UPDATE_M_SECOND = 5  # 更新頻度
    CHANNELS = 1
    HISTORY = 5  # 何個のデータまで表示しておくか

    def __init__(self, lo_frequency=1000, value_range=6):
        """
        lo_frequency:コンスタレーションを表示する信号の変調周波数
        value_range:コンスタレーションを表示する領域
        """
        # 音声の読み込み用ストリームを開く
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=self.FORMAT_PA, channels=self.CHANNELS, rate=self.RATE,
            input=True, output=False, frames_per_buffer=self.CHUNK)

        self.phase_start_index = 0  # 内部発振器の位相を記録
        self.lo_frequency = lo_frequency  # 内部発振周波数
        # コンスタレーションの表示領域：macbookでやる場合，value_range=6,音量=5でちょうどいい
        self.value_range = value_range

    def audioinput(self):
        '''PyAudioのstreamから波形を読み込んでnp.arrayにして返す'''

        data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        wave = np.frombuffer(data, dtype=self.FORMAT_NP)
        return wave

    def generate_oscillation_signal(self):
        """内部発信信号のcos波，sin波を生成して返すメソッド
        """
        # 発振器のsin,cosの中にぶっこむやつをつくる
        factor = -2 * np.pi * self.lo_frequency / self.RATE
        x = np.arange(self.phase_start_index,
                      self.phase_start_index + self.CHUNK)
        x = x * factor
        # 内部発振信号を生成
        lo_wave_cos = np.cos(x)
        lo_wave_sin = np.sin(x)
        return lo_wave_cos, lo_wave_sin

    def show(self):
        """入力音声のコンスターレーションを表示する
        """
        fig = plt.figure()
        init_array = [0] * self.CHUNK
        # 描画データのプレースホルダ
        im, = plt.plot(init_array, init_array, 'bo')
        # realパート，imgパートのそれぞれの値を保存しておく待ち行列
        queue_real = deque([0] * self.HISTORY, maxlen=self.HISTORY)
        queue_img = deque([0] * self.HISTORY, maxlen=self.HISTORY)

        def update(frame):
            wave = self.audioinput()
            # 発振信号
            lo_wave_cos, lo_wave_sin = self.generate_oscillation_signal()
            # realパート，imgパートを作成
            real = np.dot(lo_wave_cos, wave)
            img = np.dot(lo_wave_sin, wave)

            queue_real.append(real)
            queue_img.append(img)

            self.phase_start_index = (
                self.phase_start_index + self.CHUNK) % self.RATE
            # plotのプレースホルダに値を突っ込む
            im.set_data(queue_real, queue_img)

            # プレースホルダを返すことで高速な描画が可能
            return im

        ani = anm.FuncAnimation(fig, update, interval=self.UPDATE_M_SECOND)
        plt.xlim((-self.value_range, self.value_range))
        plt.ylim((-self.value_range, self.value_range))
        plt.show()


def main():
    ai = AudioInputSample()
    ai.show()


if __name__ == '__main__':
    main()
