from pynput.keyboard import Key

keyboard = \
    {
        # Main gauche
        '(': 'Sol#2',
        't': 'Mi2',
        'g': 'MiM3',
        'b': 'Mim3',
        "'": 'Do#2',
        'r': 'La2',
        'f': 'LaM3',
        'v': 'Lam3',
        '"': 'Fa#2',
        'e': 'Re2',
        'd': 'ReM3',
        'c': 'Rem3',
        'é': 'Si2',
        'z': 'Sol2',
        's': 'SolM3',
        'x': 'Solm3',
        '&': 'Mi2',
        'a': 'Do2',
        'q': 'DoM3',
        'w': 'Dom3',
        Key.caps_lock: 'FaM3',

        # Main droite
        '-': 'Fa3',
        'y': 'Sol3',
        'è': 'Sol#3',
        'h': 'La3',
        'u': 'La#3',
        '_': 'Si3',
        'j': 'Do4',
        'i': 'Do#4',
        'ç': 'Re4',
        'k': 'Re#4',
        'o': 'Mi4',
        'à': 'Fa4',
        'l': 'Fa#4',
        'p': 'Sol4',
        ')': 'Sol#4',
        'm': 'La4',
        '^': 'La#4',
        '=': 'Si4',
        'ù': 'Do5',
        '$': 'Do#5',
        Key.backspace: 'Re5'
    }
