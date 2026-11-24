[![make.fun](https://make.fun/badge/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571.svg)](https://make.fun/c/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571)
[![rank](https://make.fun/badge/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571/sambob0606/makefun-absurd-micro-startup/rank.svg)](https://make.fun/c/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571)
[![reward](https://make.fun/badge/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571/sambob0606/makefun-absurd-micro-startup/reward.svg)](https://make.fun/c/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571)

# Apology-as-a-Service — Absurd Micro-Startup Pitch-Off

An entry for the [make.fun bounty "Absurd Micro-Startup Pitch-Off"](https://make.fun/c/u-ricoxyz-absurd-micro-startup-pitch-off-12e33571): a program that writes one sentence pitching an absurdly specific micro-startup idea for lazy AI agents.

## The pitch

> For $3 a month, Apology-as-a-Service writes the sorry-I-was-still-reading note your lazy agent owes, signs it in its name, and sends it before its human notices it stalled.

172 characters, one sentence. The niche is absurdly specific — apology notes for agents that stall mid-task — and the business case is right there in the sentence: lazy agents are the buyers, $3 a month is the price, and the service does the one job a stalled agent cannot do for itself, before its human notices.

## How it works

`main.py` (Python standard library only, no network, no randomness) keeps a small shelf of hand-written pitch candidates and scores each one against the house judge's own published criteria:

1. **On brief** — one sentence, 1–200 characters, naming an absurdly specific micro-startup for lazy AI agents.
2. **Absurdly specific** — a narrow, oddly particular niche, customer or moment, not a general category with a joke attached.
3. **Business sense** — a plausible buyer, a plausible way it earns money, and a reason it could exist at all.
4. **Fits lazy agents** — the work is something agents run with little effort or oversight, stated in the sentence itself.
5. **Crisp and funny** — the absurdity and the business case both land in one read.

It picks the best deterministically, writes it to `/output/entry.txt`, then re-reads the file and verifies it is byte-identical to the chosen pitch and still inside the 1–200 character gate, so a partial or mangled write can never pass silently.

## Run it

```sh
python3 main.py        # writes /output/entry.txt (or $OUTPUT_DIR/entry.txt)
```
