# Expected R&D Spend Benchmark: web app

**Live app:** https://rd-spend-benchmark.streamlit.app

A simple web form for the [Expected R&D Spend Benchmark](https://github.com/song2siren/ml-zoomcamp-rd-spend-benchmark), my midterm project for the DataTalksClub [Machine Learning Zoomcamp](https://github.com/DataTalksClub/machine-learning-zoomcamp).

Enter a company's figures (sales, employees, capex, profit, sector and country) and the app estimates the R&D spend expected for a company with that profile. Optionally, enter a reported R&D figure to see whether it looks typical, unusually high or unusually low.

The form is built with [Streamlit](https://streamlit.io). It sends the figures to the project's machine learning service (an XGBoost model served with FastAPI on [Fly.io](https://fly.io)) and displays the result. The model, data and training code are all in the [main project repository](https://github.com/song2siren/ml-zoomcamp-rd-spend-benchmark).

> **Important:** this is a personal learning project and a proof of concept, built on public data about the world's largest corporate R&D investors (the EU Industrial R&D Investment Scoreboard). Predictions are typically off by a factor of about 2. Results are a prompt for a closer look, not a judgement on any company or claim, and are not advice. Please don't enter confidential figures.

## Running it locally

```bash
pip install -r requirements.txt
streamlit run rd_benchmark_app.py
```

By default the app uses the deployed service at `https://serene-meadow-5589.fly.dev`. To use a different instance of the service, for example one running locally:

```bash
API_URL=http://localhost:9696 streamlit run rd_benchmark_app.py
```
