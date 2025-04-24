# translation_tester

Notes:
- In production all servers must be started using WSGI (waitress): 
    waitress-serve --host=127.0.0.1 --port=5000 app.wsgi:app
- For debug purposes all server can be started as package: 
    python -m app.app