import numpy as np
import pyaudio

RATE = 44100  # sample rate
CHANNEL_NUM = 1  # チャンネル数 今回はモノラルなので1
SCALE_RATIO = {  # 音の比
    "c": 0,
    "c#": 1,
    "d": 2,
    "d#": 3,
    "e": 4,
    "f": 5,
    "f#": 6,
    "g": 7,
    "g#": 8,
    "a": 9,
    "a#": 10,
    "b": 11
}


VOLUME = 0.1  # 音の大きさ

# リストは時間方向の流れを，タプルは和音を表す
MUSIC_SCORE = [(1, "b3", "d4"), (2, "b3", "g4"),  # アメイジンググレイスの楽譜
               ([(2, "d4")], [(1, "b4"), (1, "g4")]),  # ここネスト多いけど大丈夫ですかね
               (2, "d4", "b4"), (1, "c4", "a4"),
               (2, "b3", "g4"), (1, "c4", "e4"), (2, "b3", "d4")]


def make_note_freq(music_key=[0], low_octave=2, high_octave=6):
    '''
    音名と周波数を対応づける辞書を作成する関数です．
    返り値は{"音名":周波数,...}の辞書型

    music_key:曲の調が記されたタプル，第一引数が# or b，それ以降が半音変わる音が記されている
    low_octave:一番低い音のオクターブ
    high_octave:一番高い音のオクターブ
    '''
    # グローバル変数から音の比の辞書を取ってくる
    scale_ratio = SCALE_RATIO
    # 曲の調を決める，第一インデックスが# or bを，それ以降が半音変わる音名を表す
    if music_key[0] == "#":
        # 音の比を半音高い音のものとする
        half_tone = {scale: scale_ratio[scale] + 1 for scale in music_key[1:]}
        # 結合して音の比の辞書を更新
        scale_ratio.update(half_tone)
    elif music_key[0] == "b":
        # 音の比を半音低い音のものとする
        half_tone = {scale: scale_ratio[scale] - 1 for scale in music_key[1:]}
        # 結合して音の比の辞書を更新
        scale_ratio.update(half_tone)

    # 音名のリストを取得しておく，辞書のkeyの名前をつけるときに使う
    scale_ratio_list = scale_ratio.items()
    # オクターブと音階で二重ループを回してkey=音名，value=周波数の辞書を生成
    # 基準の音はA4=440Hz
    note_freq_dic = {scale + str(octave):
                     440 * 2 ** (octave - 4 + (ratio - scale_ratio['a']) / 12)
                     for octave in range(low_octave, high_octave + 1)
                     for scale, ratio in scale_ratio_list}

    return note_freq_dic


def generate_music_wave(music_score, bpm, note_freq):
    '''
    楽譜の波形を生成して返す関数です．
    返り値は1次元のndarray．

    music_score:楽譜，((音の長さ, "音階1", "音階2",...),...)で渡されるタプル型配列
    bpm:曲のテンポ
    note_freq:音名と周波数の対応表の辞書型
    '''
    music_wave = [generate_note_wave(note, bpm, note_freq)
                  for note in music_score]
    music_wave = np.concatenate(music_wave, axis=0)
    return music_wave


def generate_note_wave(note, bpm, note_freq):
    '''
    音符の波形を生成して返す関数です．
    返り値は1次元のndarray

    note:音符，和音も表す，(音の長さ，"音階1","音階2",...)で表されるタプル
    noteはたまに不快ネスト([(音の長さ1, "音階",...),...],[(音の長さ2, "音階"),...])
    となるのでそれを判断して分岐させる
    bpm:曲のテンポ
    note_freq:音名と周波数の対応表の辞書型
    '''
    # scoreからリストになっているやつらを抽出する
    # リストがあるということは，音の長さが違う和音が存在しているということ
    alt_length_chord = [sharo for sharo in note if isinstance(sharo, list)]
    # もし音の長さが違う和音が存在するなら
    if alt_length_chord:
        # それぞれを楽譜とみなして別々に波形を生成
        alt_length_note = np.array([generate_music_wave(
            rise, bpm, note_freq) for rise in alt_length_chord])
        # 別々に生成された波形を足し合わせて和音の波形ができる
        note_wave = np.sum(alt_length_note, axis=0)
        # できた和音の波形を返して終わり
        return note_wave

    # 和音の長さが全部同じになったら波形を生成
    length = int(note[0] * (60 / bpm) * RATE)  # 音のなる長さ
    factor = np.array([2 * np.pi * note_freq[scale] /
                       RATE for scale in note[1:]])
    # 音符の音の波形，二次元ndarray,行毎に和音の構成音の波形を表す
    note_wave = np.sin(factor[:, np.newaxis] * np.arange(length))
    # 平均をとって和音にする
    note_wave = np.sum(note_wave, axis=0)
    return note_wave


def play_sound(wave):
    '''
    音を鳴らす関数です

    wave:波形が記された1次元ndarray配列
    '''
    # 音量を変える
    wave *= VOLUME
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
    note_freq = make_note_freq()
    wave = generate_music_wave(MUSIC_SCORE, 120, note_freq)
    play_sound(wave)


if __name__ == '__main__':
    main()
