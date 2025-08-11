#!/usr/bin/env python3
"""
Unified download script for all Taiwan stock industries from FinMind API
Downloads all available data up to the most recent date (no hard-coded end dates)
"""

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import os
import argparse
import json
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
FINMIND_TOKEN = os.getenv("FINMIND_TOKEN", "")

def get_next_download_date():
    """Calculate when to download based on quarterly reporting schedule
    
    Taiwan quarterly reports are due:
    - Q1 (Mar 31): Data available by May 15
    - Q2 (Jun 30): Data available by Aug 14  
    - Q3 (Sep 30): Data available by Nov 14
    - Q4 (Dec 31): Data available by Mar 31 next year
    """
    today = datetime.now()
    year = today.year
    
    # Define download dates (45 days after quarter end)
    download_dates = [
        (datetime(year, 5, 15), "Q1"),   # Q1 data available
        (datetime(year, 8, 14), "Q2"),   # Q2 data available  
        (datetime(year, 11, 14), "Q3"),  # Q3 data available
        (datetime(year + 1, 3, 31), "Q4") # Q4 data available
    ]
    
    # Find next download date
    for download_date, quarter in download_dates:
        if today < download_date:
            days_until = (download_date - today).days
            return {
                "next_date": download_date.strftime("%Y-%m-%d"),
                "quarter": quarter,
                "days_until": days_until,
                "should_download_now": days_until <= 7  # Download if within a week
            }
    
    # If past all dates this year, return next year's Q1
    return {
        "next_date": datetime(year + 1, 5, 15).strftime("%Y-%m-%d"),
        "quarter": "Q1",
        "days_until": (datetime(year + 1, 5, 15) - today).days,
        "should_download_now": False
    }

def check_last_download(output_dir="finmind_data"):
    """Check when data was last downloaded"""
    last_download_file = f"{output_dir}/.last_download.json"
    
    if os.path.exists(last_download_file):
        try:
            with open(last_download_file, 'r') as f:
                data = json.load(f)
                last_date = datetime.strptime(data['date'], "%Y-%m-%d")
                days_ago = (datetime.now() - last_date).days
                return {
                    "date": data['date'],
                    "days_ago": days_ago,
                    "industries_downloaded": data.get('industries', [])
                }
        except:
            pass
    
    return None

def record_download(industries, output_dir="finmind_data"):
    """Record download completion"""
    last_download_file = f"{output_dir}/.last_download.json"
    
    with open(last_download_file, 'w') as f:
        json.dump({
            'date': datetime.now().strftime("%Y-%m-%d"),
            'industries': industries
        }, f, indent=2)

def check_api_quota():
    """Check remaining API quota"""
    try:
        # Try to import from finmind_tools if available
        from finmind_tools import get_api_quota_info
        quota_info = get_api_quota_info()
        if quota_info:
            return quota_info
    except:
        pass
    
    # Fallback: estimate based on recent requests (simplified)
    return {"remaining": -1, "limit": 600, "minutes_until_reset": 60}

def save_progress(progress_file="download_progress.json"):
    """Save download progress to resume later"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Load existing progress if any
            if os.path.exists(progress_file):
                with open(progress_file, 'r') as f:
                    progress = json.load(f)
            else:
                progress = {}
            
            result = func(*args, **kwargs, progress=progress)
            
            # Save updated progress
            with open(progress_file, 'w') as f:
                json.dump(progress, f, indent=2)
            
            return result
        return wrapper
    return decorator

def get_companies_by_industry(target_industry=None):
    """Dynamically fetch companies from FinMind API by industry category"""
    url = "https://api.finmindtrade.com/api/v4/data"
    params = {
        "dataset": "TaiwanStockInfo",
        "token": FINMIND_TOKEN
    }
    
    try:
        print("🔍 Fetching current company list from FinMind API...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != 200:
            print(f"❌ API Error: {data.get('msg', 'Unknown error')}")
            return {}
            
        # Group companies by industry
        industry_companies = {}
        
        for company in data["data"]:
            industry = company.get("industry_category", "").strip()
            if not industry or industry in ["", "N/A"]:
                continue
                
            if industry not in industry_companies:
                industry_companies[industry] = []
                
            industry_companies[industry].append({
                'stock_id': company["stock_id"],
                'stock_name': company["stock_name"]
            })
        
        # Sort companies within each industry by stock_id
        for industry in industry_companies:
            industry_companies[industry].sort(key=lambda x: x['stock_id'])
        
        print(f"✅ Found {len(industry_companies)} industries")
        
        # If specific industry requested, return only that
        if target_industry:
            if target_industry in industry_companies:
                return {target_industry: industry_companies[target_industry]}
            else:
                print(f"❌ Industry '{target_industry}' not found")
                available = sorted(industry_companies.keys())
                print(f"Available industries: {', '.join(available[:10])}{'...' if len(available) > 10 else ''}")
                return {}
        
        return industry_companies
        
    except Exception as e:
        print(f"❌ Error fetching company data: {e}")
        return {}

def list_available_industries():
    """List all available industries from the API"""
    companies_by_industry = get_companies_by_industry()
    
    if not companies_by_industry:
        print("❌ Could not fetch industry data")
        return
        
    print(f"\n📊 Available Industries ({len(companies_by_industry)} total):")
    print("="*60)
    
    for industry, companies in sorted(companies_by_industry.items()):
        print(f"  {industry:<25} ({len(companies):>3} companies)")
        
    print("\n💡 Use: python download_all_industries.py --industry '食品工業'")
    print("💡 Or:   python download_all_industries.py  (downloads all)")

def get_industry_companies(target_industry=None):
    """Get companies for target industry or all industries"""
    return get_companies_by_industry(target_industry)

def download_financial_data(stock_id, stock_name, industry, start_date="2019-03-31", end_date=None):
    """Download financial data for a stock - gets most recent data if end_date is None"""
    datasets = [
        "TaiwanStockFinancialStatements", 
        "TaiwanStockCashFlowsStatement",
        "TaiwanStockBalanceSheet"
    ]
    
    all_data = []
    
    for dataset in datasets:
        url = "https://api.finmindtrade.com/api/v4/data"
        params = {
            "dataset": dataset,
            "data_id": stock_id,
            "start_date": start_date,
            "token": FINMIND_TOKEN
        }
        
        # Only add end_date if specified (None means get all available data)
        if end_date:
            params["end_date"] = end_date
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == 200 and data["data"]:
                df = pd.DataFrame(data["data"])
                # Add metadata
                df['stock_name'] = stock_name
                df['industry'] = industry
                all_data.append(df)
                print(f"    Downloaded {len(df)} records from {dataset}")
            else:
                print(f"    No data from {dataset}: {data.get('msg', 'Unknown error')}")
                
        except Exception as e:
            print(f"    Error downloading {dataset}: {e}")
        
        time.sleep(0.1)  # Rate limiting
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        return combined_df
    return pd.DataFrame()

def download_industry(industry_name, companies, output_dir="finmind_data"):
    """Download all companies for a specific industry with resume capability"""
    print(f"\n🔄 Downloading {industry_name} industry...")
    print(f"   Total companies: {len(companies)}")
    
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/{industry_name}.csv"
    
    # Check for existing data and get already downloaded companies
    existing_companies = set()
    existing_data = []
    
    if os.path.exists(output_file):
        try:
            existing_df = pd.read_csv(output_file)
            if not existing_df.empty:
                existing_companies = set(existing_df['stock_id'].astype(str).unique())
                existing_data = [existing_df]
                print(f"   📋 Found existing data with {len(existing_companies)} companies")
                print(f"   📊 Existing records: {len(existing_df):,}")
        except Exception as e:
            print(f"   ⚠️  Could not read existing file: {e}")
            existing_companies = set()
            existing_data = []
    
    # Filter out companies that already have data
    companies_to_download = []
    for company in companies:
        if company["stock_id"] not in existing_companies:
            companies_to_download.append(company)
        else:
            print(f"   ⏭️  Skipping {company['stock_name']} ({company['stock_id']}) - already downloaded")
    
    print(f"   🔽 Need to download: {len(companies_to_download)} companies")
    
    if not companies_to_download:
        print(f"   ✅ All companies already downloaded for {industry_name}!")
        return True
    
    all_financial_data = existing_data.copy()  # Start with existing data
    successful_downloads = 0
    
    for i, company in enumerate(companies_to_download, 1):
        stock_id = company["stock_id"]
        stock_name = company["stock_name"]
        
        print(f"  [{i}/{len(companies_to_download)}] Downloading {stock_name} ({stock_id})...")
        
        financial_data = download_financial_data(stock_id, stock_name, industry_name)
        
        if not financial_data.empty:
            all_financial_data.append(financial_data)
            successful_downloads += 1
            print(f"    ✅ Successfully downloaded {len(financial_data)} records")
        else:
            print(f"    ❌ No financial data for {stock_name}")
        
        time.sleep(0.2)  # Rate limiting between companies
    
    # Save combined data (existing + new)
    if all_financial_data:
        combined_df = pd.concat(all_financial_data, ignore_index=True)
        combined_df.to_csv(output_file, index=False, encoding='utf-8')
        
        total_companies = combined_df['stock_id'].nunique()
        previously_downloaded = len(existing_companies)
        newly_downloaded = successful_downloads
        
        print(f"  ✅ {industry_name} completed!")
        print(f"     Previously downloaded: {previously_downloaded} companies")
        print(f"     Newly downloaded: {newly_downloaded} companies")
        print(f"     Total companies: {total_companies} companies")
        print(f"     Total records: {len(combined_df):,}")
        print(f"     Date range: {combined_df['date'].min()} to {combined_df['date'].max()}")
        print(f"     Saved to: {output_file}")
        
        return True
    else:
        print(f"  ❌ No new data downloaded for {industry_name}!")
        return len(existing_companies) > 0  # Return True if we have existing data

def main():
    parser = argparse.ArgumentParser(description='Download Taiwan stock industry data from FinMind')
    parser.add_argument('--industry', type=str, help='Specific industry to download (optional)')
    parser.add_argument('--list', action='store_true', help='List available industries')
    parser.add_argument('--schedule', action='store_true', help='Check download schedule')
    parser.add_argument('--force', action='store_true', help='Force download even if not scheduled')
    args = parser.parse_args()
    
    # Check schedule
    if args.schedule:
        next_download = get_next_download_date()
        last_download = check_last_download()
        
        print("\n📅 Download Schedule Information")
        print("="*60)
        print(f"Today's date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"\nNext scheduled download: {next_download['next_date']} ({next_download['quarter']} data)")
        print(f"Days until next download: {next_download['days_until']} days")
        
        if last_download:
            print(f"\nLast download: {last_download['date']} ({last_download['days_ago']} days ago)")
            print(f"Industries downloaded: {len(last_download['industries_downloaded'])}")
        else:
            print("\nNo previous download record found")
        
        if next_download['should_download_now']:
            print("\n✅ It's time to download new quarterly data!")
            print("Run without --schedule to start downloading")
        else:
            print(f"\n⏰ Check back around {next_download['next_date']}")
            
        return
    
    # Check if it's time to download (unless forced)
    if not args.force and not args.industry:
        next_download = get_next_download_date()
        if not next_download['should_download_now']:
            last_download = check_last_download()
            if last_download and last_download['days_ago'] < 30:
                print(f"\n📊 Data was downloaded {last_download['days_ago']} days ago")
                print(f"Next quarterly update scheduled for: {next_download['next_date']}")
                print("Use --force to download anyway, or --schedule for more info")
                return
    
    if args.list:
        list_available_industries()
        return
    
    if args.industry:
        industry_companies = get_industry_companies(args.industry)
        if industry_companies:
            industry_name = list(industry_companies.keys())[0]
            companies = industry_companies[industry_name]
            download_industry(industry_name, companies)
        else:
            print(f"Use --list to see available industries.")
        return
    
    # Download all industries
    print("🚀 Starting download of all industries...")
    industry_companies = get_industry_companies()
    
    if not industry_companies:
        print("❌ Could not fetch industry data from API")
        return
        
    print(f"📊 Total industries: {len(industry_companies)}")
    
    successful_industries = 0
    failed_industries = []
    
    for industry_name, companies in industry_companies.items():
        try:
            if download_industry(industry_name, companies):
                successful_industries += 1
            else:
                failed_industries.append(industry_name)
        except Exception as e:
            print(f"❌ Error downloading {industry_name}: {e}")
            failed_industries.append(industry_name)
    
    # Summary
    print("\n" + "="*60)
    print("📈 DOWNLOAD SUMMARY")
    print("="*60)
    print(f"✅ Successful: {successful_industries}/{len(industry_companies)} industries")
    if failed_industries:
        print(f"❌ Failed: {', '.join(failed_industries)}")
    print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Record successful download
    if successful_industries > 0:
        successful_list = [ind for ind in industry_companies.keys() if ind not in failed_industries]
        record_download(successful_list)
        
        # Show next scheduled download
        next_download = get_next_download_date()
        print(f"\n📅 Next scheduled download: {next_download['next_date']} ({next_download['quarter']} data)")

if __name__ == "__main__":
    main()