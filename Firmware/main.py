import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Macros
from kmk.macros import Macro
from kmk.modules.layers import Layers
from kmk.handlers.sequences import unicode_strings
from kmk.modules.unicode import Unicode
from kmk.types import UnicodeMode
from kmk.extensions.RGB import RGB

keyboard = KMKKeyboard()

keyboard.modules.append(Macros())
keyboard.modules.append(Layers())
unicode = Unicode()
keyboard.modules.append(unicode)
keyboard.unicode_mode = UnicodeMode.WINC

PINS = [board.D5, board.D4, board.D3, board.D2, board.D1, board.D0]
rgb = RGB(
    pixel_pin=board.GP14,
    num_pixels=6,
    val_limit=50,
)
keyboard.extensions.append(rgb)

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

#MACRO DEFINITIONS
CRY = Macro().add(unicode_strings('😭'))
LAUGH = Macro().add(unicode_strings('😂'))
HEART = Macro().add(unicode_strings('❤️'))
SKULL = Macro().add(unicode_strings('💀'))
UP = Macro().add(unicode_strings('👍'))

TMGR = Macro().press(KC.LCTRL, KC.LSHIFT, KC.ESC).release()

#KEYMAP LAYERS
keyboard.keymap = [
    #Layer 0: Basic
    [
        KC.LCTL(KC.C),
        KC.LCTL(KC.V),
        KC.LCTL(KC.S),
        KC.LCTL(KC.Z),
        KC.LCTL(KC.Y),
        KC.MO(1),#Layer 1
    ],
    
    #Layer 1: Emojis
    [
        KC.MACRO(CRY),
        KC.MACRO(LAUGH),
        KC.MACRO(HEART),
        KC.MACRO(SKULL),
        KC.MACRO(UP),
        KC.MO(2),            
    ],
    
    #Layer 2: Misc
    [              
        KC.MACRO(TMGR), 
        KC.LCTL(KC.SLASH),
        KC.LCTL(KC.F),
        KC.ALT(KC.TAB),
        KC.LCTL(KC.GRAVE),
        KC.TO(0),
    ]
]

#Layer Tracker
COLOURS = {
    0: (255, 255, 255),
    1: (0, 0, 255),
    2: (0, 255, 0)
}

def update_rgb(layer):
    colour = COLOURS.get(layer, (0,0,0))
    rgb.set_rgb_fill(colour)

update_rgb(0)

prev_layer = -1

def layerTracker():
    global prev_layer
    current_layer = keyboard.active_layers[-1] if keyboard.active_layers else 0
    if current_layer != prev_layer:
        update_rgb(current_layer)
        prev_layer = current_layer

keyboard.before_matrix_scan(layerTracker)


if __name__ == '__main__':
    keyboard.go()