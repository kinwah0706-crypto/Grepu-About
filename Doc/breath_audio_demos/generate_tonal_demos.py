#!/usr/bin/env python3
"""Generate synthetic breath-cue WAV demos for Grepu product evaluation (no deps)."""
from __future__ import annotations

import math
import struct
import wave


SR = 44_100


def write_sine_chime(path: str, freq_hz: float, duration_s: float, peak: float = 0.52) -> None:
    """Short tone with Hann envelope (similar spirit to MeditationPhaseCuePlayer)."""
    n = max(1, int(SR * duration_s))
    frames = bytearray()
    two_pi = math.pi * 2
    denom = max(1, n - 1)
    for i in range(n):
        t = i / SR
        hann = 0.5 * (1 - math.cos(two_pi * i / denom))
        s = peak * math.sin(two_pi * freq_hz * t) * hann
        s = max(-1.0, min(1.0, s))
        frames.extend(struct.pack("<h", int(round(s * 32767))))
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(bytes(frames))


def append_silence(frames: bytearray, seconds: float) -> None:
    n = int(SR * seconds)
    frames.extend(b"\x00\x00" * n)


def write_cycle_demo(path: str) -> None:
    """Two breath cycles: inhale boundary + silence + exhale boundary + silence (tone-only path)."""
    frames = bytearray()
    # Cycle params aligned with a common app default ~4s in / 6s out (illustrative).
    inhale_s, exhale_s = 4.0, 6.0
    f_inhale, f_exhale = 587.33, 392.0  # D5 vs G4-ish — distinct roles without being harsh

    def append_chime(freq: float, dur: float) -> None:
        n = max(1, int(SR * dur))
        two_pi = math.pi * 2
        denom = max(1, n - 1)
        for i in range(n):
            t = i / SR
            hann = 0.5 * (1 - math.cos(two_pi * i / denom))
            s = 0.48 * math.sin(two_pi * freq * t) * hann
            s = max(-1.0, min(1.0, s))
            frames.extend(struct.pack("<h", int(round(s * 32767))))

    for _ in range(2):
        append_chime(f_inhale, 0.11)
        append_silence(frames, inhale_s - 0.11)
        append_chime(f_exhale, 0.13)
        append_silence(frames, exhale_s - 0.13)

    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(bytes(frames))


def main() -> None:
    base = __import__("pathlib").Path(__file__).resolve().parent
    write_sine_chime(str(base / "demo_S1_boundary_grepu_like.wav"), 587.33, 0.11, 0.55)
    write_sine_chime(str(base / "demo_S2_inhale_boundary_higher.wav"), 659.25, 0.10, 0.5)  # E5
    write_sine_chime(str(base / "demo_S3_exhale_boundary_lower.wav"), 349.23, 0.14, 0.5)  # F4
    write_cycle_demo(str(base / "demo_S4_two_cycles_tone_only.wav"))


if __name__ == "__main__":
    main()
