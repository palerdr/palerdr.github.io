---
# TODO(james): clear this page with your manager before the site goes public.
# Deliberately kept at method level: no corpus counts beyond the ~40k HTML schema
# files, no internal table or column names, no index/chunk/edge totals.
title: Asking a hospital data warehouse questions in English
tagline: Northwell Health, and how to tell whether the search underneath is working.
summary: >-
  An agent that takes a question in plain English, finds the schema documentation that covers it,
  and drafts SQL against the real schema. I work on the evaluation side: whether the search
  underneath is retrieving the right documentation, and how we would know.
order: 4
year: 2026
stack: [Python, LangGraph, 'Full-text search', BigQuery, CatBoost, Optuna, Chainlit]
stats:
  - value: '~40,000'
    label: schema documentation files the agent searches to answer one question
listed: false
writeup: true
---

## What it does

Nobody knows the whole warehouse.

It is large enough that no individual holds it in their head, and most of the people who need
answers from it do not write SQL. The ones who do spend a lot of their time answering the same
structural question for everyone else: where does this particular fact live?

The agent takes the question in plain English, works out what is being asked, finds the
documentation covering the relevant part of the schema, and either answers from that
documentation or drafts SQL against the real schema. If the question is ambiguous it asks for
clarification. If it cannot answer, it says so.

It is deliberately conservative. It has no connection to patient data, execution is disabled,
and any SQL it produces goes through a deterministic validator first. In a hospital setting a
confidently wrong answer is worse than no answer, and most of the design follows from that.

## The part I work on

All of it depends on retrieving the right documentation.

An agent working from the wrong table still produces SQL that reads well and runs. Nothing in
the output indicates it was built on the wrong basis. That makes retrieval both the most
consequential failure in the system and the hardest one to see.

"The retrieval seems fine" is not something a team can act on, so I built the benchmark that
makes it checkable, with questions grouped by the kind of question being asked rather than
averaged into a single score.

The grouping is what mattered. Averaged together the results looked acceptable. Split apart,
the system did well on questions naming a specific table or column and poorly on questions
phrased in business language that named neither, which are most of what the people who cannot
write SQL will ask.

That failure does not improve by searching harder. If the question and the document share no
vocabulary, returning more results just returns more things that do not match. Identifying the
cause correctly ruled out the obvious fix and pointed at a different one.

## Comparing the options

There were three views on the team about which retrieval approach to use and no measurements to
settle it. I put all three behind one runner producing directly comparable reports on the same
questions.

The approach I had expected to win made no difference to the results. The useful part was
working out why, and finding that the cause was in how it had been configured rather than in the
approach itself. Writing it up as "this does not work" would have been accurate and would have
closed off something still worth trying, so the report says specifically what was measured and
what it does and does not rule out.

## Intern Kaggle competition

I also won the intern Kaggle competition (tied for first). The final submission blended two
models weighted toward the stronger one, with the second contributing because it made different
mistakes rather than fewer.

Validation was grouped rather than random, since passengers travelling together share
information and splitting a group across folds inflates the local score. I tuned with Optuna but
treated the results as candidates rather than answers, because several configurations that
scored highest locally did worse on the leaderboard, and testing around the best blend showed it
was sensitive to small changes in weighting. That is the same problem the retrieval work kept
running into: one validation number is easy to over-trust.
