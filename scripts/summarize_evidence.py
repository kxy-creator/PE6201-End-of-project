"""Recompute saved evidence, API cost and transparent rule-maintenance cost."""
from pathlib import Path
import hashlib
import json
import statistics

ROOT = Path(__file__).resolve().parents[1]
LIVE_PATH = ROOT / 'results' / 'openrouter.json'
REVIEW_PATH = ROOT / 'results' / 'policy_answer_review.json'
SUMMARY_PATH = ROOT / 'results' / 'report_cost_summary.json'

# Instructor-provided recurring workload; midpoint used for the illustrative calculation.
RULES_PER_QUARTER_MIN = 15
RULES_PER_QUARTER_MAX = 20
MINUTES_PER_RULE = 20  # Assumption: revision, regression test and release check.
LABOUR_RATE_USD_PER_HOUR = 25  # Illustrative rate, not observed payroll data.
MONTHLY_ENQUIRIES = 400
MINUTES_SAVED_PER_USEFUL_ENQUIRY = 5
# Illustrative scenario only. This is not measured HR handling time and is distinct from minutes saved.
MINUTES_PER_UNSUCCESSFUL_ENQUIRY = 5
INITIAL_SETUP_USD = 2000

live = json.loads(LIVE_PATH.read_text())
review = json.loads(REVIEW_PATH.read_text())
assert review['source_sha256'] == hashlib.sha256(LIVE_PATH.read_bytes()).hexdigest(), 'Review belongs to a different live result file'

rows = live['rows']
api = [row['result'] for row in rows if row['result']['mode_used'] == 'openrouter']
api_cost = sum(result['usage']['cost'] for result in api)
mean_api_cost = api_cost / len(api)
models = sorted({result['model'] for result in api})
assert models == ['openai/gpt-4o-mini'], f'Expected one saved model, got {models}'
mean_prompt_tokens = statistics.mean(result['usage']['prompt_tokens'] for result in api)
mean_completion_tokens = statistics.mean(result['usage']['completion_tokens'] for result in api)

rules_per_quarter_midpoint = (RULES_PER_QUARTER_MIN + RULES_PER_QUARTER_MAX) / 2
quarterly_maintenance_hours = rules_per_quarter_midpoint * MINUTES_PER_RULE / 60
quarterly_maintenance_cost = quarterly_maintenance_hours * LABOUR_RATE_USD_PER_HOUR
monthly_maintenance_cost = quarterly_maintenance_cost / 3
monthly_api_cost = MONTHLY_ENQUIRIES * mean_api_cost
fallback_cost_per_unsuccessful_enquiry = MINUTES_PER_UNSUCCESSFUL_ENQUIRY / 60 * LABOUR_RATE_USD_PER_HOUR

sensitivity = []
for useful_resolution_rate in [0.2, 0.5, 0.8]:
    gross_value = MONTHLY_ENQUIRIES * useful_resolution_rate * MINUTES_SAVED_PER_USEFUL_ENQUIRY / 60 * LABOUR_RATE_USD_PER_HOUR
    monthly_expected_fallback_cost = MONTHLY_ENQUIRIES * (1 - useful_resolution_rate) * fallback_cost_per_unsuccessful_enquiry
    monthly_operating_cost = monthly_api_cost + monthly_maintenance_cost + monthly_expected_fallback_cost
    cost_per_query_attempt = monthly_operating_cost / MONTHLY_ENQUIRIES
    cost_per_useful_resolution = monthly_operating_cost / (MONTHLY_ENQUIRIES * useful_resolution_rate)
    net_monthly_value = gross_value - monthly_operating_cost
    sensitivity.append({
        'useful_resolution_rate': useful_resolution_rate,
        'gross_value_usd': gross_value,
        'monthly_expected_fallback_cost_usd': monthly_expected_fallback_cost,
        'monthly_operating_cost_usd': monthly_operating_cost,
        'cost_per_query_attempt_usd': cost_per_query_attempt,
        'cost_per_useful_resolution_usd': cost_per_useful_resolution,
        'net_monthly_value_usd': net_monthly_value,
        'setup_payback_months': INITIAL_SETUP_USD / net_monthly_value if net_monthly_value > 0 else None,
    })

metrics = live['metrics']
out = {
    'answer_quality_review': {
        'passed': sum(row['pass'] for row in review['rows']),
        'total': len(review['rows']),
        'method': 'AI-assisted retrospective content review; a human spot check is still required before operational use',
    },
    'ticket_structural_pass_rate': {
        'passed': metrics['ticket_schema_validity']['passed'],
        'total': metrics['ticket_schema_validity']['total'],
        'definition': 'Valid JSON object with exactly five fields and the correct request type',
    },
    'ticket_first_turn_completion': {
        **metrics['all_ticket_completion'],
        'definition': 'Complete five-field ticket on the first turn; distinct from structural validity',
    },
    'intent_accuracy': metrics['intent_accuracy'],
    'escalation_rate': {'count': sum(row['result']['intent'] == 'escalate' for row in rows), 'total': len(rows)},
    'clarification_rate': {'count': sum(row['result']['intent'] == 'clarify' for row in rows), 'total': len(rows)},
    'api_responses': len(api),
    'api_error_count': sum(bool(result['api_error']) for result in api),
    'provider_reported_cost_usd': round(api_cost, 9),
    'model_per_query': {
        'model': models[0],
        'responses': len(api),
        'mean_prompt_tokens': round(mean_prompt_tokens, 2),
        'mean_completion_tokens': round(mean_completion_tokens, 2),
        'mean_provider_reported_cost_usd': round(mean_api_cost, 9),
    },
    'api_only_median_elapsed_ms': statistics.median(result['elapsed_ms'] for result in api),
    'rule_maintenance_cost': {
        'instructor_provided_rules_per_quarter_range': [RULES_PER_QUARTER_MIN, RULES_PER_QUARTER_MAX],
        'rules_per_quarter_midpoint': rules_per_quarter_midpoint,
        'assumed_minutes_per_rule': MINUTES_PER_RULE,
        'assumed_labour_rate_usd_per_hour': LABOUR_RATE_USD_PER_HOUR,
        'quarterly_maintenance_hours': quarterly_maintenance_hours,
        'quarterly_maintenance_cost_usd': quarterly_maintenance_cost,
        'monthly_maintenance_cost_usd': monthly_maintenance_cost,
    },
    'manual_answer_spot_check': {
        'status': 'not yet completed',
        'protocol': 'tests/MANUAL_ANSWER_SPOT_CHECK.md',
        'use_in_cost_model': 'Use a completed human spot-check pass rate as the useful-resolution input; do not substitute ticket structural validity.',
    },
}

summary = {
    'evidence': 'results/openrouter.json',
    'api_responses': len(api,
    ),
    'provider_reported_cost_usd': round(api_cost, 9),
    'mean_per_api_response_usd': round(mean_api_cost, 9),
    'gpt_4o_mini_per_query': {
        'model': models[0],
        'responses': len(api),
        'mean_prompt_tokens': round(mean_prompt_tokens, 2),
        'mean_completion_tokens': round(mean_completion_tokens, 2),
        'mean_provider_reported_cost_usd': round(mean_api_cost, 9),
    },
    'two_saved_runs_cost_usd': 0.00618615,
    'api_median_elapsed_ms': statistics.median(result['elapsed_ms'] for result in api),
    'outcome_metrics': {
        'ticket_structural_pass_rate': {
            'passed': metrics['ticket_schema_validity']['passed'],
            'total': metrics['ticket_schema_validity']['total'],
            'definition': 'Valid JSON object with exactly five fields and the correct request type',
        },
        'ticket_first_turn_completion': {
            'passed': metrics['all_ticket_completion']['passed'],
            'total': metrics['all_ticket_completion']['total'],
            'definition': 'Complete five-field ticket on the first turn',
        },
        'answer_quality_review': {
            'passed': sum(row['pass'] for row in review['rows']),
            'total': len(review['rows']),
            'method': 'AI-assisted retrospective review; not a completed human spot check',
        },
        'manual_answer_spot_check': {
            'status': 'not yet completed',
            'protocol': 'tests/MANUAL_ANSWER_SPOT_CHECK.md',
        },
    },
    'rule_maintenance': {
        'basis': 'Instructor feedback: 15 to 20 regex rules rewritten every quarter.',
        'rules_per_quarter_range': [RULES_PER_QUARTER_MIN, RULES_PER_QUARTER_MAX],
        'rules_per_quarter_midpoint': rules_per_quarter_midpoint,
        'assumed_minutes_per_rule': MINUTES_PER_RULE,
        'assumed_labour_rate_usd_per_hour': LABOUR_RATE_USD_PER_HOUR,
        'quarterly_maintenance_hours': quarterly_maintenance_hours,
        'quarterly_maintenance_cost_usd': quarterly_maintenance_cost,
        'monthly_maintenance_cost_usd': monthly_maintenance_cost,
    },
    'assumptions': {
        'monthly_enquiries': MONTHLY_ENQUIRIES,
        'usd_hour': LABOUR_RATE_USD_PER_HOUR,
        'minutes_saved_per_useful_enquiry': MINUTES_SAVED_PER_USEFUL_ENQUIRY,
        'minutes_per_unsuccessful_enquiry_for_human_fallback': MINUTES_PER_UNSUCCESSFUL_ENQUIRY,
        'human_fallback_cost_per_unsuccessful_enquiry_usd': fallback_cost_per_unsuccessful_enquiry,
        'useful_resolution_rate_definition': 'Human spot-check pass rate for the answering workload; scenario values only until a spot check is completed',
        'monthly_api_cost_usd': monthly_api_cost,
        'setup_usd': INITIAL_SETUP_USD,
    },
    'sensitivity': sensitivity,
}

assert out['answer_quality_review']['passed'] == 22
assert out['ticket_first_turn_completion']['passed'] == 5
SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(out, ensure_ascii=False, indent=2))
