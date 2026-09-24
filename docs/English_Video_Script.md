# HR-Ask Video Script

**Approximate length: 4 minutes**

## Opening

Hello. This is my PE6201 end-of-course project, HR-Ask.

HR-Ask is a prototype that helps employees ask questions about HR policies and prepare unsubmitted request drafts. It covers fictional policies on leave, attendance, social insurance, and workplace procedures. The project does not connect to a real HR system, and all employee data and policies shown in this demonstration are fictional.

The business problem is repetitive HR enquiries and incomplete requests. Employees may need a simple policy explanation, while HR staff need requests to contain the right information before they can review them. HR-Ask separates these two tasks: it provides policy-based answers and, only when requested, prepares a five-field draft.

## How the system works

The application retrieves relevant sections from five policy documents. It then classifies the request as a consultation, a draft request, a clarification, or an escalation. When a draft is requested, Python validates five required fields: employee ID, request type, requested date, reason, and contact channel.

The prototype can run in a local retrieval mode or use OpenRouter with the openai/gpt-4o-mini model. The language model is used for grounded answer generation, while retrieval, ticket validation, and evaluation remain local and inspectable.

## Demonstration 1: policy consultation

On screen, I enter: “How many days of annual leave are available each year?”

This is classified as a consultation because the employee is asking for information rather than asking the system to prepare a request. The answer cites the relevant fictional policy section and no ticket is created. In this prototype, the policy states that full-time employees receive twelve days of annual leave. This is a simulated company policy, not legal advice.

## Demonstration 2: complete draft

Next, I enter: “Please draft an annual-leave request for employee E1001 on 2026-10-15. Reason: family arrangements. Contact me by email.”

The system identifies a drafting request and creates a five-field ticket. The ticket is valid JSON and includes the employee ID, request type, date, reason, and contact channel.

This is still only a draft. It has not been submitted or approved. A human employee must confirm the information and submit it through the formal HR process.

## Demonstration 3: missing information

For the third example, I enter: “Please help me correct a missed clock-in.”

The system identifies the relevant attendance process, but the employee ID, date, reason, and contact channel are missing. It keeps those fields as null and asks the employee to provide them. This avoids inventing personal information. However, it is an incomplete draft, not a completed ticket.

## Evaluation and outcome metrics

I report answer quality and ticket structure separately.

For ticket structure, all eight drafting cases produced valid JSON with exactly five fields and the correct request type. This is a narrow structural measure. Across all eight drafting requests, five were complete on the first turn, giving a first-turn completion rate of 62.5 percent.

For answer quality, a retrospective AI-assisted review passed 22 of 25 eligible policy answers. This is not a completed human spot check, so it should not be presented as independent human validation.

The project also includes 15 software regression tests, all of which pass. The automated engineering checks and structural validity results do not prove that every policy explanation is correct.

## Cost and limitations

The saved OpenRouter run used 25 accepted model responses. Its observed provider-reported inference cost was approximately 0.000144 US dollars per query. At 400 comparable queries per month, that is about 0.0577 US dollars in monthly variable model inference cost.

This is not the total cost per successful resolution. The separate cost model also includes human fallback for unsuccessful enquiries and recurring maintenance of rule-based logic. Under an illustrative 50 percent useful-resolution scenario, operating cost is 2.33 US dollars per useful resolution and the monthly value remains negative before recovering initial setup costs.

The system has important limitations. It can produce imperfect wording, it has limited support for informal requests, and it does not have multi-turn memory. It must not approve leave, submit requests, calculate legal entitlements, or handle sensitive disputes. Those cases are escalated to HR.

## Closing

In summary, HR-Ask demonstrates retrieval-based policy consultation, safe preparation of structured drafts, validation of missing information, separate evaluation of answer quality and ticket structure, and a transparent cost model.

Thank you for watching.
