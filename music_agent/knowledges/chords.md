# Chord Progression Selection Knowledge Document

## 1. Document Goal

This document guides a music-generation agent in choosing suitable modes, chord degrees, and chord progressions according to the user's requested **style, mood, and use case**.

This document describes chord-progression principles using chord degrees. During actual generation, the agent must first select a key and then convert these degrees into concrete chord symbols.

For example, in C major, the chord-degree mapping is:

| Chord degree | Concrete chord | Chord quality | Description |
|---|---|---|---|
| I | C | major triad | Tonic chord, the most stable center |
| ii | Dm | minor triad | Often used for transition and gentle forward motion |
| iii | Em | minor triad | Color chord, emotionally soft |
| IV | F | major triad | Subdominant function, often used for expansion |
| V | G | major triad | Dominant function, tends to push back to I |
| vi | Am | minor triad | Relative minor, often used for lyrical, pop, and slightly sad color |
| vii° | Bdim | diminished triad | Unstable, less common in simple BGM, useful for tension |

Therefore, in C major:

| Degree progression | Actual chord progression |
|---|---|
| I - V - vi - IV | C - G - Am - F |
| I - vi - IV - V | C - Am - F - G |
| I - IV - V - I | C - F - G - C |
| vi - IV - I - V | Am - F - C - G |
| I - V - IV - I | C - G - F - C |
| I - vi - ii - V | C - Am - Dm - G |
| ii - V - I - I | Dm - G - C - C |

Other major keys work the same way: first determine the scale of the selected key, then map I, ii, iii, IV, V, vi, and vii° to concrete chords.

For minor keys, degree-to-chord mapping depends on the minor scale. In A minor:

| Chord degree | Concrete chord | Chord quality | Description |
|---|---|---|---|
| i | Am | minor triad | Minor tonic, dark center |
| ii° | Bdim | diminished triad | Unstable, less common in simple BGM |
| III | C | major triad | Bright color, often used for epic or cinematic progressions |
| iv | Dm | minor triad | Minor subdominant, gloomy and serious |
| v | Em | minor triad | Natural-minor dominant, weaker forward pull |
| V | E | major triad | Harmonic-minor dominant, stronger pull back to i |
| VI | F | major triad | Broad, emotional, epic color |
| VII | G | major triad | Forward motion, loop feeling, cinematic quality |

Therefore, in A minor:

| Degree progression | Actual chord progression |
|---|---|
| i - VI - VII - i | Am - F - G - Am |
| i - VI - III - VII | Am - F - C - G |
| i - VII - VI - VII | Am - G - F - G |
| i - VI - VII - V | Am - F - G - E |
| i - iv - V - i | Am - Dm - E - Am |
| i - V - VI - iv | Am - E - F - Dm |
| i - iv - VII - III | Am - Dm - G - C |

Other minor keys work the same way: first determine the scale of the selected key, then map i, ii°, III, iv, v, VI, and VII to basic chords. If stronger return tension is needed, replace the natural-minor v with V.

---

# 2. Core Principles

## 2.1 Decide the mode first, then choose chord degrees

When generating chord progressions, first decide whether the music should primarily feel **major** or **minor**.

```text
Bright, relaxed, healing, everyday, playful:
Prefer major.

Dark, tense, battle, suspense, epic, dungeon:
Prefer minor.

Sad, lyrical, youth, memory:
Either start from vi in a major key, or use minor.

Traditional / East-Asian fantasy:
Use minor or pentatonic-leaning major. Harmony should not be overly complex.

Lo-fi, Chill, jazz-like:
Major or minor can both work, but seventh-chord colors and smooth movement are more suitable.
```

## 2.2 Use a 4-bar loop by default

For game BGM, short-video background music, and loopable music, a 4-bar loop is recommended by default.

Common structure:

```text
One chord per bar.
Four chords form one loop.
Later sections repeat or vary this loop.
```

Recommended:

```text
In 4/4, use one chord per bar by default.
Intro can use one chord every 2 bars.
Climax can use one chord per bar or two chords per bar.
```

## 2.3 Chord movement should have direction

Do not choose chords randomly. A usable chord progression should satisfy at least one directional logic:

```text
Stable → push → tension → return
Dark → expansion → drive → return to darkness
Bright → emotional shift → expansion → return to brightness
Pressure → descending motion → renewed push → loop
```

Common functional relationships:

```text
I / i:
Tonic function, stable, return point, opening and landing.

IV / iv / VI:
Expansion, preparation, emotional color.

V / VII:
Drive, tension, guide back to tonic.

vi / III:
Emotional, soft, pop-like, cinematic.
```

---

# 3. Common Major-Key Chord Progressions

## 3.1 I - V - vi - IV

### Character

```text
Bright
Pop
Emotional
Positive
Open
```

### Suitable styles

```text
Pop
Youth
Relaxed game BGM
Ending theme
Healing
Open-world exploration
```

### Movement principle

```text
I provides a stable opening.
V adds forward drive.
vi brings a slight emotional turn.
IV expands and naturally returns to I.
```

### Usage advice

This is the most universal major progression. It fits requests such as “good-sounding, relaxed, positive, pop, warm but not childish.”

## 3.2 I - vi - IV - V

### Character

```text
Warm
Retro
Stable
Everyday
Soft
```

### Suitable styles

```text
Everyday story
Slice-of-life BGM
Retro pop
Warm scenes
Relaxed narrative
```

### Movement principle

```text
I establishes stability.
vi shifts into gentle emotion.
IV expands.
V pushes back to I.
```

### Usage advice

Suitable for traditional, gentle music without strong dramatic conflict.

## 3.3 I - IV - V - I

### Character

```text
Simple
Clear
Traditional
Bright
Stable
```

### Suitable styles

```text
Children's music
Educational music
Country
Folk
Classic game music
Simple cheerful BGM
```

### Movement principle

```text
I is stable.
IV expands.
V pushes.
I returns.
```

### Usage advice

This is the most basic and stable major progression. Use it when the music should be clear, simple, and easy to understand.

## 3.4 vi - IV - I - V

### Character

```text
Lyrical
Youthful
Sad but not dark
Pop
Cinematic
```

### Suitable styles

```text
Youth drama
Memories
Gentle scenes
Slight sadness
Lyrical pop
```

### Movement principle

```text
vi starts with an emotional minor chord.
IV provides gentle expansion.
I brings brief stability.
V creates forward motion.
```

### Usage advice

Although this belongs to a major-key system, starting from vi creates a soft sadness similar to minor. It fits “emotional but not oppressive” scenes.

## 3.5 I - V - IV - I

### Character

```text
Open
Natural
Folk-like
Travel-like
Stable
```

### Suitable styles

```text
Travel
Natural scenery
Open world
Country
Relaxed exploration
```

### Movement principle

```text
I expands stably.
V brings outward push.
IV falls back into a gentler region.
I completes the return.
```

### Usage advice

Suitable for spacious BGM where rhythm does not need to be very intense.

---

# 4. Common Minor-Key Chord Progressions

## 4.1 i - VI - VII - i

### Character

```text
Dark
Stable
Mysterious
Strong loop feeling
Not too intense
```

### Suitable styles

```text
Dungeon
RPG
Dark exploration
Suspense
Low-intensity battle
```

### Movement principle

```text
i establishes a dark center.
VI provides broad color.
VII adds forward motion.
i returns to the dark stable point.
```

### Usage advice

Suitable when a minor atmosphere is needed but the music should not become overly tense or dramatic.

## 4.2 i - VI - III - VII

### Character

```text
Epic
Cinematic
Adventure
Wide
Emotionally rich
```

### Suitable styles

```text
Fantasy adventure
Epic orchestral
RPG main story
Battle BGM
Trailer music
```

### Movement principle

```text
i establishes darkness and seriousness.
VI expands emotion.
III brings a bright, open feeling.
VII drives the loop or continues development.
```

### Usage advice

This is highly suitable for “epic, adventure, battle, fantasy” minor music. It contains both darkness and openness.

## 4.3 i - VII - VI - VII

### Character

```text
Descending
Oppressive
Dark
Strong loop feeling
Tense
```

### Suitable styles

```text
Stealth
Dungeon
Dark electronic
Horror
Cyberpunk dark scene
```

### Movement principle

```text
i establishes the dark center.
VII pushes downward.
VI sinks further.
VII rises again, preparing to return to i.
```

### Usage advice

Suitable for music that needs “pressure, darkness, continuous looping.” Very useful as a bass-loop and electronic-rhythm foundation.

## 4.4 i - VI - VII - V

### Character

```text
Tense
Strong drive
Battle-like
Boss-like
Dramatic
```

### Suitable styles

```text
Boss battle
Cyberpunk battle
Action game
Metal battle
Tense chase
```

### Movement principle

```text
i establishes the dark center.
VI expands emotion.
VII increases upward momentum.
V creates a strong tendency to return to i.
```

### Usage advice

This progression is highly suitable for battle music. The final V strengthens tension back to i, making it suitable for boss battles and high-energy BGM.

## 4.5 i - iv - V - i

### Character

```text
Classical
Serious
Fatalistic
Gothic
Strong resolution
```

### Suitable styles

```text
Classical style
Gothic
Serious drama
Fateful scene
Dark orchestral
```

### Movement principle

```text
i establishes the minor center.
iv deepens the gloomy color.
V creates strong dominant function.
i completes stable resolution.
```

### Usage advice

Suitable for scenes requiring traditional minor functional harmony. It feels more serious and fateful than natural-minor loops.

## 4.6 i - V - VI - iv

### Character

```text
Tragic
Dramatic
Emotionally strong
Dark epic
Unsettled
```

### Suitable styles

```text
Tragic drama
Strong emotional climax
Dark epic
Fateful battle
Character sacrifice scene
```

### Movement principle

```text
i establishes the dark center.
V quickly creates tension.
VI expands emotion.
iv sinks the emotion again.
```

### Usage advice

Suitable for music with strong narrative and emotional density. Not suitable for very relaxed loop BGM.

---

# 5. Choose Chord Progressions by Style

## 5.1 Cyberpunk / Electronic Battle

### Recommended mode

```text
Prefer minor.
Natural minor is usable.
Use V in minor when stronger tension is needed.
```

### Recommended degrees

```text
i - VI - VII - V
i - VII - VI - VII
i - VI - III - VII
```

### Movement principle

```text
Bass roots should be clear.
Harmony should not be overly complex.
Emphasize loopability and forward drive.
The final chord should often be V or VII to lead back to i.
```

### Usage advice

Cyberpunk battle music should prioritize rhythm and bass drive. The progression should be stable, short-looping, and clearly tense.

## 5.2 8-bit / Retro Game

### Recommended mode

```text
Bright levels: major.
Dungeon / battle: minor.
Classic arcade feel: either major or minor can work.
```

### Recommended degrees

```text
Major:
I - V - vi - IV
I - IV - V - I

Minor:
i - VI - VII - i
i - VII - VI - VII
```

### Movement principle

```text
Chord progressions should be simple.
Avoid frequent complex changes.
Melody is more important than chords.
Prioritize 4-bar loops.
```

### Usage advice

8-bit music relies more on memorable melodies and rhythmic patterns. Chords only need to provide a clear skeleton.

## 5.3 Fantasy / RPG / Adventure

### Recommended mode

```text
Village / travel / bright adventure: major.
Dungeon / battle / main story: minor.
Epic adventure: minor with bright degrees.
```

### Recommended degrees

```text
Major:
I - V - vi - IV
I - IV - V - I

Minor:
i - VI - III - VII
i - iv - VII - III
i - VI - VII - V
```

### Movement principle

```text
Adventure needs open harmonic movement.
Epic feeling fits i - VI - III - VII.
Dark scenes fit i - VII - VI - VII.
The ending can use VII or V to return to i.
```

### Usage advice

Fantasy RPG progressions should not be too modern or complex. They should remain clear, melody-friendly, and loopable.

## 5.4 Horror / Suspense / Dark Atmosphere

### Recommended mode

```text
Prefer minor.
A single i can be held for a long time.
Chromatic tendency or modal borrowing can create unease.
```

### Recommended degrees

```text
i
i - bII
i - VII - VI - VII
i - iv - V - i
```

### Movement principle

```text
Chord changes can be very slow.
A full 4-chord loop is not always needed.
Long stays on i can create pressure.
bII can create strong unease and alien color.
Avoid overly bright pop progressions.
```

### Usage advice

Horror music does not always need a “beautiful” chord progression. The focus is suspension, pressure, instability, and space.

## 5.5 Lo-fi / Chill

### Recommended mode

```text
Major or minor can both work.
Soft major and relative minor are more suitable.
Seventh-chord color is suitable.
```

### Recommended degrees

```text
I - vi - IV - V
vi - IV - I - V
ii - V - I - I
I - vi - ii - V
```

### Movement principle

```text
Avoid strong battle-like dominant function.
Progression should be smooth.
It should loop but not feel too mechanical.
Use gentle descending motion or ii - V - I logic.
```

### Usage advice

Lo-fi depends on softness, relaxation, and slight jazz color. Chords can be richer than normal BGM, but movement should not be too aggressive.

## 5.6 Traditional / East-Asian Fantasy

### Recommended mode

```text
Prefer minor or pentatonic tendency.
Bright xianxia scenes can use major.
Dark jianghu, battle, and suspense scenes use minor.
```

### Recommended degrees

```text
Minor:
i - VII - VI - VII
i - III - VII - i
i - VI - VII - i

Major:
I - V - vi - IV
I - IV - V - I
```

### Movement principle

```text
Harmony should not become overly Western-pop-like.
Melody should stand out more than harmony.
Simple loops are suitable.
Avoid frequent complex modulations.
Weaken strong V - I functional feeling when needed.
```

### Usage advice

Traditional / East-Asian fantasy should not rely entirely on complex harmony. Prioritize melodic line, pentatonic tendency, and space.

## 5.7 Rock / Metal / Action

### Recommended mode

```text
Prefer minor.
Natural minor can be used.
Boss or metal feeling can use V to enhance tension.
```

### Recommended degrees

```text
i - VII - VI - VII
i - VI - VII - V
i - iv - VII - III
i - V - VI - iv
```

### Movement principle

```text
Bass/root motion matters more than full chords.
Strong repetition is suitable.
Descending motion or strong dominant return is suitable.
Reduce complex chord color and emphasize rhythm/power.
```

### Usage advice

In rock and metal contexts, chords can be understood as root movement or power-chord movement. Do not make harmony too soft.

## 5.8 Epic / Orchestral / Trailer

### Recommended mode

```text
Prefer minor.
Use major degrees within minor to create grandeur.
```

### Recommended degrees

```text
i - VI - III - VII
i - VI - VII - V
i - VII - VI - VII
i - iv - V - i
```

### Movement principle

```text
Progression should feel wide.
Bass roots should have strong direction.
Move from dark center toward open degrees.
Use V or VII at the end to lead back to i.
```

### Usage advice

Epic music does not necessarily need complex chords. The key is strong root motion, layered arrangement, and energy build-up.

## 5.9 Warm / Healing / Everyday

### Recommended mode

```text
Prefer major.
Starting from vi can create soft emotion.
```

### Recommended degrees

```text
I - vi - IV - V
I - V - vi - IV
vi - IV - I - V
I - IV - V - I
```

### Movement principle

```text
Avoid staying too long on highly tense V.
Avoid frequent dark minor progressions.
Chord movement should feel natural, stable, and soft.
```

### Usage advice

Warm everyday music should avoid excessive drama. The progression should feel safe, natural, and close.

## 5.10 Sad / Lyrical / Memory

### Recommended mode

```text
Minor,
or start from vi within a major key.
```

### Recommended degrees

```text
vi - IV - I - V
i - VI - III - VII
i - iv - VII - III
i - V - VI - iv
```

### Movement principle

```text
Starting from vi or i more easily creates emotion.
III and VI can provide gentleness or cinematic space.
V can create stronger emotional return.
Avoid overly bright I openings.
```

### Usage advice

Sad music does not have to remain dark throughout. In minor, adding III and VI can create a “sad but spacious” feeling.

---

# 6. Quick Selection by Mood

## 6.1 Bright, happy, positive

```text
Recommended mode: major

Recommended degrees:
I - V - vi - IV
I - IV - V - I
I - vi - IV - V
```

## 6.2 Warm, healing, everyday

```text
Recommended mode: major

Recommended degrees:
I - vi - IV - V
I - V - IV - I
vi - IV - I - V
```

## 6.3 Sad, memory, lyrical

```text
Recommended mode: minor or relative minor in major

Recommended degrees:
vi - IV - I - V
i - VI - III - VII
i - iv - VII - III
```

## 6.4 Dark, mysterious, dungeon

```text
Recommended mode: minor

Recommended degrees:
i - VI - VII - i
i - VII - VI - VII
i - iv - V - i
```

## 6.5 Tense, battle, Boss

```text
Recommended mode: minor

Recommended degrees:
i - VI - VII - V
i - VII - VI - VII
i - V - VI - iv
```

## 6.6 Epic, adventure, grand

```text
Recommended mode: mainly minor, major can also be used

Recommended degrees:
i - VI - III - VII
i - VI - VII - V
I - V - vi - IV
```

## 6.7 Horror, unease, suspense

```text
Recommended mode: minor

Recommended degrees:
i
i - bII
i - VII - VI - VII
```

## 6.8 Light, playful, simple

```text
Recommended mode: major

Recommended degrees:
I - IV - V - I
I - V - IV - I
I - V - vi - IV
```

---

# 7. Chord Movement Principles Within Sections

## 7.1 Intro

The intro does not need to fully unfold the entire progression.

Recommended approaches:

```text
Use only I / i.
Use the first two chords of the full progression.
Use slower harmonic rhythm.
Reduce chord density.
Prepare for the Main section.
```

Example degrees:

```text
Major intro:
I
I - V
I - vi

Minor intro:
i
i - VI
i - VII
```

## 7.2 Main A

Main A should use the complete core chord loop.

Recommended approaches:

```text
Use a full 4-bar progression.
Use one chord per bar.
Create a stable main loop.
Bass follows the root.
Lead is generated around current chord tones.
```

Suitable:

```text
I - V - vi - IV
i - VI - VII - V
i - VI - III - VII
i - VII - VI - VII
```

## 7.3 Main B / Climax

Main B can keep the same chord progression while increasing energy.

Recommended approaches:

```text
Keep the same chord degrees and strengthen the arrangement.
Increase harmonic-rhythm density.
Raise melody register.
Strengthen the return feeling of V or VII.
The final chord should lead back to the beginning when possible.
```

Not recommended:

```text
Suddenly switching to a completely unrelated progression.
Suddenly modulating to an unrelated key.
Breaking the loop feeling.
```

## 7.4 Ending / Loop Ending

If the user asks for loopable music, the ending chord should naturally return to the beginning.

Recommended rules:

```text
Major:
V → I
IV → I
vi → I also works, but the return is weaker.

Minor:
V → i
VII → i
VI → i works, but the return is weaker.

Battle / Boss:
Prefer V → i.

Dark loop:
VII → i can work.

Horror atmosphere:
It can remain unresolved, staying on i or bII to create suspense.
```

---

# 8. Chord Selection Principles

## 8.1 Stability principle

Openings and endings should usually revolve around the tonic chord.

```text
Major tonic: I
Minor tonic: i
```

Suitable openings:

```text
I
i
vi
```

Suitable endings:

```text
I
i
V
VII
```

## 8.2 Forward-motion principle

If the music needs momentum, use V or VII.

```text
In major:
V strongly pushes back to I.

In minor:
V strongly pushes back to i.
VII also pushes back to i, but feels more natural, folk-like, and cinematic.
```

Suitable for:

```text
Battle
Adventure
Climax
Loop ending
Before transition
```

## 8.3 Emotional-color principle

Different degrees carry different emotional colors.

```text
I / i:
Stable, center, landing point.

IV / iv:
Expansion, softness, subdominant color.

V:
Tension, strong drive, resolution feeling.

VI:
Broad, epic, emotional.

VII:
Drive, cinematic, loop feeling.

III:
Open, bright, epic.

vi:
Soft, sad, pop emotion.
```

## 8.4 Loopability principle

In loopable BGM, chord progressions should not be too long.

Recommended:

```text
4-bar loop
8-bar loop
Use the same degree group with variations in different sections.
```

Not recommended:

```text
A new complex chord every bar.
Frequent modulation.
Long delay before returning to tonic.
```

## 8.5 Style-consistency principle

Chord progressions must serve the style.

```text
Cyberpunk battle:
Minor, short loops, strong bass, V or VII return.

Lo-fi:
Soft movement, seventh-chord tendency, avoid overly strong battle feeling.

Traditional / East-Asian:
Simple harmony, melody first, avoid complex jazz-like harmony.

Horror:
Slow changes, suspension, instability, unresolved endings allowed.

Epic:
Minor with major degrees, wide root movement, strong return.

Everyday:
Major, stable, warm, not overly tense.
```

---

# 9. Common Mistakes

## 9.1 Chords are too random

Wrong approach:

```text
Ignoring key.
Ignoring style.
Randomly combining distant chords.
Changing to unrelated chords every bar.
```

Correct approach:

```text
Decide major or minor first.
Choose a degree template that fits the style.
Keep 4-bar loop logic.
```

## 9.2 Battle music is too gentle

Wrong choice:

```text
I - vi - IV - V
```

This progression is better for warm, retro, everyday scenes, not high-intensity boss battles.

Battle recommendations:

```text
i - VI - VII - V
i - VII - VI - VII
i - V - VI - iv
```

## 9.3 Horror music is too pop-like

Wrong choice:

```text
I - V - vi - IV
```

This makes horror music too bright and too pop-like.

Horror recommendations:

```text
i
i - bII
i - VII - VI - VII
```

## 9.4 Traditional / East-Asian style is overly Western-pop-like

Wrong tendencies:

```text
Heavy use of strong pop harmony.
Frequent complex seventh chords.
Chord changes too dense.
```

Better recommendations:

```text
Simple minor loops.
Melody first.
Weaken strong functional harmony.
Use i - VII - VI - VII or i - III - VII - i.
```

## 9.5 Loopable BGM ending cannot return to the beginning

Wrong approach:

```text
The final chord does not tend to return to I / i.
This makes the loop feel broken.
```

Correct approach:

```text
In major, end with V or IV to return to I.
In minor, end with V or VII to return to i.
```

---

# 10. Recommended Decision Tree

## 10.1 User asks for bright, relaxed, happy

```text
Use major.

Primary:
I - V - vi - IV

Alternatives:
I - IV - V - I
I - vi - IV - V
```

## 10.2 User asks for warm, healing, everyday

```text
Use major.

Primary:
I - vi - IV - V

Alternatives:
vi - IV - I - V
I - V - IV - I
```

## 10.3 User asks for sad, memory, lyrical

```text
Use minor or relative minor in major.

Primary:
vi - IV - I - V

Alternatives:
i - VI - III - VII
i - iv - VII - III
```

## 10.4 User asks for dark, dungeon, mysterious

```text
Use minor.

Primary:
i - VI - VII - i

Alternatives:
i - VII - VI - VII
i - iv - V - i
```

## 10.5 User asks for battle, Boss, action

```text
Use minor.

Primary:
i - VI - VII - V

Alternatives:
i - VII - VI - VII
i - V - VI - iv
```

## 10.6 User asks for epic, adventure, fantasy

```text
Use minor or major.

Primary:
i - VI - III - VII

Alternatives:
i - VI - VII - V
I - V - vi - IV
```

## 10.7 User asks for horror, suspense, unease

```text
Use minor.

Primary:
i

Alternatives:
i - bII
i - VII - VI - VII
```

## 10.8 User asks for Lo-fi, Chill, Study

```text
Use major or minor.

Primary:
I - vi - ii - V

Alternatives:
ii - V - I - I
vi - IV - I - V
I - vi - IV - V
```

## 10.9 User asks for traditional / East-Asian fantasy

```text
Use minor or pentatonic-leaning major.

Primary:
i - VII - VI - VII

Alternatives:
i - III - VII - i
i - VI - VII - i
I - V - vi - IV
```

---

# 11. Minimal Usable Chord-Degree Library

## 11.1 Major templates

```text
bright_pop:
I - V - vi - IV

warm_pop:
I - vi - IV - V

simple_major:
I - IV - V - I

open_folk:
I - V - IV - I

emotional_major:
vi - IV - I - V
```

## 11.2 Minor templates

```text
dark_loop:
i - VI - VII - i

epic_minor:
i - VI - III - VII

dark_descending:
i - VII - VI - VII

boss_battle:
i - VI - VII - V

classical_minor:
i - iv - V - i

tragic_minor:
i - V - VI - iv
```

## 11.3 Atmosphere / special templates

```text
horror_drone:
i

horror_phrygian:
i - bII

lofi_soft:
I - vi - ii - V

lofi_resolution:
ii - V - I - I

eastern_dark:
i - VII - VI - VII

eastern_fantasy:
i - III - VII - i
```

---

# 12. Minimal Usage Rules

```text
1. First decide major or minor according to the user's request.
2. Bright, relaxed, healing music prefers major.
3. Dark, battle, suspense, epic music prefers minor.
4. Use a 4-bar loop by default.
5. Use one chord per bar by default.
6. Game BGM should prioritize strongly loopable progressions.
7. Boss battle should prioritize i - VI - VII - V.
8. Epic adventure should prioritize i - VI - III - VII.
9. Dark dungeon should prioritize i - VII - VI - VII or i - VI - VII - i.
10. Warm everyday music should prioritize I - vi - IV - V.
11. Bright pop should prioritize I - V - vi - IV.
12. Lo-fi can use I - vi - ii - V or ii - V - I - I.
13. Horror music can use only i, or i - bII to create unease.
14. In loopable music, the final chord should naturally return to the first chord.
15. Do not randomly combine chords unrelated to key and style.
```

Core goal:

```text
Make the music fit the style.
Make the BGM loop naturally.
Give bass, chords, and melody a unified harmonic foundation.
Avoid chaotic music caused by random chords.
```

Priority memory:

```text
Bright pop: I - V - vi - IV
Warm everyday: I - vi - IV - V
Dark loop: i - VI - VII - i
Epic adventure: i - VI - III - VII
Boss battle: i - VI - VII - V
Dark pressure: i - VII - VI - VII
Horror suspense: i or i - bII
Lo-fi Chill: I - vi - ii - V or ii - V - I - I
```

---

# 13. Compatibility Rules for This Project

The current parser is strict. When converting degree progressions into concrete chord symbols:

```text
1. Output root-position major/minor triads only.
2. Allowed examples: C, Dm, Bb, F#m.
3. Do not output slash chords such as Eb/G.
4. Do not output extensions such as maj7, m7, sus4, add9, dim7.
5. Avoid diminished symbols.
6. If a template uses vii° or ii°, replace it with a nearby triad.
```
