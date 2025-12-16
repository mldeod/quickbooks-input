# Deployment Instructions

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run locally:
```bash
streamlit run app.py
```

## Streamlit Cloud Deployment

1. Push to GitHub (see GitHub instructions below)

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Click "New app"

4. Select your repository: `quickbooks-input`

5. Main file path: `app.py`

6. Click "Deploy"

Your app will be live at: `https://quickbooks-input.streamlit.app`

## Environment Variables

No environment variables required - all configuration is in the UI.

## File Size Limits

- Maximum upload size: 200MB (configured in `.streamlit/config.toml`)
- Adjust if needed for larger datasets
