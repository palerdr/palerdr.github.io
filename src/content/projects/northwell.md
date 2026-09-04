---
# TODO(james): clear this page with your manager before the site goes public.
# Kept at method level apart from the figures that already appear on the public resume PDF.
title: Asking a hospital data warehouse questions in English
tagline: Northwell Health, and a benchmark that shows when the search underneath fails.
summary: >-
  An agent that takes a question in plain English and drafts SQL against the real schema from
  the documentation it retrieves. I owned the evaluation: whether the search underneath finds
  the right documentation, and how we would know.
order: 4
year: 2026
stack: [Python, LangGraph, 'Full-text search', BigQuery, CatBoost, Optuna, Chainlit]
stats:
  - value: '~40,000'
    label: schema documentation files the agent searches to answer one question
listed: false
writeup: true
---

## The agent

The warehouse holds more tables than one analyst can keep in their head, and most of the people
who need answers from it do not write SQL. The analysts who do spend much of their week telling
everyone else which table holds a given fact.

The agent reads a question in plain English and finds the documentation for the relevant part
of the schema. From there it answers or drafts SQL against the real schema. It asks for
clarification when a question is ambiguous and says so when it cannot answer.

It has no connection to patient data, and a deterministic validator checks any SQL before it
leaves. In a hospital a wrong answer stated with confidence costs more than no answer, and the
team designed around that.

## My part

If retrieval returns the wrong table, the agent writes SQL from the wrong table, and the SQL
still runs. That is the failure I spent the summer measuring.

"The retrieval seems fine" gives a team nothing to act on, so I built a benchmark that groups
questions by kind. Averaged together the results looked acceptable. Split apart, the system did
well on questions that named a table or column and failed on questions in business language
that named neither, which are the questions the people without SQL ask. The benchmark attributed
82.4% of top-5 retrieval misses to vocabulary mismatch.

Searching harder does not fix a vocabulary mismatch; more results means more documents that
share no words with the question. With that diagnosis I ruled out the obvious fix and fused
BM25 full-text search with dense-vector retrieval, which raised hit@5 from 53.8% to 75% across
about 250 analyst queries.

## Comparing the options

The team held three views on which retrieval approach to use and had no measurements to settle
it, so I put all three behind one runner that produces comparable reports on the same
questions. The approach I expected to win made no difference in the measured runs. The cause was
its configuration, so the report says what I measured and what it leaves open.

## Intern Kaggle competition

I tied for first in the intern Kaggle competition. The final submission blended CatBoost and
TabNet, weighted toward the stronger model, and the second earned its weight by making
different mistakes.

I grouped validation folds so that passengers travelling together stayed in one fold, since
splitting a group inflates the local score. I tuned with Optuna and treated the results as
candidates, because several configurations that scored highest locally did worse on the
leaderboard. I ran into the same problem in the retrieval work, where a single validation number
hid the failure that the grouping exposed.
