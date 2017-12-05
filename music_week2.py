import numpy as np
import pyaudio

RATE = 44100  # sample rate
CHANNEL_NUM = 1  # チャンネル数 今回はモノラルなので1
NOTE_FREQ = {  # 音の周波数
    "d6": 1174.659,
    "c#6": 1108.731,
    "c6": 1046.502,
    "b5": 987.767,
    "a#5": 932.328,
    "a5": 880.000,
    "g#5": 830.609,
    "g5": 783.991,
    "f#5": 739.989,
    "f5": 698.456,
    "e5": 659.255,
    "d#5": 622.245,
    "d5": 587.330,
    "c#5": 554.365,
    "c5": 523.251,
    "b4": 493.883,
    "a#4": 466.164,
    "a4": 440.000,
    "g#4": 415.305,
    "g4": 391.995,
    "f#4": 369.994,
    "f4": 349.228,
    "e4": 329.628,
    "d#4": 311.127,
    "d4": 293.665,
    "c#4": 277.183,
    "c4": 261.626,
    "b3": 246.942,
    "a#3": 233.082,
    "a3": 220.000,
    "rest": 0.00
}
BPM = 120  # 曲のテンポ：一分間に四分音符が何回なるか
VOLUME = 0.1  # 音の大きさ
MUSIC_SCORE = ((1, "b3", "d4"), (2, "b3", "g4"),  # アメイジンググレイスの楽譜
               (1, "d4", "b4"), (1, "d4", "g4"), (2, "d4", "b4"),
               (1, "c4", "a4"),
               (2, "b3", "g4"), (1, "c4", "e4"), (2, "b3", "d4"))


def generate_music_wave(music_score):
    '''
    楽譜の波形を生成して返す関数です．
    返り値は1次元のndarray．

    music_score：楽譜，((音の長さ, "音階1", "音階2",...),...)で渡されるタプル型配列
    '''
    music_wave = [generate_note_wave(note)
                  for note in music_score]
    music_wave = np.concatenate(music_wave, axis=0)
    music_wave *= VOLUME
    return music_wave


def generate_note_wave(score):
    '''
    音符の波形を生成して返す関数です．
    返り値は1次元のndarray

    note:音符，和音も表す，(音の長さ，"音階1","音階2",...)で表されるタプル
    '''
    length = int(score[0] * (60 / BPM) * RATE)  # 音のなる長さ
    factor = np.array([2 * np.pi * NOTE_FREQ[scale] /
                       RATE for scale in score[1:]])
    # 音符の音の波形，二次元ndarray,行毎に和音の構成音の波形を表す
    note = np.sin(factor[:, np.newaxis] * np.arange(length))
    # 平均をとって和音にする
    note = np.sum(note, axis=0)

    return note


def play_sound(wave):
    '''
    音を鳴らす関数です

    wave:波形が記された1次元ndarray配列
    '''
    # pyaudioのストリームを開く
    # streamへ波形を書き込みすると音が出る
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM, rate=RATE,
                     output=True, frames_per_buffer=1024)

    # 鳴らす
    # pyaudioでは波形を量子化ビット数32ビット，
    # 16進数表示でstreamに書き込むことで音を鳴らせる
    stream.write(wave.astype(np.float32).tostring())


def main():
    wave = generate_music_wave(MUSIC_SCORE)
    play_sound(wave)


if __name__ == '__main__':
    main()
