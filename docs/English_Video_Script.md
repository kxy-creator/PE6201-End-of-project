# HR-Ask Video Script (Current Demonstration)

**Duration:** approximately 3 minutes 38 seconds  
**Format:** actual application screenshots, recorded English narration, and English captions

## Opening

Hello, Professor. This is HR-Ask, my course project. It is a prototype that answers employee questions using fictional HR policies and prepares safe, unsubmitted request drafts. The interface is in English, while the policy examples are Chinese course data.

## How the system works

The system first retrieves relevant policy evidence. It then classifies the request as a consultation, a draft request, a clarification, or an escalation. For draft requests, it extracts and validates five fields: employee ID, request type, requested date, reason, and contact channel.

## Demonstration 1: consultation

In this first example, I enter a question asking how many annual-leave days are available. After I click “Get response,” the system identifies this as a consultation. It returns relevant policy evidence and does not create a ticket, because the user only asked a policy question.

## Demonstration 2: complete draft

In the second example, the user requests annual leave and provides all five required fields. The system classifies it as a draft. The ticket panel shows valid JSON with exactly five fields, and the interface confirms that the draft is complete. However, it remains pending human review. This prototype never submits or approves requests automatically.

## Demonstration 3: missing information

In the third example, the user asks for leave tomorrow but does not provide all required information. The system keeps the missing fields empty and asks for clarification. It does not invent personal information. Therefore, this is an incomplete draft rather than a completed ticket.

## Evaluation and cost

I report ticket structure and answer quality separately. In eight drafting cases, all eight produced valid five-field JSON with the correct request type. Five were complete on the first turn, giving a first-turn completion rate of sixty-two point five percent. For answer quality, a retrospective AI-assisted review passed twenty-two of twenty-five policy answers. My documented manual student spot check passed eight of ten sampled answers. This manual check is not independent HR validation.

The observed variable model-inference cost was approximately zero point zero zero zero one four four US dollars per query. This is not the total cost of a successfully resolved case. The cost model also considers human fallback and recurring rule maintenance, including fifteen to twenty regex rules rewritten every quarter.

## Closing

HR-Ask is a course prototype using fictional data. It does not make legal decisions, approve leave, submit requests, or handle sensitive disputes. These cases are escalated to HR. Thank you for watching.
