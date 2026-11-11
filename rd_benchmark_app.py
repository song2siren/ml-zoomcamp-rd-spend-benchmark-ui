"""A simple form for trying the Expected R&D Spend Benchmark service.

Run (no installation needed beyond uv):
    uvx --from streamlit streamlit run rd_benchmark_app.py

By default it uses the deployed service on Fly.io. To use a local service instead:
    API_URL=http://localhost:9696 uvx --from streamlit streamlit run rd_benchmark_app.py
"""
import os

import requests
import streamlit as st

API_URL = os.environ.get('API_URL', 'https://serene-meadow-5589.fly.dev').rstrip('/')

st.set_page_config(page_title='R&D Spend Benchmark', page_icon='📊')
st.title('Expected R&D Spend Benchmark')
st.caption(
    'Estimates the R&D spend expected for a company of a given size, sector and location, '
    'and checks whether a reported figure looks typical.'
)
st.warning(
    'Proof of concept built on public data about the world\'s largest R&D investors. '
    'Predictions are typically off by a factor of about 2, so results are a prompt for a closer look, '
    'not a judgement on any claim. **Do not enter confidential figures.**'
)


@st.cache_data(ttl=3600)
def get_options():
    response = requests.get(f'{API_URL}/options', timeout=30)
    response.raise_for_status()
    return response.json()


try:
    options = get_options()
except requests.RequestException as e:
    st.error(f'Could not reach the service at {API_URL}. It may be starting up: wait a few seconds and refresh.\n\n{e}')
    st.stop()

sectors = options['sectors']
countries = options['countries']

with st.form('company'):
    col1, col2 = st.columns(2)
    sector = col1.selectbox('Sector', sectors, index=sectors.index('Software & Computer Services')
                            if 'Software & Computer Services' in sectors else 0)
    country = col2.selectbox('Country', countries, index=countries.index('UK') if 'UK' in countries else 0)

    col1, col2 = st.columns(2)
    net_sales = col1.number_input('Net sales (€m)', min_value=0.0, value=250.0, step=10.0)
    employees = col2.number_input('Employees', min_value=1, value=1200, step=50)

    col1, col2 = st.columns(2)
    capex = col1.number_input('Capital expenditure (€m)', min_value=0.0, value=15.0, step=1.0)
    operating_profit = col2.number_input('Operating profit (€m, negative for a loss)', value=20.0, step=1.0)

    col1, col2 = st.columns(2)
    year = col1.number_input('Financial year', min_value=2003, max_value=2030, value=2024, step=1)
    year_incorporated = col2.number_input('Year incorporated', min_value=1600, max_value=2030, value=1998, step=1)

    reported_rnd = st.number_input('Reported R&D spend to check (€m, optional: leave at 0 to skip)',
                                   min_value=0.0, value=30.0, step=1.0)

    submitted = st.form_submit_button('Check R&D', type='primary')

if submitted:
    payload = {
        'net_sales': net_sales,
        'employees': employees,
        'capex': capex,
        'operating_profit': operating_profit,
        'year': int(year),
        'year_incorporated': int(year_incorporated),
        'sector': sector,
        'country': country,
    }
    if reported_rnd > 0:
        payload['reported_rnd'] = reported_rnd

    try:
        with st.spinner('Asking the model...'):
            response = requests.post(f'{API_URL}/predict', json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        st.error(f'The request failed: {e}')
        st.stop()

    low, high = result['typical_range']
    col1, col2 = st.columns(2)
    col1.metric('Expected R&D', f"€{result['expected_rnd']:,.1f}m")
    col2.metric('Typical range', f'€{low:,.1f}m – €{high:,.1f}m')

    if 'assessment' in result:
        ratio = result['reported_vs_expected']
        message = (f"Reported R&D of €{result['reported_rnd']:,.1f}m is {ratio:.2f} times the expected figure: "
                   f"**{result['assessment']}** for a company with this profile.")
        if result['assessment'] == 'typical':
            st.success(message)
        else:
            st.warning(message)

    with st.expander('Raw response from the service'):
        st.json(result)

st.caption(f'Service: {API_URL}')
