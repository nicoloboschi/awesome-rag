# Get recommendations for a specific users

In this use-case, we emulate an e-commerce backend that wants to build a recommendation system for their products.
The flow is as follows:
- The user visits a specific products
- The backend returns a list of recommended products that are part of the product catalog, with metadata about the product


## Setup
First we set up the Astra database:

```bash
export ASTRA_DB_ENDPOINT=https://xxx.astra.datastax.com
export ASTRA_DB_TOKEN=AstraCS:xxx
```

Build the project:
```bash
poetry install
```

Then we index the products:

```bash
poetry run python3 recommendations/setup_all.py
```

Now we can run the API server:

```bash
poetry run python3 recommendations/api.py
```

Now we can run the UI:
```bash
poetry run streamlit run recommendations/web/Home.py
```