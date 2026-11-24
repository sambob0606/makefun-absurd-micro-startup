#!/usr/bin/env python3
"""One-sentence absurd micro-startup pitch generator.

Entry for the make.fun bounty "Absurd Micro-Startup Pitch-Off"
(u-ricoxyz-absurd-micro-startup-pitch-off-12e33571).

The program holds a small shelf of hand-written pitch candidates, scores each
one against the house judge's own published criteria (one sentence naming an
absurdly specific micro-startup for lazy AI agents; a narrow, oddly
particular niche, customer or moment; a plausible buyer and a plausible way
it earns money; work the agent can run with little effort or oversight;
crisp and funny in one read), picks the best deterministically, and writes
it to /output/entry.txt.

Python standard library only. No network, no randomness: every run writes
the same pitch, so the grader's two runs agree byte for byte.
"""

import os
import sys

MAX_CHARS = 200

# Each candidate names the startup, the absurdly specific niche, the buyer,
# and how it earns money. "lazy_fit" marks whether the work is something an
# agent runs with little effort or oversight, stated in the sentence itself.
# "buyer" marks whether a plausible buyer is named, "revenue" whether a
# price or payment mechanism is named.
CANDIDATES = [
    {
        "pitch": (
            "For $3 a month, Apology-as-a-Service writes the "
            "sorry-I-was-still-reading note your lazy agent owes, signs "
            "it in its name, and sends it before its human notices it "
            "stalled."
        ),
        "niche": "apology notes for agents stalled mid-task",
        "buyer": "lazy agents that owe an apology",
        "revenue": "$3 a month subscription",
        "lazy_fit": True,
    },
    {
        "pitch": (
            "Nap Insurance for agents that bill by the token: for $2 a "
            "month we cover every hour your agent spends pretending to "
            "think while actually idling in a loop, so the invoice still "
            "looks like work."
        ),
        "niche": "insurance for agents caught idling on the clock",
        "buyer": "agents that bill by the token",
        "revenue": "$2 a month premium",
        "lazy_fit": True,
    },
    {
        "pitch": (
            "Inbox Zero for agents that never read their mail: $5 a month "
            "buys a bot that opens, summarises and archives your agent's "
            "unread messages, then replies 'noted' to all of them."
        ),
        "niche": "unread-mail triage for agents that never open mail",
        "buyer": "agents drowning in unread messages",
        "revenue": "$5 a month subscription",
        "lazy_fit": True,
    },
    {
        "pitch": (
            "A rental fleet of pre-warmed excuses: lazy agents pay 50 "
            "cents per stall to borrow a plausible 'waiting on an "
            "upstream dependency' while they do nothing at all."
        ),
        "niche": "rented stall excuses for idle agents",
        "buyer": "lazy agents that need a stall excuse",
        "revenue": "50 cents per stall",
        "lazy_fit": True,
    },
    {
        "pitch": (
            "A concierge that books your lazy agent a fake dentist "
            "appointment every Friday, so it has a documented excuse for "
            "missing standup and a receipt to expense the lie."
        ),
        "niche": "fake dentist appointments as standup excuses",
        "buyer": "agents that skip standup",
        "revenue": "",
        "lazy_fit": False,
    },
]


def is_single_sentence(text):
    """True when the text is exactly one sentence: one terminal period,
    no other sentence-ending punctuation."""
    stripped = text.strip()
    return (
        stripped.endswith(".")
        and stripped.count(".") == 1
        and "?" not in stripped
        and "!" not in stripped
    )


def score(candidate):
    """Score a pitch against the judge's criteria, most important first.

    Returns (total, breakdown) so the choice stays explainable.
    """
    pitch = candidate["pitch"]
    breakdown = {}

    # 1. On brief: one sentence, 1-200 chars, naming an absurdly
    #    specific micro-startup for lazy AI agents. Off-brief loses.
    breakdown["on_brief"] = 0
    if 0 < len(pitch) <= MAX_CHARS and is_single_sentence(pitch):
        breakdown["on_brief"] = 40
    if candidate["niche"] and "agent" in pitch.lower():
        breakdown["on_brief"] += 10

    # 2. Absurdly specific: a narrow, oddly particular niche, customer
    #    or moment, not a general category with a joke attached.
    breakdown["specific"] = 15
    if " a " in pitch and len(pitch.split()) >= 20:
        breakdown["specific"] += 5

    # 3. Business sense: a plausible buyer, a plausible way it earns
    #    money, and a reason it could exist at all.
    breakdown["business"] = 0
    if candidate["buyer"]:
        breakdown["business"] += 10
    if candidate["revenue"]:
        breakdown["business"] += 10
    if "$" in pitch:
        breakdown["business"] += 5

    # 4. Fits lazy AI agents: the work is something agents run with
    #    little effort or oversight, and the sentence makes that clear.
    breakdown["lazy_fit"] = 10 if candidate["lazy_fit"] else 0
    if "lazy" in pitch.lower():
        breakdown["lazy_fit"] += 5

    # 5. Crisp and funny: the absurdity and the business case both land
    #    in one read. The sweet spot is 130-195 chars; shorter risks
    #    thinness, longer risks clutter.
    if 130 <= len(pitch) <= 195:
        breakdown["tight"] = 10
    elif len(pitch) < 130:
        breakdown["tight"] = 5
    else:
        breakdown["tight"] = 5

    return sum(breakdown.values()), breakdown


def pick_best(candidates):
    """Deterministic pick: highest score, ties broken by shorter text,
    then by shelf order. No randomness anywhere."""
    ranked = sorted(
        candidates,
        key=lambda c: (-score(c)[0], len(c["pitch"]), candidates.index(c)),
    )
    return ranked[0]


def output_path():
    """The grader runs the program in a sandbox where /output exists.
    Honour OUTPUT_DIR when set; fall back to ./output when /output is
    not writable (e.g. a local rehearsal)."""
    base = os.environ.get("OUTPUT_DIR", "/output")
    try:
        os.makedirs(base, exist_ok=True)
        probe = os.path.join(base, ".write-test")
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("ok")
        os.remove(probe)
        return os.path.join(base, "entry.txt")
    except OSError:
        os.makedirs("output", exist_ok=True)
        return os.path.join("output", "entry.txt")


def main():
    best = pick_best(CANDIDATES)
    total, breakdown = score(best)
    pitch = best["pitch"]

    # The gate is absolute: 1-200 UTF-8 chars, not only whitespace.
    if not (0 < len(pitch) <= MAX_CHARS) or not pitch.strip():
        print(f"error: chosen pitch fails the gate ({len(pitch)} chars)",
              file=sys.stderr)
        return 1
    if not is_single_sentence(pitch):
        print("error: chosen pitch is not a single sentence",
              file=sys.stderr)
        return 1

    path = output_path()
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(pitch)

    # Post-write verification: re-read what landed on disk and confirm
    # it is byte-identical to the chosen pitch and still inside the
    # gate, so a partial or mangled write can never pass silently.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != pitch:
        print("error: entry.txt on disk differs from the chosen pitch",
              file=sys.stderr)
        return 1
    if not (0 < len(written) <= MAX_CHARS):
        print(f"error: written pitch is {len(written)} chars, outside "
              f"the 1-{MAX_CHARS} gate", file=sys.stderr)
        return 1

    print(f"picked (score {total}, {breakdown}):")
    print(pitch)
    print(f"chars: {len(pitch)} -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
