# GitHub Upload Instructions

## Step 1: Initialize Git Repository

```bash
cd ~/projects/skagit-ymca
git init
```

## Step 2: Add Files

```bash
git add .
git commit -m "Initial commit: QuickBooks Budget File Generator for Skagit Valley YMCA"
```

## Step 3: Connect to GitHub

```bash
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/quickbooks-input.git
```

## Step 4: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

## Alternative: If Repository Already Exists

If you already have the repository created on GitHub:

```bash
cd ~/projects/skagit-ymca
git init
git add .
git commit -m "Initial commit: QuickBooks Budget File Generator"
git remote add origin https://github.com/YOUR_USERNAME/quickbooks-input.git
git branch -M main
git push -u origin main
```

## One-Line Command for Quick Setup

```bash
cd ~/projects/skagit-ymca && git init && git add . && git commit -m "Initial commit: QuickBooks Budget Generator" && git remote add origin https://github.com/YOUR_USERNAME/quickbooks-input.git && git branch -M main && git push -u origin main
```

Remember to replace `YOUR_USERNAME` with your actual GitHub username!

## What Gets Uploaded

✓ app.py (main application)
✓ requirements.txt (dependencies)
✓ README.md (documentation)
✓ DEPLOYMENT.md (deployment guide)
✓ .gitignore (excludes CSV/Excel files)
✓ .streamlit/config.toml (Streamlit settings)

✗ CSV files (excluded by .gitignore)
✗ Excel files (excluded by .gitignore)
✗ Python cache files (excluded by .gitignore)
