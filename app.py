import sys
import random
import string
import datetime
import os
from collections import Counter

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QSpinBox, QComboBox,
    QStackedWidget, QListWidget, QListWidgetItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QGroupBox, QFrame,
    QHeaderView, QMessageBox, QFileDialog, QStatusBar,
    QGraphicsOpacityEffect, QInputDialog
)
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QBrush, QKeySequence, QShortcut

# ═══════════════════════════════════════════════════════════════
#  STYLESHEETS (Catppuccin Mocha & Latte)
# ═══════════════════════════════════════════════════════════════

DARK_STYLE = """
QMainWindow{background:#1e1e2e;}
QWidget{color:#cdd6f4;font-family:'Segoe UI',Arial,sans-serif;}
QLabel{color:#cdd6f4;background:transparent;}
#sidebar{background:#181825;border-right:2px solid #313244;}
QTabWidget::pane{border:1px solid #313244;border-radius:8px;background:#1e1e2e;top:-1px;}
QTabBar::tab{background:#313244;color:#a6adc8;padding:10px 18px;margin-right:2px;border-top-left-radius:8px;border-top-right-radius:8px;font-size:12px;}
QTabBar::tab:selected{background:#1e1e2e;color:#89b4fa;font-weight:bold;}
QTabBar::tab:hover:!selected{background:#45475a;}
QGroupBox{background:#313244;border:1px solid #45475a;border-radius:10px;margin-top:16px;padding:16px;padding-top:28px;font-weight:bold;}
QGroupBox::title{subcontrol-origin:margin;left:16px;padding:0 8px;color:#89b4fa;}
QLineEdit,QSpinBox,QTextEdit{background:#45475a;border:2px solid #585b70;border-radius:8px;padding:8px 12px;color:#cdd6f4;font-size:14px;selection-background-color:#89b4fa;}
QLineEdit:focus,QSpinBox:focus,QTextEdit:focus{border-color:#89b4fa;}
QTextEdit{font-family:'Consolas','Courier New',monospace;}
QPushButton{background:#89b4fa;color:#1e1e2e;border:none;border-radius:8px;padding:10px 20px;font-weight:bold;font-size:13px;}
QPushButton:hover{background:#b4d0fb;}QPushButton:pressed{background:#6fa3f8;}
QPushButton#secondaryBtn{background:#45475a;color:#cdd6f4;}QPushButton#secondaryBtn:hover{background:#585b70;}
QPushButton#dangerBtn{background:#f38ba8;color:#1e1e2e;}QPushButton#dangerBtn:hover{background:#f5a3b8;}
QPushButton#successBtn{background:#a6e3a1;color:#1e1e2e;}QPushButton#successBtn:hover{background:#bceab8;}
QPushButton#smallBtn{padding:6px 12px;font-size:11px;}
QTableWidget{background:#313244;border:1px solid #45475a;border-radius:8px;gridline-color:#45475a;color:#cdd6f4;font-size:13px;}
QTableWidget::item{padding:4px;}QTableWidget::item:selected{background:#89b4fa;color:#1e1e2e;}
QHeaderView::section{background:#45475a;color:#89b4fa;padding:6px;border:1px solid #585b70;font-weight:bold;font-size:11px;}
QScrollBar:vertical{background:#181825;width:10px;border-radius:5px;}
QScrollBar::handle:vertical{background:#585b70;border-radius:5px;min-height:20px;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}
QComboBox{background:#45475a;border:2px solid #585b70;border-radius:8px;padding:6px 12px;color:#cdd6f4;font-size:13px;}
QComboBox:focus{border-color:#89b4fa;}QComboBox::drop-down{border:none;width:24px;}
QComboBox QAbstractItemView{background:#313244;color:#cdd6f4;selection-background-color:#89b4fa;selection-color:#1e1e2e;border:1px solid #585b70;}
QStatusBar{background:#181825;color:#a6adc8;font-size:12px;border-top:1px solid #313244;padding:4px 12px;}
QListWidget{background:transparent;border:none;outline:none;padding:4px;}
QListWidget::item{padding:8px 14px;border-radius:8px;margin:1px 4px;color:#a6adc8;font-size:12px;}
QListWidget::item:selected{background:#89b4fa;color:#1e1e2e;font-weight:bold;}
QListWidget::item:hover:!selected{background:#313244;color:#cdd6f4;}
"""

LIGHT_STYLE = """
QMainWindow{background:#eff1f5;}
QWidget{color:#4c4f69;font-family:'Segoe UI',Arial,sans-serif;}
QLabel{color:#4c4f69;background:transparent;}
#sidebar{background:#e6e9ef;border-right:2px solid #ccd0da;}
QTabWidget::pane{border:1px solid #ccd0da;border-radius:8px;background:#eff1f5;top:-1px;}
QTabBar::tab{background:#ccd0da;color:#6c6f85;padding:10px 18px;margin-right:2px;border-top-left-radius:8px;border-top-right-radius:8px;font-size:12px;}
QTabBar::tab:selected{background:#eff1f5;color:#1e66f5;font-weight:bold;}
QTabBar::tab:hover:!selected{background:#bcc0cc;}
QGroupBox{background:#e6e9ef;border:1px solid #ccd0da;border-radius:10px;margin-top:16px;padding:16px;padding-top:28px;font-weight:bold;}
QGroupBox::title{subcontrol-origin:margin;left:16px;padding:0 8px;color:#1e66f5;}
QLineEdit,QSpinBox,QTextEdit{background:#ffffff;border:2px solid #bcc0cc;border-radius:8px;padding:8px 12px;color:#4c4f69;font-size:14px;selection-background-color:#1e66f5;}
QLineEdit:focus,QSpinBox:focus,QTextEdit:focus{border-color:#1e66f5;}
QTextEdit{font-family:'Consolas','Courier New',monospace;}
QPushButton{background:#1e66f5;color:#ffffff;border:none;border-radius:8px;padding:10px 20px;font-weight:bold;font-size:13px;}
QPushButton:hover{background:#4e84f7;}QPushButton:pressed{background:#1550d3;}
QPushButton#secondaryBtn{background:#bcc0cc;color:#4c4f69;}QPushButton#secondaryBtn:hover{background:#acb0be;}
QPushButton#dangerBtn{background:#d20f39;color:#ffffff;}QPushButton#dangerBtn:hover{background:#e03e5e;}
QPushButton#successBtn{background:#40a02b;color:#ffffff;}QPushButton#successBtn:hover{background:#56b83f;}
QPushButton#smallBtn{padding:6px 12px;font-size:11px;}
QTableWidget{background:#e6e9ef;border:1px solid #ccd0da;border-radius:8px;gridline-color:#ccd0da;color:#4c4f69;font-size:13px;}
QTableWidget::item{padding:4px;}QTableWidget::item:selected{background:#1e66f5;color:#ffffff;}
QHeaderView::section{background:#ccd0da;color:#1e66f5;padding:6px;border:1px solid #bcc0cc;font-weight:bold;font-size:11px;}
QScrollBar:vertical{background:#e6e9ef;width:10px;border-radius:5px;}
QScrollBar::handle:vertical{background:#bcc0cc;border-radius:5px;min-height:20px;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}
QComboBox{background:#ffffff;border:2px solid #bcc0cc;border-radius:8px;padding:6px 12px;color:#4c4f69;font-size:13px;}
QComboBox:focus{border-color:#1e66f5;}QComboBox::drop-down{border:none;width:24px;}
QComboBox QAbstractItemView{background:#ffffff;color:#4c4f69;selection-background-color:#1e66f5;selection-color:#ffffff;border:1px solid #bcc0cc;}
QStatusBar{background:#e6e9ef;color:#6c6f85;font-size:12px;border-top:1px solid #ccd0da;padding:4px 12px;}
QListWidget{background:transparent;border:none;outline:none;padding:4px;}
QListWidget::item{padding:8px 14px;border-radius:8px;margin:1px 4px;color:#6c6f85;font-size:12px;}
QListWidget::item:selected{background:#1e66f5;color:#ffffff;font-weight:bold;}
QListWidget::item:hover:!selected{background:#ccd0da;color:#4c4f69;}
"""

# ═══════════════════════════════════════════════════════════════
#  CIPHER ENGINES
# ═══════════════════════════════════════════════════════════════

ENGLISH_FREQ = {'A':8.167,'B':1.492,'C':2.782,'D':4.253,'E':12.702,'F':2.228,'G':2.015,'H':6.094,'I':6.966,'J':0.153,'K':0.772,'L':4.025,'M':2.406,'N':6.749,'O':7.507,'P':1.929,'Q':0.095,'R':5.987,'S':6.327,'T':9.056,'U':2.758,'V':0.978,'W':2.360,'X':0.150,'Y':1.974,'Z':0.074}
MORSE_CODE = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.', '.':'.-.-.-',',':'--..--','?':'..--..','!':'-.-.--'}
MORSE_REVERSE = {v: k for k, v in MORSE_CODE.items()}

class CaesarCipher:
    @staticmethod 
    def name(): return "Caesar Cipher"
    @staticmethod 
    def icon(): return "🔤"
    @staticmethod 
    def category(): return "Substitution"
    @staticmethod 
    def difficulty(): return "Beginner"
    @staticmethod 
    def encrypt(t, s): 
        s = int(s) % 26; r = []
        for c in t:
            if c.isupper(): r.append(chr((ord(c)-65+s)%26+65))
            elif c.islower(): r.append(chr((ord(c)-97+s)%26+97))
            else: r.append(c)
        return ''.join(r)
    @staticmethod 
    def decrypt(t, s): return CaesarCipher.encrypt(t, -int(s))
    @staticmethod 
    def key_info(): return {"type":"int","label":"Shift","min":1,"max":25,"default":3}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>Caesar Cipher</h3><p>Each letter shifted by a fixed number. E(x)=(x+n) mod 26.</p>"
    @staticmethod 
    def get_steps(t, k, e=True):
        s = int(k)%26 if e else -(int(k)%26); steps = []
        for c in t:
            if c.isalpha():
                b = ord('A') if c.isupper() else ord('a'); o = ord(c)-b; n = (o+s)%26
                steps.append({"char":c,"pos":o,"new_pos":n,"result":chr(n+b),"op":f"({o}+{s}) mod 26={n}"})
            else: steps.append({"char":c,"pos":"—","new_pos":"—","result":c,"op":"Non-alpha"})
        return steps
    @staticmethod 
    def get_mapping(k): s=int(k)%26; return {chr(i+65):chr((i+s)%26+65) for i in range(26)}
    @staticmethod 
    def brute_force(t): return [(i, CaesarCipher.decrypt(t,i)) for i in range(1,26)]

class VigenereCipher:
    @staticmethod 
    def name(): return "Vigenère Cipher"
    @staticmethod 
    def icon(): return "🔑"
    @staticmethod 
    def category(): return "Polyalphabetic"
    @staticmethod 
    def difficulty(): return "Intermediate"
    @staticmethod 
    def encrypt(t, kw):
        kw = str(kw).upper()
        if not kw.isalpha(): return "Error: Key must be letters only"
        r, ki = [], 0
        for c in t:
            if c.isalpha():
                b = ord('A') if c.isupper() else ord('a'); sh = ord(kw[ki%len(kw)])-65
                r.append(chr((ord(c)-b+sh)%26+b)); ki += 1
            else: r.append(c)
        return ''.join(r)
    @staticmethod 
    def decrypt(t, kw):
        kw = str(kw).upper()
        if not kw.isalpha(): return "Error: Key must be letters only"
        r, ki = [], 0
        for c in t:
            if c.isalpha():
                b = ord('A') if c.isupper() else ord('a'); sh = ord(kw[ki%len(kw)])-65
                r.append(chr((ord(c)-b-sh)%26+b)); ki += 1
            else: r.append(c)
        return ''.join(r)
    @staticmethod 
    def key_info(): return {"type":"text","label":"Keyword","default":"SECRET"}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>Vigenère Cipher</h3><p>Polyalphabetic with keyword. E(x<sub>i</sub>)=(x<sub>i</sub>+k<sub>i</sub>) mod 26</p>"
    @staticmethod 
    def get_steps(t, k, e=True):
        kw = str(k).upper()
        if not kw.isalpha(): return []; steps, ki = [], 0
        for c in t:
            if c.isalpha():
                b = ord('A') if c.isupper() else ord('a'); kc = kw[ki%len(kw)]; sh = ord(kc)-65
                if not e: sh = -sh
                o = ord(c)-b; n = (o+sh)%26
                steps.append({"char":c,"pos":o,"new_pos":n,"result":chr(n+b),"op":f"'{c}'({o})+'{kc}'({sh})={chr(n+b)}({n})"})
                ki += 1
            else: steps.append({"char":c,"pos":"—","new_pos":"—","result":c,"op":"Non-alpha"})
        return steps
    @staticmethod 
    def get_mapping(k):
        kw = str(k).upper()
        if not kw.isalpha(): return []
        return [(kc, {chr(i+65):chr((i+ord(kc)-65)%26+65) for i in range(26)}) for kc in kw[:4]]

class AtbashCipher:
    @staticmethod 
    def name(): return "Atbash Cipher"
    @staticmethod 
    def icon(): return "🔄"
    @staticmethod 
    def category(): return "Substitution"
    @staticmethod 
    def difficulty(): return "Beginner"
    @staticmethod 
    def encrypt(t, _=None):
        r = []
        for c in t:
            if c.isupper(): r.append(chr(90-(ord(c)-65)))
            elif c.islower(): r.append(chr(122-(ord(c)-97)))
            else: r.append(c)
        return ''.join(r)
    @staticmethod 
    def decrypt(t, _=None): return AtbashCipher.encrypt(t)
    @staticmethod 
    def key_info(): return {"type":"none","label":"None (fixed)"}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>Atbash</h3><p>Mirrors alphabet: E(x)=(25−x) mod 26. Encryption=decryption.</p>"
    @staticmethod 
    def get_steps(t, _=None, e=True):
        steps = []
        for c in t:
            if c.isalpha():
                b = ord('A') if c.isupper() else ord('a'); o = ord(c)-b; n = 25-o
                steps.append({"char":c,"pos":o,"new_pos":n,"result":chr(n+b),"op":f"25−{o}={n}"})
            else: steps.append({"char":c,"pos":"—","new_pos":"—","result":c,"op":"Non-alpha"})
        return steps
    @staticmethod 
    def get_mapping(_=None): return {chr(i+65):chr(25-i+65) for i in range(26)}

class ROT13Cipher:
    @staticmethod 
    def name(): return "ROT13"
    @staticmethod 
    def icon(): return "🔁"
    @staticmethod 
    def category(): return "Substitution"
    @staticmethod 
    def difficulty(): return "Beginner"
    @staticmethod 
    def encrypt(t, _=None): return CaesarCipher.encrypt(t, 13)
    @staticmethod 
    def decrypt(t, _=None): return CaesarCipher.encrypt(t, 13)
    @staticmethod 
    def key_info(): return {"type":"none","label":"None (shift 13)"}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>ROT13</h3><p>Caesar shift=13. Self-inverse.</p>"
    @staticmethod 
    def get_steps(t, _=None, e=True):
        steps = []
        for c in t:
            if c.isalpha():
                b = ord('A') if c.isupper() else ord('a'); o = ord(c)-b; n = (o+13)%26
                steps.append({"char":c,"pos":o,"new_pos":n,"result":chr(n+b),"op":f"({o}+13) mod 26={n}"})
            else: steps.append({"char":c,"pos":"—","new_pos":"—","result":c,"op":"Non-alpha"})
        return steps
    @staticmethod 
    def get_mapping(_=None): return {chr(i+65):chr((i+13)%26+65) for i in range(26)}

class AffineCipher:
    @staticmethod 
    def name(): return "Affine Cipher"
    @staticmethod 
    def icon(): return "📐"
    @staticmethod 
    def category(): return "Mathematical"
    @staticmethod 
    def difficulty(): return "Advanced"
    @staticmethod 
    def mod_inverse(a, m):
        for x in range(1, m):
            if (a*x)%m == 1: return x
        return None
    @staticmethod 
    def encrypt(t, k):
        a, b = int(k[0]), int(k[1])
        if AffineCipher.mod_inverse(a, 26) is None: return "Error: 'a' coprime with 26 needed"
        r = []
        for c in t:
            if c.isupper(): r.append(chr((a*(ord(c)-65)+b)%26+65))
            elif c.islower(): r.append(chr((a*(ord(c)-97)+b)%26+97))
            else: r.append(c)
        return ''.join(r)
    @staticmethod 
    def decrypt(t, k):
        a, b = int(k[0]), int(k[1]); ai = AffineCipher.mod_inverse(a, 26)
        if ai is None: return "Error: 'a' coprime with 26 needed"
        r = []
        for c in t:
            if c.isupper(): r.append(chr((ai*((ord(c)-65)-b))%26+65))
            elif c.islower(): r.append(chr((ai*((ord(c)-97)-b))%26+97))
            else: r.append(c)
        return ''.join(r)
    @staticmethod 
    def key_info(): return {"type":"pair","label":"Key (a, b)","label_a":"a","label_b":"b","default_a":5,"default_b":8,"valid_a":[1,3,5,7,9,11,15,17,19,21,23,25]}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>Affine</h3><p>E(x)=(a·x+b) mod 26. 'a' coprime with 26.</p>"
    @staticmethod 
    def get_steps(t, k, e=True):
        a, b = int(k[0]), int(k[1]); ai = AffineCipher.mod_inverse(a, 26); steps = []
        for c in t:
            if c.isalpha():
                b2 = ord('A') if c.isupper() else ord('a'); o = ord(c)-b2
                if e: n = (a*o+b)%26; ops = f"({a}×{o}+{b}) mod 26={n}"
                else: n = (ai*(o-b))%26; ops = f"({ai}×({o}−{b})) mod 26={n}"
                steps.append({"char":c,"pos":o,"new_pos":n,"result":chr(n+b2),"op":ops})
            else: steps.append({"char":c,"pos":"—","new_pos":"—","result":c,"op":"Non-alpha"})
        return steps
    @staticmethod 
    def get_mapping(k):
        a, b = int(k[0]), int(k[1])
        if AffineCipher.mod_inverse(a, 26) is None: return {}
        return {chr(i+65):chr((a*i+b)%26+65) for i in range(26)}
    @staticmethod 
    def brute_force(t):
        r = []
        for a in [1,3,5,7,9,11,15,17,19,21,23,25]:
            for b in range(26): r.append((a, b, AffineCipher.decrypt(t, (a,b))))
        return r

class RailFenceCipher:
    @staticmethod 
    def name(): return "Rail Fence Cipher"
    @staticmethod 
    def icon(): return "🚂"
    @staticmethod 
    def category(): return "Transposition"
    @staticmethod 
    def difficulty(): return "Intermediate"
    @staticmethod 
    def encrypt(t, rails):
        rails = int(rails)
        if rails < 2 or not t: return t
        fence = [[] for _ in range(rails)]; rail, d = 0, 1
        for c in t:
            fence[rail].append(c)
            if rail == 0: d = 1
            elif rail == rails-1: d = -1
            rail += d
        return ''.join(''.join(row) for row in fence)
    @staticmethod 
    def decrypt(t, rails):
        rails = int(rails)
        if rails < 2 or not t: return t
        n = len(t); pat, rail, d = [], 0, 1
        for _ in range(n):
            pat.append(rail)
            if rail == 0: d = 1
            elif rail == rails-1: d = -1
            rail += d
        lens = [0]*rails
        for r in pat: lens[r] += 1
        pos, st = [0]*rails, 0
        for r in range(rails): pos[r] = st; st += lens[r]
        res = ['']*n
        for i in range(n): r = pat[i]; res[i] = t[pos[r]]; pos[r] += 1
        return ''.join(res)
    @staticmethod 
    def key_info(): return {"type":"int","label":"Rails","min":2,"max":10,"default":3}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>Rail Fence</h3><p>Zigzag transposition across N rails.</p>"
    @staticmethod 
    def get_steps(t, k, e=True):
        rails = int(k); steps = []
        if e and t:
            fence = [[] for _ in range(rails)]; rail, d = 0, 1
            for c in t:
                fence[rail].append(c)
                if rail == 0: d = 1
                elif rail == rails-1: d = -1
                rail += d
            for r in range(rails):
                ch = ''.join(fence[r])
                if ch: steps.append(f"Rail {r}: {ch}")
        return steps
    @staticmethod 
    def get_mapping(_=None): return {}
    @staticmethod 
    def brute_force(t): return [(i, RailFenceCipher.decrypt(t,i)) for i in range(2,11)]

class XORCipher:
    @staticmethod 
    def name(): return "XOR Cipher"
    @staticmethod 
    def icon(): return "⊕"
    @staticmethod 
    def category(): return "Bitwise"
    @staticmethod 
    def difficulty(): return "Intermediate"
    @staticmethod 
    def encrypt(t, k):
        k = str(k)
        if not k: return t
        r = []
        for i, c in enumerate(t):
            xv = ord(c) ^ ord(k[i%len(k)]); r.append(chr(xv) if 32 <= xv <= 126 else f'\\x{xv:02x}')
        return ''.join(r)
    @staticmethod 
    def decrypt(t, k): return XORCipher.encrypt(t, k)
    @staticmethod 
    def key_info(): return {"type":"text","label":"Key","default":"KEY"}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>XOR</h3><p>Bitwise XOR. Enc=Dec. Random key=OTP (unbreakable).</p>"
    @staticmethod 
    def get_steps(t, k, e=True):
        k = str(k)
        if not k: return []; steps = []
        for i, c in enumerate(t):
            kc = k[i%len(k)]; xv = ord(c) ^ ord(kc); d = chr(xv) if 32 <= xv <= 126 else f'\\x{xv:02x}'
            steps.append({"char":c,"pos":f"0x{ord(c):02X}","new_pos":f"0x{xv:02X}","result":d,"op":f"'{c}'⊕'{kc}'=0x{xv:02X}"})
        return steps
    @staticmethod 
    def get_mapping(_=None): return {}

class SubstitutionCipher:
    @staticmethod 
    def name(): return "Simple Substitution"
    @staticmethod 
    def icon(): return "📝"
    @staticmethod 
    def category(): return "Substitution"
    @staticmethod 
    def difficulty(): return "Intermediate"
    @staticmethod 
    def encrypt(t, a):
        a = str(a).upper()
        if len(a) != 26 or len(set(a)) != 26 or not a.isalpha(): return "Error: 26 unique letters"
        r = []
        for c in t:
            if c.isupper(): r.append(a[ord(c)-65])
            elif c.islower(): r.append(a[ord(c)-97].lower())
            else: r.append(c)
        return ''.join(r)
    @staticmethod 
    def decrypt(t, a):
        a = str(a).upper()
        if len(a) != 26 or len(set(a)) != 26 or not a.isalpha(): return "Error: 26 unique letters"
        inv = {a[i]: chr(i+65) for i in range(26)}; r = []
        for c in t:
            if c.isupper(): r.append(inv.get(c, c))
            elif c.islower(): r.append(inv.get(c.upper(), c).lower())
            else: r.append(c)
        return ''.join(r)
    @staticmethod 
    def key_info(): return {"type":"text","label":"Subst. Alphabet","default":"QWERTYUIOPASDFGHJKLZXCVBNM"}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>Simple Substitution</h3><p>Full 26-letter permutation. 26!≈4×10²⁶ keys.</p>"
    @staticmethod 
    def get_steps(t, k, e=True):
        a = str(k).upper()
        if len(a) != 26 or not a.isalpha(): return []
        steps = []
        for c in t:
            if c.isalpha():
                b = ord('A') if c.isupper() else ord('a'); o = ord(c)-b
                if e:
                    nc = a[o]; steps.append({"char":c,"pos":o,"new_pos":f"→{nc}","result":nc if c.isupper() else nc.lower(),"op":f"'{c}'→'{nc}'"})
                else:
                    inv = {a[i]: chr(i+65) for i in range(26)}; nc = inv.get(c.upper(), c)
                    steps.append({"char":c,"pos":"inv","new_pos":f"→{nc}","result":nc if c.isupper() else nc.lower(),"op":f"'{c}'→'{nc}'"})
            else: steps.append({"char":c,"pos":"—","new_pos":"—","result":c,"op":"Non-alpha"})
        return steps
    @staticmethod 
    def get_mapping(k):
        a = str(k).upper()
        if len(a) != 26 or not a.isalpha(): return {}
        return {chr(i+65): a[i] for i in range(26)}

class PlayfairCipher:
    @staticmethod 
    def name(): return "Playfair Cipher"
    @staticmethod 
    def icon(): return "♟️"
    @staticmethod 
    def category(): return "Digraphic"
    @staticmethod 
    def difficulty(): return "Advanced"
    @staticmethod 
    def _grid(kw):
        kw = str(kw).upper().replace('J', 'I'); seen = set(); g = []
        for c in kw:
            if c.isalpha() and c not in seen: seen.add(c); g.append(c)
        for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
            if c not in seen: seen.add(c); g.append(c)
        return [g[i*5:(i+1)*5] for i in range(5)]
    @staticmethod 
    def _pos(grid, ch):
        for r in range(5):
            for c in range(5):
                if grid[r][c] == ch: return (r, c)
        return (0, 0)
    @staticmethod 
    def encrypt(t, kw):
        grid = PlayfairCipher._grid(kw); t = ''.join(c.upper() for c in t if c.isalpha()).replace('J', 'I')
        if not t: return ""
        pairs, i = [], 0
        while i < len(t):
            a = t[i]
            if i+1 < len(t):
                b = t[i+1]
                if a == b: pairs.append((a, 'X')); i += 1
                else: pairs.append((a, b)); i += 2
            else: pairs.append((a, 'X')); i += 1
        r = []
        for a, b in pairs:
            r1, c1 = PlayfairCipher._pos(grid, a); r2, c2 = PlayfairCipher._pos(grid, b)
            if r1 == r2: r.append(grid[r1][(c1+1)%5]); r.append(grid[r2][(c2+1)%5])
            elif c1 == c2: r.append(grid[(r1+1)%5][c1]); r.append(grid[(r2+1)%5][c2])
            else: r.append(grid[r1][c2]); r.append(grid[r2][c1])
        return ''.join(r)
    @staticmethod 
    def decrypt(t, kw):
        grid = PlayfairCipher._grid(kw); t = ''.join(c.upper() for c in t if c.isalpha()).replace('J', 'I')
        if len(t) % 2 != 0: t += 'X'; r = []
        for i in range(0, len(t), 2):
            a, b = t[i], t[i+1]; r1, c1 = PlayfairCipher._pos(grid, a); r2, c2 = PlayfairCipher._pos(grid, b)
            if r1 == r2: r.append(grid[r1][(c1-1)%5]); r.append(grid[r2][(c2-1)%5])
            elif c1 == c2: r.append(grid[(r1-1)%5][c1]); r.append(grid[(r2-1)%5][c2])
            else: r.append(grid[r1][c2]); r.append(grid[r2][c1])
        return ''.join(r)
    @staticmethod 
    def key_info(): return {"type":"text","label":"Keyword","default":"PLAYFAIR"}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>Playfair</h3><p>Digraphic 5×5 grid cipher. I/J share cell.</p>"
    @staticmethod 
    def get_steps(t, k, e=True):
        grid = PlayfairCipher._grid(k); cl = ''.join(c.upper() for c in t if c.isalpha()).replace('J', 'I')
        steps = [f"Grid: {''.join(''.join(row) for row in grid)}"]; pairs, i = [], 0
        while i < len(cl):
            a = cl[i]
            if i+1 < len(cl):
                b = cl[i+1]
                if a == b: pairs.append((a, 'X')); i += 1
                else: pairs.append((a, b)); i += 2
            else: pairs.append((a, 'X')); i += 1
        for a, b in pairs:
            r1, c1 = PlayfairCipher._pos(grid, a); r2, c2 = PlayfairCipher._pos(grid, b)
            rule = "Same row→right" if r1 == r2 else ("Same col→down" if c1 == c2 else "Rect→swap cols")
            steps.append(f"'{a}{b}' @ ({r1},{c1}),({r2},{c2}): {rule}")
        return steps
    @staticmethod 
    def get_mapping(_=None): return {}

class A1Z26Cipher:
    @staticmethod 
    def name(): return "A1Z26"
    @staticmethod 
    def icon(): return "🔢"
    @staticmethod 
    def category(): return "Encoding"
    @staticmethod 
    def difficulty(): return "Beginner"
    @staticmethod 
    def encrypt(t, _=None):
        r = []
        for c in t:
            if c.isupper(): r.append(str(ord(c)-64))
            elif c.islower(): r.append(str(ord(c)-96))
            else: r.append(c)
        return ' '.join(r)
    @staticmethod 
    def decrypt(t, _=None):
        r = []
        for tok in t.split():
            if tok.isdigit():
                n = int(tok)
                if 1 <= n <= 26: r.append(chr(n+64))
                else: r.append(tok)
            else:
                for c in tok: r.append(c)
        return ''.join(r)
    @staticmethod 
    def key_info(): return {"type":"none","label":"None (A=1…Z=26)"}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>A1Z26</h3><p>A=1, B=2, … Z=26. Space-separated numbers.</p>"
    @staticmethod 
    def get_steps(t, _=None, e=True):
        steps = []
        for c in t:
            if c.isalpha(): b = ord('A') if c.isupper() else ord('a'); v = ord(c)-b+1; steps.append({"char":c,"pos":v,"new_pos":v,"result":str(v),"op":f"'{c}'={v}"})
            else: steps.append({"char":c,"pos":"—","new_pos":"—","result":c,"op":"Non-alpha"})
        return steps
    @staticmethod 
    def get_mapping(_=None): return {chr(i+65): str(i+1) for i in range(26)}

class MorseCodeCipher:
    @staticmethod 
    def name(): return "Morse Code"
    @staticmethod 
    def icon(): return "📡"
    @staticmethod 
    def category(): return "Encoding"
    @staticmethod 
    def difficulty(): return "Beginner"
    @staticmethod 
    def encrypt(t, _=None):
        r = []
        for c in t.upper():
            if c in MORSE_CODE: r.append(MORSE_CODE[c])
            elif c == ' ': r.append('/')
            else: r.append(c)
        return ' '.join(r)
    @staticmethod 
    def decrypt(t, _=None):
        r = []
        for tok in t.split():
            if tok == '/': r.append(' ')
            elif tok in MORSE_REVERSE: r.append(MORSE_REVERSE[tok])
            else: r.append(tok)
        return ''.join(r)
    @staticmethod 
    def key_info(): return {"type":"none","label":"None (standard)"}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>Morse Code</h3><p>Samuel Morse, 1836. Dots and dashes for telegraph.</p>"
    @staticmethod 
    def get_steps(t, _=None, e=True):
        steps = []
        for c in t.upper():
            if c in MORSE_CODE: steps.append({"char":c,"pos":MORSE_CODE[c],"new_pos":"—","result":MORSE_CODE[c],"op":f"'{c}'→{MORSE_CODE[c]}"})
            elif c == ' ': steps.append({"char":"⎵","pos":"/","new_pos":"—","result":"/","op":"Space→/"})
            else: steps.append({"char":c,"pos":"—","new_pos":"—","result":c,"op":"Unknown"})
        return steps
    @staticmethod 
    def get_mapping(_=None): return {chr(i+65): MORSE_CODE.get(chr(i+65), '?') for i in range(26)}

class BaconianCipher:
    @staticmethod 
    def name(): return "Baconian Cipher"
    @staticmethod 
    def icon(): return "🥓"
    @staticmethod 
    def category(): return "Steganographic"
    @staticmethod 
    def difficulty(): return "Intermediate"
    @staticmethod 
    def encrypt(t, _=None):
        r = []
        for c in t.upper():
            if c.isalpha(): v = ord(c)-65; b = '{0:05b}'.format(v).replace('0','A').replace('1','B'); r.append(b)
            else: r.append(c)
        return ' '.join(r)
    @staticmethod 
    def decrypt(t, _=None):
        r = []
        for tok in t.split():
            if all(c in 'ABab' for c in tok) and len(tok) == 5:
                bits = tok.upper().replace('A','0').replace('B','1'); v = int(bits, 2)
                if 0 <= v <= 25: r.append(chr(v+65))
                else: r.append(tok)
            else: r.append(tok)
        return ''.join(r)
    @staticmethod 
    def key_info(): return {"type":"none","label":"None (A=AAAAA…Z=BBAAB)"}
    @staticmethod 
    def description(): return "<h3 style='color:#89b4fa'>Baconian</h3><p>Francis Bacon, 1605. 5-bit binary with A/B forms.</p>"
    @staticmethod 
    def get_steps(t, _=None, e=True):
        steps = []
        for c in t.upper():
            if c.isalpha(): v = ord(c)-65; b = '{0:05b}'.format(v).replace('0','A').replace('1','B'); steps.append({"char":c,"pos":v,"new_pos":b,"result":b,"op":f"'{c}'({v})={v:05b}→{b}"})
            else: steps.append({"char":c,"pos":"—","new_pos":"—","result":c,"op":"Non-alpha"})
        return steps
    @staticmethod
    def get_mapping(_=None): return {chr(i+65): '{0:05b}'.format(i).replace('0','A').replace('1','B') for i in range(26)}

CIPHERS = [CaesarCipher, VigenereCipher, AtbashCipher, ROT13Cipher, AffineCipher, RailFenceCipher, XORCipher, SubstitutionCipher, PlayfairCipher, A1Z26Cipher, MorseCodeCipher, BaconianCipher]

# ═══════════════════════════════════════════════════════════════
#  HISTORY & TOAST
# ═══════════════════════════════════════════════════════════════

class EncryptionHistory:
    def __init__(self): self.records = []
    def add(self, cn, d, p, c, ks):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.records.append({"time":ts,"cipher":cn,"dir":d,"plain":p[:80],"cipher_text":c[:80],"key":ks})
        if len(self.records) > 100: self.records = self.records[-100:]
    def clear(self): self.records = []

HISTORY = EncryptionHistory()

class ToastWidget(QFrame):
    def __init__(self, text, parent=None, duration=2500):
        super().__init__(parent)
        self.setStyleSheet("QFrame{background:#45475a;border:1px solid #585b70;border-radius:10px;padding:12px 20px;}")
        lay = QVBoxLayout(self)
        lbl = QLabel(text); lbl.setStyleSheet("color:#cdd6f4;font-size:13px;font-weight:bold;background:transparent;")
        lay.addWidget(lbl)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.adjustSize()
        if parent:
            px = parent.x() + parent.width() - self.width() - 30
            py = parent.y() + 60
            self.move(px, py)
        self.show()
        QTimer.singleShot(duration, self._fade_out)

    def _fade_out(self):
        eff = QGraphicsOpacityEffect(self); self.setGraphicsEffect(eff)
        self._anim = QPropertyAnimation(eff, b"opacity")
        self._anim.setDuration(400); self._anim.setStartValue(1.0); self._anim.setEndValue(0.0)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.finished.connect(self.close); self._anim.start()

# ═══════════════════════════════════════════════════════════════
#  CUSTOM WIDGETS
# ═══════════════════════════════════════════════════════════════

class AlphabetWidget(QWidget):
    def __init__(self, p=None): super().__init__(p); self.mapping={}; self.multi=[]; self.is_text=False; self.setMinimumHeight(120); self.setMaximumHeight(180)
    def set_mapping(self, m, it=False): self.mapping=m or{}; self.multi=[]; self.is_text=it; self.update()
    def set_multi_mappings(self, m): self.multi=m or[]; self.mapping={}; self.is_text=False; self.update()
    def paintEvent(self, ev):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        if not self.mapping and not self.multi: p.setPen(QColor("#a6adc8")); p.setFont(QFont("Segoe UI",12)); p.drawText(self.rect(), Qt.AlignCenter, "Select cipher & key"); p.end(); return
        if self.multi: self._multi(p)
        elif self.is_text: self._text(p)
        else: self._single(p)
        p.end()

    def _single(self, p):
        w = self.width(); bw = min(34, (w-20)//26); bh = 28; g = 2; sx = max(5, (w-26*(bw+g))//2); y1 = 10
        p.setFont(QFont("Consolas", 10, QFont.Bold))
        for i in range(26): x = sx+i*(bw+g); p.setBrush(QBrush(QColor("#45475a"))); p.setPen(Qt.NoPen); p.drawRoundedRect(x,y1,bw,bh,3,3); p.setPen(QColor("#cdd6f4")); p.drawText(QRect(x,y1,bw,bh), Qt.AlignCenter, chr(i+65))
        ya = y1+bh+2; p.setPen(QColor("#89b4fa")); p.setFont(QFont("Segoe UI", 9))
        for i in range(26): x = sx+i*(bw+g); p.drawText(QRect(x,ya,bw,14), Qt.AlignCenter, "↓")
        y2 = ya+14
        for i in range(26):
            x = sx+i*(bw+g); l = chr(i+65); m = self.mapping.get(l,l); ch = m!=l
            p.setBrush(QBrush(QColor("#89b4fa") if ch else QColor("#585b70"))); p.setPen(Qt.NoPen); p.drawRoundedRect(x,y2,bw,bh,3,3)
            p.setPen(QColor("#1e1e2e") if ch else QColor("#cdd6f4")); p.setFont(QFont("Consolas", 10, QFont.Bold)); p.drawText(QRect(x,y2,bw,bh), Qt.AlignCenter, m)

    def _text(self, p):
        w = self.width(); cw = max(60, min(100, (w-20)//6)); rh = 28; cols = 6; sx = max(5, (w-cols*cw)//2); sy = 10
        for idx in range(26):
            r = idx//cols; c = idx%cols; x = sx+c*cw; y = sy+r*(rh+6); l = chr(idx+65); m = self.mapping.get(l, '?')
            p.setBrush(QBrush(QColor("#45475a"))); p.setPen(Qt.NoPen); p.drawRoundedRect(x,y,24,rh,3,3)
            p.setPen(QColor("#cdd6f4")); p.setFont(QFont("Consolas", 10, QFont.Bold)); p.drawText(QRect(x,y,24,rh), Qt.AlignCenter, l)
            p.setBrush(QBrush(QColor("#89b4fa"))); p.setPen(Qt.NoPen); p.drawRoundedRect(x+26,y,max(cw-28,30),rh,3,3)
            p.setPen(QColor("#1e1e2e")); p.setFont(QFont("Consolas", 8, QFont.Bold)); d = m if len(m) <= 5 else m[:4]+"…"
            p.drawText(QRect(x+26,y,max(cw-28,30),rh), Qt.AlignCenter, d)

    def _multi(self, p):
        w = self.width(); nm = min(4, len(self.multi)); bw = min(26, (w-20)//26); bh = 22; g = 1; sx = max(5, (w-26*(bw+g))//2)
        y = 5; p.setFont(QFont("Consolas", 8, QFont.Bold))
        for i in range(26): x = sx+i*(bw+g); p.setBrush(QBrush(QColor("#45475a"))); p.setPen(Qt.NoPen); p.drawRoundedRect(x,y,bw,bh,2,2); p.setPen(QColor("#cdd6f4")); p.drawText(QRect(x,y,bw,bh), Qt.AlignCenter, chr(i+65))
        cs = [QColor("#89b4fa"), QColor("#a6e3a1"), QColor("#f9e2af"), QColor("#f38ba8")]
        for mi in range(nm):
            kc, mp = self.multi[mi]; y = 5+(bh+5)*(mi+1); col = cs[mi%len(cs)]
            for i in range(26): x = sx+i*(bw+g); m = mp.get(chr(i+65), chr(i+65)); p.setBrush(QBrush(col)); p.setPen(Qt.NoPen); p.drawRoundedRect(x,y,bw,bh,2,2); p.setPen(QColor("#1e1e2e")); p.setFont(QFont("Consolas", 8, QFont.Bold)); p.drawText(QRect(x,y,bw,bh), Qt.AlignCenter, m)
            p.setPen(col); p.setFont(QFont("Segoe UI", 9, QFont.Bold)); p.drawText(sx-42, y+bh//2+4, f"K={kc}")

class StepTableWidget(QWidget):
    def __init__(self, p=None):
        super().__init__(p); l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        self.t = QTableWidget(); self.t.setColumnCount(5); self.t.setHorizontalHeaderLabels(["Input","Pos","Op","New","Output"])
        self.t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); self.t.setAlternatingRowColors(True)
        self.t.setEditTriggers(QTableWidget.NoEditTriggers); self.t.setMaximumHeight(300); l.addWidget(self.t)
    def set_steps(self, steps):
        self.t.setRowCount(len(steps))
        for r, s in enumerate(steps):
            if isinstance(s, dict):
                vs = [str(s.get(k, "")) for k in ("char","pos","op","new_pos","result")]
                for c, v in enumerate(vs):
                    it = QTableWidgetItem(v); it.setTextAlignment(Qt.AlignCenter)
                    if c == 0: it.setForeground(QBrush(QColor("#89b4fa"))); it.setFont(QFont("Consolas", 12, QFont.Bold))
                    elif c == 4: it.setForeground(QBrush(QColor("#a6e3a1"))); it.setFont(QFont("Consolas", 12, QFont.Bold))
                    self.t.setItem(r, c, it)
            elif isinstance(s, str):
                it = QTableWidgetItem(s); it.setForeground(QBrush(QColor("#f9e2af"))); it.setFont(QFont("Consolas", 11, QFont.Bold))
                self.t.setSpan(r, 0, 1, 5); self.t.setItem(r, 0, it)
    def clear(self): self.t.setRowCount(0)

class RailFenceVisualizer(QWidget):
    def __init__(self, p=None): super().__init__(p); self.text=""; self.rails=3; self.setMinimumHeight(160); self.setMaximumHeight(260)
    def set_data(self, t, r): self.text=t; self.rails=max(2,int(r)); self.update()
    def paintEvent(self, ev):
        if not self.text: return
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing); w, h = self.width(), self.height(); n = len(self.text)
        if n == 0: p.end(); return
        cw = min(44, (w-40)//max(n,1)); rh = min(36, (h-20)//max(self.rails,1)); sx = max(10, (w-n*cw)//2); sy = 10
        pos = []; rail, d = 0, 1
        for i in range(n):
            pos.append((i, rail))
            if rail == 0: d = 1
            elif rail == self.rails-1: d = -1
            rail += d
        pen = QPen(QColor("#45475a"), 1, Qt.DashLine); p.setPen(pen)
        for idx in range(len(pos)-1):
            x1=sx+pos[idx][0]*cw+cw//2; y1=sy+pos[idx][1]*rh+rh//2; x2=sx+pos[idx+1][0]*cw+cw//2; y2=sy+pos[idx+1][1]*rh+rh//2
            p.drawLine(x1,y1,x2,y2)
        rc = [QColor("#89b4fa"), QColor("#a6e3a1"), QColor("#f9e2af"), QColor("#f38ba8"), QColor("#cba6f7"), QColor("#94e2d5"), QColor("#fab387"), QColor("#f5c2e7"), QColor("#b4befe"), QColor("#89dceb")]
        for i, r in pos:
            cx=sx+i*cw+cw//2; cy=sy+r*rh+rh//2; col=rc[r%len(rc)]
            p.setBrush(QBrush(col)); p.setPen(Qt.NoPen); rad=min(cw,rh)//2-2
            p.drawEllipse(cx-rad,cy-rad,rad*2,rad*2); p.setPen(QColor("#1e1e2e")); p.setFont(QFont("Consolas", max(8,rad-1), QFont.Bold))
            p.drawText(QRect(cx-rad,cy-rad,rad*2,rad*2), Qt.AlignCenter, self.text[i]); p.end()

class PlayfairGridWidget(QWidget):
    def __init__(self, p=None): super().__init__(p); self.grid=[]; self.setMinimumHeight(180); self.setMaximumHeight(220)
    def set_grid(self, kw): self.grid=PlayfairCipher._grid(kw); self.update()
    def paintEvent(self, ev):
        if not self.grid: return
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing); w, h = self.width(), self.height(); cell = min(40, (w-40)//5, (h-20)//5)
        sx = (w-5*cell)//2; sy = (h-5*cell)//2
        for r in range(5):
            for c in range(5):
                x=sx+c*cell; y=sy+r*cell; p.setBrush(QBrush(QColor("#313244") if (r+c)%2==0 else QColor("#383850")))
                p.setPen(QPen(QColor("#585b70"), 1)); p.drawRoundedRect(x,y,cell-2,cell-2,4,4)
                p.setPen(QColor("#89b4fa")); p.setFont(QFont("Consolas", cell//2-2, QFont.Bold)); p.drawText(QRect(x,y,cell-2,cell-2), Qt.AlignCenter, self.grid[r][c])
        p.end()

class FrequencyWidget(QWidget):
    def __init__(self, p=None): super().__init__(p); self.freqs={}; self.setMinimumHeight(220); self.setMaximumHeight(280)
    def set_text(self, t):
        ls = [c.upper() for c in t if c.isalpha()]; tot = len(ls)
        if tot == 0: self.freqs={}; self.update(); return
        ct = Counter(ls); self.freqs = {c:(ct.get(c,0)/tot)*100 for c in string.ascii_uppercase}; self.update()
    def paintEvent(self, ev):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing); w, h = self.width(), self.height()
        if not self.freqs: p.setPen(QColor("#a6adc8")); p.setFont(QFont("Segoe UI", 12)); p.drawText(self.rect(), Qt.AlignCenter, "Enter text"); p.end(); return
        ml, mb, mt = 40, 30, 20; cw = w-ml-20; ch = h-mb-mt; bw = max(6, cw//26-2); g = 2; sx = ml+(cw-26*(bw+g))//2; mv = 15
        p.setPen(QPen(QColor("#45475a"), 1, Qt.DotLine))
        for pct in range(0, 16, 5):
            y = mt+ch-int(pct/mv*ch); p.drawLine(sx,y,sx+26*(bw+g),y); p.setPen(QColor("#585b70")); p.setFont(QFont("Segoe UI", 8))
            p.drawText(ml-38,y-4,36,16,Qt.AlignRight|Qt.AlignVCenter, f"{pct}%"); p.setPen(QPen(QColor("#45475a"), 1, Qt.DotLine))
        for i in range(26):
            l = chr(i+65); x = sx+i*(bw+g); ep = ENGLISH_FREQ.get(l,0); eh = int(ep/mv*ch); ye = mt+ch-eh
            p.setBrush(QBrush(QColor(166,173,200,60))); p.setPen(Qt.NoPen); p.drawRect(x,ye,bw,eh)
            tp = self.freqs.get(l,0); th = int(tp/mv*ch); yt = mt+ch-th
            p.setBrush(QBrush(QColor("#89b4fa"))); p.drawRect(x,yt,bw,th)
            p.setPen(QColor("#a6adc8")); p.setFont(QFont("Consolas", 8, QFont.Bold)); p.drawText(QRect(x-1,mt+ch+4,bw+2,18), Qt.AlignCenter, l)
        p.end()

# ═══════════════════════════════════════════════════════════════
#  CIPHER PAGE
# ═══════════════════════════════════════════════════════════════

class CipherPage(QWidget):
    def __init__(self, cc, p=None):
        super().__init__(p); self.cipher=cc; self.quiz_answer=""; self.quiz_key=None
        self.correct=0; self.wrong=0; self.streak=0; self.timer_secs=0
        self.quiz_timer=QTimer(); self.quiz_timer.setInterval(1000)
        self.quiz_timer.timeout.connect(lambda: (setattr(self, 'timer_secs', self.timer_secs+1), self.timer_lbl.setText(f"⏱ {self.timer_secs}s")))
        self._build()

    def _build(self):
        root = QVBoxLayout(self); root.setContentsMargins(16,8,16,16); root.setSpacing(8)
        hdr = QFrame(); hl = QHBoxLayout(hdr); hl.setContentsMargins(0,0,0,0)
        ic = QLabel(self.cipher.icon()); ic.setFont(QFont("Segoe UI Emoji", 28)); ic.setStyleSheet("background:transparent;")
        info = QVBoxLayout(); nm = QLabel(self.cipher.name()); nm.setStyleSheet("font-size:24px;font-weight:bold;color:#89b4fa;background:transparent;")
        meta = QHBoxLayout()
        for t in [f"📁 {self.cipher.category()}", f"⭐ {self.cipher.difficulty()}"]:
            ml = QLabel(t); ml.setStyleSheet("color:#a6adc8;font-size:12px;background:transparent;"); meta.addWidget(ml)
        meta.addStretch(); info.addWidget(nm); info.addLayout(meta); hl.addWidget(ic); hl.addLayout(info, 1); root.addWidget(hdr)
        self.tabs = QTabWidget()
        self.tabs.addTab(self._tab_learn(), "📖 Learn")
        self.tabs.addTab(self._tab_encode(), "🔐 Encode/Decode")
        self.tabs.addTab(self._tab_analysis(), "📊 Analysis")
        if hasattr(self.cipher, 'brute_force'): self.tabs.addTab(self._tab_brute(), "🔨 Brute Force")
        self.tabs.addTab(self._tab_practice(), "🎯 Practice")
        root.addWidget(self.tabs)

    def _bki(self, lay, pfx, ki):
        t = ki["type"]
        if t == "int":
            sb = QSpinBox(); sb.setRange(ki.get("min",0), ki.get("max",25)); sb.setValue(ki.get("default",3)); setattr(self, f"{pfx}_ks", sb); sb.valueChanged.connect(self._mp(pfx)); lay.addWidget(sb)
        elif t == "text":
            le = QLineEdit(ki.get("default","")); le.setMaxLength(50); setattr(self, f"{pfx}_kt", le); le.textChanged.connect(self._mp(pfx)); lay.addWidget(le)
            if self.cipher is SubstitutionCipher: rb = QPushButton("🎲"); rb.setObjectName("smallBtn"); rb.clicked.connect(lambda: self._rsub(pfx)); lay.addWidget(rb)
        elif t == "pair":
            cb = QComboBox(); cb.addItems([str(v) for v in ki.get("valid_a",[1])]); cb.setCurrentText(str(ki.get("default_a",5))); setattr(self, f"{pfx}_ka", cb)
            sb = QSpinBox(); sb.setRange(0,25); sb.setValue(ki.get("default_b",8)); setattr(self, f"{pfx}_kb", sb)
            lay.addWidget(QLabel("a:")); lay.addWidget(cb); lay.addWidget(QLabel("b:")); lay.addWidget(sb)
            cb.currentTextChanged.connect(self._mp(pfx)); sb.valueChanged.connect(self._mp(pfx))
        elif t == "none": lbl = QLabel("No key"); lbl.setStyleSheet("color:#a6adc8;font-style:italic;"); lay.addWidget(lbl)

    def _mp(self, pfx):
        def f():
            if pfx == "learn": self._rlm()
        return f

    def _kv(self, pfx):
        ki = self.cipher.key_info(); t = ki["type"]
        if t == "int": return getattr(self, f"{pfx}_ks").value()
        if t == "text": return getattr(self, f"{pfx}_kt").text()
        if t == "pair": return (int(getattr(self, f"{pfx}_ka").currentText()), getattr(self, f"{pfx}_kb").value())
        return None

    def _rsub(self, pfx):
        a = list(string.ascii_uppercase)
        random.shuffle(a)
        le = getattr(self, f"{pfx}_kt", None)
        if le:
            le.setText(''.join(a))

    def _rlm(self):
        k = self._kv("learn"); m = self.cipher.get_mapping(k); it = self.cipher in (A1Z26Cipher, MorseCodeCipher, BaconianCipher)
        if isinstance(m, dict) and m: self.learn_alpha.set_mapping(m, it)
        elif isinstance(m, list): self.learn_alpha.set_multi_mappings(m)
        else: self.learn_alpha.set_mapping({})
        if self.cipher is PlayfairCipher and hasattr(self, 'pf_grid'): self.pf_grid.set_grid(str(k) if k else "PLAYFAIR")

    def _tab_learn(self):
        w = QWidget(); l = QVBoxLayout(w); d = QTextEdit(); d.setHtml(self.cipher.description()); d.setReadOnly(True); d.setMaximumHeight(300)
        d.setStyleSheet("QTextEdit{background:#313244;border:1px solid #45475a;border-radius:8px;padding:12px;}"); l.addWidget(d)
        ag = QGroupBox("Alphabet Mapping"); al = QVBoxLayout(ag); self.learn_alpha = AlphabetWidget(); al.addWidget(self.learn_alpha)
        ki = self.cipher.key_info()
        if ki["type"] != "none": row = QHBoxLayout(); row.addWidget(QLabel("Key:")); self._bki(row, "learn", ki); row.addStretch(); al.addLayout(row); self._rlm()
        else: self._rlm()
        l.addWidget(ag)
        if self.cipher is PlayfairCipher:
            pg = QGroupBox("5×5 Grid"); pl = QVBoxLayout(pg); self.pf_grid = PlayfairGridWidget(); pl.addWidget(self.pf_grid); self._rlm(); l.addWidget(pg)
        return w

    def _tab_encode(self):
        w = QWidget(); l = QVBoxLayout(w); ig = QGroupBox("Input"); il = QVBoxLayout(ig)
        ki = self.cipher.key_info(); kr = QHBoxLayout(); kr.addWidget(QLabel(f"🔑 {ki.get('label', 'Key')}:")); self._bki(kr, "enc", ki); kr.addStretch(); il.addLayout(kr)
        tr = QHBoxLayout()
        left = QVBoxLayout(); left.addWidget(QLabel("📝 Plaintext:")); self.pi = QTextEdit(); self.pi.setPlaceholderText("Enter text…"); self.pi.setMaximumHeight(100); left.addWidget(self.pi); tr.addLayout(left)
        btns = QVBoxLayout(); btns.setAlignment(Qt.AlignCenter)
        for tx, nm, sl in [("Encrypt →","successBtn",self._enc), ("← Decrypt","",self._dec), ("⇄ Swap","secondaryBtn",self._swap), ("🗑 Clear","dangerBtn",self._clr)]:
            b = QPushButton(tx);
            if nm: b.setObjectName(nm)
            b.clicked.connect(sl); btns.addWidget(b)
        tr.addLayout(btns)
        right = QVBoxLayout(); right.addWidget(QLabel("🔒 Ciphertext:")); self.co = QTextEdit(); self.co.setPlaceholderText("Result…"); self.co.setMaximumHeight(100); self.co.setReadOnly(True); right.addWidget(self.co)
        cb = QPushButton("📋 Copy"); cb.setObjectName("smallBtn"); cb.clicked.connect(self._cpo); right.addWidget(cb); tr.addLayout(right)
        il.addLayout(tr); l.addWidget(ig)
        fg = QGroupBox("File I/O"); fl = QHBoxLayout(fg)
        sb = QPushButton("💾 Save Output"); sb.setObjectName("smallBtn"); sb.clicked.connect(self._save_file); fl.addWidget(sb)
        lb = QPushButton("📂 Load Text"); lb.setObjectName("smallBtn"); lb.clicked.connect(self._load_file); fl.addWidget(lb)
        fl.addStretch(); l.addWidget(fg)
        sg = QGroupBox("Step-by-Step"); sl = QVBoxLayout(sg); self.st = StepTableWidget(); sl.addWidget(self.st); l.addWidget(sg)
        self.rf_viz = None
        if self.cipher is RailFenceCipher: rg = QGroupBox("Zigzag"); rl = QVBoxLayout(rg); self.rf_viz = RailFenceVisualizer(); rl.addWidget(self.rf_viz); l.addWidget(rg)
        self.epf = None
        if self.cipher is PlayfairCipher: pg = QGroupBox("Grid"); pl = QVBoxLayout(pg); self.epf = PlayfairGridWidget(); pl.addWidget(self.epf); l.addWidget(pg)
        return w

    def _enc(self):
        t = self.pi.toPlainText(); k = self._kv("enc"); r = self.cipher.encrypt(t, k); self.co.setText(r)
        self.st.set_steps(self.cipher.get_steps(t, k, True))
        if self.rf_viz and self.cipher is RailFenceCipher: self.rf_viz.set_data(t, k)
        if self.epf and self.cipher is PlayfairCipher: self.epf.set_grid(str(k) if k else "PLAYFAIR")
        ks = str(k) if k else "—"; HISTORY.add(self.cipher.name(), "Enc", t, r, ks); self.window().sb.showMessage(f"✅ Encrypted with {self.cipher.name()}")

    def _dec(self):
        t = self.co.toPlainText(); k = self._kv("enc"); r = self.cipher.decrypt(t, k); self.pi.setText(r)
        self.st.set_steps(self.cipher.get_steps(t, k, False))
        ks = str(k) if k else "—"
        HISTORY.add(self.cipher.name(), "Dec", t, r, ks)
        self.window().sb.showMessage(f"✅ Decrypted with {self.cipher.name()}")

    def _swap(self): p, c = self.pi.toPlainText(), self.co.toPlainText(); self.pi.setText(c); self.co.setText(p)
    def _clr(self): self.pi.clear(); self.co.clear(); self.st.clear()
    def _cpo(self): QApplication.clipboard().setText(self.co.toPlainText()); ToastWidget("📋 Copied to clipboard!", self.window())
    def _save_file(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Save Ciphertext", "", "Text Files (*.txt);;All Files (*)")
        if fn:
            with open(fn, 'w', encoding='utf-8') as f: f.write(self.co.toPlainText())
            ToastWidget(f"💾 Saved to {os.path.basename(fn)}", self.window())
    def _load_file(self):
        fn, _ = QFileDialog.getOpenFileName(self, "Load Text", "", "Text Files (*.txt);;All Files (*)")
        if fn:
            with open(fn, 'r', encoding='utf-8') as f: self.pi.setText(f.read())
            ToastWidget(f"📂 Loaded {os.path.basename(fn)}", self.window())

    def _tab_analysis(self):
        w = QWidget(); l = QVBoxLayout(w); info = QLabel("📊 Compare ciphertext frequencies against English averages."); info.setWordWrap(True); info.setStyleSheet("font-size:13px;color:#a6adc8;background:transparent;padding:4px;"); l.addWidget(info)
        ir = QHBoxLayout(); ir.addWidget(QLabel("Text:")); self.ai = QLineEdit(); self.ai.setFont(QFont("Consolas", 13)); self.ai.textChanged.connect(self._ua); ir.addWidget(self.ai)
        pb = QPushButton("📋 Paste"); pb.setObjectName("smallBtn"); pb.clicked.connect(lambda: self.ai.setText(QApplication.clipboard().text())); ir.addWidget(pb); l.addLayout(ir)
        cg = QGroupBox("Chart"); cl = QVBoxLayout(cg); self.fw = FrequencyWidget(); cl.addWidget(self.fw); l.addWidget(cg)
        tg = QGroupBox("Table"); tl = QVBoxLayout(tg); self.ft = QTableWidget(); self.ft.setColumnCount(4); self.ft.setHorizontalHeaderLabels(["Letter","Text %","Eng %","Diff"])
        self.ft.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); self.ft.setEditTriggers(QTableWidget.NoEditTriggers); self.ft.setMaximumHeight(250); tl.addWidget(self.ft); l.addWidget(tg)
        return w
    def _ua(self):
        t = self.ai.text(); self.fw.set_text(t); ls = [c.upper() for c in t if c.isalpha()]; tot = len(ls)
        if tot == 0: self.ft.setRowCount(0); return
        ct = Counter(ls); self.ft.setRowCount(26)
        for i in range(26):
            l = chr(i+65); tp = (ct.get(l,0)/tot)*100; ep = ENGLISH_FREQ.get(l,0); d = tp-ep
            for c, tv in enumerate([l, f"{tp:.2f}%", f"{ep:.2f}%", f"{d:+.2f}%"]):
                it = QTableWidgetItem(tv); it.setTextAlignment(Qt.AlignCenter)
                if c == 0: it.setFont(QFont("Consolas", 11, QFont.Bold)); it.setForeground(QBrush(QColor("#89b4fa")))
                elif c == 3: it.setForeground(QBrush(QColor("#a6e3a1") if abs(d) < 2 else QColor("#f9e2af") if abs(d) < 5 else QColor("#f38ba8")))
                self.ft.setItem(i, c, it)

    def _tab_brute(self):
        w = QWidget(); l = QVBoxLayout(w); info = QLabel("🔨 Try all keys. Click a row to copy."); info.setWordWrap(True); info.setStyleSheet("font-size:13px;color:#a6adc8;background:transparent;"); l.addWidget(info)
        ir = QHBoxLayout(); ir.addWidget(QLabel("Ciphertext:")); self.bi = QLineEdit(); self.bi.setFont(QFont("Consolas", 13)); ir.addWidget(self.bi)
        bb = QPushButton("🔨 Crack!"); bb.clicked.connect(self._rbf); ir.addWidget(bb); l.addLayout(ir)
        self.bt = QTableWidget(); self.bt.setColumnCount(3); self.bt.setHorizontalHeaderLabels(["Key","Result","Score"])
        self.bt.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); self.bt.setEditTriggers(QTableWidget.NoEditTriggers)
        self.bt.setSelectionBehavior(QTableWidget.SelectRows); self.bt.cellClicked.connect(self._bfc); l.addWidget(self.bt)
        self.bfs = QLabel(""); self.bfs.setStyleSheet("color:#a6adc8;font-size:12px;background:transparent;"); l.addWidget(self.bfs); return w
    def _rbf(self):
        t = self.bi.text()
        if not t: self.bfs.setText("⚠ Enter ciphertext."); return
        res = self.cipher.brute_force(t); self.bt.setRowCount(len(res))
        cm = {"THE","AND","FOR","ARE","BUT","NOT","YOU","ALL","CAN","HER","WAS","ONE","OUR","OUT","HAD","HAS","HIS","HOW","ITS","MAY","NEW","NOW","OLD","SEE","WAY","WHO"}
        for r, it in enumerate(res):
            k, d = it[0], it[-1]; ks = str(k) if not isinstance(k, tuple) else f"a={k[0]},b={k[1]}"; u = d.upper(); sc = sum(1 for w in cm if w in u)
            ki2 = QTableWidgetItem(ks); ki2.setTextAlignment(Qt.AlignCenter); ki2.setFont(QFont("Consolas", 10, QFont.Bold)); ki2.setForeground(QBrush(QColor("#89b4fa"))); self.bt.setItem(r, 0, ki2)
            di = QTableWidgetItem(d); di.setFont(QFont("Consolas", 10)); self.bt.setItem(r, 1, di)
            si = QTableWidgetItem(f"{sc}"); si.setTextAlignment(Qt.AlignCenter)
            si.setForeground(QBrush(QColor("#a6e3a1") if sc >= 3 else QColor("#f9e2af") if sc >= 1 else QColor("#585b70"))); self.bt.setItem(r, 2, si)
        self.bt.sortItems(2, Qt.DescendingOrder); self.bfs.setText(f"✅ Tested {len(res)} keys.")
    def _bfc(self, r, c):
        res = self.bt.item(r, 1)
        if res: QApplication.clipboard().setText(res.text()); self.bfs.setText(f"📋 Copied: {res.text()[:60]}…")

    def _tab_practice(self):
        w = QWidget(); l = QVBoxLayout(w); l.setSpacing(12)
        info = QLabel("🧠 Decrypt the message!"); info.setWordWrap(True); info.setStyleSheet("font-size:14px;color:#cdd6f4;background:transparent;"); l.addWidget(info)
        dr = QHBoxLayout(); dr.addWidget(QLabel("Difficulty:")); self.qd = QComboBox(); self.qd.addItems(["Easy","Medium","Hard"]); dr.addWidget(self.qd)
        gb = QPushButton("🔄 New"); gb.clicked.connect(self._gq); dr.addWidget(gb); dr.addStretch(); l.addLayout(dr)
        tr = QHBoxLayout(); self.timer_lbl = QLabel("⏱ 0s"); self.timer_lbl.setStyleSheet("color:#f9e2af;font-size:13px;font-weight:bold;background:transparent;"); tr.addWidget(self.timer_lbl); tr.addStretch(); l.addLayout(tr)
        cg = QGroupBox("Challenge"); cl = QVBoxLayout(cg)
        self.qcl = QLabel(); self.qcl.setStyleSheet("font-size:14px;color:#89b4fa;background:transparent;"); cl.addWidget(self.qcl)
        self.qkl = QLabel(); self.qkl.setStyleSheet("font-size:14px;color:#f9e2af;background:transparent;"); cl.addWidget(self.qkl)
        self.qel = QLabel(); self.qel.setWordWrap(True); self.qel.setStyleSheet("font-size:18px;font-weight:bold;color:#f38ba8;background:#45475a;border-radius:8px;padding:12px;font-family:'Consolas',monospace;"); cl.addWidget(self.qel); l.addWidget(cg)
        ag = QGroupBox("Answer"); al = QVBoxLayout(ag); self.qi = QLineEdit(); self.qi.setPlaceholderText("Type answer…"); self.qi.setFont(QFont("Consolas", 14)); self.qi.returnPressed.connect(self._cq); al.addWidget(self.qi)
        br = QHBoxLayout()
        for tx, nm, sl in [("✓ Check","successBtn",self._cq), ("💡 Hint","secondaryBtn",self._hq), ("👁 Reveal","dangerBtn",self._rq)]:
            b = QPushButton(tx);
            if nm: b.setObjectName(nm)
            b.clicked.connect(sl); br.addWidget(b)
        br.addStretch(); al.addLayout(br); self.qr = QLabel(); self.qr.setAlignment(Qt.AlignCenter); self.qr.setStyleSheet("font-size:16px;background:transparent;"); al.addWidget(self.qr); l.addWidget(ag)
        sg = QGroupBox("Stats"); sl = QHBoxLayout(sg)
        self.sok = QLabel("✅ 0"); self.sok.setStyleSheet("color:#a6e3a1;font-size:14px;background:transparent;")
        self.sba = QLabel("❌ 0"); self.sba.setStyleSheet("color:#f38ba8;font-size:14px;background:transparent;")
        self.sst = QLabel("🔥 0"); self.sst.setStyleSheet("color:#f9e2af;font-size:14px;background:transparent;")
        for s in (self.sok, self.sba, self.sst): sl.addWidget(s); l.addWidget(sg); self._gq(); return w

    def _gq(self):
        self.qr.setText(""); self.qi.setText(""); d = self.qd.currentIndex()
        easy = ["CAT","DOG","SUN","RUN","HAT","BAT","CUP","KEY","BOX","FOX","RED","ICE","SKY","OWL","ANT"]
        med = ["HELLO","WORLD","CIPHER","SECRET","ENIGMA","CRYPTO","PYTHON","ALPHA","DELTA","BRAVO"]
        hard = ["ATTACK AT DAWN","MEET ME AT NOON","THE EAGLE HAS LANDED","STAY FROSTY","MISSION COMPLETE"]
        self.quiz_answer = random.choice([easy, med, hard][d])
        ki = self.cipher.key_info(); t = ki["type"]
        if t == "int": self.quiz_key = random.randint(ki.get("min",1), ki.get("max",25))
        elif t == "text":
            if self.cipher is XORCipher:
                for _ in range(200):
                    k = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                    if all(32 <= (ord(c)^ord(k)) <= 126 for c in self.quiz_answer): self.quiz_key = k; break
                else: self.quiz_key = "A"
            elif self.cipher is SubstitutionCipher: a = list(string.ascii_uppercase); random.shuffle(a); self.quiz_key = ''.join(a)
            else: kl = random.randint(3,6); self.quiz_key = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=kl))
        elif t == "pair": va = ki.get("valid_a",[1,3,5,7,9,11,15,17,19,21,23,25]); self.quiz_key = (random.choice(va), random.randint(0,25))
        else: self.quiz_key = None
        enc = self.cipher.encrypt(self.quiz_answer, self.quiz_key); self.qcl.setText(f"🔐 {self.cipher.name()}")
        if self.quiz_key is not None:
            if isinstance(self.quiz_key, tuple): self.qkl.setText(f"🔑 a={self.quiz_key[0]}, b={self.quiz_key[1]}")
            else: self.qkl.setText(f"🔑 {str(self.quiz_key)[:35]}")
        else: self.qkl.setText("🔑 No key")
        self.qel.setText(f"🔍  {enc}"); self.timer_secs = 0; self.timer_lbl.setText("⏱ 0s"); self.quiz_timer.start()

    def _cq(self):
        a = self.qi.text().strip().upper(); self.quiz_timer.stop()
        if not a: return
        if a == self.quiz_answer.upper():
            self.correct += 1; self.streak += 1; self.qr.setText(f"🎉 Correct! ({self.timer_secs}s)")
            self.qr.setStyleSheet("color:#a6e3a1;font-weight:bold;font-size:16px;background:transparent;")
        else:
            self.wrong += 1; self.streak = 0; self.qr.setText(f"❌ Answer: {self.quiz_answer}")
            self.qr.setStyleSheet("color:#f38ba8;font-weight:bold;font-size:16px;background:transparent;")
        self.sok.setText(f"✅ {self.correct}"); self.sba.setText(f"❌ {self.wrong}"); self.sst.setText(f"🔥 {self.streak}")

    def _hq(self):
        a = self.quiz_answer
        if len(a) <= 3: h = a[0]+"_"*(len(a)-1)
        elif len(a) <= 6: h = a[0]+"_"*(len(a)-2)+a[-1]
        else: rv = set(random.sample(range(len(a)), min(3, len(a)//2))); h = ''.join(a[i] if i in rv else '_' for i in range(len(a)))
        QMessageBox.information(self, "💡 Hint", f"Hint: {h}")

    def _rq(self):
        self.quiz_timer.stop(); self.streak = 0; self.qr.setText(f"👁 Answer: {self.quiz_answer}")
        self.qr.setStyleSheet("color:#f9e2af;font-weight:bold;font-size:16px;background:transparent;")
        self.sok.setText(f"✅ {self.correct}"); self.sba.setText(f"❌ {self.wrong}"); self.sst.setText(f"🔥 {self.streak}")

# ═══════════════════════════════════════════════════════════════
#  TOOL PAGES
# ═══════════════════════════════════════════════════════════════

class ChainingPage(QWidget):
    def __init__(self, p=None): super().__init__(p); self._build()
    def _build(self):
        l = QVBoxLayout(self); l.setContentsMargins(24,16,24,16); l.setSpacing(12)
        title = QLabel("🔗 Cipher Chaining"); title.setStyleSheet("font-size:24px;font-weight:bold;color:#89b4fa;background:transparent;"); l.addWidget(title)
        desc = QLabel("Apply multiple ciphers in sequence. Each step feeds its output to the next."); desc.setWordWrap(True); desc.setStyleSheet("font-size:13px;color:#a6adc8;background:transparent;"); l.addWidget(desc)
        ig = QGroupBox("Input"); il = QVBoxLayout(ig); il.addWidget(QLabel("📝 Plaintext:")); self.chain_input = QTextEdit(); self.chain_input.setPlaceholderText("Enter text to chain-encrypt…"); self.chain_input.setMaximumHeight(60); il.addWidget(self.chain_input); l.addWidget(ig)
        sg = QGroupBox("Cipher Chain (top to bottom)"); sl = QVBoxLayout(sg)
        self.chain_list = QListWidget(); self.chain_list.setMaximumHeight(200); sl.addWidget(self.chain_list)
        br = QHBoxLayout(); ab = QPushButton("➕ Add Step"); ab.clicked.connect(self._add_step); br.addWidget(ab)
        rb = QPushButton("➖ Remove"); rb.setObjectName("dangerBtn"); rb.clicked.connect(self._rm_step); br.addWidget(rb)
        ab2 = QPushButton("⬆ Up"); ab2.setObjectName("secondaryBtn"); ab2.clicked.connect(lambda: self._mv_step(-1)); br.addWidget(ab2)
        ab3 = QPushButton("⬇ Down"); ab3.setObjectName("secondaryBtn"); ab3.clicked.connect(lambda: self._mv_step(1)); br.addWidget(ab3)
        br.addStretch(); sl.addLayout(br); l.addWidget(sg)
        er = QHBoxLayout(); eb = QPushButton("🔗 Chain Encrypt!"); eb.clicked.connect(self._chain_enc); er.addWidget(eb)
        db = QPushButton("🔓 Chain Decrypt"); db.setObjectName("secondaryBtn"); db.clicked.connect(self._chain_dec); er.addWidget(db); er.addStretch(); l.addLayout(er)
        rg = QGroupBox("Result"); rl = QVBoxLayout(rg)
        self.chain_result = QTextEdit(); self.chain_result.setReadOnly(True); self.chain_result.setFont(QFont("Consolas", 13)); rl.addWidget(self.chain_result)
        self.chain_steps = QLabel(); self.chain_steps.setWordWrap(True); self.chain_steps.setStyleSheet("color:#a6adc8;font-size:12px;background:transparent;"); rl.addWidget(self.chain_steps)
        cpb = QPushButton("📋 Copy Result"); cpb.setObjectName("smallBtn"); cpb.clicked.connect(lambda: (QApplication.clipboard().setText(self.chain_result.toPlainText()), ToastWidget("📋 Copied!", self.window()))); rl.addWidget(cpb)
        l.addWidget(rg)

    def _add_step(self):
        names = [c.name() for c in CIPHERS]; name, ok = QInputDialog.getItem(self, "Add Cipher Step", "Select cipher:", names, 0, False)
        if not ok: return; ci = names.index(name); cc = CIPHERS[ci]; ki = cc.key_info(); k = None
        if ki["type"] == "int": v, ok2 = QInputDialog.getInt(self, f"Key for {name}", ki["label"], ki.get("default",3), ki.get("min",0), ki.get("max",25)); k = v if ok2 else None
        elif ki["type"] == "text": v, ok2 = QInputDialog.getText(self, f"Key for {name}", ki["label"], text=ki.get("default","")); k = v if ok2 else None
        elif ki["type"] == "pair":
            v1, ok2 = QInputDialog.getInt(self, f"Key for {name}", "a:", ki.get("default_a",5)); v2, ok3 = QInputDialog.getInt(self, f"Key for {name}", "b:", ki.get("default_b",8), 0, 25)
            k = (v1, v2) if ok2 and ok3 else None
        else: k = None
        if k is not None or ki["type"] == "none":
            item = QListWidgetItem(f"{name} | Key: {k if k is not None else 'None'}"); item.setData(Qt.UserRole, {"cipher": cc, "key": k}); self.chain_list.addItem(item)

    def _rm_step(self):
        cr = self.chain_list.currentRow()
        if cr >= 0: self.chain_list.takeItem(cr)
    def _mv_step(self, direction):
        cr = self.chain_list.currentRow(); nr = cr+direction
        if 0 <= nr < self.chain_list.count(): item = self.chain_list.takeItem(cr); self.chain_list.insertItem(nr, item); self.chain_list.setCurrentRow(nr)

    def _chain_enc(self):
        t = self.chain_input.toPlainText()
        if not t or self.chain_list.count() == 0: return
        steps_log = []
        for i in range(self.chain_list.count()):
            data = self.chain_list.item(i).data(Qt.UserRole); cc, k = data["cipher"], data["key"]
            t = cc.encrypt(t, k); steps_log.append(f"{i+1}. {cc.name()} → {t[:60]}{'…' if len(t)>60 else ''}")
        self.chain_result.setText(t); self.chain_steps.setText("Steps:\n" + "\n".join(steps_log)); ToastWidget("🔗 Chain encryption complete!", self.window())

    def _chain_dec(self):
        t = self.chain_result.toPlainText()
        if not t or self.chain_list.count() == 0: return
        steps_log = []
        for i in range(self.chain_list.count()-1, -1, -1):
            data = self.chain_list.item(i).data(Qt.UserRole); cc, k = data["cipher"], data["key"]
            t = cc.decrypt(t, k); steps_log.append(f"{self.chain_list.count()-i}. {cc.name()} ← {t[:60]}{'…' if len(t)>60 else ''}")
        self.chain_result.setText(t); self.chain_steps.setText("Decryption steps:\n" + "\n".join(reversed(steps_log))); ToastWidget("🔓 Chain decryption complete!", self.window())

class IdentifyCipherPage(QWidget):
    def __init__(self, p=None): super().__init__(p); self._build()
    def _build(self):
        l = QVBoxLayout(self); l.setContentsMargins(24,16,24,16); l.setSpacing(12)
        title = QLabel("🔍 Identify Cipher"); title.setStyleSheet("font-size:24px;font-weight:bold;color:#89b4fa;background:transparent;"); l.addWidget(title)
        desc = QLabel("Analyze ciphertext to guess which cipher was used. Uses frequency analysis, pattern matching, and brute-force scoring."); desc.setWordWrap(True); desc.setStyleSheet("font-size:13px;color:#a6adc8;background:transparent;"); l.addWidget(desc)
        ir = QHBoxLayout(); ir.addWidget(QLabel("Ciphertext:")); self.id_input = QTextEdit(); self.id_input.setPlaceholderText("Paste ciphertext…"); self.id_input.setMaximumHeight(80); self.id_input.setFont(QFont("Consolas", 13)); ir.addWidget(self.id_input, 1)
        pb = QPushButton("📋 Paste"); pb.setObjectName("smallBtn"); pb.clicked.connect(lambda: self.id_input.setText(QApplication.clipboard().text())); ir.addWidget(pb); l.addLayout(ir)
        ab = QPushButton("🔍 Identify!"); ab.clicked.connect(self._identify); l.addWidget(ab)
        self.id_result = QTextEdit(); self.id_result.setReadOnly(True); self.id_result.setMaximumHeight(400); l.addWidget(self.id_result)

    def _identify(self):
        t = self.id_input.toPlainText().strip()
        if not t: self.id_result.setText("⚠ Please enter some ciphertext."); return
        results = []; letters = [c.upper() for c in t if c.isalpha()]
        morse_chars = set(c for c in t if c not in ' \t\n')
        if morse_chars.issubset(set('.-/')) and '.' in t and '-' in t: results.append(("📡 Morse Code", 95, "Contains dots, dashes, and slashes"))
        words = t.split(); bc_words = [w for w in words if len(w) == 5 and all(c in 'ABab' for c in w)]
        if len(bc_words) > 2 and len(bc_words)/max(len(words),1) > 0.7: results.append(("🥓 Baconian Cipher", 85, "Mostly 5-char A/B groups"))
        num_words = [w for w in words if w.isdigit() and 1 <= int(w) <= 26]
        if len(num_words) > 2 and len(num_words)/max(len(words),1) > 0.6: results.append(("🔢 A1Z26", 80, "Mostly numbers 1–26"))
        if letters:
            total = len(letters); counts = Counter(letters); freqs = {c:counts.get(c,0)/total for c in string.ascii_uppercase}
            chi = sum((freqs.get(c,0)-ENGLISH_FREQ.get(c,0)/100)**2/(ENGLISH_FREQ.get(c,0)/100) for c in string.ascii_uppercase if ENGLISH_FREQ.get(c,0) > 0)
            if chi < 0.1: results.append(("🔄 Atbash / ROT13", 60, f"Frequency very close to English (χ²={chi:.3f})"))
            elif chi < 0.5: results.append(("🔤 Caesar Cipher", 55, f"Frequency close to English (χ²={chi:.3f})"))
            elif chi < 2.0: results.append(("📝 Substitution / Affine", 45, f"Somewhat close (χ²={chi:.3f})"))
            else: results.append(("🔑 Vigenère / Playfair / Transposition", 30, f"Far from English (χ²={chi:.3f})"))
            common = {"THE","AND","FOR","ARE","BUT","NOT","YOU","ALL","CAN","HER","WAS","ONE","OUR"}
            best_shift, best_score = 0, 0
            for s in range(1, 26):
                dec = CaesarCipher.decrypt(t, s); up = dec.upper(); score = sum(1 for w in common if w in up)
                if score > best_score: best_score = score; best_shift = s
            if best_score >= 2: results.append((f"🔤 Caesar (shift={best_shift}?)", 70, f"Shift {best_shift} scores {best_score} common words"))
            for rails in range(2, 6):
                dec = RailFenceCipher.decrypt(t, rails); up = dec.upper(); score = sum(1 for w in common if w in up)
                if score >= 2: results.append((f"🚂 Rail Fence ({rails} rails?)", 50, f"Rails={rails} scores {score}"))
        if not results: results.append(("❓ Unknown", 10, "No patterns detected"))
        results.sort(key=lambda x: x[1], reverse=True)
        html = "<h3 style='color:#89b4fa'>Identification Results</h3>"
        for name, confidence, reason in results:
            color = "#a6e3a1" if confidence >= 70 else "#f9e2af" if confidence >= 40 else "#f38ba8"
            html += f"<p><b style='color:{color}'>{name}</b> — Confidence: <b>{confidence}%</b><br><i style='color:#a6adc8'>{reason}</i></p>"
        html += "<hr><p style='color:#585b70;font-size:11px;'><i>Note: Identification is heuristic. Try Brute Force tabs for confirmation.</i></p>"
        self.id_result.setHtml(html)

class ReferencePage(QWidget):
    def __init__(self, p=None): super().__init__(p); self._build()
    def _build(self):
        l = QVBoxLayout(self); l.setContentsMargins(24,16,24,16)
        title = QLabel("📋 Cipher Reference Card"); title.setStyleSheet("font-size:24px;font-weight:bold;color:#89b4fa;background:transparent;"); l.addWidget(title)
        desc = QLabel("Quick reference for all supported ciphers."); desc.setStyleSheet("font-size:13px;color:#a6adc8;background:transparent;"); l.addWidget(desc)
        tw = QTableWidget(); tw.setColumnCount(5); tw.setHorizontalHeaderLabels(["Cipher","Category","Difficulty","Key Type","Formula / Notes"])
        tw.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); tw.setEditTriggers(QTableWidget.NoEditTriggers); tw.setRowCount(len(CIPHERS))
        notes = {"Caesar Cipher":"E(x)=(x+n) mod 26","Vigenère Cipher":"E(xᵢ)=(xᵢ+kᵢ) mod 26","Atbash Cipher":"E(x)=(25−x) mod 26","ROT13":"E(x)=(x+13) mod 26","Affine Cipher":"E(x)=(ax+b) mod 26","Rail Fence Cipher":"Zigzag transposition","XOR Cipher":"E(x)=x⊕k","Simple Substitution":"26! permutations","Playfair Cipher":"5×5 grid digraphic","A1Z26":"A=1…Z=26","Morse Code":"Dots & dashes","Baconian Cipher":"5-bit A/B binary"}
        for i, c in enumerate(CIPHERS):
            ki = c.key_info()
            for col, val in enumerate([c.name(), c.category(), c.difficulty(), ki["label"], notes.get(c.name(), "")]):
                it = QTableWidgetItem(val); it.setTextAlignment(Qt.AlignCenter if col < 4 else Qt.AlignLeft|Qt.AlignVCenter)
                if col == 0: it.setFont(QFont("Segoe UI", 10, QFont.Bold)); it.setForeground(QBrush(QColor("#89b4fa")))
                tw.setItem(i, col, it)
        l.addWidget(tw)
        sg = QGroupBox("⌨️ Keyboard Shortcuts"); sl = QVBoxLayout(sg)
        for shortcut, desc in [("Ctrl+E","Encrypt current text"),("Ctrl+D","Decrypt current text"),("Ctrl+S","Save output to file"),("Ctrl+Shift+C","Copy output"),("Ctrl+L","Load text file"),("Ctrl+T","Toggle dark/light theme")]:
            lbl = QLabel(f"<b>{shortcut}</b> — {desc}"); lbl.setStyleSheet("color:#cdd6f4;background:transparent;"); sl.addWidget(lbl)
        l.addWidget(sg)

class ComparisonPage(QWidget):
    def __init__(self, p=None): super().__init__(p); self._build()
    def _build(self):
        l = QVBoxLayout(self); l.setContentsMargins(24,16,24,16); l.setSpacing(12)
        title = QLabel("⚖️ Cipher Comparison"); title.setStyleSheet("font-size:24px;font-weight:bold;color:#89b4fa;background:transparent;"); l.addWidget(title)
        desc = QLabel("Encrypt the same text with all ciphers at once."); desc.setWordWrap(True); desc.setStyleSheet("font-size:13px;color:#a6adc8;background:transparent;"); l.addWidget(desc)
        ig = QGroupBox("Input"); il = QVBoxLayout(ig)
        tr = QHBoxLayout(); tr.addWidget(QLabel("Text:")); self.comp_input = QLineEdit(); self.comp_input.setFont(QFont("Consolas", 13)); self.comp_input.setPlaceholderText("Enter text…"); tr.addWidget(self.comp_input); il.addLayout(tr)
        kr = QHBoxLayout(); kr.addWidget(QLabel("Caesar shift:")); self.cs = QSpinBox(); self.cs.setRange(1,25); self.cs.setValue(3); kr.addWidget(self.cs)
        kr.addWidget(QLabel("Vigenère key:")); self.vk = QLineEdit("SECRET"); kr.addWidget(self.vk); kr.addStretch(); il.addLayout(kr)
        go = QPushButton("🔄 Compare All"); go.clicked.connect(self._cmp); il.addWidget(go); l.addWidget(ig)
        self.ct = QTableWidget(); self.ct.setColumnCount(4); self.ct.setHorizontalHeaderLabels(["Cipher","Category","Key","Result"])
        self.ct.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); self.ct.setEditTriggers(QTableWidget.NoEditTriggers); l.addWidget(self.ct)
    def _cmp(self):
        t = self.comp_input.text()
        if not t: return; rows = []
        for c in CIPHERS:
            ki = c.key_info()
            if ki["type"] == "int": k = self.cs.value() if c is CaesarCipher else ki.get("default",3)
            elif ki["type"] == "text": k = self.vk.text() if c is VigenereCipher else ki.get("default","KEY")
            elif ki["type"] == "pair": k = (5,8)
            else: k = None
            r = c.encrypt(t, k); ks = str(k) if k else "—"
            if isinstance(k, tuple): ks = f"a={k[0]},b={k[1]}"
            rows.append((c.name(), c.category(), ks, r[:120]))
        self.ct.setRowCount(len(rows))
        for row, (nm, ca, ks, r) in enumerate(rows):
            for col, v in enumerate([nm, ca, ks, r]):
                it = QTableWidgetItem(v); it.setTextAlignment(Qt.AlignCenter if col < 3 else Qt.AlignLeft|Qt.AlignVCenter)
                if col == 0: it.setFont(QFont("Segoe UI", 11, QFont.Bold)); it.setForeground(QBrush(QColor("#89b4fa")))
                if col == 3: it.setFont(QFont("Consolas", 10))
                self.ct.setItem(row, col, it)

class HistoryPage(QWidget):
    def __init__(self, p=None): super().__init__(p); self._build()
    def _build(self):
        l = QVBoxLayout(self); l.setContentsMargins(24,16,24,16)
        title = QLabel("📜 History"); title.setStyleSheet("font-size:24px;font-weight:bold;color:#89b4fa;background:transparent;"); l.addWidget(title)
        br = QHBoxLayout(); ref = QPushButton("🔄 Refresh"); ref.clicked.connect(self._ref); br.addWidget(ref)
        clr = QPushButton("🗑 Clear"); clr.setObjectName("dangerBtn"); clr.clicked.connect(lambda: (HISTORY.clear(), self._ref())); br.addWidget(clr); br.addStretch(); l.addLayout(br)
        self.ht = QTableWidget(); self.ht.setColumnCount(6); self.ht.setHorizontalHeaderLabels(["Time","Cipher","Dir","Key","Plain","Cipher"])
        self.ht.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); self.ht.setEditTriggers(QTableWidget.NoEditTriggers); l.addWidget(self.ht); self._ref()
    def _ref(self):
        self.ht.setRowCount(len(HISTORY.records))
        for row, rec in enumerate(reversed(HISTORY.records)):
            for col, key in enumerate(["time","cipher","dir","key","plain","cipher_text"]):
                it = QTableWidgetItem(str(rec.get(key, ""))); it.setTextAlignment(Qt.AlignCenter if col < 4 else Qt.AlignLeft|Qt.AlignVCenter)
                if col == 1: it.setFont(QFont("Segoe UI", 10, QFont.Bold)); it.setForeground(QBrush(QColor("#89b4fa")))
                if col >= 4: it.setFont(QFont("Consolas", 9))
                self.ht.setItem(row, col, it)

class GlobalAnalysisPage(QWidget):
    def __init__(self, p=None): super().__init__(p); self._build()
    def _build(self):
        l = QVBoxLayout(self); l.setContentsMargins(24,16,24,16)
        title = QLabel("📊 Frequency Analysis"); title.setStyleSheet("font-size:24px;font-weight:bold;color:#89b4fa;background:transparent;"); l.addWidget(title)
        ir = QHBoxLayout(); ir.addWidget(QLabel("Text:")); self.gi = QTextEdit(); self.gi.setPlaceholderText("Paste ciphertext…"); self.gi.setMaximumHeight(80); self.gi.setFont(QFont("Consolas", 13))
        self.gi.textChanged.connect(self._upd); ir.addWidget(self.gi, 1)
        pb = QPushButton("📋 Paste"); pb.setObjectName("smallBtn"); pb.clicked.connect(lambda: self.gi.setText(QApplication.clipboard().text())); ir.addWidget(pb); l.addLayout(ir)
        cg = QGroupBox("Chart"); cl = QVBoxLayout(cg); self.gf = FrequencyWidget(); cl.addWidget(self.gf); l.addWidget(cg)
        tg = QGroupBox("Table"); tl = QVBoxLayout(tg); self.gt = QTableWidget(); self.gt.setColumnCount(4); self.gt.setHorizontalHeaderLabels(["Letter","Text %","Eng %","Diff"])
        self.gt.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); self.gt.setEditTriggers(QTableWidget.NoEditTriggers); tl.addWidget(self.gt); l.addWidget(tg)
    def _upd(self):
        t = self.gi.toPlainText(); self.gf.set_text(t); ls = [c.upper() for c in t if c.isalpha()]; tot = len(ls)
        if tot == 0: self.gt.setRowCount(0); return
        ct = Counter(ls); self.gt.setRowCount(26)
        for i in range(26):
            l = chr(i+65); tp = (ct.get(l,0)/tot)*100; ep = ENGLISH_FREQ.get(l,0); d = tp-ep
            for col, tv in enumerate([l, f"{tp:.2f}%", f"{ep:.2f}%", f"{d:+.2f}%"]):
                it = QTableWidgetItem(tv); it.setTextAlignment(Qt.AlignCenter)
                if col == 0: it.setFont(QFont("Consolas", 11, QFont.Bold)); it.setForeground(QBrush(QColor("#89b4fa")))
                elif col == 3: it.setForeground(QBrush(QColor("#a6e3a1") if abs(d) < 2 else QColor("#f9e2af") if abs(d) < 5 else QColor("#f38ba8")))
                self.gt.setItem(i, col, it)

# ═══════════════════════════════════════════════════════════════
#  HOME PAGE
# ═══════════════════════════════════════════════════════════════

class HomePage(QWidget):
    def __init__(self, on_sel, p=None): super().__init__(p); self.on_sel=on_sel; self._build()
    def _build(self):
        l = QVBoxLayout(self); l.setContentsMargins(32,32,32,32); l.setSpacing(12)
        title = QLabel("🔐  Cipher Academy"); title.setStyleSheet("font-size:36px;font-weight:bold;color:#89b4fa;background:transparent;"); l.addWidget(title)
        sub = QLabel("Learn, practise, and master classical encryption  ✨"); sub.setStyleSheet("font-size:16px;color:#a6adc8;background:transparent;"); l.addWidget(sub)
        sep = QFrame(); sep.setFrameShape(QFrame.HLine); sep.setStyleSheet("background:#45475a;max-height:2px;"); l.addWidget(sep)
        s = QHBoxLayout()
        for t in [f"📚 {len(CIPHERS)} Ciphers","📊 Analysis","🔨 Brute Force","🔗 Chaining","🔍 Identify","📜 History"]:
            lbl = QLabel(t); lbl.setStyleSheet("color:#a6adc8;font-size:11px;background:transparent;"); s.addWidget(lbl)
        l.addLayout(s)
        gl = QLabel("Available Ciphers"); gl.setStyleSheet("font-size:18px;font-weight:bold;color:#cdd6f4;background:transparent;"); l.addWidget(gl)
        gw = QWidget(); gl2 = QHBoxLayout(gw); gl2.setSpacing(10); cols = [QVBoxLayout(), QVBoxLayout(), QVBoxLayout()]
        for i, c in enumerate(CIPHERS): cols[i%3].addWidget(self._card(c))
        for c in cols: c.addStretch()
        for c in cols: gl2.addLayout(c)
        l.addWidget(gw, 1)
    def _card(self, cipher):
        card = QFrame(); card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet("QFrame{background:#313244;border:2px solid #45475a;border-radius:12px;padding:10px;}QFrame:hover{border-color:#89b4fa;background:#383850;}")
        cl = QVBoxLayout(card); cl.setSpacing(3)
        hdr = QHBoxLayout(); ic = QLabel(cipher.icon()); ic.setFont(QFont("Segoe UI Emoji", 18)); ic.setStyleSheet("background:transparent;")
        nm = QLabel(cipher.name()); nm.setStyleSheet("font-size:13px;font-weight:bold;color:#89b4fa;background:transparent;")
        hdr.addWidget(ic); hdr.addWidget(nm, 1); cl.addLayout(hdr)
        mt = QLabel(f"📁 {cipher.category()} • ⭐ {cipher.difficulty()}")
        mt.setStyleSheet("font-size:10px;color:#a6adc8;background:transparent;"); cl.addWidget(mt)
        if hasattr(cipher, 'brute_force'): bf = QLabel("🔨 Brute force"); bf.setStyleSheet("font-size:9px;color:#a6e3a1;background:transparent;"); cl.addWidget(bf)
        card.mousePressEvent = lambda e, c=cipher: self.on_sel(c); return card

# ═══════════════════════════════════════════════════════════════
#  MAIN WINDOW
# ═══════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 Cipher Academy — Learn Cryptography")
        self.setMinimumSize(1100, 700); self.resize(1360, 880); self.dark_mode = True; self._build(); self._shortcuts()

    @staticmethod
    def _hon(): return "QPushButton{background:#89b4fa;color:#1e1e2e;border:none;border-radius:8px;padding:12px 16px;font-size:14px;font-weight:bold;text-align:left;}QPushButton:hover{background:#b4d0fb;}"
    @staticmethod
    def _hoff(): return "QPushButton{background:#313244;color:#cdd6f4;border:none;border-radius:8px;padding:12px 16px;font-size:14px;text-align:left;}QPushButton:hover{background:#45475a;}"
    def _tbs(self):
        if self.dark_mode: return "QPushButton{background:#313244;color:#a6adc8;border:none;border-radius:8px;padding:9px 14px;font-size:12px;text-align:left;}QPushButton:hover{background:#45475a;}"
        return "QPushButton{background:#ccd0da;color:#4c4f69;border:none;border-radius:8px;padding:9px 14px;font-size:12px;text-align:left;}QPushButton:hover{background:#bcc0cc;}"

    def _build(self):
        central = QWidget(); self.setCentralWidget(central); ml = QHBoxLayout(central); ml.setContentsMargins(0,0,0,0); ml.setSpacing(0)
        self.sb = QStatusBar(); self.setStatusBar(self.sb); self.sb.showMessage("Welcome to Cipher Academy! 🔐")
        sb = QFrame(); sb.setObjectName("sidebar"); sb.setFixedWidth(240)
        sbl = QVBoxLayout(sb); sbl.setContentsMargins(10,18,10,18); sbl.setSpacing(4)
        al = QLabel("🔐 Cipher Academy"); al.setStyleSheet("font-size:16px;font-weight:bold;color:#89b4fa;padding:8px;background:transparent;"); sbl.addWidget(al)
        self.home_btn = QPushButton("🏠  Home"); self.home_btn.setObjectName("secondaryBtn"); self.home_btn.setStyleSheet(self._hon()); self.home_btn.clicked.connect(self._sh); sbl.addWidget(self.home_btn)
        sep = QFrame(); sep.setFrameShape(QFrame.HLine); sep.setStyleSheet("background:#45475a;max-height:1px;margin:4px 0;"); sbl.addWidget(sep)
        ll = QLabel("CIPHERS"); ll.setStyleSheet("color:#585b70;font-size:11px;font-weight:bold;padding:4px 8px;background:transparent;"); sbl.addWidget(ll)
        self.cl = QListWidget()
        for c in CIPHERS: it = QListWidgetItem(f"  {c.icon()}  {c.name()}"); it.setData(Qt.UserRole, c); self.cl.addItem(it)
        self.cl.currentItemChanged.connect(self._ss); sbl.addWidget(self.cl)
        sep2 = QFrame(); sep2.setFrameShape(QFrame.HLine); sep2.setStyleSheet("background:#45475a;max-height:1px;margin:4px 0;"); sbl.addWidget(sep2)
        tl = QLabel("TOOLS"); tl.setStyleSheet("color:#585b70;font-size:11px;font-weight:bold;padding:4px 8px;background:transparent;"); sbl.addWidget(tl)
        for text, slot in [("📊 Freq Analysis",self._sa),("⚖️ Compare Ciphers",self._sc),("📜 History",self._shh),("🔗 Chaining",self._sch),("🔍 Identify Cipher",self._si),("📋 Reference",self._sr)]:
            b = QPushButton(text); b.setStyleSheet(self._tbs()); b.clicked.connect(slot); sbl.addWidget(b)
        sep3 = QFrame(); sep3.setFrameShape(QFrame.HLine); sep3.setStyleSheet("background:#45475a;max-height:1px;margin:4px 0;"); sbl.addWidget(sep3)
        self.theme_btn = QPushButton("🌙 Dark Mode"); self.theme_btn.setStyleSheet(self._tbs()); self.theme_btn.clicked.connect(self._tt); sbl.addWidget(self.theme_btn)
        foot = QLabel("v4.0 — PySide6"); foot.setStyleSheet("color:#585b70;font-size:10px;padding:8px;background:transparent;"); foot.setAlignment(Qt.AlignCenter); sbl.addWidget(foot); ml.addWidget(sb)

        self.stack = QStackedWidget()
        self.home_page = HomePage(self._gc); self.stack.addWidget(self.home_page)
        self.pages = {}
        for c in CIPHERS: p = CipherPage(c); self.pages[c] = p; self.stack.addWidget(p)
        self.analysis_page = GlobalAnalysisPage(); self.stack.addWidget(self.analysis_page)
        self.comparison_page = ComparisonPage(); self.stack.addWidget(self.comparison_page)
        self.history_page = HistoryPage(); self.stack.addWidget(self.history_page)
        self.chaining_page = ChainingPage(); self.stack.addWidget(self.chaining_page)
        self.identify_page = IdentifyCipherPage(); self.stack.addWidget(self.identify_page)
        self.reference_page = ReferencePage(); self.stack.addWidget(self.reference_page)
        ml.addWidget(self.stack, 1)

    def _shortcuts(self):
        QShortcut(QKeySequence("Ctrl+E"), self, activated=self._shortcut_enc)
        QShortcut(QKeySequence("Ctrl+D"), self, activated=self._shortcut_dec)
        QShortcut(QKeySequence("Ctrl+S"), self, activated=self._shortcut_save)
        QShortcut(QKeySequence("Ctrl+Shift+C"), self, activated=self._shortcut_copy)
        QShortcut(QKeySequence("Ctrl+L"), self, activated=self._shortcut_load)
        QShortcut(QKeySequence("Ctrl+T"), self, activated=self._tt)

    def _current_cipher_page(self):
        w = self.stack.currentWidget()
        if isinstance(w, CipherPage): return w
        return None

    def _shortcut_enc(self):
        p = self._current_cipher_page()
        if p: p._enc(); self.sb.showMessage("✅ Encrypted (Ctrl+E)")
    def _shortcut_dec(self):
        p = self._current_cipher_page()
        if p: p._dec(); self.sb.showMessage("✅ Decrypted (Ctrl+D)")
    def _shortcut_save(self):
        p = self._current_cipher_page()
        if p: p._save_file(); self.sb.showMessage("💾 Saved (Ctrl+S)")
    def _shortcut_copy(self):
        p = self._current_cipher_page()
        if p: p._cpo(); self.sb.showMessage("📋 Copied (Ctrl+Shift+C)")
    def _shortcut_load(self):
        p = self._current_cipher_page()
        if p: p._load_file(); self.sb.showMessage("📂 Loaded (Ctrl+L)")

    def _tt(self):
        self.dark_mode = not self.dark_mode
        QApplication.instance().setStyleSheet(DARK_STYLE if self.dark_mode else LIGHT_STYLE)
        self.theme_btn.setText("🌙 Dark Mode" if self.dark_mode else "☀️ Light Mode")
        self.theme_btn.setStyleSheet(self._tbs()); self.sb.showMessage(f"Theme: {'Dark' if self.dark_mode else 'Light'}")

    def _off(self): self.home_btn.setStyleSheet(self._hoff()); self.cl.clearSelection()
    def _sh(self): self.stack.setCurrentWidget(self.home_page); self.cl.clearSelection(); self.home_btn.setStyleSheet(self._hon()); self.sb.showMessage("🏠 Home")
    def _ss(self, cur, _):
        if cur: self._gc(cur.data(Qt.UserRole))
    def _gc(self, c):
        p = self.pages.get(c)
        if not p: return
        self.stack.setCurrentWidget(p)
        for i in range(self.cl.count()):
            if self.cl.item(i).data(Qt.UserRole) is c: self.cl.setCurrentItem(self.cl.item(i)); break
        self._off(); self.sb.showMessage(f"📖 {c.name()} — {c.category()}")
    def _sa(self): self.stack.setCurrentWidget(self.analysis_page); self._off(); self.sb.showMessage("📊 Frequency Analysis")
    def _sc(self): self.stack.setCurrentWidget(self.comparison_page); self._off(); self.sb.showMessage("⚖️ Cipher Comparison")
    def _shh(self): self.history_page._ref(); self.stack.setCurrentWidget(self.history_page); self._off(); self.sb.showMessage("📜 History")
    def _sch(self): self.stack.setCurrentWidget(self.chaining_page); self._off(); self.sb.showMessage("🔗 Cipher Chaining")
    def _si(self): self.stack.setCurrentWidget(self.identify_page); self._off(); self.sb.showMessage("🔍 Identify Cipher")
    def _sr(self): self.stack.setCurrentWidget(self.reference_page); self._off(); self.sb.showMessage("📋 Reference Card")

def main():
    app = QApplication(sys.argv); app.setStyleSheet(DARK_STYLE); app.setFont(QFont("Segoe UI", 11))
    win = MainWindow(); win.show(); sys.exit(app.exec())

if __name__ == "__main__":
    main()