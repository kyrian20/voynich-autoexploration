# Skill: Query Knowledge Base

## Purpose
Search the Librarian KB at ~/voynich-kb/ before designing any experiment. The KB contains 100+ summarized sources. If a hypothesis has already been tested and settled, you should not retest it — instead, use the prior result as a starting point for a genuinely new variant.

## When to Use This Skill

Use query_kb at the start of every hypothesis evaluation cycle, specifically:
- Before adding a new hypothesis to the backlog (to check if it's a duplicate)
- Before running an experiment (to check if someone already ran the equivalent test)
- When interpreting a result (to contextualize it against prior findings)
- When a finding raises a follow-up question (to check if the KB already answers it)

## Inputs
- `topic`: A keyword or phrase describing the concept (e.g., "entropy," "Currier A," "gallows characters," "verbose cipher")
- `hypothesis_id`: Optional — the specific backlog entry being checked

## Procedure

### Step 1: Check state files
Read these first, as they summarize what's already resolved:
```bash
cat ~/voynich-kb/state/failed_approaches.md
cat ~/voynich-kb/state/findings.md
cat ~/voynich-kb/state/open_questions.md
```
If your hypothesis appears in `failed_approaches.md`, it has been ruled out. Do not retest unless you have a specific reason to believe the prior test was methodologically flawed — and if so, flag this as an open question before proceeding.

### Step 2: Query the registry
```bash
sqlite3 ~/voynich-kb/registry.db
```

**Keyword search:**
```sql
SELECT id, title, authors, year, tags
FROM sources
WHERE title LIKE '%entropy%' OR tags LIKE '%entropy%'
ORDER BY cite_count DESC;
```

**Find highly cited sources on a topic:**
```sql
SELECT id, title, authors, year, cite_count
FROM sources
WHERE tags LIKE '%statistical%'
ORDER BY cite_count DESC
LIMIT 10;
```

**Traverse the citation graph** — find sources connected to a known relevant source:
```sql
-- Sources that cite source X (discovered_from = X):
SELECT id, title, authors, year
FROM sources
WHERE discovered_from = 'bowern_entropy_2021';

-- Sources that X was discovered from (parent):
SELECT s2.id, s2.title, s2.authors, s2.year
FROM sources s1
JOIN sources s2 ON s1.discovered_from = s2.id
WHERE s1.id = 'bowern_entropy_2021';
```

**Find all sources tagged with a specific topic:**
```sql
SELECT id, title, authors, year, ingestion_status
FROM sources
WHERE tags LIKE '%verbose cipher%'
ORDER BY year DESC;
```

### Step 3: Read relevant summaries
For each source with `ingestion_status = 'summarized'`:
```bash
cat ~/voynich-kb/summaries/{id}.md
```

Focus on:
- **Claim** — what the source argues
- **Methodological Lessons** — what worked, what didn't
- **Open Questions Raised** — questions the source left unanswered (these are often good experiment seeds)

### Step 4: Grep summary files
For fast cross-source keyword search:
```bash
grep -r "positional entropy" ~/voynich-kb/summaries/ -l
grep -r "h2\|second.order entropy" ~/voynich-kb/summaries/ -i
grep -r "Stolfi" ~/voynich-kb/summaries/ -l
```

### Step 5: Synthesize
After reading, answer:
1. Has this exact hypothesis been tested? By whom? What result?
2. Has a close variant been tested? What does that tell us about this one?
3. Are there methodological lessons that apply to how I should design my experiment?
4. Are there reference numbers in the literature (e.g., "Voynich h2 ≈ 2.0") that my experiment should reproduce as a sanity check?

## Recognizing When Prior Work Has Settled a Hypothesis

A hypothesis is settled if:
- A peer-reviewed source (or multiple independent sources in agreement) tested it with a rigorous method
- The result has not been credibly contested
- The prior test used similar or better data than you have access to

A hypothesis is NOT settled if:
- The prior test had a methodological flaw you can identify specifically
- Your variant involves a different decomposition, corpus subset, or control comparison
- The prior test was on older/coarser transcription data (e.g., Currier system only) and you have newer EVA data

When in doubt, flag the question in `open_questions.md` and ask the user whether the prior work covers your variant adequately.

## Output
A brief synthesis for your own use before designing the experiment:
- Prior work summary (sources, results, limitations)
- Whether your proposed experiment is genuinely new or a duplicate
- Reference numbers to reproduce as sanity checks
- Methodological pitfalls to avoid based on prior failures
