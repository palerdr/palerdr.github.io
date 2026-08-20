---
title: Surpassing the Leader
tagline: Formalizing a game from a manga, then solving it exactly.
summary: >-
  A gambling game from the manga Usogui. The rules are stated outright, but sparsely: enough to
  follow a match, not enough to compute with. The first problem was settling the questions the
  source leaves open. After that I proved the state space collapses and solved the game exactly,
  with a certificate attached to every stored value.
order: 1
year: 2026
stack: [Python, 'C++', Rust, OCaml, 'Linear programming', 'Dynamic programming']
stats:
  - value: '0.5449'
    label: the first Dropper's win probability under optimal play
  - value: 18.2× smaller
    label: the state-space collapse that made an exact solution possible
links:
  - href: 'https://github.com/palerdr/SURPASSING-THE-LEADER'
    label: Repository
  - href: 'https://github.com/palerdr/SURPASSING-THE-LEADER/blob/main/paper/dth_exact_solution.pdf'
    label: Paper (PDF)
writeup: true
---

## Working out what the game is

The rules are stated. There is a panel that lays them out verbatim, and the match that follows is
played under them.

What the panel does not do is answer every question you need answered to compute with the game. It
is sparse, because the game is sparse: it fixes the shape of a round and leaves the edges to be
read off the match. Some of what a solver needs is stated outright, some is only implied by play,
and in a few places the commentary and the round-by-round numbers disagree with each other. Before
I could solve anything I had to decide what I was solving.

So every executable rule in the project cites the specific evidence it rests on, in a ledger
with stable IDs so citations do not rot as the documents change. Where the sources genuinely
underdetermine a rule, I made a choice and recorded why.

One example of the disagreements. The commentary describes an immediate check as taking zero
seconds, which would make checking free and change the game completely. The round-by-round
numbers disagree: on the turn where this happens, the player's accumulated total goes from 0:32
to 0:33. The instant check costs exactly one second. The narration says one thing, the
arithmetic says another, and the arithmetic is what the rest of the match is consistent with.

## The game as I settled it

Two players alternate between Dropper and Checker. Each round, both commit simultaneously to a
second between 1 and 60. If the Checker's second does not come before the Dropper's, the check
succeeds: the Checker absorbs the elapsed interval as poison into a personal cylinder that holds
five minutes, and the roles swap. If the check fails, the Checker is injected with everything
they have accumulated plus a sixty-second penalty, which is fatal unless a fixed revival rule
saves them. Filling the cylinder past its limit is an immediate loss. The last player alive
wins.

## Why it is hard

The difficulty is not the size.

Both players commit at the same time, so there is no single best second to pick: anything you
would always play is something an opponent learns to exploit. Each round is a small matrix game
requiring a mixed strategy, and the damage carries forward into the next one.

Written out directly the game has about 5.27 billion reachable states, enough to rule out
solving it exactly. Earlier attempts searched around anchor values instead. That produces an
answer, but no way to confirm it.

## The collapse

The observation that made it tractable is simple. Once a player can no longer survive an
injection, the game stops reading how long they have been dead. That quantity feeds exactly
*one* calculation, and being unable to survive zeroes it out. So the coordinate can be replaced
by a single placeholder, separately for each player.

Applying that takes 5.27 billion states down to 289,374,121 classes. A potential function then
sorts those classes into 1,201 layers where every live move goes strictly upward, which means
the whole table can be computed in one backward pass, with no search and no reachability
analysis.

## Checking the answer

No value is stored on the solver's word alone.

Each one is accepted only with a certificate showing it sits within one part in a million of
equilibrium against the full 60 by 60 round. If the certificate does not verify, the value is
not stored, and a more general method is tried until one does.

Each round is a linear program, so the LP solve is the inner loop of the entire sweep. There is
a C++ implementation of it that sits directly on the HiGHS backend rather than reaching it through
a wrapper.

I also wrote the sweep twice, once as a parallel Rust kernel and once as a straightforward
Python reference, and checked that the two agree byte for byte everywhere both were run. Two
independent implementations matching exactly is the main reason I trust the result.

## Result

Under optimal play the first Dropper wins with probability 0.5449. Going first is worth about
four and a half points, which is less than most estimates I had seen and, unlike those
estimates, checkable.

Every one of the 289,374,121 classes is solved and certified, with the worst gap anywhere in the
table coming in under half the tolerance. The sweep runs in 5,432 seconds on one twelve-core
desktop. The recorded single-core projection for the unquotiented, search-based design was 3.7 to
5.1 years.

The full argument is written up as a paper in the repository. Alongside it are the game engine, a
separate OCaml solver that re-derives the rules independently as a cross-check, and an arena
where you can play against the solved table.
