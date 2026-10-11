#!/usr/bin/env python3
"""
CipherVault — Cryptographic Toolkit v3.0
PySide6 Desktop Application
"""

import sys, math, random, re, time, base64
from collections import Counter

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLabel, QPushButton, QComboBox, QSlider, QLineEdit,
    QTabWidget, QScrollArea, QGroupBox, QCheckBox, QSplitter,
    QListWidget, QListWidgetItem, QSizePolicy, QFrame, QSpinBox,
    QToolBar, QStatusBar, QFileDialog, QMessageBox, QToolTip
)
from PySide6.QtCore import Qt, QSize, QPoint, QTimer, QMimeData, Signal
from PySide6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush, QIcon, QKeySequence,
    QShortcut, QDragEnterEvent, QDropEvent, QPainterPath, QLinearGradient
)

# ═══════════════════════════════════════════════════════════
# CIPHER IMPLEMENTATIONS
# ═══════════════════════════════════════════════════════════

ENGLISH_FREQ = [
    0.0817,0.0149,0.0278,0.0425,0.127,0.0223,0.0202,0.0609,
    0.0697,0.0015,0.0077,0.0403,0.0241,0.0675,0.0751,0.0193,
    0.001,0.0599,0.0633,0.0906,0.0276,0.0098,0.0236,0.0015,0.0197,0.0007
]

MORSE_MAP = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....',
    'I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.',
    'Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-',
    'Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---','3':'...--','4':'....-',
    '5':'.....','6':'-....','7':'--...','8':'---..','9':'----.', '.':'.-.-.-',',':'--..--',
    '?':'..--..','!':'-.-.--','/':'-..-.','(':'-.--.',')':'-.--.-','&':'.-...',
    ':':'---...',';':'-.-.-.','=':'-...-','+':'.-.-.','-':'-....-','_':'..--.',
    '"':'.-..-.','@':'.--.-.',"'":'.----.'
}
REV_MORSE = {v: k for k, v in MORSE_MAP.items()}

def gcd(a, b):
    while b: a, b = b, a % b
    return a

def mod_inverse(a, m):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1: return x
    return 1

def shift_alpha(n):
    return ''.join(chr((i + n) % 26 + 65) for i in range(26))

def build_pf_grid(kw):
    kw = re.sub(r'[^A-Z]', '', kw.upper()).replace('J', 'I')
    seen, chars = set(), []
    for c in kw:
        if c not in seen: seen.add(c); chars.append(c)
    for i in range(65, 91):
        c = chr(i)
        if c != 'J' and c not in seen: seen.add(c); chars.append(c)
    return [chars[r*5:(r+1)*5] for r in range(5)]

def find_pf(grid, ch):
    c = 'I' if ch == 'J' else ch
    for r in range(5):
        for col in range(5):
            if grid[r][col] == c: return r, col
    return 0, 0

def prep_pf(text):
    cl = re.sub(r'[^A-Z]', '', text.upper()).replace('J', 'I')
    res, i = [], 0
    while i < len(cl):
        a = cl[i]
        b = cl[i+1] if (i+1 < len(cl) and cl[i+1] != a) else 'X'
        res.append(a + b)
        i += 2 if (i+1 < len(cl) and cl[i+1] != a) else 1
    s = ''.join(res)
    return s + 'X' if len(s) % 2 else s

def _caesar(text, s, encode=True):
    r = []
    for c in text:
        if c.isalpha():
            b = 65 if c.isupper() else 97
            d = s if encode else -s
            r.append(chr((ord(c) - b + d + 26) % 26 + b))
        else: r.append(c)
    return ''.join(r)

def _vigenere(text, key, encode=True):
    key = re.sub(r'[^A-Z]', '', key.upper())
    if not key: return text
    r, ki = [], 0
    for c in text:
        if c.isalpha():
            b = 65 if c.isupper() else 97
            s = ord(key[ki % len(key)]) - 65
            ki += 1
            d = s if encode else -s
            r.append(chr((ord(c) - b + d + 26) % 26 + b))
        else: r.append(c)
    return ''.join(r)

def _playfair(text, kw, encode=True):
    grid = build_pf_grid(kw)
    cl = re.sub(r'[^A-Z]', '', text.upper())
    if encode: cl = prep_pf(text)
    r, d = [], 1 if encode else -1
    for i in range(0, len(cl) - 1, 2):
        r1, c1 = find_pf(grid, cl[i]); r2, c2 = find_pf(grid, cl[i+1])
        if r1 == r2:
            r += [grid[r1][(c1+d)%5], grid[r2][(c2+d)%5]]
        elif c1 == c2:
            r += [grid[(r1+d)%5][c1], grid[(r2+d)%5][c2]]
        else:
            r += [grid[r1][c2], grid[r2][c1]]
    return ''.join(r)

def _railfence(text, n, encode=True):
    if n < 2: return text
    if encode:
        rails = [[] for _ in range(n)]
        r, d = 0, 1
        for c in text:
            rails[r].append(c)
            if r == 0: d = 1
            elif r == n - 1: d = -1
            r += d
        return ''.join(c for rail in rails for c in rail)
    else:
        ln = len(text)
        pat, r, d = [], 0, 1
        for i in range(ln):
            pat.append(r)
            if r == 0: d = 1
            elif r == n - 1: d = -1
            r += d
        counts = [0] * n
        for p in pat: counts[p] += 1
        rails, idx = [], 0
        for i in range(n):
            rails.append(list(text[idx:idx+counts[i]])); idx += counts[i]
        indices = [0] * n
        return ''.join(rails[p][indices[p]] or '' for p in pat)  # safe access

def _affine(text, a, b, encode=True):
    if gcd(a, 26) != 1: a = 5
    if encode:
        return ''.join(chr((a*(ord(c)-65)+b)%26+65) if c.isalpha() and c.isupper() else
                       chr((a*(ord(c)-97)+b)%26+97) if c.isalpha() else c for c in text)
    else:
        ai = mod_inverse(a, 26)
        return ''.join(chr((ai*((ord(c)-65-b+260)%26))%26+65) if c.isalpha() and c.isupper() else
                       chr((ai*((ord(c)-97-b+260)%26))%26+97) if c.isalpha() else c for c in text)

_sub_key = _sub_inv = None
def get_sub():
    global _sub_key, _sub_inv
    if _sub_key is None:
        a = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'); sh = a[:]; random.shuffle(sh)
        _sub_key = ''.join(sh); _sub_inv = ''.join(a[sh.index(c)] for c in a)
    return _sub_key, _sub_inv

def _substitution(text, encode=True):
    k, inv = get_sub()
    key = k if encode else inv
    return ''.join((key[ord(c.upper())-65] if c.isupper() else key[ord(c.upper())-65].lower())
                   if c.isalpha() else c for c in text)

def _morse_enc(text):
    return ' '.join(MORSE_MAP.get(c, c) if c != ' ' else '/' for c in text.upper())
def _morse_dec(text):
    return ' '.join(REV_MORSE.get(t, t) if t != '/' else ' ' for t in text.split(' '))

def _b64_enc(text):
    try: return base64.b64encode(text.encode()).decode()
    except: return '[Error]'
def _b64_dec(text):
    try: return base64.b64decode(text.strip()).decode()
    except: return '[Invalid Base64]'

# ═══════════════════════════════════════════════════════════
# CIPHER REGISTRY
# ═══════════════════════════════════════════════════════════

CIPHERS = {
    'caesar': {
        'name': 'Caesar', 'full': 'Caesar Cipher', 'tag': 'Classical', 'strength': 'weak',
        'desc': 'Shift each letter by a fixed number of positions.',
        'info': 'Replaces each letter with the letter a fixed number of positions down the alphabet.\nShift 3: A→D, B→E, Z→C. Only 25 keys — trivially breakable.',
        'params': [{'id':'shift','label':'Shift Value','type':'slider','min':1,'max':25,'default':3}],
        'encode': lambda t,p: _caesar(t, int(p.get('shift',3)), True),
        'decode': lambda t,p: _caesar(t, int(p.get('shift',3)), False),
        'alphabet': lambda p: ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', shift_alpha(int(p.get('shift',3)))),
        'brute': lambda t: [(f'Shift {i+1}', _caesar(t, i+1, False)) for i in range(25)],
    },
    'rot13': {
        'name': 'ROT13', 'full': 'ROT13 Cipher', 'tag': 'Classical', 'strength': 'weak',
        'desc': 'Fixed 13-position rotation. Self-inverse.',
        'info': 'Encoding and decoding are the same operation.\nA↔N, B↔O. No real security.',
        'params': [],
        'encode': lambda t,p: _caesar(t, 13, True),
        'decode': lambda t,p: _caesar(t, 13, False),
        'alphabet': lambda p: ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', shift_alpha(13)),
    },
    'atbash': {
        'name': 'Atbash', 'full': 'Atbash Cipher', 'tag': 'Classical', 'strength': 'weak',
        'desc': 'Mirror the alphabet: A→Z, B→Y. Self-inverse.',
        'info': 'First letter to last: A↔Z, B↔Y, M↔N.\nEncoding and decoding are identical.',
        'params': [],
        'encode': lambda t,p: _caesar(t, 0, True).swapcase() or  # fallback
                 ''.join(chr(65+25-(ord(c)-65)) if c.isupper() and c.isalpha() else
                         chr(97+25-(ord(c)-97)) if c.islower() else c for c in t),
        'decode': lambda t,p: CIPHERS['atbash']['encode'](t, p),
        'alphabet': lambda p: ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'ZYXWVUTSRQPONMLKJIHGFEDCBA'),
    },
    'vigenere': {
        'name': 'Vigenere', 'full': 'Vigenere Cipher', 'tag': 'Classical', 'strength': 'medium',
        'desc': 'Polyalphabetic key cipher.',
        'info': 'Each keyword letter determines the shift.\nCalled "le chiffre indechiffrable" for 300 years.',
        'params': [{'id':'keyword','label':'Keyword','type':'text','default':'SECRET'}],
        'encode': lambda t,p: _vigenere(t, p.get('keyword','SECRET'), True),
        'decode': lambda t,p: _vigenere(t, p.get('keyword','SECRET'), False),
    },
    'playfair': {
        'name': 'Playfair', 'full': 'Playfair Cipher', 'tag': 'Classical', 'strength': 'medium',
        'desc': '5x5 digraph substitution.',
        'info': '5x5 grid from keyword. I/J share a cell.\nSame row→shift right, Same col→shift down, else→opposite corners.',
        'params': [{'id':'keyword','label':'Keyword','type':'text','default':'MONARCHY'}],
        'encode': lambda t,p: _playfair(t, p.get('keyword','MONARCHY'), True),
        'decode': lambda t,p: _playfair(t, p.get('keyword','MONARCHY'), False),
    },
    'railfence': {
        'name': 'Rail Fence', 'full': 'Rail Fence Cipher', 'tag': 'Classical', 'strength': 'weak',
        'desc': 'Zigzag transposition.',
        'info': 'Message written diagonally across N rails, then each rail read left-to-right.',
        'params': [{'id':'rails','label':'Rails','type':'slider','min':2,'max':10,'default':3}],
        'encode': lambda t,p: _railfence(t, int(p.get('rails',3)), True),
        'decode': lambda t,p: _railfence(t, int(p.get('rails',3)), False),
    },
    'substitution': {
        'name': 'Random Sub', 'full': 'Random Substitution', 'tag': 'Substitution', 'strength': 'medium',
        'desc': 'Random alphabet permutation.',
        'info': '26! possible keys (~4×10²⁶). Frequency analysis can break it.',
        'params': [], 'has_gen_key': True,
        'encode': lambda t,p: _substitution(t, True),
        'decode': lambda t,p: _substitution(t, False),
        'alphabet': lambda p: ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', get_sub()[0]),
    },
    'affine': {
        'name': 'Affine', 'full': 'Affine Cipher', 'tag': 'Substitution', 'strength': 'medium',
        'desc': 'Mathematical (ax+b) mod 26.',
        'info': 'E(x) = (ax + b) mod 26\nAllowed a: 1,3,5,7,9,11,15,17,19,21,23,25',
        'params': [
            {'id':'a','label':'Multiplier (a)','type':'slider','min':1,'max':25,'default':5,
             'filter': lambda x: gcd(x,26)==1},
            {'id':'b','label':'Shift (b)','type':'slider','min':0,'max':25,'default':8},
        ],
        'encode': lambda t,p: _affine(t, int(p.get('a',5)), int(p.get('b',8)), True),
        'decode': lambda t,p: _affine(t, int(p.get('a',5)), int(p.get('b',8)), False),
        'alphabet': lambda p: ('ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            ''.join(chr((int(p.get('a',5))*i+int(p.get('b',8)))%26+65) for i in range(26))),
        'brute': lambda t: [(f'a={a},b={b}', _affine(t,a,b,False))
                            for a in range(1,26) if gcd(a,26)==1 for b in range(26)][:80],
    },
    'morse': {
        'name': 'Morse', 'full': 'Morse Code', 'tag': 'Encoding', 'strength': 'none',
        'desc': 'Dots and dashes encoding.',
        'info': 'Each character → dots (.) and dashes (-).\nLetters separated by space, words by /',
        'params': [],
        'encode': lambda t,p: _morse_enc(t),
        'decode': lambda t,p: _morse_dec(t),
    },
    'base64': {
        'name': 'Base64', 'full': 'Base64 Encoding', 'tag': 'Encoding', 'strength': 'none',
        'desc': '6-bit group encoding.',
        'info': 'Every 3 bytes → 4 ASCII chars from A-Z a-z 0-9 + /\nEncoding, not encryption — zero security.',
        'params': [],
        'encode': lambda t,p: _b64_enc(t),
        'decode': lambda t,p: _b64_dec(t),
    },
}

CIPHER_GROUPS = {
    'Classical': ['caesar','rot13','atbash','vigenere','playfair','railfence'],
    'Substitution': ['substitution','affine'],
    'Encoding': ['morse','base64'],
}

# ═══════════════════════════════════════════════════════════
# STYLESHEET
# ═══════════════════════════════════════════════════════════

DARK_STYLE = """
QMainWindow, QWidget { background-color: #08080d; color: #e8e6e3; }
QToolTip { background: #1a1a28; color: #e8e6e3; border: 1px solid #32324a; padding: 4px 8px; font-size: 12px; }
QScrollBar:vertical {
    background: transparent; width: 6px; margin: 0;
}
QScrollBar::handle:vertical { background: #32324a; border-radius: 3px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #6b6b80; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: transparent; height: 6px; margin: 0; }
QScrollBar::handle:horizontal { background: #32324a; border-radius: 3px; min-width: 30px; }
QScrollBar::handle:horizontal:hover { background: #6b6b80; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

QTextEdit {
    background-color: #14141e; color: #e8e6e3; border: 1px solid #262638;
    border-radius: 8px; padding: 10px; font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 13px; line-height: 1.6; selection-background-color: rgba(224,165,38,0.25);
}
QTextEdit:focus { border-color: #e0a526; }

QLineEdit {
    background-color: #0a0a0f; color: #e8e6e3; border: 1px solid #262638;
    border-radius: 6px; padding: 7px 12px; font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 13px;
}
QLineEdit:focus { border-color: #e0a526; }

QPushButton {
    background-color: #14141e; color: #e8e6e3; border: 1px solid #262638;
    border-radius: 7px; padding: 8px 16px; font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
    font-size: 12px; font-weight: 500;
}
QPushButton:hover { background-color: #20202f; border-color: #32324a; }
QPushButton:pressed { background-color: #0a0a0f; }
QPushButton:disabled { color: #32324a; border-color: #1a1a28; }

QPushButton#primaryBtn {
    background-color: #e0a526; color: #0a0a0f; border-color: #e0a526; font-weight: 600;
}
QPushButton#primaryBtn:hover { background-color: #f0b830; }
QPushButton#primaryBtn:pressed { background-color: #c89020; }

QPushButton#dangerBtn { color: #f87171; border-color: rgba(248,113,113,0.2); }
QPushButton#dangerBtn:hover { background-color: rgba(248,113,113,0.08); }

QPushButton#infoBtn { color: #60a5fa; border-color: rgba(96,165,250,0.2); }
QPushButton#infoBtn:hover { background-color: rgba(96,165,250,0.06); }

QComboBox {
    background-color: #14141e; color: #e8e6e3; border: 1px solid #262638;
    border-radius: 6px; padding: 6px 10px; font-size: 12px;
    font-family: 'Space Grotesk', 'Segoe UI', sans-serif; min-width: 60px;
}
QComboBox:hover { border-color: #32324a; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow { image: none; border-left: 5px solid transparent;
    border-right: 5px solid transparent; border-top: 5px solid #6b6b80; margin-right: 8px; }
QComboBox QAbstractItemView {
    background-color: #14141e; color: #e8e6e3; border: 1px solid #262638;
    selection-background-color: rgba(224,165,38,0.15); selection-color: #e0a526;
    outline: none;
}

QSlider::groove:horizontal {
    height: 5px; background: #262638; border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #e0a526; width: 16px; height: 16px; margin: -6px 0;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover { background: #f0b830; }
QSlider::sub-page:horizontal { background: rgba(224,165,38,0.3); border-radius: 2px; }

QCheckBox { spacing: 6px; font-size: 12px; color: #6b6b80; }
QCheckBox::indicator { width: 16px; height: 16px; border-radius: 4px;
    border: 1px solid #32324a; background: #14141e; }
QCheckBox::indicator:checked { background: #e0a526; border-color: #e0a526; }

QTabWidget::pane { border: none; }
QTabBar::tab {
    background: transparent; color: #6b6b80; border: none;
    border-bottom: 2px solid transparent; padding: 10px 16px;
    font-size: 12px; font-family: 'Space Grotesk', 'Segoe UI', sans-serif; font-weight: 500;
}
QTabBar::tab:hover { color: #c4c2bf; }
QTabBar::tab:selected { color: #e0a526; border-bottom-color: #e0a526; }

QListWidget {
    background-color: transparent; border: none; outline: none;
    font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
}
QListWidget::item { padding: 8px 12px; border-radius: 7px; margin: 1px 0; }
QListWidget::item:hover { background-color: #20202f; }
QListWidget::item:selected { background-color: rgba(224,165,38,0.1); color: #e0a526; }

QGroupBox {
    background-color: #14141e; border: 1px solid #262638;
    border-radius: 10px; margin-top: 12px; padding: 16px 14px 14px;
    font-size: 12px; font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin; left: 14px; padding: 0 8px;
    color: #6b6b80; text-transform: uppercase; letter-spacing: 1px; font-size: 10px;
}

QLabel#headerLabel { font-size: 22px; font-weight: 700; }
QLabel#subLabel { font-size: 13px; color: #6b6b80; line-height: 1.5; }
QLabel#tagLabel {
    font-family: 'JetBrains Mono', monospace; font-size: 10px;
    padding: 2px 8px; border-radius: 12px; background: rgba(224,165,38,0.1); color: #e0a526;
}
QLabel#weakLabel { font-size: 10px; padding: 2px 8px; border-radius: 12px;
    background: rgba(248,113,113,0.1); color: #f87171; }
QLabel#mediumLabel { font-size: 10px; padding: 2px 8px; border-radius: 12px;
    background: rgba(251,191,36,0.1); color: #fbbf24; }
QLabel#noneLabel { font-size: 10px; padding: 2px 8px; border-radius: 12px;
    background: rgba(107,107,128,0.1); color: #6b6b80; }
QLabel#statLabel {
    font-family: 'JetBrains Mono', monospace; font-size: 10px;
    padding: 3px 10px; background: #14141e; border: 1px solid #262638;
    border-radius: 14px; color: #6b6b80;
}
QLabel#statVal { color: #c4c2bf; font-weight: 500; }

QFrame#separator { background-color: #262638; max-height: 1px; }
QFrame#sidebarSep { background-color: #262638; max-width: 1px; }

QStatusBar { background: #0e0e16; color: #6b6b80; font-size: 11px;
    border-top: 1px solid #1a1a28; padding: 2px 10px; }
"""

MONO_FONT = QFont('JetBrains Mono', 13)
MONO_FONT.setStyleHint(QFont.StyleHint.Monospace)
UI_FONT = QFont('Space Grotesk', 12)
SMALL_FONT = QFont('Space Grotesk', 10)
SMALL_MONO = QFont('JetBrains Mono', 10)
SMALL_MONO.setStyleHint(QFont.StyleHint.Monospace)
HEADER_FONT = QFont('Space Grotesk', 22, QFont.Weight.Bold)

# ═══════════════════════════════════════════════════════════
# FREQUENCY CHART WIDGET
# ═══════════════════════════════════════════════════════════

class FrequencyChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.in_freq = [0.0] * 26
        self.out_freq = [0.0] * 26
        self.setMinimumHeight(180)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_data(self, input_text, output_text):
        self.in_freq = self._calc(input_text)
        self.out_freq = self._calc(output_text)
        self.update()

    @staticmethod
    def _calc(text):
        counts = [0] * 26
        total = 0
        for c in text.upper():
            i = ord(c) - 65
            if 0 <= i < 26:
                counts[i] += 1
                total += 1
        return [c / total if total else 0 for c in counts]

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        p.fillRect(self.rect(), QColor('#14141e'))

        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        gap = (w - 40) / 26
        bar_w = max(1, gap - 2)
        max_h = h - 30
        start_x = 20
        max_val = 0.15

        for i in range(26):
            x = start_x + i * gap

            # English reference
            eh = max(1, (ENGLISH_FREQ[i] / max_val) * max_h)
            p.fillRect(int(x), int(h - 18 - eh), int(bar_w), int(eh), QColor(107, 107, 128, 40))

            # Input bar
            ih = max(0, (self.in_freq[i] / max_val) * max_h)
            p.fillRect(int(x), int(h - 18 - ih), int(bar_w * 0.55), int(ih), QColor(224, 165, 38, 140))

            # Output bar
            oh = max(0, (self.out_freq[i] / max_val) * max_h)
            p.fillRect(int(x + bar_w * 0.55), int(h - 18 - oh), int(bar_w * 0.45), int(oh), QColor(96, 165, 250, 140))

            # Letter label
            p.setPen(QColor(107, 107, 128, 160))
            p.setFont(SMALL_MONO)
            p.drawText(int(x + bar_w / 2), h - 4, letters[i])

        # Legend
        p.setFont(SMALL_FONT)
        lx = w - 320
        items = [
            (QColor(224, 165, 38, 140), "Input"),
            (QColor(96, 165, 250, 140), "Output"),
            (QColor(107, 107, 128, 40), "English avg"),
        ]
        for idx, (color, label) in enumerate(items):
            px = lx + idx * 100
            p.fillRect(px, 6, 12, 8, color)
            p.setPen(QColor(107, 107, 128))
            p.drawText(px + 16, 14, label)

        p.end()


# ═══════════════════════════════════════════════════════════
# ALPHABET DISPLAY WIDGET
# ═══════════════════════════════════════════════════════════

class AlphabetDisplay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.top = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.bottom = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.setObjectName("alphabetFrame")
        self.setStyleSheet("""
            #alphabetFrame { background: #14141e; border: 1px solid #262638;
            border-radius: 10px; }
        """)
        self.setVisible(False)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        self.top_label = QLabel()
        self.top_label.setFont(SMALL_MONO)
        self.bot_label = QLabel()
        self.bot_label.setFont(SMALL_MONO)
        self.top_label.setStyleSheet("color: #c4c2bf; background: rgba(224,165,38,0.05);"
                                     "padding: 4px 6px; border-radius: 4px;")
        self.bot_label.setStyleSheet("color: #e0a526; font-weight: bold; background: rgba(224,165,38,0.1);"
                                     "padding: 4px 6px; border-radius: 4px;")
        lbl1 = QLabel("Plain ")
        lbl1.setFont(SMALL_FONT)
        lbl1.setStyleSheet("color: #6b6b80;")
        lbl1.setFixedWidth(40)
        lbl2 = QLabel("Cipher")
        lbl2.setFont(SMALL_FONT)
        lbl2.setStyleSheet("color: #6b6b80;")
        lbl2.setFixedWidth(40)
        row1 = QHBoxLayout(); row1.addWidget(lbl1); row1.addWidget(self.top_label); row1.addStretch()
        row2 = QHBoxLayout(); row2.addWidget(lbl2); row2.addWidget(self.bot_label); row2.addStretch()
        layout.addLayout(row1)
        layout.addLayout(row2)

    def set_alphabet(self, top, bottom):
        self.top = top
        self.bottom = bottom
        spaced_top = '  '.join(top)
        spaced_bot = '  '.join(bottom)
        self.top_label.setText(spaced_top)
        self.bot_label.setText(spaced_bot)
        self.setVisible(True)


# ═══════════════════════════════════════════════════════════
# DROP TEXT EDIT (drag & drop support)
# ═══════════════════════════════════════════════════════════

class DropTextEdit(QTextEdit):
    fileDropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.isLocalFile():
                try:
                    with open(url.toLocalFile(), 'r', encoding='utf-8') as f:
                        self.fileDropped.emit(f.read())
                except Exception:
                    pass
        elif event.mimeData().hasText():
            self.setPlainText(event.mimeData().text())


# ═══════════════════════════════════════════════════════════
# BRUTE FORCE WIDGET
# ═══════════════════════════════════════════════════════════

class BruteForceWidget(QWidget):
    resultSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.list = QListWidget()
        self.list.setFont(MONO_FONT)
        self.list.setStyleSheet("""
            QListWidget { background: #14141e; border: 1px solid #262638;
            border-radius: 10px; }
            QListWidget::item { padding: 8px 12px; }
        """)
        self.list.itemClicked.connect(self._on_click)
        layout.addWidget(self.list)
        self.empty_label = QLabel("  Brute force available for Caesar and Affine ciphers.")
        self.empty_label.setStyleSheet("color: #6b6b80; font-size: 12px; padding: 40px;")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.empty_label)
        self.empty_label.setVisible(True)
        self.list.setVisible(False)

    def _on_click(self, item):
        text = item.data(Qt.ItemDataRole.UserRole)
        if text:
            self.resultSelected.emit(text)

    def show_results(self, results):
        self.list.clear()
        self.empty_label.setVisible(len(results) == 0)
        self.list.setVisible(len(results) > 0)
        if not results:
            self.empty_label.setText("  Enter text to see brute force results.")
            return
        for label, decoded in results:
            item = QListWidgetItem(f"{label:20s} {decoded[:80]}")
            item.setData(Qt.ItemDataRole.UserRole, decoded)
            item.setToolTip(f"{label}\n{decoded}")
            self.list.addItem(item)

    def clear(self):
        self.list.clear()
        self.empty_label.setVisible(True)
        self.empty_label.setText("  Brute force available for Caesar and Affine ciphers.")
        self.list.setVisible(False)


# ═══════════════════════════════════════════════════════════
# CHAIN WIDGET
# ═══════════════════════════════════════════════════════════

class ChainStepWidget(QFrame):
    changed = Signal()
    removeRequested = Signal(object)

    def __init__(self, step_num, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            ChainStepWidget { background: #0a0a0f; border: 1px solid #262638;
            border-radius: 8px; padding: 8px; }
        """)
        self.params = {}
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(8)

        self.num_label = QLabel(str(step_num))
        self.num_label.setFont(SMALL_MONO)
        self.num_label.setStyleSheet("color: #e0a526; font-weight: bold; min-width: 20px;")
        layout.addWidget(self.num_label)

        self.cipher_combo = QComboBox()
        self.cipher_combo.setMinimumWidth(120)
        for cid, c in CIPHERS.items():
            self.cipher_combo.addItem(c['name'], cid)
        self.cipher_combo.currentIndexChanged.connect(self._cipher_changed)
        layout.addWidget(self.cipher_combo)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Encode", "Decode"])
        self.mode_combo.setFixedWidth(80)
        layout.addWidget(self.mode_combo)

        self.param_container = QWidget()
        self.param_layout = QHBoxLayout(self.param_container)
        self.param_layout.setContentsMargins(0, 0, 0, 0)
        self.param_layout.setSpacing(6)
        layout.addWidget(self.param_container)
        layout.addStretch()

        remove_btn = QPushButton("×")
        remove_btn.setFixedSize(24, 24)
        remove_btn.setObjectName("dangerBtn")
        remove_btn.setFont(QFont('Space Grotesk', 14, QFont.Weight.Bold))
        remove_btn.clicked.connect(lambda: self.removeRequested.emit(self))
        layout.addWidget(remove_btn)

        self._cipher_changed()

    def _cipher_changed(self):
        # Clear old param widgets
        while self.param_layout.count():
            w = self.param_layout.takeAt(0).widget()
            if w: w.deleteLater()
        self.params = {}
        cid = self.cipher_combo.currentData()
        if not cid: return
        cipher = CIPHERS[cid]
        for p in cipher.get('params', []):
            lbl = QLabel(p['label'])
            lbl.setFont(SMALL_FONT)
            lbl.setStyleSheet("color: #6b6b80; min-width: 60px;")
            self.param_layout.addWidget(lbl)
            if p['type'] == 'slider':
                slider = QSlider(Qt.Orientation.Horizontal)
                slider.setRange(p['min'], p['max'])
                val = p['default']
                if p.get('filter'):
                    for v in range(p['min'], p['max']+1):
                        if p['filter'](v):
                            val = v; break
                slider.setValue(val)
                val_lbl = QLabel(str(val))
                val_lbl.setFont(SMALL_MONO)
                val_lbl.setStyleSheet("color: #e0a526; font-weight: bold; min-width: 24px;")
                slider.valueChanged.connect(lambda v, vl=val_lbl, pid=p['id']: (
                    vl.setText(str(v)), self.params.update({pid: v})))
                self.params[p['id']] = val
                self.param_layout.addWidget(slider)
                self.param_layout.addWidget(val_lbl)
            elif p['type'] == 'text':
                le = QLineEdit(p.get('default', ''))
                le.setFixedWidth(120)
                le.setFont(SMALL_MONO)
                le.textChanged.connect(lambda t, pid=p['id']: self.params.update({pid: t}))
                self.params[p['id']] = p.get('default', '')
                self.param_layout.addWidget(le)
        self.changed.emit()

    def get_config(self):
        return {
            'cipher': self.cipher_combo.currentData(),
            'mode': 'encode' if self.mode_combo.currentIndex() == 0 else 'decode',
            'params': dict(self.params),
        }


class ChainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        top = QHBoxLayout()
        top.addStretch()
        add_btn = QPushButton("  Add Step")
        add_btn.setObjectName("infoBtn")
        add_btn.setIcon(self._icon('fa-plus'))
        add_btn.clicked.connect(self.add_step)
        top.addWidget(add_btn)

        run_btn = QPushButton("  Run Chain")
        run_btn.setObjectName("primaryBtn")
        run_btn.setIcon(self._icon('fa-play'))
        run_btn.clicked.connect(self.run)
        top.addWidget(run_btn)
        layout.addLayout(top)

        self.steps_layout = QVBoxLayout()
        self.steps_layout.setSpacing(4)
        layout.addLayout(self.steps_layout)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setMaximumHeight(100)
        self.output_box.setStyleSheet("""
            QTextEdit { background: #0a0a0f; color: #e0a526;
            border: 1px solid #262638; border-radius: 8px;
            font-family: 'JetBrains Mono', monospace; font-size: 12px; }
        """)
        self.output_box.setVisible(False)
        layout.addWidget(self.output_box)

        self.empty = QLabel("  Add cipher steps to build a processing pipeline")
        self.empty.setStyleSheet("color: #6b6b80; font-size: 12px; padding: 30px;")
        self.empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.empty)

        self.steps = []
        self._update_empty()

    def _icon(self, name):
        # Return empty icon - styling handles it
        return QIcon()

    def add_step(self):
        step = ChainStepWidget(len(self.steps) + 1)
        step.removeRequested.connect(self.remove_step)
        self.steps_layout.addWidget(step)
        self.steps.append(step)
        self._update_empty()
        self._renumber()

    def remove_step(self, step):
        if step in self.steps:
            self.steps_layout.removeWidget(step)
            self.steps.remove(step)
            step.deleteLater()
            self._update_empty()
            self._renumber()

    def _renumber(self):
        for i, s in enumerate(self.steps):
            s.num_label.setText(str(i + 1))

    def _update_empty(self):
        self.empty.setVisible(len(self.steps) == 0)

    def run(self, input_text=""):
        if not self.steps:
            return ""
        text = input_text
        for step in self.steps:
            cfg = step.get_config()
            cid = cfg['cipher']
            if not cid: continue
            cipher = CIPHERS[cid]
            fn = cipher['encode'] if cfg['mode'] == 'encode' else cipher['decode']
            text = fn(text, cfg['params'])
        self.output_box.setVisible(True)
        self.output_box.setPlainText(text)
        return text


# ═══════════════════════════════════════════════════════════
# HISTORY WIDGET
# ═══════════════════════════════════════════════════════════

class HistoryWidget(QWidget):
    entrySelected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        top = QHBoxLayout()
        top.addStretch()
        self.clear_btn = QPushButton("  Clear History")
        self.clear_btn.setObjectName("dangerBtn")
        self.clear_btn.setVisible(False)
        self.clear_btn.clicked.connect(self.clear)
        top.addWidget(self.clear_btn)
        layout.addLayout(top)

        self.list = QListWidget()
        self.list.setFont(SMALL_FONT)
        self.list.setStyleSheet("""
            QListWidget { background: transparent; border: none; }
            QListWidget::item { background: #14141e; border: 1px solid #262638;
            border-radius: 8px; padding: 10px 14px; margin: 2px 0; }
            QListWidget::item:hover { background: #1a1a28; border-color: #32324a; }
        """)
        self.list.itemClicked.connect(self._on_click)
        layout.addWidget(self.list)

        self.empty = QLabel("  No history yet")
        self.empty.setStyleSheet("color: #6b6b80; font-size: 13px; padding: 50px;")
        self.empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.empty)
        self.empty.setVisible(True)
        self.list.setVisible(False)

        self.entries = []

    def _on_click(self, item):
        idx = item.data(Qt.ItemDataRole.UserRole)
        if idx is not None and idx < len(self.entries):
            self.entrySelected.emit(self.entries[idx])

    def add_entry(self, entry):
        self.entries.insert(0, entry)
        if len(self.entries) > 50:
            self.entries.pop()
        self._refresh()

    def clear(self):
        self.entries.clear()
        self._refresh()

    def _refresh(self):
        self.list.clear()
        has = len(self.entries) > 0
        self.empty.setVisible(not has)
        self.list.setVisible(has)
        self.clear_btn.setVisible(has)
        for i, e in enumerate(self.entries):
            cipher_name = CIPHERS.get(e.get('cipher', ''), {}).get('name', '?')
            mode = e.get('mode', '?').upper()
            time_str = e.get('time', '')
            inp = e.get('input', '')[:50]
            out = e.get('output', '')[:50]
            text = f"[{cipher_name}] {mode}  {time_str}\n  {inp}  →  {out}"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, i)
            self.list.addItem(item)


# ═══════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════

class CipherVault(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CipherVault — Cryptographic Toolkit")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 800)

        self.current_cipher = 'caesar'
        self.current_mode = 'encode'
        self.current_params = {}
        self.param_widgets = {}

        self._build_ui()
        self._build_sidebar()
        self._build_shortcuts()
        self._select_cipher('caesar')

        self.statusBar().showMessage("Ready  ·  Ctrl+Enter to process  ·  Ctrl+Shift+C to copy output")

    # ── UI Construction ──

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setFixedWidth(280)
        self.sidebar_widget.setStyleSheet("background: #0e0e16; border-right: 1px solid #1a1a28;")
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)
        main_layout.addWidget(self.sidebar_widget)

        # Separator
        sep = QFrame()
        sep.setObjectName("sidebarSep")
        sep.setFixedWidth(1)
        main_layout.addWidget(sep)

        # Main content
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_scroll.setStyleSheet("QScrollArea { border: none; background: #08080d; }")
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(32, 28, 32, 32)
        self.main_layout.setSpacing(0)
        main_scroll.setWidget(self.main_widget)
        main_layout.addWidget(main_scroll, 1)

        self._build_header()
        self._build_controls()
        self._build_params()
        self._build_io()
        self._build_stats()
        self._build_actions()
        self._build_alphabet()
        self._build_tabs()

    def _build_header(self):
        self.header_label = QLabel()
        self.header_label.setObjectName("headerLabel")
        self.main_layout.addWidget(self.header_label)

        tags_row = QHBoxLayout()
        tags_row.setSpacing(8)
        tags_row.setContentsMargins(0, 6, 0, 0)
        self.tag_label = QLabel()
        self.tag_label.setObjectName("tagLabel")
        tags_row.addWidget(self.tag_label)
        self.strength_label = QLabel()
        self.strength_label.setObjectName("noneLabel")
        tags_row.addWidget(self.strength_label)
        tags_row.addStretch()
        self.main_layout.addLayout(tags_row)

        self.sub_label = QLabel()
        self.sub_label.setObjectName("subLabel")
        self.sub_label.setWordWrap(True)
        self.sub_label.setContentsMargins(0, 8, 0, 0)
        self.main_layout.addWidget(self.sub_label)

        self.main_layout.addSpacing(16)

    def _build_controls(self):
        row = QHBoxLayout()
        row.setSpacing(12)

        # Mode toggle
        self.encode_btn = QPushButton("  Encode")
        self.encode_btn.setObjectName("primaryBtn")
        self.encode_btn.setCheckable(True)
        self.encode_btn.setChecked(True)
        self.encode_btn.clicked.connect(lambda: self._set_mode('encode'))
        row.addWidget(self.encode_btn)

        self.decode_btn = QPushButton("  Decode")
        self.decode_btn.setCheckable(True)
        self.decode_btn.clicked.connect(lambda: self._set_mode('decode'))
        row.addWidget(self.decode_btn)

        row.addSpacing(8)

        # Case option
        lbl = QLabel("Output:")
        lbl.setStyleSheet("color: #6b6b80; font-size: 12px;")
        row.addWidget(lbl)
        self.case_combo = QComboBox()
        self.case_combo.addItems(["Preserve case", "UPPERCASE", "lowercase"])
        self.case_combo.setFixedWidth(120)
        self.case_combo.currentIndexChanged.connect(self._process)
        row.addWidget(self.case_combo)

        # Strip non-alpha
        self.strip_cb = QCheckBox("Strip non-alpha")
        self.strip_cb.stateChanged.connect(self._process)
        row.addWidget(self.strip_cb)

        row.addStretch()

        # Auto-detect
        self.detect_btn = QPushButton("  Auto-detect")
        self.detect_btn.setObjectName("infoBtn")
        self.detect_btn.clicked.connect(self._auto_detect)
        row.addWidget(self.detect_btn)

        self.main_layout.addLayout(row)
        self.main_layout.addSpacing(14)

    def _build_params(self):
        self.params_group = QGroupBox("Parameters")
        self.params_group.setVisible(False)
        self.params_layout = QHBoxLayout(self.params_group)
        self.params_layout.setSpacing(16)
        self.main_layout.addWidget(self.params_group)
        self.main_layout.addSpacing(10)

    def _build_io(self):
        io_layout = QHBoxLayout()
        io_layout.setSpacing(10)

        # Input
        input_col = QVBoxLayout()
        input_header = QHBoxLayout()
        input_header.addWidget(self._make_section_label("Input"))
        self.input_count = QLabel("0 chars")
        self.input_count.setFont(SMALL_MONO)
        self.input_count.setStyleSheet("color: #6b6b80;")
        input_header.addStretch()
        input_header.addWidget(self.input_count)
        input_col.addLayout(input_header)

        self.input_text = DropTextEdit()
        self.input_text.setPlaceholderText("Type or paste your message here...\nYou can also drag & drop a text file.")
        self.input_text.setFont(MONO_FONT)
        self.input_text.textChanged.connect(self._process)
        self.input_text.fileDropped.connect(self._on_file_dropped)
        input_col.addWidget(self.input_text)
        io_layout.addLayout(input_col, 1)

        # Swap button
        swap_btn = QPushButton("⇄")
        swap_btn.setFixedSize(38, 38)
        swap_btn.setToolTip("Swap input/output and flip mode")
        swap_btn.clicked.connect(self._swap)
        io_layout.addWidget(swap_btn, 0, Qt.AlignmentFlag.AlignVCenter)

        # Output
        output_col = QVBoxLayout()
        output_header = QHBoxLayout()
        output_header.addWidget(self._make_section_label("Output"))
        self.output_count = QLabel("0 chars")
        self.output_count.setFont(SMALL_MONO)
        self.output_count.setStyleSheet("color: #6b6b80;")
        output_header.addStretch()
        output_header.addWidget(self.output_count)
        output_col.addLayout(output_header)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Result will appear here...")
        self.output_text.setFont(MONO_FONT)
        self.output_text.setStyleSheet("""
            QTextEdit { color: #e0a526; }
        """)
        output_col.addWidget(self.output_text)
        io_layout.addLayout(output_col, 1)

        self.main_layout.addLayout(io_layout)
        self.main_layout.addSpacing(10)

    def _build_stats(self):
        row = QHBoxLayout()
        row.setSpacing(6)
        self.stat_labels = {}
        for key, icon in [('chars','Chars'), ('words','Words'), ('unique','Unique'),
                          ('letters','Letters'), ('digits','Digits')]:
            lbl = QLabel(f" {icon}: 0 ")
            lbl.setObjectName("statLabel")
            row.addWidget(lbl)
            self.stat_labels[key] = lbl
        row.addStretch()
        self.main_layout.addLayout(row)
        self.main_layout.addSpacing(10)

    def _build_actions(self):
        row = QHBoxLayout()
        row.setSpacing(8)

        process_btn = QPushButton("  Process")
        process_btn.setObjectName("primaryBtn")
        process_btn.clicked.connect(lambda: (self._process(), self._add_history()))
        row.addWidget(process_btn)

        copy_btn = QPushButton("  Copy")
        copy_btn.clicked.connect(self._copy_output)
        row.addWidget(copy_btn)

        save_btn = QPushButton("  Save")
        save_btn.clicked.connect(self._save_output)
        row.addWidget(save_btn)

        clear_btn = QPushButton("  Clear")
        clear_btn.clicked.connect(self._clear)
        row.addWidget(clear_btn)

        self.gen_key_btn = QPushButton("  Generate Key")
        self.gen_key_btn.setObjectName("infoBtn")
        self.gen_key_btn.setVisible(False)
        self.gen_key_btn.clicked.connect(self._generate_key)
        row.addWidget(self.gen_key_btn)

        row.addStretch()
        self.main_layout.addLayout(row)
        self.main_layout.addSpacing(16)

    def _build_alphabet(self):
        self.alphabet_display = AlphabetDisplay()
        self.main_layout.addWidget(self.alphabet_display)
        self.main_layout.addSpacing(12)

    def _build_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setFont(UI_FONT)

        # Frequency Analysis
        freq_tab = QWidget()
        freq_layout = QVBoxLayout(freq_tab)
        freq_layout.setContentsMargins(0, 8, 0, 0)
        self.freq_chart = FrequencyChart()
        freq_layout.addWidget(self.freq_chart)
        self.tabs.addTab(freq_tab, "Frequency Analysis")

        # Brute Force
        self.brute_widget = BruteForceWidget()
        self.brute_widget.resultSelected.connect(self._use_brute_result)
        self.tabs.addTab(self.brute_widget, "Brute Force")

        # Chain
        self.chain_widget = ChainWidget()
        self.tabs.addTab(self.chain_widget, "Chain")

        # History
        self.history_widget = HistoryWidget()
        self.history_widget.entrySelected.connect(self._restore_history)
        self.tabs.addTab(self.history_widget, "History")

        self.main_layout.addWidget(self.tabs)

    def _build_sidebar(self):
        # Logo
        logo = QWidget()
        logo_layout = QVBoxLayout(logo)
        logo_layout.setContentsMargins(18, 18, 18, 14)
        title = QLabel("CipherVault")
        title.setFont(QFont('JetBrains Mono', 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #e0a526;")
        logo_layout.addWidget(title)
        sub = QLabel("cryptographic toolkit v3.0")
        sub.setFont(SMALL_MONO)
        sub.setStyleSheet("color: #6b6b80;")
        logo_layout.addWidget(sub)
        self.sidebar_layout.addWidget(logo)

        # Separator
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFixedHeight(1)
        self.sidebar_layout.addWidget(sep)

        # Search
        search_container = QWidget()
        sc_layout = QVBoxLayout(search_container)
        sc_layout.setContentsMargins(12, 8, 12, 4)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("  Search ciphers...")
        self.search_input.setFont(UI_FONT)
        self.search_input.textChanged.connect(self._filter_sidebar)
        sc_layout.addWidget(self.search_input)
        self.sidebar_layout.addWidget(search_container)

        # Scrollable cipher list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.sidebar_list_layout = QVBoxLayout(scroll_content)
        self.sidebar_list_layout.setContentsMargins(6, 4, 6, 12)
        self.sidebar_list_layout.setSpacing(0)
        scroll.setWidget(scroll_content)
        self.sidebar_layout.addWidget(scroll, 1)

        # Build cipher buttons
        self.cipher_buttons = {}
        for group_name, cipher_ids in CIPHER_GROUPS.items():
            group_lbl = QLabel(f"  {group_name.upper()}")
            group_lbl.setFont(SMALL_FONT)
            group_lbl.setStyleSheet("color: #6b6b80; padding: 10px 8px 4px; letter-spacing: 1.5px;")
            self.sidebar_list_layout.addWidget(group_lbl)

            for cid in cipher_ids:
                c = CIPHERS[cid]
                btn = QPushButton()
                btn.setCheckable(True)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
                strength_colors = {'weak': '#f87171', 'medium': '#fbbf24', 'strong': '#34d399', 'none': '#6b6b80'}

                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: transparent; border: none; color: #e8e6e3;
                        text-align: left; padding: 9px 12px; border-radius: 7px;
                        font-size: 13px; font-family: 'Space Grotesk', sans-serif;
                    }}
                    QPushButton:hover {{ background: #20202f; }}
                    QPushButton:checked {{
                        background: rgba(224,165,38,0.1); color: #e0a526;
                    }}
                """)

                btn.setText(f"  {c['name']}")
                btn.setToolTip(f"{c['full']}\n{c['desc']}")

                btn.clicked.connect(lambda checked, id=cid: self._select_cipher(id))
                self.sidebar_list_layout.addWidget(btn)
                self.cipher_buttons[cid] = btn

        self.sidebar_list_layout.addStretch()

        # Footer
        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(14, 8, 14, 10)
        footer_lbl = QLabel("Ctrl+Enter  Process")
        footer_lbl.setFont(SMALL_MONO)
        footer_lbl.setStyleSheet("color: #32324a;")
        footer_layout.addWidget(footer_lbl)
        self.sidebar_layout.addWidget(footer)

    def _build_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+Return"), self, lambda: (self._process(), self._add_history()))
        QShortcut(QKeySequence("Ctrl+Shift+C"), self, self._copy_output)
        QShortcut(QKeySequence("Ctrl+Shift+S"), self, self._save_output)

    # ── Helpers ──

    @staticmethod
    def _make_section_label(text):
        lbl = QLabel(text.upper())
        lbl.setFont(SMALL_FONT)
        lbl.setStyleSheet("color: #6b6b80; letter-spacing: 1px;")
        return lbl

    # ── Cipher Selection ──

    def _select_cipher(self, cid):
        self.current_cipher = cid
        c = CIPHERS[cid]

        # Update sidebar
        for bid, btn in self.cipher_buttons.items():
            btn.setChecked(bid == cid)

        # Update header
        self.header_label.setText(c['full'])
        self.tag_label.setText(c['tag'])
        strength_map = {
            'weak': ('noneLabel', '#f87171', 'Weak'),
            'medium': ('mediumLabel', '#fbbf24', 'Medium'),
            'strong': ('noneLabel', '#34d399', 'Strong'),
            'none': ('noneLabel', '#6b6b80', 'None'),
        }
        obj, color, text = strength_map.get(c['strength'], strength_map['none'])
        self.strength_label.setObjectName(obj)
        self.strength_label.setText(f"  {text}  ")
        self.strength_label.setStyleSheet(
            f"font-size: 10px; padding: 2px 8px; border-radius: 12px; "
            f"background: {color}18; color: {color};"
        )
        self.sub_label.setText(c['desc'])

        # Build params
        self._build_cipher_params(c)

        # Show/hide gen key
        self.gen_key_btn.setVisible(c.get('has_gen_key', False))

        # Reset params
        self.current_params = {}
        for p in c.get('params', []):
            self.current_params[p['id']] = p['default']

        # Update brute force
        self._update_brute()

        # Update alphabet
        self._update_alphabet()

        self._process()

    def _build_cipher_params(self, cipher):
        params = cipher.get('params', [])
        # Clear old
        while self.params_layout.count():
            w = self.params_layout.takeAt(0).widget()
            if w: w.deleteLater()
        self.param_widgets = {}

        if not params:
            self.params_group.setVisible(False)
            return

        self.params_group.setVisible(True)
        for p in params:
            lbl = QLabel(p['label'])
            lbl.setFont(UI_FONT)
            lbl.setStyleSheet("color: #6b6b80; min-width: 90px;")
            self.params_layout.addWidget(lbl)

            if p['type'] == 'slider':
                slider = QSlider(Qt.Orientation.Horizontal)
                slider.setRange(p['min'], p['max'])
                val = p['default']
                if p.get('filter'):
                    valid = [v for v in range(p['min'], p['max']+1) if p['filter'](v)]
                    if valid:
                        # Set to first valid, but try to keep default
                        if p['filter'](val):
                            slider.setValue(val)
                        else:
                            val = valid[0]
                            slider.setValue(val)
                    slider._valid_values = valid if p.get('filter') else None
                else:
                    slider._valid_values = None
                    slider.setValue(val)

                val_lbl = QLabel(str(val))
                val_lbl.setFont(QFont('JetBrains Mono', 14, QFont.Weight.Bold))
                val_lbl.setStyleSheet("color: #e0a526; min-width: 28px;")
                val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

                def on_slider(v, vl=val_lbl, pid=p['id'], s=slider):
                    # Snap to valid if needed
                    if s._valid_values:
                        closest = min(s._valid_values, key=lambda x: abs(x - v))
                        if closest != v:
                            s.blockSignals(True)
                            s.setValue(closest)
                            s.blockSignals(False)
                            v = closest
                    vl.setText(str(v))
                    self.current_params[pid] = v
                    self._update_alphabet()
                    self._update_brute()
                    self._process()

                slider.valueChanged.connect(on_slider)
                self.params_layout.addWidget(slider)
                self.params_layout.addWidget(val_lbl)
                self.param_widgets[p['id']] = (slider, val_lbl)

            elif p['type'] == 'text':
                le = QLineEdit(p.get('default', ''))
                le.setFont(MONO_FONT)
                le.setFixedWidth(200)
                le.textChanged.connect(lambda t, pid=p['id']: (
                    self.current_params.update({pid: t}), self._process()))
                self.params_layout.addWidget(le)
                self.param_widgets[p['id']] = le

            self.params_layout.addStretch()

    # ── Mode ──

    def _set_mode(self, mode):
        self.current_mode = mode
        self.encode_btn.setChecked(mode == 'encode')
        self.decode_btn.setChecked(mode == 'decode')
        if mode == 'encode':
            self.encode_btn.setObjectName("primaryBtn")
            self.decode_btn.setObjectName("")
        else:
            self.encode_btn.setObjectName("")
            self.decode_btn.setObjectName("primaryBtn")
        self.encode_btn.style().unpolish(self.encode_btn)
        self.encode_btn.style().polish(self.encode_btn)
        self.decode_btn.style().unpolish(self.decode_btn)
        self.decode_btn.style().polish(self.decode_btn)
        self._process()

    # ── Processing ──

    def _process(self, *_):
        raw = self.input_text.toPlainText()
        strip = self.strip_cb.isChecked()
        case_opt = self.case_combo.currentIndex()  # 0=preserve, 1=upper, 2=lower
        text = re.sub(r'[^a-zA-Z]', '', raw) if strip else raw

        self.input_count.setText(f"{len(raw)} chars")
        self._update_stats(raw)

        if not text.strip():
            self.output_text.clear()
            self.output_count.setText("0 chars")
            self.freq_chart.set_data('', '')
            return

        cipher = CIPHERS[self.current_cipher]
        fn = cipher['encode'] if self.current_mode == 'encode' else cipher['decode']
        try:
            output = fn(text, self.current_params)
        except Exception as e:
            output = f"[Error: {e}]"

        if case_opt == 1:
            output = output.upper()
        elif case_opt == 2:
            output = output.lower()

        self.output_text.setPlainText(output)
        self.output_count.setText(f"{len(output)} chars")
        self.freq_chart.set_data(text, output)

    def _update_stats(self, text):
        letters = len(re.findall(r'[a-zA-Z]', text))
        digits = len(re.findall(r'\d', text))
        words = len(text.split()) if text.strip() else 0
        unique = len(set(re.sub(r'[^a-z]', '', text.lower())))
        vals = {'chars': len(text), 'words': words, 'unique': unique,
                'letters': letters, 'digits': digits}
        for key, val in vals.items():
            labels = {'chars': 'Chars', 'words': 'Words', 'unique': 'Unique',
                      'letters': 'Letters', 'digits': 'Digits'}
            self.stat_labels[key].setText(f" {labels[key]}: {val} ")

    def _update_alphabet(self):
        cipher = CIPHERS[self.current_cipher]
        if 'alphabet' not in cipher:
            self.alphabet_display.setVisible(False)
            return
        try:
            top, bottom = cipher['alphabet'](self.current_params)
            self.alphabet_display.set_alphabet(top, bottom)
        except Exception:
            self.alphabet_display.setVisible(False)

    def _update_brute(self):
        cipher = CIPHERS[self.current_cipher]
        if 'brute' not in cipher:
            self.brute_widget.clear()
            return
        text = self.input_text.toPlainText()
        if not text.strip():
            self.brute_widget.clear()
            return
        try:
            results = cipher['brute'](text)
            self.brute_widget.show_results(results)
        except Exception:
            self.brute_widget.clear()

    # ── Actions ──

    def _swap(self):
        inp = self.input_text.toPlainText()
        out = self.output_text.toPlainText()
        self.input_text.setPlainText(out)
        self._set_mode('decode' if self.current_mode == 'encode' else 'encode')

    def _copy_output(self):
        text = self.output_text.toPlainText()
        if not text:
            self.statusBar().showMessage("Nothing to copy", 3000)
            return
        QApplication.clipboard().setText(text)
        self.statusBar().showMessage("Copied to clipboard", 3000)

    def _save_output(self):
        text = self.output_text.toPlainText()
        if not text:
            self.statusBar().showMessage("Nothing to save", 3000)
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Output", f"ciphervault_{self.current_cipher}_{int(time.time())}.txt",
            "Text Files (*.txt);;All Files (*)")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            self.statusBar().showMessage(f"Saved to {path}", 4000)

    def _clear(self):
        self.input_text.clear()
        self.output_text.clear()
        self.input_count.setText("0 chars")
        self.output_count.setText("0 chars")
        self._update_stats('')
        self.freq_chart.set_data('', '')

    def _generate_key(self):
        global _sub_key, _sub_inv
        _sub_key = None
        get_sub()
        self._update_alphabet()
        self._process()
        self.statusBar().showMessage("New random key generated", 3000)

    def _on_file_dropped(self, text):
        self.input_text.setPlainText(text)
        self.statusBar().showMessage("File loaded", 3000)

    def _use_brute_result(self, text):
        self.output_text.setPlainText(text)
        self.output_count.setText(f"{len(text)} chars")
        self.statusBar().showMessage("Brute force result applied", 3000)

    def _auto_detect(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            self.statusBar().showMessage("Enter text to auto-detect", 3000)
            return

        # Base64 check
        if re.match(r'^[A-Za-z0-9+/]+=*$', text) and len(text) > 4 and len(text) % 4 == 0:
            try:
                decoded = base64.b64decode(text).decode('utf-8')
                if decoded.isprintable():
                    self._select_cipher('base64')
                    self._set_mode('decode')
                    self.statusBar().showMessage("Detected: Base64 encoded text", 4000)
                    return
            except Exception:
                pass

        # Morse check
        if re.match(r'^[\.\-\/\s]+$', text) and ('.' in text or '-' in text):
            self._select_cipher('morse')
            self._set_mode('decode')
            self.statusBar().showMessage("Detected: Morse code", 4000)
            return

        # Caesar brute — check for common English words
        common = {'THE','AND','FOR','ARE','BUT','NOT','YOU','ALL','CAN','HER','WAS',
                  'ONE','OUR','OUT','HAD','HAS','HIS','HOW','ITS','MAY','NEW','NOW',
                  'OLD','SEE','WAY','WHO','DID','GET','LET','SAY','SHE','TOO','USE'}
        alpha = re.sub(r'[^a-zA-Z]', '', text)
        if len(alpha) > 10 and len(alpha) == len(text.replace(' ', '')):
            for shift in range(1, 26):
                decoded = _caesar(text, shift, False)
                words = set(re.findall(r'[a-zA-Z]+', decoded.upper()))
                if len(words & common) >= 2:
                    self._select_cipher('caesar')
                    self.current_params['shift'] = shift
                    if 'shift' in self.param_widgets:
                        slider, lbl = self.param_widgets['shift']
                        slider.setValue(shift)
                    self._set_mode('decode')
                    self.statusBar().showMessage(
                        f"Detected: Caesar shift {shift} ({len(words & common)} common words)", 4000)
                    return

        self.statusBar().showMessage("Could not auto-detect the encoding", 4000)

    def _add_history(self):
        inp = self.input_text.toPlainText()
        if not inp or len(inp) < 2:
            return
        self.history_widget.add_entry({
            'cipher': self.current_cipher,
            'mode': self.current_mode,
            'input': inp[:80],
            'output': self.output_text.toPlainText()[:80],
            'time': time.strftime('%H:%M:%S'),
        })

    def _restore_history(self, entry):
        cid = entry.get('cipher', 'caesar')
        if cid in CIPHERS:
            self._select_cipher(cid)
        self._set_mode(entry.get('mode', 'encode'))
        self.input_text.setPlainText(entry.get('input', ''))
        self._process()
        self.statusBar().showMessage("History entry restored", 3000)

    def _filter_sidebar(self, query):
        q = query.lower().strip()
        for cid, btn in self.cipher_buttons.items():
            c = CIPHERS[cid]
            name = c['name'].lower()
            desc = c['desc'].lower()
            match = not q or q in name or q in desc
            btn.setVisible(match)

    # ── Override tab change to update brute ──
    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(100, self._update_brute)


# ═══════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Set default fonts that fall back gracefully
    app.setFont(UI_FONT)

    app.setStyleSheet(DARK_STYLE)

    window = CipherVault()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()