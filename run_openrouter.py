"""Start optional OpenRouter-backed HR-Ask use without saving an API key.

The script reads ``OPENROUTER_API_KEY`` from the environment or a hidden
terminal prompt. With ``--evaluate`` it delegates to ``evaluate.py`` and writes
a fresh live result; otherwise it starts the local demo server. The key is not
printed, written to project files, or added to results. Historical evaluation
files should be archived before a new run replaces them.
"""
import getpass, os, runpy, sys
if not os.getenv('OPENROUTER_API_KEY'):
    os.environ['OPENROUTER_API_KEY']=getpass.getpass('OpenRouter key (hidden, not saved): ')
if not os.environ['OPENROUTER_API_KEY'].strip():raise SystemExit('No API key supplied')
if '--evaluate' in sys.argv:
    sys.argv=['evaluate.py','--mode','openrouter','--output','results/openrouter.json']
    runpy.run_path('evaluate.py',run_name='__main__')
else:
    runpy.run_path('server.py',run_name='__main__')
