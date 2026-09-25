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

The agent takes a question in plain English through these steps:

<svg class="figure agent-flow" viewBox="0 0 400 352" role="img" aria-labelledby="agent-flow-title">
<title id="agent-flow-title">A question goes to retrieval, then to the agent. The agent answers, asks to clarify, says it cannot answer, or drafts a query plan, and a validator checks the plan before a compiler writes the SQL. A red path runs from a wrong-table retrieval through the agent to the validator, and the validator passes it. Patient data sits apart with no connection.</title>
<defs>
<marker id="af-ink" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" class="head"/></marker>
<marker id="af-red" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" class="head red"/></marker>
</defs>
<rect class="box" x="155" y="4" width="170" height="36" rx="6"/>
<text x="240" y="27">Question in plain English</text>
<line class="edge" x1="240" y1="40" x2="240" y2="60" marker-end="url(#af-ink)"/>
<rect class="box" x="155" y="62" width="170" height="36" rx="6"/>
<text x="240" y="85">Retrieve schema docs</text>
<text class="red" x="331" y="85" text-anchor="start">wrong table</text>
<line class="edge red" x1="240" y1="98" x2="240" y2="118" marker-end="url(#af-red)"/>
<rect class="box" x="155" y="120" width="170" height="36" rx="6"/>
<text x="240" y="143">Agent reads the docs</text>
<polyline class="edge" points="155,138 132,138 132,226"/>
<line class="edge" x1="132" y1="174" x2="124" y2="174" marker-end="url(#af-ink)"/>
<line class="edge" x1="132" y1="200" x2="124" y2="200" marker-end="url(#af-ink)"/>
<line class="edge" x1="132" y1="226" x2="124" y2="226" marker-end="url(#af-ink)"/>
<text x="118" y="178" text-anchor="end">answer</text>
<text x="118" y="204" text-anchor="end">ask to clarify</text>
<text x="118" y="230" text-anchor="end">say it cannot answer</text>
<line class="edge red" x1="240" y1="156" x2="240" y2="176" marker-end="url(#af-red)"/>
<rect class="box" x="170" y="178" width="140" height="32" rx="6"/>
<text x="240" y="199">Draft query plan</text>
<line class="edge red" x1="240" y1="210" x2="240" y2="228" marker-end="url(#af-red)"/>
<polygon class="box" points="240,230 310,258 240,286 170,258"/>
<text x="240" y="262">validator</text>
<text class="red" x="318" y="262" text-anchor="start">passes</text>
<line class="edge red" x1="240" y1="286" x2="240" y2="304" marker-end="url(#af-red)"/>
<rect class="box" x="170" y="306" width="140" height="32" rx="6"/>
<text x="240" y="327">Compiler writes SQL</text>
<rect class="box apart" x="10" y="292" width="120" height="46" rx="6"/>
<text x="70" y="311">patient data</text>
<text x="70" y="329">no connection</text>
</svg>

The agent has no connection to patient data. In a hospital a wrong answer stated with confidence costs
more than no answer, and the team designed around that.

## My part

The validator checks that each table and column in the agent's query plan appears in the
documentation it retrieved. If the agent builds its plan from the wrong table, the plan passes that
check. The red path in the figure shows this case, and it is the failure I spent the summer
measuring.

"The retrieval seems fine" gives a team nothing to act on, so I built a benchmark that groups
questions by kind. Averaged together the results looked acceptable. Split apart, the system did
well on questions that named a table or column and failed on questions in business language
that named neither, which are the questions the people without SQL ask. The benchmark attributed
82.4% of top-5 retrieval misses to vocabulary mismatch.

I made up the schema entry and the two questions below, and both questions ask for the same count:

![Diagram of an invented schema entry, 'Readmission flag: marks a stay that follows a recent discharge', between two questions that ask for the same count. The question 'Readmission flag count per stay' shares three words with the entry. The question 'How many patients came back soon after they went home?' shares no word with it, and red lines pair its phrases with entry words of the same meaning. A keyword search finds no word in the entry to match the business question.](../../assets/figures/northwell/term_overlap.svg)

The business question gives a keyword search no word to match.

Searching harder does not fix a vocabulary mismatch; more results means more documents that
share no words with the question. BM25 scores document $d$ for question $q$ with one term per
question word $t$, where $f_{t,d}$ counts $t$ in $d$ and $\ell_d$ grows with the length of $d$:

$$
\mathrm{BM25}(q,d)=\sum_{t\in q}\mathrm{idf}(t)\,\frac{(k_1+1)\,f_{t,d}}{f_{t,d}+k_1\,\ell_d}
$$

A document that shares no word with the question gets 0 from every term, so a deeper search
cannot lift it.

With that diagnosis I ruled out the obvious fix and fused BM25 full-text search with
dense-vector retrieval, which raised hit@5 from 53.8% to 75% across about 250 analyst queries.

## Comparing the options

The team held three views on which retrieval approach to use and had no measurements to settle
it, so I put all three behind one runner that produces comparable reports on the same
questions. The approach I expected to win made no difference in the measured runs. The cause was
its configuration, so the report says what I measured and what it leaves open.

## Intern Kaggle competition

I tied for first in the intern Kaggle competition. The final submission blended CatBoost and
TabNet, weighted toward the stronger model, and the second earned its weight by making
different mistakes. The blend averages the two models' probabilities for a passenger $x$ and
predicts a transport when $p(x)$ reaches one half:

$$
p(x)=w\,p_{\text{CatBoost}}(x)+(1-w)\,p_{\text{TabNet}}(x),\qquad w>\tfrac12
$$

Because CatBoost carries more than half the weight, TabNet can change a prediction only inside a
band of CatBoost probabilities around one half.

I grouped validation folds so that passengers travelling together stayed in one fold, since
splitting a group inflates the local score. I reran both splitters from my code on the training
file and plotted where each one put the first eight travel groups with more than one passenger:

![Two panels of validation folds for the passengers in the training file's first eight travel groups with more than one passenger. Under the plain stratified split, six of the eight groups have members in two or more folds, shown as red zigzags. Under the grouped split, each group sits in one fold.](../../assets/figures/northwell/group_folds.svg)

The plain split sends six of the eight groups across folds, and the grouped split keeps each
group in one fold.

I tuned with Optuna and treated the results as candidates, because several configurations that
scored highest locally did worse on the leaderboard. I ran into the same problem in the retrieval work, where a single validation number
hid the failure that the grouping exposed.
