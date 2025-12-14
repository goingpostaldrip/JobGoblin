#!/bin/bash
# Quick start script for email extraction and sending

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  JOB SCRAPER ULTIMATE - Quick Start${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install requirements
echo -e "${YELLOW}Installing requirements...${NC}"
pip install -r requirements.txt > /dev/null 2>&1

# Create output directory
mkdir -p output

echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "Examples:"
echo ""
echo "1. Basic scrape (no email extraction):"
echo "   python cli.py --keywords 'Python Developer' --locations 'New York' --engines duckduckgo,indeed"
echo ""
echo "2. Scrape + Extract Emails:"
echo "   python cli.py --keywords 'Python Developer' --locations 'New York' --engines duckduckgo,indeed --extract-emails"
echo ""
echo "3. Scrape + Extract + Send Emails (max 50/day):"
echo "   python cli.py --keywords 'Python Developer' --locations 'New York' --engines duckduckgo,indeed --extract-emails --send-emails"
echo ""
echo "4. With multiple locations and job boards:"
echo "   python cli.py --keywords 'IT Support,System Admin' --locations 'Chicago,Denver,Boston' --engines duckduckgo,indeed,greenhouse,lever --max-per-query 30 --extract-emails"
echo ""
echo -e "${YELLOW}Setup your email backend first:${NC}"
echo ""
echo "For SendGrid:"
echo "  export SENDGRID_API_KEY='SG.xxxxxxxxxxxxx'"
echo ""
echo "For SMTP (Gmail):"
echo "  export SMTP_HOST='smtp.gmail.com'"
echo "  export SMTP_PORT='587'"
echo "  export SMTP_USER='your@gmail.com'"
echo "  export SMTP_PASSWORD='app_password'"
echo ""
echo -e "${YELLOW}Output files will be saved to:${NC}"
echo "  - output/web_jobs_ultimate.json (all jobs)"
echo "  - output/web_jobs_ultimate.txt (readable summary)"
echo "  - output/found_emails.csv (extracted emails)"
echo ""
