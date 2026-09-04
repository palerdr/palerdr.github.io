---
title: Sentinel
tagline: Reorders a waiting room based on who is getting worse.
summary: >-
  Waiting rooms run on arrival order and one triage score taken at intake. Sentinel rescores
  patients from the live stream and reorders the board as their condition changes, while holding
  the order steady enough that staff can trust it.
order: 3
year: 2026
award: 1st place, URMC × WICC × Gemini Hackathon
stack: [Python, 'Risk modeling', 'Queue control']
links:
  - href: 'https://sentinel.thekoppe.com/'
    label: Live demo
---

Staff assess a patient once at arrival, and then the patient waits. If the condition changes an
hour later, the board does not show it.

Sentinel reads the live stream instead and scores each patient across five bounded risk
dimensions. It promotes anyone whose picture worsens, and hard override rules escalate a
critical case at once without waiting for points to accumulate.

The queue took more work than the scoring. Re-ranking on noisy input every few seconds makes the
board unstable, and staff stop trusting what they see. I made the displayed order slow to move:
a patient has to stay elevated for a period before moving up, and stay improved before moving
back down, while the underlying scores update on every reading.

A summary strip shows the charge nurse the current high-risk count and the trend in the room's
acuity.

Our team won first place at the URMC × WICC × Gemini Hackathon.
