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
INITIAL_SETUP_USD = 2000

live = json.loads(LIVE_PATH.read_text())
review = json.loads(REVIEW_PATH.read_text())
assert review['source_sha256'] == hashlib.sha256(LIVE_PATH.read_bytes()).hexdigest(), 'Review belongs to a different live result file'

rows = live['rows']
api = [row['result'] for row in rows if row['result']['mode_used'] == 'openrouter']
api_cost = sum(result['usage']['cost'] for result in api)
mean_api_cost = api_cost / len(api)

rules_per_quarter_midpoint = (RULES_PER_QUARTER_MIN + RULES_PER_QUARTER_MAX) / 2
quarterly_maintenance_hours = rules_per_quarter_midpoint * MINUTES_PER_RULE / 60
quarterly_maintenance_cost = quarterly_maintenance_hours * LABOUR_RATE_USD_PER_HOUR
monthly_maintenance_cost = quarterly_maintenance_cost / 3
monthly_api_cost = MONTHLY_ENQUIRIES * mean_api_cost

sensitivity = []
for useful_resolution_rate in [0.2, 0.5, 0.8]:
    gross_value = MONTHLY_ENQUIRIES * useful_resolution_rate * MINUTES_SAVED_PER_USEFUL_ENQUIRY / 60 * LABOUR_RATE_USD_PER_HOUR
    net_monthly_value = gross_value - monthly_maintenance_cost - monthly_api_cost
    sensitivity.append({
        'useful_resolution_rate': useful_resolution_rate,
        'gross_value_usd': gross_value,
        'net_monthly_value_usd': net_monthly_value,
        'setup_payback_months': INITIAL_SETUP_USD / net_monthly_value,
    })

metrics = live['metrics']
out = {
    'policy_answer_review': {'passed': sum(row['pass'] for row in review['rows']), 'total': len(review['rows']), 'method': 'AI-assisted retrospective judgments, not an independent human or pre-registered evaluation'},
    'ticket_first_turn_completion': metrics['all_ticket_completion'],
    'intent_accuracy': metrics['intent_accuracy'],
    'escalation_rate': {'count': sum(row['result']['intent'] == 'escalate' for row in rows), 'total': len(rows)},
    'clarification_rate': {'count': sum(row['result']['intent'] == 'clarify' for row in rows), 'total': len(rows)},
    'api_responses': len(api),
    'api_error_count': sum(bool(result['api_error']) for result in api),
    'provider_reported_cost_usd': round(api_cost, 9),
    'mean_cost_per_api_response_usd': round(mean_api_cost, 9),
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
}

summary = {
    'evidence': 'results/openrouter.json',
    'api_responses': len(api,
    ),
    'provider_reported_cost_usd': round(api_cost, 9),
    'mean_per_api_response_usd': round(mean_api_cost, 9),
    'two_saved_runs_cost_usd': 0.00618615,
    'api_median_elapsed_ms': statistics.median(result['elapsed_ms'] for result in api),
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
        'minutes_saved': MINUTES_SAVED_PER_USEFUL_ENQUIRY,
        'monthly_api_cost_usd': monthly_api_cost,
        'setup_usd': INITIAL_SETUP_USD,
    },
    'sensitivity': sensitivity,
}

assert out['policy_answer_review']['passed'] == 22
assert out['ticket_first_turn_completion']['passed'] == 5
SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(out, ensure_ascii=False, indent=2))
