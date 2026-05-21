# General MIDI Instrument Reference

## 1. Core Rule

- In this project, `program` uses the range `0–127`.
- Standard General MIDI numbering is usually written as `1–128`.
- Therefore: `program = general_midi_number - 1`.

Examples:

- General MIDI 1 = Acoustic Grand Piano → mido program 0
- General MIDI 25 = Acoustic Guitar nylon → mido program 24
- General MIDI 81 = Lead 1 square → mido program 80

---

## 2. General MIDI Instrument Families (program 0–127)

### Piano

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 0 | 1 | Acoustic Grand Piano |
| 1 | 2 | Bright Acoustic Piano |
| 2 | 3 | Electric Grand Piano |
| 3 | 4 | Honky-tonk Piano |
| 4 | 5 | Electric Piano 1 |
| 5 | 6 | Electric Piano 2 |
| 6 | 7 | Harpsichord |
| 7 | 8 | Clavinet |

Suggested use:

- 0: general piano melody/accompaniment
- 1: brighter piano texture
- 4: lo-fi / R&B / soft electric piano
- 5: dreamy electric piano
- 6: baroque / retro color
- 7: funk / vintage keyboard

### Chromatic Percussion

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 8 | 9 | Celesta |
| 9 | 10 | Glockenspiel |
| 10 | 11 | Music Box |
| 11 | 12 | Vibraphone |
| 12 | 13 | Marimba |
| 13 | 14 | Xylophone |
| 14 | 15 | Tubular Bells |
| 15 | 16 | Dulcimer |

Suggested use:

- 8: dreamy / fairy / magical tone
- 9: crisp high accents
- 10: cute / creepy lullaby / music-box color
- 11: jazz / soft ambience
- 12: tropical / light wooden feel
- 14: bells / epic / suspense

### Organ

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 16 | 17 | Drawbar Organ |
| 17 | 18 | Percussive Organ |
| 18 | 19 | Rock Organ |
| 19 | 20 | Church Organ |
| 20 | 21 | Reed Organ |
| 21 | 22 | Accordion |
| 22 | 23 | Harmonica |
| 23 | 24 | Tango Accordion |

Suggested use:

- 16: jazz / blues / vintage
- 18: rock
- 19: church / sacred / gothic

### Guitar

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 24 | 25 | Acoustic Guitar nylon |
| 25 | 26 | Acoustic Guitar steel |
| 26 | 27 | Electric Guitar jazz |
| 27 | 28 | Electric Guitar clean |
| 28 | 29 | Electric Guitar muted |
| 29 | 30 | Overdriven Guitar |
| 30 | 31 | Distortion Guitar |
| 31 | 32 | Guitar Harmonics |

Suggested use:

- 24/25: folk / acoustic accompaniment
- 27: clean guitar / city pop / pop
- 28: muted rhythm / funk
- 30: heavy rock / battle / metal

### Bass

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 32 | 33 | Acoustic Bass |
| 33 | 34 | Electric Bass finger |
| 34 | 35 | Electric Bass pick |
| 35 | 36 | Fretless Bass |
| 36 | 37 | Slap Bass 1 |
| 37 | 38 | Slap Bass 2 |
| 38 | 39 | Synth Bass 1 |
| 39 | 40 | Synth Bass 2 |

Suggested use:

- 33: all-purpose pop bass
- 34: rock / clearer picked bass
- 38/39: electronic / cyberpunk / game BGM

### Strings

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 40 | 41 | Violin |
| 41 | 42 | Viola |
| 42 | 43 | Cello |
| 43 | 44 | Contrabass |
| 44 | 45 | Tremolo Strings |
| 45 | 46 | Pizzicato Strings |
| 46 | 47 | Orchestral Harp |
| 47 | 48 | Timpani |

### Ensemble

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 48 | 49 | String Ensemble 1 |
| 49 | 50 | String Ensemble 2 |
| 50 | 51 | Synth Strings 1 |
| 51 | 52 | Synth Strings 2 |
| 52 | 53 | Choir Aahs |
| 53 | 54 | Voice Oohs |
| 54 | 55 | Synth Voice |
| 55 | 56 | Orchestra Hit |

### Brass

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 56 | 57 | Trumpet |
| 57 | 58 | Trombone |
| 58 | 59 | Tuba |
| 59 | 60 | Muted Trumpet |
| 60 | 61 | French Horn |
| 61 | 62 | Brass Section |
| 62 | 63 | Synth Brass 1 |
| 63 | 64 | Synth Brass 2 |

### Reed

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 64 | 65 | Soprano Sax |
| 65 | 66 | Alto Sax |
| 66 | 67 | Tenor Sax |
| 67 | 68 | Baritone Sax |
| 68 | 69 | Oboe |
| 69 | 70 | English Horn |
| 70 | 71 | Bassoon |
| 71 | 72 | Clarinet |

### Pipe

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 72 | 73 | Piccolo |
| 73 | 74 | Flute |
| 74 | 75 | Recorder |
| 75 | 76 | Pan Flute |
| 76 | 77 | Blown Bottle |
| 77 | 78 | Shakuhachi |
| 78 | 79 | Whistle |
| 79 | 80 | Ocarina |

### Synth Lead

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 80 | 81 | Lead 1 square |
| 81 | 82 | Lead 2 sawtooth |
| 82 | 83 | Lead 3 calliope |
| 83 | 84 | Lead 4 chiff |
| 84 | 85 | Lead 5 charang |
| 85 | 86 | Lead 6 voice |
| 86 | 87 | Lead 7 fifths |
| 87 | 88 | Lead 8 bass + lead |

### Synth Pad

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 88 | 89 | Pad 1 new age |
| 89 | 90 | Pad 2 warm |
| 90 | 91 | Pad 3 polysynth |
| 91 | 92 | Pad 4 choir |
| 92 | 93 | Pad 5 bowed |
| 93 | 94 | Pad 6 metallic |
| 94 | 95 | Pad 7 halo |
| 95 | 96 | Pad 8 sweep |

### Synth FX

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 96 | 97 | FX 1 rain |
| 97 | 98 | FX 2 soundtrack |
| 98 | 99 | FX 3 crystal |
| 99 | 100 | FX 4 atmosphere |
| 100 | 101 | FX 5 brightness |
| 101 | 102 | FX 6 goblins |
| 102 | 103 | FX 7 echoes |
| 103 | 104 | FX 8 sci-fi |

### Ethnic

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 104 | 105 | Sitar |
| 105 | 106 | Banjo |
| 106 | 107 | Shamisen |
| 107 | 108 | Koto |
| 108 | 109 | Kalimba |
| 109 | 110 | Bagpipe |
| 110 | 111 | Fiddle |
| 111 | 112 | Shanai |

### Percussive

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 112 | 113 | Tinkle Bell |
| 113 | 114 | Agogo |
| 114 | 115 | Steel Drums |
| 115 | 116 | Woodblock |
| 116 | 117 | Taiko Drum |
| 117 | 118 | Melodic Tom |
| 118 | 119 | Synth Drum |
| 119 | 120 | Reverse Cymbal |

### Sound Effects

| program | GM # | Instrument |
| ------: | ---: | ---------- |
| 120 | 121 | Guitar Fret Noise |
| 121 | 122 | Breath Noise |
| 122 | 123 | Seashore |
| 123 | 124 | Bird Tweet |
| 124 | 125 | Telephone Ring |
| 125 | 126 | Helicopter |
| 126 | 127 | Applause |
| 127 | 128 | Gunshot |

Note: SFX instruments vary significantly across soundfonts and are usually not recommended as core musical tracks.

---

## 3. Common Style-to-Instrument Recommendations

### 3.1 8-bit / Retro Game

```json
{
  "lead": 80,
  "bass": 38,
  "chords": 80,
  "pad": 90,
  "drums_channel": 9
}
```

### 3.2 Cyberpunk / Electronic Battle

```json
{
  "lead": 81,
  "bass": 38,
  "chords": 90,
  "pad": 95,
  "fx": 103,
  "drums_channel": 9
}
```

### 3.3 Fantasy / Adventure / RPG

```json
{
  "lead": 73,
  "bass": 42,
  "chords": 48,
  "pad": 88,
  "accent": 46,
  "drums": 47
}
```

### 3.4 Horror / Suspense

```json
{
  "lead": 77,
  "bass": 43,
  "chords": 44,
  "pad": 93,
  "fx": 101
}
```

### 3.5 Lo-fi / Chill

```json
{
  "lead": 4,
  "bass": 33,
  "chords": 4,
  "pad": 89,
  "melody": 11
}
```

### 3.6 Traditional / East-Asian Fantasy

```json
{
  "lead": 77,
  "chords": 107,
  "accent": 15,
  "pad": 88,
  "drums": 116
}
```

Note:

```text
General MIDI does not contain true Erhu, Pipa, Dizi, Guzheng, etc.
Use Shakuhachi, Koto, Dulcimer, Flute, Shamisen, and Taiko Drum as approximations.
```

### 3.7 Rock / Metal Battle

```json
{
  "lead": 30,
  "rhythm_guitar": 29,
  "bass": 34,
  "brass": 61,
  "drums_channel": 9
}
```

### 3.8 Epic / Orchestral Battle

```json
{
  "strings": 48,
  "brass": 61,
  "horn": 60,
  "choir": 52,
  "timpani": 47,
  "taiko": 116
}
```

---

## 4. LLM Decision Rules for Instrument Assignment

The LLM should follow:

```text
1. Use zero-based General MIDI program numbers.
2. program = General MIDI number - 1.
3. Use channel 9 only for drums.
4. Do not set program_change on drum channel 9.
5. For non-drum tracks, set program_change at track start.
6. Validate program range: 0–127.
7. Validate channel range: 0–15.
```

