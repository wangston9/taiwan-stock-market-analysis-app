# GitHub Actions Setup Guide

## 🚀 Quick Setup

### 1. Enable GitHub Actions
1. Go to your repository on GitHub
2. Click on "Actions" tab
3. Click "I understand my workflows, go ahead and enable them"

### 2. Add Required Secrets
Go to Settings → Secrets and variables → Actions → New repository secret

#### For Hugging Face Deployment (Optional):
- `HF_TOKEN`: Your Hugging Face access token
  - Get it from: https://huggingface.co/settings/tokens
- `HF_USERNAME`: Your Hugging Face username
- `HF_SPACE_NAME`: Your Space name (e.g., "Personal_Finance_App")

#### For Streamlit Cloud (Optional):
- `STREAMLIT_API_TOKEN`: Your Streamlit Cloud API token
  - Get it from: https://share.streamlit.io/settings

### 3. Configure OpenAI API Key
Add to repository secrets:
- `OPENAI_API_KEY`: Your OpenAI API key (for the AI Stock Agent)

## 📅 Automated Features

### Quarterly Data Updates
The app will automatically download new financial data on:
- **May 15**: Q1 data (Jan-Mar)
- **August 14**: Q2 data (Apr-Jun) 
- **November 14**: Q3 data (Jul-Sep)
- **March 31**: Q4 data (Oct-Dec)

### Manual Controls
You can manually trigger downloads from the Actions tab:
1. Go to Actions → "Quarterly Data Update"
2. Click "Run workflow"
3. Options:
   - Force download: Override schedule check
   - Specific industry: Download only one industry

## 🛠️ Workflow Files

### 1. `quarterly_data_update.yml`
- **Purpose**: Downloads Taiwan stock data quarterly
- **Schedule**: Runs 4 times per year automatically
- **Manual trigger**: Yes, with options
- **What it does**:
  - Checks if it's time to download
  - Downloads all industry data
  - Commits changes automatically
  - Creates issue if download fails

### 2. `deploy_app.yml`
- **Purpose**: Deploys app to Streamlit/HuggingFace
- **Trigger**: Push to main branch
- **What it does**:
  - Runs tests
  - Checks Python syntax
  - Deploys to Streamlit Cloud
  - Pushes to HuggingFace Spaces

## 📊 Monitor Progress

### Check Workflow Status
1. Go to Actions tab
2. Click on a workflow run
3. View detailed logs

### Download Logs
After each run, check the Summary for:
- Number of industries updated
- Which industries were updated
- Next scheduled download date

## 🔧 Troubleshooting

### If Data Download Fails
1. Check API quota (600 calls/hour limit)
2. Verify network connectivity
3. Check for script errors in logs
4. An issue will be auto-created with details

### If Deployment Fails
1. Check that all secrets are set correctly
2. Verify requirements.txt is complete
3. Ensure no syntax errors in Python files

## 📝 Local Testing

Test workflows locally before pushing:

```bash
# Check schedule
python download_all_industries.py --schedule

# Test download for one industry
python download_all_industries.py --industry '食品工業'

# Force download all
python download_all_industries.py --force
```

## 🔒 Security Notes

- Never commit API keys or tokens directly
- Use GitHub Secrets for sensitive data
- The workflows use `GITHUB_TOKEN` which is automatically provided
- Data files are committed by github-actions[bot]

## 📈 API Quota Management

The FinMind free tier allows 600 calls/hour:
- Each company needs 3 API calls
- Can download ~200 companies per hour
- The script automatically:
  - Tracks progress
  - Pauses when quota is low
  - Can resume from where it stopped

## 🎯 Next Steps

1. Push these workflow files to your repository
2. Add required secrets in GitHub settings
3. Monitor the first scheduled run
4. Check Actions tab for any issues

## 📧 Notifications

To get email notifications:
1. Go to Settings → Notifications
2. Enable "Actions" notifications
3. Choose when to receive emails

---

**Note**: The first run might take longer as it downloads all historical data. Subsequent runs will be faster as they only update with new quarterly data.