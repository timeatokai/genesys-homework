# genesys-homework

Genesys homework assignment.

# How to test:

1. clone the repository
    `git clone https://github.com/timeatokai/genesys-homework.git`
2. install the requirements (preferably in a separate environment, e.g. Conda)
    `pip install -r requirements.txt`
    (or `requirements-frozen.txt`, to match the exact package versions)
3. from the repo root, run `uvicorn app.main:app --reload`
4. the server will be available at http://127.0.0.1:8000. The interactive OpenAPI docs will be available at http://127.0.0.1:8000/docs.

# TODO:

- add missing tests
- avoid using endpoints in endpoint tests
- add test teardown
