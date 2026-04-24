source .venv/bin/activate
uvicorn app.main:app --reload

PYTHONPATH=. python3 app/editor.py