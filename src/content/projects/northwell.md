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

The agent turns a plain-English question into SQL for a hospital data warehouse. It has no
connection to patient data.

<svg class="figure agent-flow" viewBox="0 0 400 352" role="img" aria-labelledby="agent-flow-title">
<title id="agent-flow-title">A question goes to retrieval, then to the agent. The agent answers, asks to clarify, says it cannot answer, or drafts a query plan, and a validator checks the plan before a compiler writes the SQL. A red path runs from a wrong-table retrieval through the agent to the validator, and the validator passes it. Patient data sits apart with no connection.</title>
<defs>
<marker id="af-ink" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" class="head"/></marker>
<marker id="af-red" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" class="head red"/></marker>
</defs>
<rect class="box" x="155" y="4" width="170" height="36"/>
<text x="240" y="27">Question in plain English</text>
<line class="edge" x1="240" y1="40" x2="240" y2="60" marker-end="url(#af-ink)"/>
<rect class="box" x="155" y="62" width="170" height="36"/>
<text x="240" y="85">Retrieve schema docs</text>
<text class="red" x="331" y="85" text-anchor="start">wrong table</text>
<line class="edge red" x1="240" y1="98" x2="240" y2="118" marker-end="url(#af-red)"/>
<rect class="box" x="155" y="120" width="170" height="36"/>
<text x="240" y="143">Agent reads the docs</text>
<polyline class="edge" points="155,138 132,138 132,226"/>
<line class="edge" x1="132" y1="174" x2="124" y2="174" marker-end="url(#af-ink)"/>
<line class="edge" x1="132" y1="200" x2="124" y2="200" marker-end="url(#af-ink)"/>
<line class="edge" x1="132" y1="226" x2="124" y2="226" marker-end="url(#af-ink)"/>
<text x="118" y="178" text-anchor="end">answer</text>
<text x="118" y="204" text-anchor="end">ask to clarify</text>
<text x="118" y="230" text-anchor="end">say it cannot answer</text>
<line class="edge red" x1="240" y1="156" x2="240" y2="176" marker-end="url(#af-red)"/>
<rect class="box" x="170" y="178" width="140" height="32"/>
<text x="240" y="199">Draft query plan</text>
<line class="edge red" x1="240" y1="210" x2="240" y2="228" marker-end="url(#af-red)"/>
<polygon class="box" points="240,230 310,258 240,286 170,258"/>
<text x="240" y="262">validator</text>
<text class="red" x="318" y="262" text-anchor="start">passes</text>
<line class="edge red" x1="240" y1="286" x2="240" y2="304" marker-end="url(#af-red)"/>
<rect class="box" x="170" y="306" width="140" height="32"/>
<text x="240" y="327">Compiler writes SQL</text>
<rect class="box apart" x="10" y="292" width="120" height="46"/>
<text x="70" y="311">patient data</text>
<text x="70" y="329">no connection</text>
</svg>

## My part

The validator passes a query plan built from the wrong table, and the red path shows this case.
I built the benchmark that measures this failure. It traced 82.4% of top-5 retrieval misses to
vocabulary mismatch:

![Diagram of an invented schema entry, 'Readmission flag: marks a stay that follows a recent discharge', between two questions that ask for the same count. The question 'Readmission flag count per stay' shares three words with the entry. The question 'How many patients came back soon after they went home?' shares no word with it, and red lines pair its phrases with entry words of the same meaning. A keyword search finds no word in the entry to match the business question.](../../assets/figures/northwell/term_overlap.svg)

A keyword search finds no word to match in the business question. I fused BM25 full-text search
with dense-vector retrieval, and hit@5 rose from 53.8% to 75% across about 250 analyst queries.

## Comparing the options

The team held three views on which retrieval approach to use. I put all three behind one runner
that reports on the same questions.

## Intern Kaggle competition

I tied for first with a blend of CatBoost and TabNet. I grouped validation folds so passengers who
travelled together stayed in one fold:

![Two panels of validation folds for the passengers in the training file's first eight travel groups with more than one passenger. Under the plain stratified split, six of the eight groups have members in two or more folds, shown as red zigzags. Under the grouped split, each group sits in one fold.](../../assets/figures/northwell/group_folds.svg)

The plain split sends six of the eight groups across folds.
