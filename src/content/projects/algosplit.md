---
title: AlgoSplit
tagline: Predicts what a training program is worth before you run it.
summary: >-
  Most training apps record what you did. AlgoSplit models the growth signal a week of training
  produces across 29 muscle regions, so you can compare two programs and find the muscles a
  program underworks before you spend two months on it.
order: 2
year: 2026
stack:
  [TypeScript, 'React Native / Expo', React, Rust, Python, FastAPI, Supabase, Vercel]
stats:
  - value: '+35%'
    label: average net weekly stimulus across 100+ user-submitted splits
  - value: '29'
    label: muscle regions AlgoSplit scores before you run a program
links:
  - href: 'https://algo-split.vercel.app'
    label: Live app
  - href: 'https://github.com/palerdr/AlgoSplit'
    label: Repository
writeup: true
---

## The gap

Training apps record what you lifted and total it up. That tells you whether you trained, and
you find out whether the program was any good two months later, with no way to trace the outcome
back to one decision.

The research is specific about what drives hypertrophy: how much stimulus a set produces as it
approaches failure, and how fatigue accumulates against it across a week. That research sits in
papers, in no form you can apply to your own program.

AlgoSplit does that. Each program gets a predicted weekly outcome across 29 muscle regions before
you run any of it.

## In use

You can compare two programs and see that one trains rear delts once a week. You can find the
muscles receiving more volume than they can convert into growth, or move a session to another
day and see the effect on the rest of the week.

For the model to score a program it has not seen, the parser resolves each lift into the muscles
it works and the fatigue it adds, along with its movement pattern and resistance profile.

Across the first hundred user programs, average net weekly stimulus rose 35 percent, most of it
from undertrained muscles people had not noticed.

## Shipped

Google and Apple sign-in, workout logging with previous entries as placeholders so logging stays
quick between sets, history and trend charts, a 3D stimulus body, custom exercises, saved
program comparisons, and microcycle scheduling. Web and iOS ship from one codebase.

The analysis kernel recomputes all 29 regions on each program change, which was slow in Python.
I ported it to Rust, with uncached p95 down from 31.9 ms to 3.85 ms, and kept the Python version
behind a parity check within 1×10⁻⁸.
