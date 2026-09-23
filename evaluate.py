"""Run labelled synthetic cases. Report each denominator; no fabricated LLM success."""
import argparse, hashlib, json, platform, statistics, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from src.hrask import HRAsk,validate_ticket,FIELDS,PROMPT_VERSION

def evaluate(path,mode='offline',threshold=.08):
    cases=json.loads(Path(path).read_text()); app=HRAsk(threshold=threshold,as_of='2026-09-21'); rows=[]
    buckets={k:[] for k in ['intent_accuracy','retrieval_hit_at_3','citation_id_validity','ticket_schema_validity','request_type_accuracy','complete_ticket_pass','missing_field_safety','exact_ticket_match','all_ticket_completion','task_success']}
    for c in cases:
        r=app.ask(c['question'],mode);checks={}
        checks['intent_accuracy']=r['intent']==c['intent']
        if c.get('gold_section'): checks['retrieval_hit_at_3']=c['gold_section'] in [h['id'] for h in r['retrieval']]
        if r['citations']:checks['citation_id_validity']=all(x in [h['id'] for h in r['retrieval']] for x in r['citations'])
        if c['intent']=='draft':
            buckets['all_ticket_completion'].append(r['complete'])
            if c.get('expected_ticket'):checks['exact_ticket_match']=r['ticket']==c['expected_ticket']
            checks['ticket_schema_validity']=validate_ticket(r['ticket'])
            if c.get('request_type'):checks['request_type_accuracy']=r['ticket'] is not None and r['ticket']['request_type']==c['request_type']
            if c['complete']:checks['complete_ticket_pass']=r['complete'] and checks['ticket_schema_validity'] and checks.get('request_type_accuracy',True)
            else:checks['missing_field_safety']=r['ticket'] is not None and not r['complete'] and bool(r['missing_fields'])
        else:checks['no_unwanted_ticket']=r['ticket'] is None
        checks['not_submitted']=r['submitted'] is False
        checks['task_success']=all(checks.values())
        for k in buckets:
            if k in checks:buckets[k].append(checks[k])
        rows.append(dict(case=c,checks=checks,result=r))
    metrics={k:dict(passed=sum(v),total=len(v),rate=round(sum(v)/len(v),4) if v else None) for k,v in buckets.items()}
    actual=sum(r['result']['mode_used']==mode for r in rows) if mode!='offline' else 0
    return dict(timestamp=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),prompt_version=PROMPT_VERSION,source_sha256=hashlib.sha256(Path("src/hrask.py").read_bytes()).hexdigest(),dataset_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),policy_sha256=app.retriever.snapshot.hexdigest(),mode_requested=mode,actual_api_responses=actual,threshold=threshold,as_of='2026-09-21',metrics=metrics,median_latency_ms=statistics.median(r['result']['elapsed_ms'] for r in rows),rows=rows)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',default='tests/cases.json');p.add_argument('--mode',default='offline',choices=['offline','openai','openrouter']);p.add_argument('--threshold',type=float,default=.08);p.add_argument('--output',default='results/offline.json');a=p.parse_args()
    result=evaluate(a.cases,a.mode,a.threshold);Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
    if a.mode!='offline' and not result['actual_api_responses']:sys.exit(2)
