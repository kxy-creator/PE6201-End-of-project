"""Prompt without echoing or storing the API key, then run the chosen task."""
import getpass, os, runpy, sys
if not os.getenv('OPENROUTER_API_KEY'):
    os.environ['OPENROUTER_API_KEY']=getpass.getpass('OpenRouter key (hidden, not saved): ')
if not os.environ['OPENROUTER_API_KEY'].strip():raise SystemExit('No API key supplied')
if '--evaluate' in sys.argv:
    sys.argv=['evaluate.py','--mode','openrouter','--output','results/openrouter.json']
    runpy.run_path('evaluate.py',run_name='__main__')
else:
    runpy.run_path('server.py',run_name='__main__')
