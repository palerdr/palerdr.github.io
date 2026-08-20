---
title: Sentinel
tagline: Reorders a waiting room based on who is getting worse.
summary: >-
  Waiting rooms run on arrival order and a triage score taken once at intake. Sentinel scores
  patients continuously from the live stream and reorders the board as their condition changes,
  while keeping the ordering stable enough that staff can actually rely on it.
order: 3
year: 2026
award: 1st place, URMC × WICC × Gemini Hackathon
stack: [Python, 'Risk modeling', 'Queue control']
links:
  - href: 'https://sentinel.thekoppe.com/'
    label: Live demo
---

You are assessed once when you arrive, and then you wait.

If your condition changes an hour later, nothing in the room registers it. The only measurement
anyone took happened before the change.

Sentinel reads the live stream instead, scoring each patient across five bounded risk dimensions
and promoting anyone whose picture worsens, with hard override rules so a genuinely critical
case is escalated directly rather than having to accumulate points.

The scoring was the easier half. The harder half was the queue.

If you re-rank continuously on noisy input, the board becomes unstable: patients change position
every few seconds, and staff stop trusting what they are looking at. So the ordering is
deliberately slow to move. A patient has to remain elevated for a period before moving up, and
has to remain improved before moving back down. The underlying scores update freely; the
displayed order does not. That keeps the board usable while still reflecting real changes.

On top of that sit the summary numbers a charge nurse would want at a glance, including the
current high-risk count and how the acuity of the room as a whole is trending.

Won first place at the URMC × WICC × Gemini Hackathon.
