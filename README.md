# HR-Ask

PE6201 End-of-Course Project — Kang Xingyao, Section C.
A local HR policy assistant with evidence citations and unsubmitted five-field ticket drafts. All policies and employee examples are fictional. The evaluated core uses prompt version `draft-intent-v2`.

## Run

Python 3.10+; the application and evaluator use the standard library. Extract the ZIP, open a terminal in this folder, and run:

```bash
python3 server.py
```
Open http://127.0.0.1:8765. Stop with Ctrl+C. If the port is occupied, stop your previously launched HR-Ask server first.

For real model mode:

```bash
python3 run_openrouter.py
```
Enter the API key only after the hidden prompt, select **OpenRouter** in the webpage, and check that actual mode is `openrouter`. Never commit keys. An API error falls back visibly to local excerpts; fallback is not a model response. The default model is `openai/gpt-4o-mini`; the `HRASK_MODEL` environment variable can override it. Historical scores apply only to the saved model and source revision.

## Separate outcomes

| Measure | Saved result | Meaning |
|---|---:|---|
| Policy answers | 22/25 (88%) | Retrospective AI-assisted content review; not independent human validation |
| Complete tickets across all requests | 5/8 (62.5%) | Below the revised proposal target of >85% |
| Complete-input ticket cases | 5/5 | All required input available |
| Safe incomplete drafts | 3/3 | Unknown fields preserved; not completed tickets |
| Intent accuracy | 30/30 | Known development questions |
| Escalation | 3/30 (10%) | Workflow handling, not API errors |
| Clarification | 2/30 (6.67%) | Separate from escalation |
| Automatic engineering checks | 30/30 | Does not measure all answer-content defects |
| Existing offline challenge | 10/12 | Developer-authored diagnostic set |
| New informal offline diagnostics | 7/12 | Misspellings, abbreviations, informal wording and controls |
| Software regression tests | 15/15 | Includes mocked model boundaries |

The September 21 revised run has 25 accepted OpenRouter responses and no API errors; the other five cases are handled locally. The earlier live run passed only 22/30 engineering tasks and 0/8 draft schemas. The prompt repair distinguishes drafting from submitting. The September 23 informal diagnostic does not call an API and is not a live-model robustness score. No dataset is an independent holdout.

`results/openrouter.json` is frozen historical evidence. Do not overwrite it casually. Its full source, dataset and policy hashes support traceability. Content review labels were authored after reading those outputs, and this timing is explicitly disclosed. The supplied revised proposal's stronger goal of expected answers fixed before the original live test was not met retrospectively.

## Reproduce without an API key

```bash
python3 -m unittest discover -v
python3 evaluate.py --output results/reproduced_offline.json
python3 evaluate.py --cases tests/challenge.json --output results/reproduced_challenge.json
python3 evaluate.py --cases tests/informal_cases.json --output results/reproduced_informal.json
python3 scripts/summarize_evidence.py
python3 compare.py
```
The last command rewrites the reproducible keyword/threshold comparison. The content review is a documented judgment file, not an automated semantic grader. `summarize_evidence.py` aggregates judgments and verifies their source hash; it does not independently prove them correct.

For a new live evaluation, `python3 run_openrouter.py --evaluate` writes `results/openrouter.json`. Archive the historical file first, and review any new outputs anew; a review of an earlier answer cannot be reused for a changed response.

## Demonstrate

1. `年假一年有几天？` — consultation, policy citation, no ticket.
2. `帮我申请年假，E1001，2026-10-15，原因：家庭安排；联系：email` — complete unsubmitted draft.
3. `帮我申请补卡` — unknown fields remain null and are requested.

Known defects include redundant requests for a name, an overly absolute response to tomorrow's leave request, and weak support for informal expressions. The code is frozen to match the live evidence; these are not claimed fixed. A null-filled draft is not complete. Users must resend a full request; there is no multi-turn memory.

## Package map

- `docs/Final_Report.docx`: updated report and revised-proposal alignment.
- `docs/Problem_Statement_Revised.docx`: supplied revised proposal, unchanged.
- `docs/Self_Appraisal.docx`: evidence-based cover, with personal confirmation pending.
- `docs/HR_Ask_English_Demo.mp4`: actual screenshots with synthetic English narration and subtitles.
- `docs/English_Narration.txt`: matching narration.
- `src/`, `policies/`, `tests/`: application, fictional evidence, tests and review rubric.
- `results/`: frozen live evidence, separate policy review and diagnostics.
- `scripts/summarize_evidence.py`: traceable metric and cost aggregation.
- `HR_Ask_Demo.ipynb`: optional notebook walkthrough.

## Costs and deployment limits

The revised run reports USD 0.0036039 across 25 API responses in provider metadata. It is not a reconciled account bill. The cost model uses instructor feedback that 15–20 regex rules require rewriting each quarter; its midpoint is combined with transparent assumptions about minutes per rule and hourly labour rate. No real productivity savings, production deployment, security certification or independent HR review are claimed. No submission or approval tools exist.

## Attribution and outstanding submission steps

AI assisted the implementation, synthetic policies, tests, review, report and video. Synthetic narration is not the student's voice; footage consists of actual application screenshots, not continuous screen capture. The student must understand and review the work and follow course disclosure rules.

The course Class 5 cost-to-serve material informed the report methodology; insurance-project results are not reused as HR evidence. The course source files are not redistributed in this package.

GitHub publication is pending. Create a repository and upload this folder's project files, then record its verified URL in `SUBMISSION_LINKS.txt`. Keep the video and personal cover off a public repository if you prefer, and submit them through the course platform. The course requires code in GitHub: a ZIP alone does not fulfill that requirement. Verify grader access to all links and review/sign the self-appraisal before submission.
