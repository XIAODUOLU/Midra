# Note and Duration Generation Knowledge Based on Chord Progressions

## 1. Document Goal

This document guides how to generate suitable notes for different timbres and instruments after the following context is already determined: key, chord degrees, concrete chords, section structure, BPM, and time signature.

It covers note selection, register range, rhythmic patterns, duration, velocity tendency, and track role for drums, bass, chord accompaniment, pads, lead melody, arpeggios, strings, brass, piano, guitar, ethnic / East-Asian instruments, and FX / transition sounds.

---

# 2. Core Principles

## 2.1 Chord progression is the foundation

Before generating MIDI notes, identify which chord is active at the current time.

- Bass: prefer current chord root; may add fifth, octave, and passing tones.
- Chord track: mainly use current chord tones.
- Pad: use current chord tones with longer durations.
- Lead: use chord tones on strong beats and in-key passing tones on weak beats.
- Arpeggio: break current chord tones into sequential notes.
- Drums: do not use chord pitches, but rhythm should follow chord and section changes.
- Strings / brass: use chord tones, sustained tones, accents, and counter-lines.
- Ethnic / East-Asian instruments: prefer modal scale tones and structural tones; avoid overly complex harmony.

## 2.2 Strong beats prefer chord tones

In 4/4, beat 1 and beat 3 are strong beats; beat 2 and beat 4 are secondary strong beats; offbeats and syncopations are weak beats.

Recommended:

- Strong beats: root, third, fifth.
- Weak beats: in-key passing tones, neighbor tones, ornaments.
- Endings: prefer current chord tones, especially root or third.

## 2.3 Different instruments have different duration tendencies

- Drums: 0.05 - 0.25 beats.
- Bass: mostly 0.25 - 1 beat; slow music may use 2 - 4 beats.
- Chord accompaniment: 0.5 - 4 beats.
- Pad: 2 - 8 beats, often sustained across bars.
- Lead melody: 0.25 - 2 beats, varied by motif.
- Arpeggio: mostly 0.25 - 0.5 beats.
- Long strings: 2 - 8 beats.
- Brass accents: 0.5 - 2 beats.
- Piano accompaniment: 0.25 - 2 beats, mixing long and short values.
- Guitar strumming: 0.25 - 1 beat.
- Ethnic melodic instruments: 0.25 - 2 beats, often with more space.

## 2.4 Register should fit the instrument role

- Bass: C1 - C3.
- Low strings / cello / low brass: C2 - C4.
- Piano left hand: C2 - C4.
- Piano right hand: C3 - C6.
- Chords / Pad: C3 - C5.
- Lead: C4 - C6.
- High accents: C5 - C7.
- Drums: use GM drum pitches; do not interpret as melodic register.

## 2.5 Section energy determines density

- Intro: few notes, long durations, low density.
- Main: complete rhythmic patterns, stable density.
- Climax: higher register, stronger velocity, denser rhythm.
- Ending: reduce notes or use strong / suspense cadence.

---

# 3. Drums

Drums do not use chord pitches, but their rhythmic emphasis should follow chord progression and section structure.

Recommended:

- Add kick or crash at bars where chords change.
- Add crash at new section starts.
- Add fills on the final chord of a loop to return to the beginning.
- Increase hi-hat, kick, and tom-fill density in climax sections.

Common roles:

- Kick: low-frequency center, often beats 1 and 3 or synchronized with bass.
- Snare / Clap: backbeat center, often beats 2 and 4.
- Closed Hat: subdivision rhythm and groove density.
- Open Hat: second half of bar, weak beats, or pre-transition.
- Crash: section starts, climax starts, loop returns.
- Tom: fills, transitions, battle-energy reinforcement.

Durations:

- Kick: 0.05 - 0.15 beats.
- Snare: 0.05 - 0.2 beats.
- Hi-hat: 0.05 - 0.15 beats.
- Crash: 0.25 - 1 beat.
- Tom: 0.1 - 0.25 beats.

Style patterns:

- Electronic / Cyberpunk: kick on 1 and 3 with syncopation, snare on 2 and 4, 1/8 or 1/16 hats, crash at section start, fill every 4 or 8 bars.
- Lo-fi / Chill: sparse kick, slightly laid-back snare on 2 and 4, mostly 1/8 hats with lower velocity, minimal fills.
- Rock / Metal: kick synchronized with bass/guitar roots, strong snare on 2 and 4, continuous hat/ride, crash on strong beats, tom fills before transitions.
- Traditional / East-Asian: taiko / kick emphasizes beat 1 or section accents, sparse percussion, more space, big-drum rolls as fills.

---

# 4. Bass

Bass is the harmonic foundation and clarifies the current chord.

Note priority:

1. current chord root
2. fifth
3. octave root
4. in-key passing tone
5. chromatic passing tone only for special styles

Register:

- Normal / electronic bass: C1 - C3.
- Acoustic bass: E1 - C3.
- Synth sub bass: C1 - C2 for pressure.
- Melodic bass: C2 - C3.

Duration by style:

- Slow / ambient: one long note per bar, 2 - 4 beats.
- Pop / BGM: one note per beat or half-beat, 0.5 - 1 beat.
- Electronic / battle: mostly 1/8 rhythm, 0.25 - 0.5 beats.
- Metal / rock: repeated roots, 0.25 - 0.5 beats.
- Lo-fi: relaxed, mostly 0.5 - 1 beat, can be syncopated.

Common patterns:

- Root Only: root at chord start, 2 - 4 beats; good for intro, ambient, pad atmosphere.
- Root Pulse: repeat root every beat, 0.5 - 1 beat; good for pop/game BGM.
- Root-Octave: alternate root and octave, 0.25 - 0.5 beats; good for electronic, 8-bit, cyberpunk.
- Root-Fifth: alternate root and fifth, 0.5 - 1 beat; good for rock, folk, RPG, medieval / fantasy.
- Syncopated Bass: root/octave/fifth with syncopation, 0.25 - 0.5 beats; good for cyberpunk, Boss battle, electronic, funk.

When chords change, the first bass note of each new chord should prefer the current chord root. Between chord changes, use fifths, octaves, and passing tones. Avoid staying on a previous chord root after harmony changes.

---

# 5. Chord Accompaniment

Chord tracks directly present current harmony.

Use current chord root, third, and fifth. Optional color tones such as seventh/ninth may be used only when compatible with context, but MVP should prioritize triads.

Register: C3 - C5. Avoid being too low (muddy, conflicts with bass) or too high (steals lead space).

Duration types:

- Long chords: one chord lasts a full bar, usually 4 beats in 4/4. Good for pad, string bed, slow BGM, intro, ambient.
- Rhythmic chords: repeat current chord multiple times per bar. Good for piano, guitar strumming, electronic stabs, pop BGM. Common durations: 1, 0.5, or 0.25 beats.
- Chord stabs: short chord accents, 0.25 - 0.75 beats. Good for electronic, funk, battle, brass, orchestral hits.

Generation principles:

- Update chord tones at every chord-change point.
- Keep neighboring chords smooth.
- Retain common tones when possible.
- Avoid all chord voices leaping at once.
- Avoid sharing the same register as lead for long periods.

Style expression:

- Pop / Warm: stable rhythmic chords, every beat or every two beats, medium velocity, 0.5 - 1.5 beats.
- Electronic / Cyberpunk: short synth stabs or pads, syncopated, 0.25 - 1 beat.
- Lo-fi: soft electric piano chords, longer durations, light syncopation, not too dense.
- Epic / Orchestral: long string chords plus short brass accents, clear changes every bar or every two bars.

---

# 6. Pad / Atmospheric Bed

Pad establishes space, emotion, and sustained harmony. It extends chords, fills background, creates atmosphere, and smooths transitions.

Note choice:

- mainly current chord tones: root, third, fifth.
- seventh or ninth may be added sparingly if suitable.
- if bass covers low end, omit low root and use higher voicing.

Register: C3 - C5 or C4 - C6. Avoid sustained pads below C2 and overly high/bright pads.

Durations: 2, 4, or 8 beats; sustained across bars.

Usage:

- Intro: pad may enter before drums and bass.
- Main: background support, not too prominent.
- Climax: raise octave or increase note count.
- Ending: extend final chord for closure or suspense.

---

# 7. Lead Melody

Lead is the most memorable part and must reference current key, chord, section energy, rhythm density, and instrument timbre.

Note choice:

- Strong beats: current chord tones.
- Weak beats: in-key scale tones.
- Passing tones: connect two chord tones.
- Ornaments: short notes near the main note.
- Ending notes: prefer current chord tones.

Register:

- Normal lead / 8-bit lead / female-like synth lead: C4 - C6.
- Flute / dizi-like: C5 - C6 for brightness.
- Violin: G3 - C6, usually C4 - C6 for melody.
- Brass lead: C3 - C5.

Durations should form motifs, not random averages:

- short-short-long: 0.5 + 0.5 + 1.0.
- short-short-short-long: 0.25 + 0.25 + 0.5 + 1.0.
- syncopated: 0.5 + 1.0 + 0.5.
- long-note answer: 1.0 + 1.0 + 2.0.
- recommended range: 0.25 - 2 beats.

At the start of each new chord, the first lead note should preferably be root, third, or fifth. Within bars, use in-key passing tones, neighbor tones, repeated notes, and leaps followed by stepwise return.

Generation principles:

- Use short motifs and repeat them.
- Vary motifs slightly when repeated.
- Avoid every bar being random.
- Avoid continuous large leaps.
- Avoid the same note density throughout.
- In climax, raise register or increase rhythm density.

Style usage:

- 8-bit: clear short motifs, more leaps, strong rhythm, strong beats on chord tones.
- Cyberpunk: short repeated motifs, syncopation, saw/square timbre, more repetition and ascent in high energy.
- Fantasy / RPG: singable melodies, more stepwise motion, flute/strings/harp responses.
- Traditional / East-Asian: more space, pentatonic tendency, avoid overly dense modern pop ornaments.
- Lo-fi: simple relaxed melody, not too dense, suitable for electric piano/vibraphone/soft synth.

---

# 8. Arpeggio

Arpeggio breaks current chord tones into sequential notes to add flow.

Use root, third, fifth, octave root, optional seventh.

Register:

- general: C3 - C6.
- low arpeggio: C2 - C4.
- high sparkling arpeggio: C5 - C7.

Durations:

- 1/8 note: 0.5 beats.
- 1/16 note: 0.25 beats.
- slow arpeggio: 1 or 0.5 beats.
- fast electronic / 8-bit: 0.25 beats.

Directions:

- ascending: root → third → fifth → octave.
- descending: octave → fifth → third → root.
- up-down: root → third → fifth → octave → fifth → third.
- leaping: root → fifth → octave → third.

Style use:

- 8-bit: fast 1/8 or 1/16 arpeggios, can replace full chords.
- Electronic / cyberpunk: repeating arpeggios for tension and groove.
- Fantasy: harp arpeggios, not too fast, good for transitions and dreaminess.
- Lo-fi: sparse soft arpeggios as background decoration.

---

# 9. Piano / Electric Piano

Piano can do chord accompaniment, lead melody, bass, arpeggio, and rhythmic accompaniment, but should not take all roles unless it is a piano solo.

Left hand:

- root long notes.
- root + fifth.
- root + octave.
- broken-chord bass.
- register C2 - C4.
- duration 0.5 - 4 beats.

Right hand:

- chords.
- melody.
- broken chords.
- ornaments.
- register C3 - C6.
- duration 0.25 - 2 beats.

Patterns:

- Block chords: full chord together; fits pop, lyrical, warm music; 1 - 4 beats.
- Broken chords: split chord tones; fits lyrical, fantasy, piano solo; 0.25 - 0.5 beats.
- Offbeat chords: weak-beat/backbeat chords; fits lo-fi, light music, pop; 0.25 - 1 beat.

---

# 10. Guitar

Guitar usually provides strumming, broken chords, rhythmic accompaniment, power chords, or riffs.

Acoustic guitar:

- fits folk, warmth, travel, everyday, light music.
- use chord tones: root + third + fifth; high string repetition allowed.
- strumming duration: 0.25 - 1 beat.
- broken duration: 0.25 - 0.5 beats.
- rhythm: four strums per bar or 1/8 broken chords.

Clean / muted electric guitar:

- fits city pop, funk, light pop, rhythmic accompaniment.
- use upper chord tones, short repeated chords, offbeat chords.
- duration 0.1 - 0.5 beats.

Distortion / metal guitar:

- fits rock, metal, battle, Boss.
- use root, fifth, octave, power-chord logic.
- duration 0.25 - 1 beat.
- rhythm: repeated roots, syncopated roots, strong-beat power chords.
- avoid dense full triads because distortion can become muddy.

---

# 11. Strings

Strings can provide long beds, chord support, melodies, tremolo tension, pizzicato rhythm, and epic layering.

- Long strings: current chord tones, thirds/fifths for color, low voices can use roots; 2 - 8 beats; fits epic/fantasy/lyrical/horror/ambient.
- Short / staccato strings: root, fifth, chord tones; 0.25 - 0.75 beats; fits battle/chase/tension/trailer.
- Pizzicato: current chord tones, root/fifth priority; 0.25 - 0.5 beats; fits stealth/humorous/light/medieval/fantasy.
- Tremolo strings: current chord tones; in minor often tones from i, iv, V, VI; 1 - 4 beats; fits suspense/horror/tension/dark orchestral.

---

# 12. Brass

Brass is suitable for strong themes, heroic melodies, climax accents, short stabs, and epic layers.

Note choice: current chord root, fifth, third, octave root.

Avoid excessive quick passing tones, overly dense small notes, and long piercing high-register notes.

Durations:

- short accents: 0.5 - 1 beat.
- theme melody: 0.5 - 2 beats.
- long support: 2 - 4 beats.

Use:

- Epic / orchestral: reinforce chords with root/fifth, add high brass in climax, use strong V→i or V→I resolution.
- Battle: short stabs, emphasize chord changes, synchronize with crash/kick.
- Adventure: singable horn melody, strong beats on chord tones, avoid excessive density.

---

# 13. Woodwinds / Flutes

Woodwinds work for lead, countermelody, ornaments, natural/fantasy ambience, and East-Asian melodic color.

Rules:

- strong beats land on chord tones.
- weak beats use in-key passing tones.
- prefer stepwise motion.
- reduce continuous large leaps.

Durations:

- normal melody: 0.5 - 2 beats.
- ornaments: 0.125 - 0.25 beats.
- long tones: 2 - 4 beats.

Style use:

- Fantasy / RPG: flute lead, singable melody, stepwise motion and small leaps.
- Traditional / East-Asian: flute/shakuhachi-like timbre, more space, avoid dense Western-pop melodic writing.
- Horror / suspense: isolated long tones, short ornaments, unstable intervals, slower rhythms.

---

# 14. Ethnic / East-Asian Instruments

Do not rely only on timbre replacement. More important: melodic space, pentatonic tendency, limited ornaments, simple harmony, and rhythm that is not overly Western-pop-like.

Koto / guzheng-like:

- roles: broken chords, high accents, slide-like ornaments, transitions.
- notes: current chord tones, modal structural tones, pentatonic notes.
- duration: 0.25 - 0.5 beats for arpeggio; 1 - 2 beats for accent long notes.

Shakuhachi / flute-like:

- roles: lead melody, lonely atmosphere, East-Asian fantasy, suspense.
- notes: chord tones on strong beats, in-key tones on weak beats, more space, avoid density.
- duration: 0.5 - 2 beats; long tones up to 4 beats.

Taiko / big drum:

- roles: section accents, epic/battle feeling, low-frequency impact.
- duration: 0.1 - 0.25 beats.
- use at section starts, beat 1, fills before climax, loop return.

---

# 15. FX / Transition Timbres

FX usually does not carry main harmony. It is used for transitions, atmosphere, rises, falls, suspense, and space.

Harmony relation:

- before transition: use current chord tones or dominant-function tones.
- entering a new section: land on new chord root or fifth.
- horror atmosphere: unstable tones may be used, but should not destroy overall tonality too much.

Durations:

- short FX: 0.25 - 1 beat.
- rise / sweep: 1 - 4 beats.
- ambient long tone: 4 - 16 beats.

---

# 16. General Multi-Track Generation Flow

For each chord:

- Drums: create rhythmic center, not chord pitches.
- Bass: state root at chord start.
- Chords: play full or partial chord tones.
- Pad: sustain current chord.
- Lead: chord tones on strong beats, in-key tones on weak beats.
- Arp: break current chord.
- FX: appear around chord or section changes.

Default one-chord-per-bar generation in 4/4:

- Beat 1: bass root, kick, chord/pad starts, lead may land on chord tone.
- Beat 2: snare, lead develops motif.
- Beat 3: bass root/fifth/octave, kick, chord repeats or sustains.
- Beat 4: snare, transition note or fill.
- End of bar: passing tones may lead to next chord.

If harmonic rhythm is two chords per bar, first chord starts on beat 1 and second chord starts on beat 3. Bass and chords should switch accordingly; lead should land near those beats on corresponding chord tones.

---

# 17. Multi-Track Suggestions by Style

## 17.1 Cyberpunk Battle

- Drums: high-density kick / snare / hat.
- Bass: synth bass, root-octave or syncopated.
- Chords: short synth stabs or dark pads.
- Lead: saw / square short motifs.
- FX: sweep / sci-fi transition.
- Durations: bass 0.25 - 0.5; chords 0.25 - 1 or long pad; lead 0.25 - 1; pad 4; drums 1/8 or 1/16 hats.

## 17.2 8-bit / Retro Game

- Drums: simple electronic drums.
- Bass: square / synth bass, root-octave.
- Chords: arpeggio instead of full chords.
- Lead: clear square melody.
- Durations: bass 0.25 - 0.5; arp 0.25 - 0.5; lead 0.25 - 1; fewer long chords, more broken patterns.

## 17.3 Fantasy / RPG

- Drums: sparse or orchestral percussion.
- Bass: cello / low string roots.
- Chords: strings / harp.
- Lead: flute / violin / horn.
- Arp: harp broken chords.
- Durations: bass 1 - 4; pad/strings 2 - 8; harp arp 0.25 - 0.5; lead 0.5 - 2.

## 17.4 Lo-fi / Chill

- Drums: low-density, relaxed.
- Bass: soft electric bass.
- Chords: electric piano chords.
- Lead: vibraphone / soft synth / simple piano.
- Durations: bass 0.5 - 1; chords 1 - 4 and may syncopate; lead 0.5 - 2 with space; drums mainly 1/8 lower velocity.

## 17.5 Traditional / East-Asian Fantasy

- Drums: sparse big drums.
- Bass: low strings or simple roots.
- Chords: pad or simplified chords.
- Lead: flute / shakuhachi / koto-like instruments.
- Arp: koto / harp-like broken tones.
- Durations: bass 1 - 4; lead 0.5 - 2 with more space; arp 0.25 - 0.5 as accents; pad 4 - 8.

## 17.6 Horror / Suspense

- Drums: very few or none.
- Bass: low long tone / drone.
- Chords: tremolo strings / metallic pad.
- Lead: isolated woodwind or high FX.
- FX: ambience, echo, strange timbres.
- Durations: bass 4 - 16; pad 4 - 16; lead 1 - 4 with large gaps; FX long tones or short bursts; drums sparse low impacts.

## 17.7 Epic / Orchestral

- Drums: timpani / taiko / crash.
- Bass: low string roots.
- Chords: long strings.
- Lead: horn / trumpet / string melody.
- Brass: strong-beat accents.
- Choir: long background tones.
- Durations: bass 1 - 4; strings 2 - 8; brass stabs 0.5 - 1; lead 0.5 - 2; choir 4 - 8.

---

# 18. Section Energy and Density

- Intro: drums absent/low density, bass long tone/root, chords/pad long tones, lead few motifs or absent, optional sparse arp; durations mainly 2 - 8 beats.
- Main: complete drums, stable bass pattern, stable chords/pad, full lead theme, optional arp; mixed durations 0.25 - 4 beats.
- Climax: denser drums, more active bass, stronger/higher chords, higher and denser lead, brass/strings accents; more short values, higher velocity and register.
- Ending / Loop: drums fill/crash, bass guides back to opening root, chords final chord returns naturally to first chord, lead lands on leading tone or tonic, FX sweep/transition.

---

# 19. Common Mistakes

- All instruments play full chords: causes crowding, unclear roles, muddy low end, weak melody. Correct division: bass roots, chords harmony, pad sustained harmony, lead melody, arp broken chord.
- Bass does not follow chord roots: bass should prefer the current chord root at each chord start.
- Lead strong beats use too many non-chord tones: strong beats should prefer current chord tones; weak beats may use in-key passing tones.
- Pad is too short: pad should use 2 - 8 beat long tones, not many 0.25 beat notes.
- Drums ignore section changes: add crash at section starts, fill at loop end, increase hat/kick density in climax.
- All tracks have same rhythmic density: bass stable, chords medium, lead breathes, arp may move, pad sustains.

---

# 20. Minimal Usage Rules

1. Determine the current chord for each bar/beat first.
2. Bass uses root at each chord start.
3. Chords use current chord tones.
4. Pad uses current chord tones with long durations.
5. Lead uses chord tones on strong beats and in-key passing tones on weak beats.
6. Arp breaks current chord tones.
7. Drums do not use chord pitches, but emphasize chord and section changes.
8. Each instrument should occupy a different register.
9. Each instrument should have different rhythmic density.
10. Intro uses low density and long durations.
11. Main uses complete rhythmic patterns.
12. Climax increases density, velocity, and register.
13. Loop ending should let bass, chords, and lead naturally return to the opening chord.
14. Do not make all instruments play full chords simultaneously.
15. Do not let melody or bass stay detached from the current chord for long.

Recommended role division:

- Drums: rhythmic skeleton, sections, loops.
- Bass: harmonic foundation, current chord clarity.
- Chords: direct harmony.
- Pad: extended harmony and atmosphere.
- Lead: memorable melody based on chord and mode.
- Arp: broken chord and flow.
- Strings / Brass: emotional, epic, section energy.
- FX: transitions and atmosphere.

Core generation logic:

```text
current chord
  ↓
determine each instrument role
  ↓
choose register
  ↓
choose note source: root / chord tone / in-key tone / passing tone
  ↓
choose duration: long tone / rhythmic pattern / short accent / arpeggio
  ↓
adjust density, velocity, and register according to section energy
```

Final goal: make bass, harmony, melody, and rhythm unfold around the same chord progression, producing MIDI that is structurally clear, stylistically coherent, loopable, and controllable.
