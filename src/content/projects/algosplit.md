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

Training apps log what you lifted, and you learn whether a program worked two months later.
AlgoSplit predicts a program's weekly outcome across 29 muscle regions before you run it.

## In use

Take six rear-delt sets a week. Net is stimulus minus atrophy:

| Schedule             | Stimulus | Atrophy |    Net |
| -------------------- | -------: | ------: | -----: |
| 6 sets Monday        |    1.572 |   1.610 | −0.038 |
| 3 Monday, 3 Thursday |    2.543 |   0.966 |  1.577 |
| 3 Monday, 3 Tuesday  |    1.859 |   1.288 |  0.571 |

Each set in a session adds less than the set before it:

![The bar chart shows the stimulus from each of the six weekly rear-delt sets in the three schedules. Sets 4 to 6 add 0.300 at the end of a six-set Monday session and 1.271 as a separate Thursday session. On Tuesday, one day after Monday, they add 0.588.](../../assets/figures/algosplit/per-set-stimulus.svg)

Sets 4 to 6 add 0.300 at the end of a Monday session and 1.271 as a separate Thursday session.
Atrophy builds through the idle hours after each 48-hour window:

![The timeline shows the 168-hour week for the three schedules, with a 48-hour stimulus window after each session and the idle hours after it. One Monday session leaves 120 idle hours and 1.610 atrophy, and Monday with Thursday leaves 72 hours and 0.966. A Tuesday session leaves 96 idle hours and 1.288 atrophy.](../../assets/figures/algosplit/week-timeline.svg)

Across the first hundred user programs, average net weekly stimulus rose 35 percent.

## Shipped

Web and iOS ship from one codebase. I ported the analysis kernel from Python to Rust, and
uncached p95 fell from 31.9 ms to 3.85 ms.
