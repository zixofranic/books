"""
Voice registry for the books project.

Friendly names map to Chatterbox reference files + render defaults.
Add a new voice by appending to VOICES; per-book generate.py scripts
import these and pick one. Don't rename existing entries — book scripts
reference them by name.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Voice:
    name: str
    ref_filename: str       # basename in C:\AI\system\voice\recordings\
    atempo: float           # ffmpeg time-stretch factor for post-synth
    silence_cap: bool       # apply ffmpeg silenceremove post-render
    stop_duration: float = 1.5  # silenceremove threshold — silences ABOVE this get trimmed
    stop_silence: float = 1.0   # silenceremove target — trim TO this many seconds
    notes: str = ""


BURTON = Voice(
    name="burton",
    ref_filename="wisdom_burton_long_ref.wav",
    atempo=0.89,
    silence_cap=True,
    stop_duration=0.9,
    stop_silence=0.5,
    notes="Wisdom channel narrator. Measured authority, smart-friend register. "
          "Default for non-fiction. Aggressive silence_cap (trim >0.9s pauses "
          "down to 0.5s) — needed because the author uses many short emphatic "
          "sentences ('Google was losing. Badly.') that CB over-pauses on "
          "(1.0-1.4s of dead air slipping under the old 1.5s threshold). "
          "Previously stop_duration=1.5, stop_silence=0.7 — both too loose.",
)

DON = Voice(
    name="don",
    ref_filename="na_old_timer_5min_cbref.wav",
    atempo=0.88,
    silence_cap=True,
    stop_duration=1.5,
    stop_silence=1.0,
    notes="NA/AA old timer voice. More energetic and weathered than Burton. "
          "Hard silence_cap (trim >1.5s pauses down to 1.0s) needed — this "
          "ref hallucinates 30s+ of dead air at chunk boundaries around short "
          "isolated lines (e.g. 'Two months.'). Looser than Burton because "
          "NA/AA content benefits from longer reflective beats.",
)


VOICES = {v.name: v for v in (BURTON, DON)}


def get(name: str) -> Voice:
    if name not in VOICES:
        raise KeyError(f"unknown voice {name!r}; available: {sorted(VOICES)}")
    return VOICES[name]
