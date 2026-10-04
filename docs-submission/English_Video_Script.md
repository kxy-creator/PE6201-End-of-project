# HR-Ask Video Script

**Target duration:** approximately 4 minutes
**Format:** live HR-Ask screen demonstration with the presenter visible in the upper-right corner

## Recording setup

Keep the HR-Ask initial page visible from the first second. Keep your camera visible in the upper-right corner throughout the recording. Read only the spoken text below; the stage directions are not subtitles.

## 0:00–0:20 — Opening

**On screen:** HR-Ask initial page and your camera.

**Spoken text:**

Hello, Professor. This is HR-Ask, my course project. It is a prototype that answers employee questions using fictional HR policies and prepares safe, unsubmitted request drafts. You can see the live HR-Ask page beside my camera. The interface is in English, while the policy examples are Chinese course data.

## 0:20–0:38 — Workflow

**On screen:** Remain on the initial page.

**Spoken text:**

The system first retrieves relevant policy evidence. It then classifies the request as a consultation, a draft request, a clarification, or an escalation. For draft requests, it extracts and validates five fields: employee ID, request type, requested date, reason, and contact channel.

## 0:38–1:05 — Demonstration 1: consultation

**On screen:** Type `年假一年有几天？`, then click **Get response**.

**Spoken text:**

In this first example, I enter a question asking how many annual-leave days are available. After I click “Get response,” the system identifies this as a consultation. It returns relevant policy evidence and does not create a ticket, because the user only asked a policy question.

## 1:05–1:35 — Demonstration 2: complete draft

**On screen:** Type `帮我申请年假，E1001，2026-10-15，原因：家庭安排；联系：email`, then click **Get response**.

**Spoken text:**

In the second example, the user requests annual leave and provides all five required fields. The system classifies it as a draft. The ticket panel shows valid JSON with exactly five fields, and the interface confirms that the draft is complete. However, it remains pending human review. This prototype never submits or approves requests automatically.

## 1:35–2:05 — Demonstration 3: missing information

**On screen:** Type `帮我申请补卡`, then click **Get response**.

**Spoken text:**

In the third example, the user asks for an attendance correction but does not provide all required information. The system keeps the missing fields empty and asks for clarification. It does not invent personal information. Therefore, this is an incomplete draft rather than a completed ticket.

## 2:05–2:40 — Evaluation

**On screen:** Leave the third result visible.

**Spoken text:**

I report ticket structure and answer quality separately. In eight drafting cases, all eight produced valid five-field JSON with the correct request type. Five were complete on the first turn, giving a first-turn completion rate of sixty-two point five percent. For answer quality, a retrospective AI-assisted review passed twenty-two of twenty-five policy answers. My documented manual student spot check passed eight of ten sampled answers. This manual check is not independent HR validation.

## 2:40–3:05 — Cost

**On screen:** Keep the app visible, or show the results section in the repository.

**Spoken text:**

The observed variable model-inference cost was approximately zero point zero zero zero one four four US dollars per query. This is not the total cost of a successfully resolved case. The cost model also considers human fallback and recurring rule maintenance, including fifteen to twenty regex rules rewritten every quarter.

## 3:05–3:25 — Closing

**On screen:** Return to the HR-Ask page; your camera remains visible.

**Spoken text:**

HR-Ask is a course prototype using fictional data. It does not make legal decisions, approve leave, submit requests, or handle sensitive disputes. These cases are escalated to HR. Thank you for watching.
