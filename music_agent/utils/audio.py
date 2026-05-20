from __future__ import annotations

import subprocess
import time
from pathlib import Path


def _run_command_stream(cmd: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    stdout_chunks: list[str] = []
    stderr_chunks: list[str] = []

    while True:
        if proc.stdout is not None:
            out = proc.stdout.readline()
            if out:
                stdout_chunks.append(out)

        if proc.stderr is not None:
            err = proc.stderr.readline()
            if err:
                stderr_chunks.append(err)

        if proc.poll() is not None:
            break

        time.sleep(0.02)

    if proc.stdout is not None:
        remaining_out = proc.stdout.read()
        if remaining_out:
            stdout_chunks.append(remaining_out)

    if proc.stderr is not None:
        remaining_err = proc.stderr.read()
        if remaining_err:
            stderr_chunks.append(remaining_err)

    return proc.returncode, "".join(stdout_chunks), "".join(stderr_chunks)


def midi_to_wav(
    midi_path: str,
    wav_path: str,
    soundfont_path: str = "/usr/share/sounds/sf2/FluidR3_GM.sf2",
) -> str:
    midi_file = Path(midi_path)
    wav_file = Path(wav_path)
    sf2_file = Path(soundfont_path)

    if not midi_file.exists():
        raise FileNotFoundError(f"MIDI file not found: {midi_file}")
    if not sf2_file.exists():
        raise FileNotFoundError(f"SoundFont file not found: {sf2_file}")

    wav_file.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "fluidsynth",
        "-ni",
        str(sf2_file),
        str(midi_file),
        "-F",
        str(wav_file),
        "-r",
        "44100",
    ]

    code, _out, err = _run_command_stream(cmd)
    if code != 0:
        raise RuntimeError(f"fluidsynth failed with exit code {code}:\n{err}")

    return str(wav_file)


def wav_to_mp3(
    wav_path: str,
    mp3_path: str | None = None,
    bitrate: str = "192k",
    overwrite: bool = True,
) -> str:
    wav_file = Path(wav_path)
    if not wav_file.exists():
        raise FileNotFoundError(f"WAV file not found: {wav_file}")
    if wav_file.suffix.lower() != ".wav":
        raise ValueError(f"Input file must be .wav: {wav_file}")

    if mp3_path is None:
        mp3_file = wav_file.with_suffix(".mp3")
    else:
        mp3_file = Path(mp3_path)

    mp3_file.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["ffmpeg", "-y" if overwrite else "-n", "-i", str(wav_file), "-codec:a", "libmp3lame", "-b:a", bitrate, str(mp3_file)]

    code, _out, err = _run_command_stream(cmd)
    if code != 0:
        raise RuntimeError(f"ffmpeg failed with exit code {code}:\n{err}")

    return str(mp3_file)

