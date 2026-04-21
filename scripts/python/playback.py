#!/usr/bin/env python3 
import os 
import numpy as np 
import pitch_utils as pu

# data from https://tunableapp.com/temperaments/werckmeister-iii/ 
freq = [ 
    261.626, #C4 
    277.183, #C#4, Db4 
    293.665, #D4 
    311.127, #D#4, Eb4 
    329.628, #E4 
    349.228, #F4 
    369.994, #F#4, Gb4 
    391.995, #G4 
    415.305, #G#4, Ab4
    440.000, #A4 
    466.164, #A#4, Bb4 
    493.883  #B4 
] 

#Uncomment for 12-TET instead of the above (baroque temperament) 
#f0 = 261.625565 # C4 
#n = np.arange(12) # 12 semitones 
#freq = f0 * (2 ** (n / 12)) 

def compute_signal(frequency, t, harmonics=3, alpha=0.8):
    signal = 0.0
    for n in range(1, harmonics+1):
        amplitude = np.exp(-alpha * (n-1)) 
        signal += amplitude * np.sin(2 * np.pi * frequency * n * t) 
    return signal

def synthesize(chorale_df, pitch_cols, bass_col, sampleRate=44100, eventTime=2):
    N = int(sampleRate * eventTime)
    t = np.arange(N) / sampleRate

    fade = int(0.05 * sampleRate)
    attack = np.linspace(0, 1, fade) 
    sustain = np.ones(N - 2 * fade) 
    release = np.linspace(1, 0, fade)
    envelope = np.concatenate([attack, sustain, release])
    
    bass_gain = 1.3
    audio = [] 
    for _, row in chorale_df.iterrows(): 
        signal = np.zeros(N) 
        
        # Computes pitches columns
        for i, active in enumerate(row[pitch_cols].values): 
            if active: 
                signal += compute_signal(freq[i], t)
        
        # Computes bass column
        bass_idx = pu.pitch_class(row[bass_col])
        signal += bass_gain * compute_signal(freq[bass_idx]/4, t, 5, 1)

        signal /= np.max(np.abs(signal) + 1e-9)
        signal *= envelope
        audio.append(signal)

    audio = np.concatenate(audio) 
    audio /= np.max(np.abs(audio) + 1e-9) 
    return audio 

def get_audio(chorale_id, df, pitch_cols, dataDir):
    cache_path = os.path.join(dataDir, f"cache/chorale_{chorale_id}.npy")

    chorale = df[df["chorale_ID"] == chorale_id]

    if os.path.exists(cache_path):
        return np.load(cache_path)

    audio = synthesize(chorale, freq, pitch_cols)
    
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    np.save(cache_path, audio)

    return audio
