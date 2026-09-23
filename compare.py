"""Compare a fixed keyword FAQ with TF-IDF; sweep a non-probabilistic threshold."""
import json
from pathlib import Path
from evaluate import evaluate
from src.hrask import Retriever
r=Retriever(as_of='2026-09-21');cases=json.loads(Path('tests/cases.json').read_text())
faq=[('年假','HR-LV-01/annual'),('病假','HR-LV-01/sick'),('事假','HR-LV-01/personal'),('打卡','HR-AT-01/correction'),('补卡','HR-AT-01/correction'),('迟到','HR-AT-01/late'),('加班','HR-AT-01/overtime'),('排班','HR-AT-01/shift'),('社保','HR-SC-01/enrol'),('公积金','HR-SC-01/fund'),('工单','HR-WF-01/fields')]
scored=[c for c in cases if c['gold_section']]
hits=sum(next((v for k,v in faq if k in c['question']),None)==c['gold_section'] for c in scored)
out={'keyword_faq':{'passed':hits,'total':len(scored),'rate':hits/len(scored),'definition':'First matching keyword returns one fixed policy section; section-ID hit only.'},'threshold_sweep':[]}
for threshold in [0,.08,.2,.4,.65]:
 x=evaluate('tests/cases.json',threshold=threshold)
 out['threshold_sweep'].append({'threshold':threshold,'task_success':x['metrics']['task_success'],'escalations':sum(z['result']['intent']=='escalate' for z in x['rows'])})
Path('results/comparison.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
