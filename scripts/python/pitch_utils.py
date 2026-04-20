#!/usr/bin/env python3

NOTE = { "C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11 }
ACC = { "b": -1, "_": 0, "#": 1 }
INV = {
    0: "root",
    3: "1st", 4: "1st",
    6: "2nd", 7: "2nd",
    10:"3rd", 11:"3rd",
}

INV_LABELS = ["root", "1st", "2nd", "3rd", "non-chord"]
INV_MAP = {label: i for i, label in enumerate(INV_LABELS)}

def pitch_class(note):
    return (NOTE[note[0]] + (ACC.get(note[1], 0) if len(note)>1 else 0)) % 12

def inversion(chord_label, bass):
    root, _, _ = parse_chord(chord_label)
    bass = pitch_class(bass)

    tones = chord_tones(chord_label)

    if bass not in tones:
        return "non-chord"

    interval = (bass - root) % 12
    return INV.get(interval, "non-chord")

def inversion_code(chord_label, bass_note):
    return INV_MAP[inversion(chord_label, bass_note)]

def parse_chord(label):
    root_letter = label[0]
    accidental  = label[1]
    quality     = label[2] 
    extension   = label[3:] if len(label)>3 else ""

    root = (NOTE[root_letter] + ACC[accidental]) % 12

    return root, quality, extension

def chord_tones(label):
    root, quality, extension = parse_chord(label)
    tones = set()

    if quality == "M":
        tones.update([root, (root+4)%12, (root+7)%12])
    elif quality == "m":
        tones.update([root, (root+3)%12, (root+7)%12])
    elif quality == "d":
        tones.update([root, (root+3)%12, (root+6)%12])

    if extension == "6":
        tones.add((root+9)%12)
    elif extension == "7":
        tones.add((root+10)%12)
    elif extension == "4":
        tones.add((root+5)%12)

    return tones
