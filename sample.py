#!/usr/bin/env python3
"""
音階から周波数を取得するプログラムのサンプル
"""

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


def freq_from_scale(scale):
    """単一のscaleに対する周波数を返す

    例： "c#5" -> 554.365, "a5"-> 880.000
    """

    # 正規表現で音階，変化記号，オクターブ番号を抽出
    match = re.match(r'([a-gA-G])([b#]?)([0-9]+)$', scale)
    key, accidental, octave_str = match.groups()
    octave = int(octave_str)

    factor = BASE_KEY_FACTOR[key]

    if accidental == '#':
        factor += 1
    elif accidental == 'b':
        factor -= 1

    freq = 440 * 2**((octave - 4) + factor / 12)
    return freq


print(freq_from_scale("a4"))
