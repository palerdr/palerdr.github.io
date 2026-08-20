---
title: AlgoSplit
tagline: Predicts what a training program is worth before you run it.
summary: >-
  Most training apps record what you already did. AlgoSplit models the growth signal a week of
  training actually produces across 29 muscle regions, so you can compare two programs, find the
  muscles a program is underworking, and fix it before spending two months on it.
order: 2
year: 2026
stack:
  [TypeScript, 'React Native / Expo', React, Rust, Python, FastAPI, Supabase, Vercel]
stats:
  - value: '+35%'
    label: average net weekly stimulus across 100+ user-submitted splits
  - value: '29'
    label: muscle regions a program is scored across before it is run
links:
  - href: 'https://algo-split.vercel.app'
    label: Live app
  - href: 'https://github.com/palerdr/AlgoSplit'
    label: Repository
writeup: true
---

## The gap

Training apps are logbooks.

You record what you lifted and they total it up. That tells you whether you trained. It does not
tell you whether the program was any good, and you generally find that out two months later,
with no way to trace the outcome back to a specific decision.

The research is reasonably specific about what drives hypertrophy: how much stimulus a set
produces as it approaches failure, how that decays across a week, how fatigue accumulates
against it and affects the following sessions. It just is not in a form you can apply to your
own program.

AlgoSplit puts it in that form. Each program gets a predicted weekly outcome across 29 muscle
regions before you run any of it.

## What that lets you do

You can compare two programs directly and see that one of them trains rear delts once a week.
You can find the muscles receiving more volume than they can convert into growth. You can move
a session to a different day and see the effect on the rest of the week.

For that to work on a program the model has not seen, exercises cannot just be names. The parser
resolves a lift into its movement pattern, the muscles it works, its resistance profile, whether
it loads one side or both, and how much systemic fatigue it contributes. That is what lets the
model score an arbitrary program someone types in.

Across the first hundred or so user programs, average net weekly stimulus increased 35 percent,
mostly from identifying undertrained muscles that people had not noticed.

## What shipped

Google and Apple sign-in, workout logging with sets, reps, load, RIR and notes, previous entries
shown as placeholder values so logging is quick between sets, history and trend charts, a 3D
stimulus body, bodyweight tracking, custom exercises, saved program comparisons, and microcycle
scheduling. Web and iOS from one codebase.

The analysis kernel recomputes all 29 regions whenever a program changes, which was noticeably
slow in Python. It runs in Rust now, with uncached p95 down from 31.9 ms to 3.8 ms, and the
Python version kept behind a parity check so the two can be tested against each other.
