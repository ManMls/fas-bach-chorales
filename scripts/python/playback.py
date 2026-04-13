#!/usr/bin/env python3

import sys
import numpy as np
import sounddevice as sd

dataDir = "../../data/processed/"
fileName = sys.argv[1]
choraleFilePath = dataDir + fileName

try:
    f = open(choraleFilePath, 'r')
except OSError:
    print("Couldn't open file: ", fileName)
    print("\tDid you run 'scripts/bash/extract_chorale_events.sh'?")
    sys.exit()

# data from https://tunableapp.com/temperaments/werckmeister-iii/
freq = [ 
    261.626, #C4
    277.183, #Db4
    293.665, #D4
    311.127, #Eb4
    329.628, #E4
    349.228, #F4
    369.994, #Gb4
    391.995, #G4
    415.305, #Ab4
    440.000, #A4
    466.164, #Bb4
    493.883  #B4
]

# Uncomment for 12-TET instead of the above
#f0 = 261.625565  # C4
#n = np.arange(12)  # 12 semitones
#freq = f0 * (2 ** (n / 12))

eventTime = 1
sampleRate = 44100
sd.default.samplerate = sampleRate

N = int(sampleRate*eventTime)
tSample = np.arange(N) / sampleRate

audio = []
fade = int(0.1 * sampleRate)
attack = np.linspace(0, 1, fade)
sustain = np.ones(N - 2 * fade)
release = np.linspace(1, 0, fade)
envelope = np.concatenate([attack, sustain, release])

with open(choraleFilePath, 'r') as f:
    for line in f:
        notes = line.strip().split()
        signal = np.zeros(N)
        for i, note in enumerate(notes):
            if int(note) == 1:
                signal += np.sin(2 * np.pi * freq[i] * tSample)

        # normalize
        max_amp = np.max(np.abs(signal)) + 1e-9
        signal /= max_amp
        signal *= envelope

        audio.append(signal)

audio = np.concatenate(audio)
audio /= np.max(np.abs(audio) + 1e-9)

sd.play(audio)
sd.wait()
