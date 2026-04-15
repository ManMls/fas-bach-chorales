#!/usr/bin/env python3 
import os 
import sys 
import pandas as pd 
import numpy as np 
import sounddevice as sd 

dataDir = "../../data/" 

df = pd.read_csv(f"{dataDir}raw/bach_chorales.dataset") 
pitch_cols = df.columns[3:14] 
df[pitch_cols] = (df[pitch_cols] == "YES").astype(int) 

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
    493.883 #B4 
] 

# Uncomment for 12-TET instead of the above (baroque temperament) 
#f0 = 261.625565 # C4 
#n = np.arange(12) # 12 semitones 
#freq = f0 * (2 ** (n / 12)) 

def get_chorale(df, chorale_id):
    return df[df["choral_ID"] == chorale_id] 

def synthesize(chorale_id, freq, sampleRate=44100, eventTime=2.5):
    N = int(sampleRate * eventTime) 
    t = np.arange(N) / sampleRate

    fade = int(0.1 * sampleRate) 
    attack = np.linspace(0, 1, fade) 
    sustain = np.ones(N - 2 * fade) 
    release = np.linspace(1, 0, fade) 
    envelope = np.concatenate([attack, sustain, release])
    
    audio = [] 
    for _, row in chorale.iterrows(): 
        signal = np.zeros(N) 

        for i, active in enumerate(row[pitch_cols].values): 
            if active: 
                signal += np.sin(2 * np.pi * freq[i] * t) 

        # normalize 
        signal /= np.max(np.abs(signal) + 1e-9) 
        signal *= envelope 

        audio.append(signal)

    audio = np.concatenate(audio) 
    audio /= np.max(np.abs(audio) + 1e-9) 
    return audio 

# --------- 
chorale_id = sys.argv[1] 
cache_path = f"{dataDir}cache/chorale_{chorale_id}.npy" 

chorale = get_chorale(df, chorale_id) 

if os.path.exists(cache_path):
    print("trovato cachato") 
    audio = np.load(cache_path)
else: 
    print("non trovato ma ora lo cacho") 
    audio = synthesize(chorale, freq) 
    os.makedirs("../../data/cache", exist_ok=True) 
    np.save(cache_path, audio) 

sd.play(audio) 
sd.wait()
