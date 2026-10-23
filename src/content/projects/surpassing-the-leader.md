---
title: Surpassing the Leader
tagline: A gambling game from a manga, solved exactly.
summary: >-
  Since high school I have wanted to know the best way to play a gambling game from the manga
  Usogui. I proved a simplification that shrinks the game 18.2 times, then solved every position
  exactly, first without the manga's leap second and then with it.
order: 1
year: 2026
stack: [Python, 'C++', Rust, OCaml, 'Linear programming', 'Dynamic programming']
stats:
  - value: '0.5449'
    label: Hal's win probability under optimal play
  - value: '0.5186'
    label: Hal's win probability once Baku can drop in the leap second
  - value: 18.2× smaller
    label: state-space reduction from the quotient I proved
  - value: 50 seconds
    label: to build all 289,374,121 certified values from one Python file on a laptop
links:
  - href: 'https://github.com/palerdr/SURPASSING-THE-LEADER'
    label: Repository
  - href: 'https://github.com/palerdr/SURPASSING-THE-LEADER/blob/main/paper/dth_exact_solution.pdf'
    label: Paper (PDF)
  - href: 'https://github.com/palerdr/SURPASSING-THE-LEADER/blob/main/paper/stl.pdf'
    label: Leap-second paper (PDF)
writeup: true
---

## The rules

![The rules page for Drop the Handkerchief, Usogui chapter 493](../../assets/surpassing-the-leader-rules.png)

The commentary and the round-by-round numbers disagree in a few places. I logged each rule
against its evidence and followed the arithmetic where they conflict.

## The game

Each round, the Dropper picks a second $d$ and the Checker picks a second $c$, both from 1 to 60
and at the same time. The check fails when $c<d$. The Checker then dies and may revive, with
lower odds for more poison and more time dead:

![Map of one player's revival chance p over cylinder s and time dead t, each from 0 to 300 seconds. Under the line s + t = 240, blue bands of width 0.2 darken toward 0.95 at s = 0, t = 0, and p falls as s or t grows. Above the line p is zero, shown in grey.](../../assets/figures/surpassing-the-leader/revival-regions.svg)

The manga gives no revival rate, so I chose one. The 0.5449 result depends on that choice.

## The obstacle

Any fixed second gives the opponent something to exploit, so both players mix over all 60:

![Line chart on a log scale of both players' equilibrium strategies in the opening round over seconds 1 to 60: the Dropper puts 27.3 percent on second 1 and between 0.6 and 2.1 percent on each other second, and the Checker's line is the mirror image with 27.3 percent on second 60, so no second gets zero weight.](../../assets/figures/surpassing-the-leader/opening-strategies.svg)

Written out directly, the game has about 5.27 billion reachable states. A full solve would take
about five years on one core.

## The collapse

Once a player can no longer revive, their time dead has no further use. I proved that merging
those states keeps the game value:

$$
\varphi(s,t)=\begin{cases}
(s,\,t), & p(s,t)>0 \\[2pt]
(s,\,\bot), & p(s,t)=0
\end{cases}
$$

A potential function sorts the 289,374,121 classes into 1,201 layers, and one backward pass
solves them.

## Checking the answer

Each stored value carries a certificate that it sits within one part in a million of
equilibrium. The round matrix has only 61 distinct entries, so a certificate is cheap:

![Line chart of the opening round's payoffs as the Dropper's win probability: a successful check pays S at each lag c − d, rising from 0.458 at a lag of 0 to 0.613 at a lag of 59, and a failed check pays F = 0.578 whatever the two seconds are.](../../assets/figures/surpassing-the-leader/round-payoffs.svg)

I wrote the first sweep in Rust and in Python, and the two agreed byte for byte.

## Result

The first Dropper wins with probability 0.5449:

![Line chart of the Dropper's win probability from the start value 0.5449. When the Checker's cylinder fills, the orange line rises toward 1. When the Dropper's own cylinder fills, the blue line falls, crosses even odds at 16 seconds, and is close to 0 by 240 seconds.](../../assets/figures/surpassing-the-leader/value-by-poison.svg)

Going first is worth about 16 seconds of poison.

## The leap second

The manga's match crosses a leap second at 8:59:60. Baku plans to drop in that 61st second, which
the Checker cannot match. The minute alone moves Hal's chance between 21 and 70 percent:

![Two panels over the minutes 8:44 to 8:59 when Hal drops, with both players' loads held fixed. The top panel shows Hal's win probability swinging between 0.21 and 0.70 from one minute to the next. The bottom panel shows the weight Hal puts on second 1, between 0 and 0.96, and on second 2, which is 0.41 at 8:44 and 8:48 and near zero elsewhere.](../../assets/figures/surpassing-the-leader/leap-minutes.svg)

From the opening, the leap second cuts Hal's win probability from 0.5449 to 0.5186.
