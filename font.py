# LEGO type:standard slot:11 autostart
import hub

font = {
    "A": ["99999", "90009", "90009", "99999", "90009"],
    "a": ["99999", "90009", "90009", "99999", "90009"],
    
    "B": ["99999", "90009", "99990", "90009", "99999"],
    "b": ["99999", "90009", "99990", "90009", "99999"],
    
    "C": ["99999", "90000", "90000", "90000", "99999"],
    "c": ["99999", "90000", "90000", "90000", "99999"],
    
    "D": ["99990", "90009", "90009", "90009", "99990"],
    "d": ["99990", "90009", "90009", "90009", "99990"],
    
    "E": ["99999", "90000", "99990", "90000", "99999"],
    "e": ["99999", "90000", "99990", "90000", "99999"],
    
    "F": ["99999", "90000", "99990", "90000", "90000"],
    "f": ["99999", "90000", "99990", "90000", "90000"],
    
    "G": ["99999", "90000", "90099", "90009", "99999"],
    "g": ["99999", "90000", "90099", "90009", "99999"],
    
    "H": ["90009", "90009", "99999", "90009", "90009"],
    "h": ["90009", "90009", "99999", "90009", "90009"],
    
    "I": ["99999", "00900", "00900", "00900", "99999"],
    "i": ["99999", "00900", "00900", "00900", "99999"],
    
    "J": ["00099", "00009", "00009", "90009", "99999"],
    "j": ["00099", "00009", "00009", "90009", "99999"],
    
    "K": ["90009", "90090", "99900", "90090", "90009"],
    "k": ["90009", "90090", "99900", "90090", "90009"],
    
    "L": ["90000", "90000", "90000", "90000", "99999"],
    "l": ["90000", "90000", "90000", "90000", "99999"],

    "M": ["90009", "99099", "90909", "90009", "90009"],
    "m": ["90009", "99099", "90909", "90009", "90009"],
    
    "N": ["90009", "99009", "90909", "90099", "90009"],
    "n": ["90009", "99009", "90909", "90099", "90009"],
    
    "O": ["09990", "90009", "90009", "90009", "09990"],
    "o": ["09990", "90009", "90009", "90009", "09990"],
    
    "P": ["99990", "90009", "99990", "90000", "90000"],
    "p": ["99990", "90009", "99990", "90000", "90000"],
    
    "Q": ["99999", "90009", "90009", "99999", "00900"],
    "q": ["99999", "90009", "90009", "99999", "00900"],
    
    "R": ["99990", "90009", "99990", "90009", "90009"],
    "r": ["99990", "90009", "99990", "90009", "90009"],
    
    "S": ["99999", "90000", "99999", "00009", "99999"],
    "s": ["99999", "90000", "99999", "00009", "99999"],
    
    "T": ["99999", "00900", "00900", "00900", "00900"],
    "t": ["99999", "00900", "00900", "00900", "00900"],
    
    "U": ["90009", "90009", "90009", "90009", "99999"],
    "u": ["90009", "90009", "90009", "90009", "99999"],
    
    "V": ["90009", "90009", "09090", "09090", "00900"],
    "v": ["90009", "90009", "09090", "09090", "00900"],
    
    "W": ["90009", "90009", "90909", "90909", "09090"],
    "w": ["90009", "90009", "90909", "90909", "09090"],
    
    "X": ["90009", "09090", "00900", "09090", "90009"],
    "x": ["90009", "09090", "00900", "09090", "90009"],
    
    "Y": ["90009", "90009", "09090", "00900", "00900"],
    "y": ["90009", "90009", "09090", "00900", "00900"],
    
    "Z": ["99999", "00090", "00900", "09000", "99999"],
    "z": ["99999", "00090", "00900", "09000", "99999"],
    
    "0": ["99999", "90099", "90909", "99009", "99999"],
    "1": ["00900", "09900", "00900", "00900", "09990"],
    "2": ["99990", "00009", "09990", "90000", "99999"],
    "3": ["99999", "00009", "09990", "00009", "99999"],
    "4": ["09000", "09090", "09090", "09999", "00090"],
    "5": ["99999", "90000", "99990", "00009", "99990"],
    "6": ["99999", "90000", "99999", "90009", "99999"],
    "7": ["99999", "00009", "00090", "00900", "00900"],
    "8": ["99999", "90009", "99999", "90009", "99999"],
    "9": ["99999", "90009", "99999", "00009", "99999"],
    
    "+": ["00900", "00900", "99999", "00900", "00900"],
    "-": ["00000", "00000", "99999", "00000", "00000"],
    "*": ["00900", "09990", "00900", "00000", "00000"],
    "/": ["00090", "00090", "00900", "09000", "09000"],
    "=": ["00000", "99999", "00000", "99999", "00000"],
    "_": ["00000", "00000", "00000", "00000", "99999"],
    ",": ["00000", "00000", "00000", "00900", "00900"],
    ".": ["00000", "00000", "00000", "00000", "00900"],
    "%": ["90009", "00090", "00900", "09000", "90009"],
    
    " ": ["0" * 5 for _ in range(5)],
}


def interpolate(a, b):
    output = []
    c = [i + "0" + j for i, j in zip(a, b)]
    for i in range(6):
        output.append([j[i : i + 5] for j in c])
    return output


def write(string, delay=100):
    pr = []
    
    for j, i in enumerate(string[:-1]):
        pr += interpolate(font[i], font[string[j + 1]])
    
    pr.append(font[string[-1]])
    
    hub.display.show(
        [hub.Image(":".join(i)) for i in pr],
        delay=delay,
        wait=True,
        clear=False,
        loop=False,
        fade=0,
    )

def write_full(string, delay=500):
    hub.display.show(
        [hub.Image(":".join(font[i])) for i in string],
        delay=delay,
        wait=True,
        clear=False,
        loop=False,
        fade=0,
    )

write_full(" ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/=_,.% ")
