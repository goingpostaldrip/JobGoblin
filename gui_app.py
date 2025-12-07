"""
JOB SCRAPER ULTIMATE - Professional GUI Application
Modern, colorful interface for job scraping and email extraction
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import ttkbootstrap as ttk_boot
from ttkbootstrap.constants import *
import json
import os
import threading
import time
from datetime import datetime
from typing import List, Dict
import sys
import smtplib
import ssl
from email.mime.text import MIMEText

# Import scraper modules
from search_engines import ENGINE_FUNCS
from site_indeed import indeed_search
from site_greenhouse import greenhouse_search
from site_lever import lever_search
from site_simplyhired import simplyhired_search
from normalize import normalize_record, is_relevant
from email_extractor import extract_from_job_results, filter_and_dedupe_emails
from email_manager import EmailManager
from email_sender import EmailSender


class JobScraperGUI:
    """Professional GUI for Job Scraper Ultimate"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("JobGoblin - Lead Finder")
        self.root.geometry("1400x900")
        
        # State variables
        self.scraping = False
        self.results = []
        self.extracted_emails = {}
        self.archive_file = "output/scrape_archive.json"
        
        # Archive selection tracking for email manager
        self.current_archive_entry = None
        self.current_archive_id = None
        self.current_archive_emails = {}
        
        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)
        
        # Initialize archive data (but don't display yet)
        self.archive_data = []
        
        # Build the UI
        self.setup_ui()
        
        # Load archive after UI is built
        self.load_archive()
        
    def setup_ui(self):
        """Setup the main UI layout"""
        
        # Create notebook (tabbed interface)
        self.notebook = ttk_boot.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Tab 1: Scraper
        self.scraper_tab = ttk_boot.Frame(self.notebook)
        self.notebook.add(self.scraper_tab, text="🟢 Job Scraper")
        
        # Tab 2: Archive/History
        self.archive_tab = ttk_boot.Frame(self.notebook)
        self.notebook.add(self.archive_tab, text="🟢 Scrape Archive")
        
        # Tab 3: Email Manager
        self.email_tab = ttk_boot.Frame(self.notebook)
        self.notebook.add(self.email_tab, text="🟢 Email Manager")
        
        # Tab 4: Help & Support
        self.help_tab = ttk_boot.Frame(self.notebook)
        self.notebook.add(self.help_tab, text="🟢 Help & Support")
        
        # Tab 5: Settings
        self.settings_tab = ttk_boot.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="🟢 Settings")
        
        # Setup each tab
        self.setup_scraper_tab()
        self.setup_archive_tab()
        self.setup_email_tab()
        self.setup_help_tab()
        self.setup_settings_tab()
        
    def setup_scraper_tab(self):
        """Setup the main scraper interface"""
        
        # Left panel - Configuration (with scrollbar)
        left_outer = ttk_boot.Frame(self.scraper_tab)
        left_outer.pack(side=LEFT, fill=BOTH, expand=NO, padx=10, pady=10)
        
        # Create scrollable frame
        left_canvas = tk.Canvas(left_outer, bg="white", highlightthickness=0, width=400)
        left_scrollbar = ttk_boot.Scrollbar(left_outer, orient=VERTICAL, command=left_canvas.yview)
        left_panel = ttk_boot.Frame(left_canvas)
        
        left_panel.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )
        
        left_canvas.create_window((0, 0), window=left_panel, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        
        left_canvas.pack(side="left", fill="both", expand=True)
        left_scrollbar.pack(side="right", fill="y")
        
        # Right panel - Results
        right_panel = ttk_boot.Frame(self.scraper_tab)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES, padx=10, pady=10)
        
        # === LEFT PANEL WIDGETS ===
        
        # Keywords section
        keywords_frame = ttk_boot.Labelframe(left_panel, text="🔑 Keywords", bootstyle="primary", padding=10)
        keywords_frame.pack(fill=X, pady=5)
        
        ttk_boot.Label(keywords_frame, text="Enter keywords (comma-separated):").pack(anchor=W)
        self.keywords_entry = ttk_boot.Entry(keywords_frame, width=40)
        self.keywords_entry.pack(fill=X, pady=5)
        self.keywords_entry.insert(0, "Python Developer, Data Scientist")
        
        # Locations section
        locations_frame = ttk_boot.Labelframe(left_panel, text="📍 Locations", bootstyle="info", padding=10)
        locations_frame.pack(fill=X, pady=5)
        
        ttk_boot.Label(locations_frame, text="Enter locations (comma-separated):").pack(anchor=W)
        self.locations_entry = ttk_boot.Entry(locations_frame, width=40)
        self.locations_entry.pack(fill=X, pady=5)
        self.locations_entry.insert(0, "New York, Los Angeles")
        
        # Search Engines section
        engines_frame = ttk_boot.Labelframe(left_panel, text="🌐 Search Engines", bootstyle="success", padding=10)
        engines_frame.pack(fill=X, pady=5)
        
        # Engine checkboxes
        self.engine_vars = {}
        engines_config = [
            ("DuckDuckGo (Free - Working ✓)", "duckduckgo", True),
            ("Startpage (Free - Privacy)", "startpage", False),
            ("SerpAPI (Paid - Requires API Key)", "serpapi", False),
            ("Google CSE (Paid - Requires API Key)", "google_cse", False),
            ("Bing (Paid - Requires API Key)", "bing", False),
        ]
        
        for label, engine, default in engines_config:
            var = tk.BooleanVar(value=default)
            self.engine_vars[engine] = var
            cb = ttk_boot.Checkbutton(engines_frame, text=label, variable=var, bootstyle="success-round-toggle")
            cb.pack(anchor=W, pady=2)
        
        # Select All / Deselect All buttons
        btn_frame = ttk_boot.Frame(engines_frame)
        btn_frame.pack(fill=X, pady=5)
        ttk_boot.Button(btn_frame, text="Select All", command=self.select_all_engines, bootstyle="success-outline", width=12).pack(side=LEFT, padx=2)
        ttk_boot.Button(btn_frame, text="Deselect All", command=self.deselect_all_engines, bootstyle="danger-outline", width=12).pack(side=LEFT, padx=2)
        
        # Options section
        options_frame = ttk_boot.Labelframe(left_panel, text="⚡ Options", bootstyle="warning", padding=10)
        options_frame.pack(fill=X, pady=5)
        
        ttk_boot.Label(options_frame, text="Max results per query:").pack(anchor=W)
        self.max_results = ttk_boot.Scale(options_frame, from_=10, to=100, orient=HORIZONTAL, bootstyle="warning")
        self.max_results.set(25)
        self.max_results.pack(fill=X, pady=5)
        self.max_results_label = ttk_boot.Label(options_frame, text="25")
        self.max_results_label.pack(anchor=W)
        self.max_results.configure(command=self.update_max_results_label)
        
        # Email extraction
        self.extract_emails_var = tk.BooleanVar(value=True)
        ttk_boot.Checkbutton(options_frame, text="Extract contact emails", variable=self.extract_emails_var, bootstyle="info-round-toggle").pack(anchor=W, pady=5)
        
        self.send_emails_var = tk.BooleanVar(value=False)
        ttk_boot.Checkbutton(options_frame, text="Send emails (50/day limit)", variable=self.send_emails_var, bootstyle="danger-round-toggle").pack(anchor=W, pady=5)
        
        # Action buttons
        action_frame = ttk_boot.Frame(left_panel)
        action_frame.pack(fill=X, pady=10)
        
        self.start_btn = ttk_boot.Button(action_frame, text="🚀 Start Scraping", command=self.start_scraping, bootstyle="success", width=20)
        self.start_btn.pack(fill=X, pady=5)
        
        self.stop_btn = ttk_boot.Button(action_frame, text="⛔ Stop", command=self.stop_scraping, bootstyle="danger", width=20, state=DISABLED)
        self.stop_btn.pack(fill=X, pady=5)
        
        ttk_boot.Button(action_frame, text="💾 Save Results", command=self.save_results, bootstyle="info", width=20).pack(fill=X, pady=5)
        
        ttk_boot.Button(action_frame, text="🗑️ Clear Results", command=self.clear_results, bootstyle="warning", width=20).pack(fill=X, pady=5)
        
        # === RIGHT PANEL WIDGETS ===
        
        # Progress section
        progress_frame = ttk_boot.Labelframe(right_panel, text="📊 Progress", bootstyle="primary", padding=10)
        progress_frame.pack(fill=X, pady=5)
        
        self.progress_bar = ttk_boot.Progressbar(progress_frame, mode='indeterminate', bootstyle="success-striped")
        self.progress_bar.pack(fill=X, pady=5)
        
        self.status_label = ttk_boot.Label(progress_frame, text="Ready to scrape", font=("Helvetica", 10, "bold"))
        self.status_label.pack(anchor=W, pady=5)
        
        # Stats section
        stats_frame = ttk_boot.Frame(progress_frame)
        stats_frame.pack(fill=X, pady=5)
        
        self.stats_jobs = ttk_boot.Label(stats_frame, text="Jobs Found: 0", bootstyle="info")
        self.stats_jobs.pack(side=LEFT, padx=10)
        
        self.stats_emails = ttk_boot.Label(stats_frame, text="Emails Found: 0", bootstyle="success")
        self.stats_emails.pack(side=LEFT, padx=10)
        
        self.stats_time = ttk_boot.Label(stats_frame, text="Time: 0s", bootstyle="warning")
        self.stats_time.pack(side=LEFT, padx=10)
        
        # Results section
        results_frame = ttk_boot.Labelframe(right_panel, text="📋 Results", bootstyle="success", padding=10)
        results_frame.pack(fill=BOTH, expand=YES, pady=5)
        
        # Export buttons
        export_btn_frame = ttk_boot.Frame(results_frame)
        export_btn_frame.pack(fill=X, pady=(0, 5))
        
        ttk_boot.Button(export_btn_frame, text="💾 Export to TXT", command=self.export_jobs_to_txt, bootstyle="success-outline").pack(side=LEFT, padx=5)
        ttk_boot.Button(export_btn_frame, text="📧 Email Results", command=self.email_jobs_to_user, bootstyle="info-outline").pack(side=LEFT, padx=5)
        
        # Results text area with scrollbar
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, font=("Courier", 9))
        self.results_text.pack(fill=BOTH, expand=YES)
        
        # Color tags for results
        self.results_text.tag_config("title", foreground="#2E86AB", font=("Courier", 9, "bold"))
        self.results_text.tag_config("url", foreground="#A23B72")
        self.results_text.tag_config("engine", foreground="#F18F01")
        self.results_text.tag_config("email", foreground="#06A77D", font=("Courier", 9, "bold"))
        
    def setup_archive_tab(self):
        """Setup the archive/history viewer"""
        
        # Top controls
        controls_frame = ttk_boot.Frame(self.archive_tab)
        controls_frame.pack(fill=X, padx=10, pady=10)
        
        ttk_boot.Label(controls_frame, text="📁 Scrape Archive - All Past Scrapes", font=("Helvetica", 14, "bold")).pack(side=LEFT, padx=10)
        
        ttk_boot.Button(controls_frame, text="🔄 Refresh", command=self.load_archive, bootstyle="info-outline").pack(side=RIGHT, padx=5)
        ttk_boot.Button(controls_frame, text="🗑️ Clear Archive", command=self.clear_archive, bootstyle="danger-outline").pack(side=RIGHT, padx=5)
        
        # Filter frame
        filter_frame = ttk_boot.Labelframe(self.archive_tab, text="🔍 Filter", bootstyle="primary", padding=10)
        filter_frame.pack(fill=X, padx=10, pady=5)
        
        ttk_boot.Label(filter_frame, text="Search:").pack(side=LEFT, padx=5)
        self.archive_search = ttk_boot.Entry(filter_frame, width=40)
        self.archive_search.pack(side=LEFT, padx=5)
        self.archive_search.bind('<KeyRelease>', lambda e: self.filter_archive())
        
        # Archive list (treeview)
        tree_frame = ttk_boot.Frame(self.archive_tab)
        tree_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Scrollbars
        tree_scroll_y = ttk_boot.Scrollbar(tree_frame, orient=VERTICAL)
        tree_scroll_y.pack(side=RIGHT, fill=Y)
        
        tree_scroll_x = ttk_boot.Scrollbar(tree_frame, orient=HORIZONTAL)
        tree_scroll_x.pack(side=BOTTOM, fill=X)
        
        # Treeview
        self.archive_tree = ttk_boot.Treeview(
            tree_frame,
            columns=("date", "keywords", "locations", "engines", "jobs", "emails"),
            show="tree headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        
        tree_scroll_y.config(command=self.archive_tree.yview)
        tree_scroll_x.config(command=self.archive_tree.xview)
        
        # Configure columns
        self.archive_tree.heading("#0", text="ID")
        self.archive_tree.heading("date", text="Date & Time")
        self.archive_tree.heading("keywords", text="Keywords")
        self.archive_tree.heading("locations", text="Locations")
        self.archive_tree.heading("engines", text="Engines")
        self.archive_tree.heading("jobs", text="Jobs Found")
        self.archive_tree.heading("emails", text="Emails Found")
        
        self.archive_tree.column("#0", width=50)
        self.archive_tree.column("date", width=180)
        self.archive_tree.column("keywords", width=250)
        self.archive_tree.column("locations", width=200)
        self.archive_tree.column("engines", width=200)
        self.archive_tree.column("jobs", width=100)
        self.archive_tree.column("emails", width=100)
        
        self.archive_tree.pack(fill=BOTH, expand=YES)
        
        # Bind double-click to view details
        self.archive_tree.bind("<Double-1>", self.view_archive_details)
        
        # Details panel
        details_frame = ttk_boot.Labelframe(self.archive_tab, text="📝 Details", bootstyle="info", padding=10)
        details_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        self.archive_details = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, font=("Courier", 9), height=10)
        self.archive_details.pack(fill=BOTH, expand=YES)
        
    def setup_email_tab(self):
        """Setup email manager tab"""
        
        # Top section - Archive Selection
        archive_frame = ttk_boot.Labelframe(self.email_tab, text="📂 Select Archive to Extract Emails From", bootstyle="info", padding=15)
        archive_frame.pack(fill=X, padx=10, pady=10)
        
        archive_selection_row = ttk_boot.Frame(archive_frame)
        archive_selection_row.pack(fill=X)
        
        ttk_boot.Label(archive_selection_row, text="Archive:").pack(side=LEFT, padx=5)
        self.archive_dropdown = ttk_boot.Combobox(archive_selection_row, width=50, state="readonly")
        self.archive_dropdown.pack(side=LEFT, padx=5, fill=X, expand=YES)
        
        ttk_boot.Button(archive_selection_row, text="📧 Load Emails from Selected Archive", command=self.load_archive_emails, bootstyle="info", width=30).pack(side=LEFT, padx=5)
        
        # Top section - Stats
        stats_frame = ttk_boot.Labelframe(self.email_tab, text="📊 Email Statistics", bootstyle="primary", padding=15)
        stats_frame.pack(fill=X, padx=10, pady=10)
        
        stats_grid = ttk_boot.Frame(stats_frame)
        stats_grid.pack(fill=X)
        
        self.email_stats_total = ttk_boot.Label(stats_grid, text="Total Emails: 0", font=("Helvetica", 12, "bold"), bootstyle="info")
        self.email_stats_total.grid(row=0, column=0, padx=20, pady=5)
        
        self.email_stats_sent_today = ttk_boot.Label(stats_grid, text="Sent Today: 0/50", font=("Helvetica", 12, "bold"), bootstyle="success")
        self.email_stats_sent_today.grid(row=0, column=1, padx=20, pady=5)
        
        self.email_stats_remaining = ttk_boot.Label(stats_grid, text="Remaining: 50", font=("Helvetica", 12, "bold"), bootstyle="warning")
        self.email_stats_remaining.grid(row=0, column=2, padx=20, pady=5)
        
        # Actions
        actions_frame = ttk_boot.Labelframe(self.email_tab, text="⚡ Actions", bootstyle="success", padding=15)
        actions_frame.pack(fill=X, padx=10, pady=10)
        
        btn_row = ttk_boot.Frame(actions_frame)
        btn_row.pack(fill=X)
        
        ttk_boot.Button(btn_row, text="📧 Send Emails to Contacts", command=self.send_email_from_archive, bootstyle="success", width=25).pack(side=LEFT, padx=5)
        ttk_boot.Button(btn_row, text="📊 View Email CSV", command=self.view_email_csv, bootstyle="info", width=20).pack(side=LEFT, padx=5)
        ttk_boot.Button(btn_row, text="🔄 Refresh Stats", command=self.refresh_email_stats, bootstyle="primary", width=20).pack(side=LEFT, padx=5)
        ttk_boot.Button(btn_row, text="🔓 Reset Daily Limit", command=self.reset_email_limit, bootstyle="warning", width=20).pack(side=LEFT, padx=5)
        
        # Email list
        list_frame = ttk_boot.Labelframe(self.email_tab, text="📋 Extracted Emails from Selected Archive", bootstyle="info", padding=10)
        list_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        self.email_list_text = scrolledtext.ScrolledText(list_frame, wrap=tk.WORD, font=("Courier", 9))
        self.email_list_text.pack(fill=BOTH, expand=YES)
        
        # Initialize current archive entry tracking
        self.current_archive_entry = None
        self.current_archive_id = None
        self.current_archive_emails = {}
        
        # Populate archive dropdown on startup
        self.refresh_archive_dropdown()

    def setup_help_tab(self):
        """Setup help and support tab"""
        # Make the whole help tab scrollable so the send button is always reachable
        outer = ttk_boot.Frame(self.help_tab)
        outer.pack(fill=BOTH, expand=YES)
        canvas = tk.Canvas(outer, highlightthickness=0)
        vscroll = ttk_boot.Scrollbar(outer, orient=VERTICAL, command=canvas.yview)
        inner = ttk_boot.Frame(canvas)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=vscroll.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        vscroll.pack(side=RIGHT, fill=Y)

        # Help content
        help_frame = ttk_boot.Labelframe(inner, text="📖 How to Use", bootstyle="info", padding=15)
        help_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        help_text = scrolledtext.ScrolledText(help_frame, wrap=tk.WORD, font=("Courier", 10), height=12)
        help_text.pack(fill=BOTH, expand=YES)
        help_content = """
Getting Started
- Enter keywords and locations, select engines (DuckDuckGo works free), then click "Start Scraping".
- Results appear on the right; emails are extracted automatically if enabled.

Saving & Archive
- Results auto-save to output/web_jobs_ultimate.json/txt and found_emails.csv.
- Archive tab stores past scrapes; double-click an entry to view details.

Emailing Contacts
- In Settings, enter SendGrid API key or SMTP creds (host/port/user/password).
- Enable "Send emails" when scraping to send up to 50/day (enforced).

API Keys
- Settings tab > API & Email Credentials. Enter keys and click "Save Credentials to .env".

Tips
- Start with fewer keywords; add locations for more targeted results.
- DuckDuckGo is the free, working engine; paid engines need keys.
"""
        help_text.insert(1.0, help_content)
        help_text.config(state=DISABLED)

        # Contact form
        contact_frame = ttk_boot.Labelframe(inner, text="✉️ Contact Support", bootstyle="success", padding=15)
        contact_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        ttk_boot.Label(contact_frame, text="Your Email (reply-to):").pack(anchor=W)
        self.support_from_email = ttk_boot.Entry(contact_frame)
        self.support_from_email.pack(fill=X, pady=4)

        ttk_boot.Label(contact_frame, text="Subject:").pack(anchor=W)
        self.support_subject = ttk_boot.Entry(contact_frame)
        self.support_subject.pack(fill=X, pady=4)

        ttk_boot.Label(contact_frame, text="Message:").pack(anchor=W)
        self.support_message = scrolledtext.ScrolledText(contact_frame, wrap=tk.WORD, height=6)
        self.support_message.pack(fill=X, expand=False, pady=4)

        action_row = ttk_boot.Frame(contact_frame)
        action_row.pack(fill=X, pady=6)
        self.support_status = ttk_boot.Label(action_row, text="", bootstyle="info")
        self.support_status.pack(side=LEFT, padx=4)
        ttk_boot.Button(action_row, text="Send to Support", bootstyle="success", command=self.send_support_message).pack(side=RIGHT)
        
    def setup_settings_tab(self):
        """Setup settings tab"""
        
        # Make settings tab scrollable
        outer_canvas = tk.Canvas(self.settings_tab, highlightthickness=0)
        outer_vscroll = ttk_boot.Scrollbar(self.settings_tab, orient=VERTICAL, command=outer_canvas.yview)
        settings_inner = ttk_boot.Frame(outer_canvas)
        settings_inner.bind("<Configure>", lambda e: outer_canvas.configure(scrollregion=outer_canvas.bbox("all")))
        outer_canvas.create_window((0, 0), window=settings_inner, anchor="nw")
        outer_canvas.configure(yscrollcommand=outer_vscroll.set)
        outer_canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        outer_vscroll.pack(side=RIGHT, fill=Y)
        
        settings_frame = ttk_boot.Labelframe(settings_inner, text="⚙️ Application Settings", bootstyle="primary", padding=20)
        settings_frame.pack(fill=BOTH, expand=NO, padx=10, pady=10)
        
        # Output directory
        ttk_boot.Label(settings_frame, text="Output Directory:", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=5)
        
        dir_frame = ttk_boot.Frame(settings_frame)
        dir_frame.pack(fill=X, pady=5)
        
        self.output_dir = ttk_boot.Entry(dir_frame)
        self.output_dir.insert(0, "output")
        self.output_dir.pack(side=LEFT, fill=X, expand=YES, padx=(0, 5))
        
        ttk_boot.Button(dir_frame, text="Browse", command=self.browse_output_dir, bootstyle="info-outline").pack(side=RIGHT)
        
        # ===== COMPREHENSIVE INSTRUCTIONS =====
        ttk_boot.Label(settings_inner, text="📋 HOW TO GET API KEYS & CREDENTIALS", font=("Helvetica", 12, "bold"), bootstyle="success").pack(anchor=W, padx=10, pady=(20, 10))
        
        instructions_frame = ttk_boot.Labelframe(settings_inner, text="Step-by-Step Instructions", bootstyle="info", padding=15)
        instructions_frame.pack(fill=BOTH, expand=NO, padx=10, pady=10)
        
        instructions_text = scrolledtext.ScrolledText(instructions_frame, wrap=tk.WORD, height=18, font=("Courier", 9))
        instructions_text.pack(fill=BOTH, expand=YES)
        
        instructions = """
🔍 GOOGLE API + CUSTOM SEARCH ENGINE (CSE)
1. Go to cse.google.com - Create a new Custom Search Engine
2. Go to console.cloud.google.com > Create a new project
3. Enable "Custom Search API" in APIs & Services
4. Create an API key in "Credentials" section
5. Copy both: GOOGLE_API_KEY and GOOGLE_CSE_ID from CSE settings
6. Enter below in the credential fields

🔎 BING SEARCH API
1. Go to portal.azure.com - Create a new resource
2. Search for "Bing Search v7"
3. Create the resource and copy the API Key
4. Enter as BING_API_KEY below

🔗 SERPAPI (Google Search API)
1. Go to serpapi.com - Sign up for free account
2. Get your API key from dashboard
3. Enter as SERPAPI_KEY below

📧 SENDGRID (Email Sending)
1. Go to sendgrid.com - Create free account
2. Go to Settings > API Keys > Create API Key
3. Use Full Access or Mail Send scope
4. Enter as SENDGRID_API_KEY below (format: SG.xxxxx)

📧 GMAIL SMTP (Alternative to SendGrid)
1. Enable 2-Step Verification on your Google Account
2. Go to myaccount.google.com > Security > App passwords
3. Select "Mail" and "Windows Computer" (or your device)
4. Google generates an App Password (16 characters)
5. Use these settings:
   - SMTP_HOST: smtp.gmail.com
   - SMTP_PORT: 587
   - SMTP_USER: your@gmail.com
   - SMTP_PASSWORD: (the 16-char app password Google generated)
"""
        instructions_text.insert(1.0, instructions)
        instructions_text.config(state=DISABLED)        # Editable API credentials (scrollable)
        creds_outer = ttk_boot.Labelframe(self.settings_tab, text="🔑 API & Email Credentials (writes to .env)", bootstyle="success", padding=10)
        creds_outer.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        canvas = tk.Canvas(creds_outer, height=260, highlightthickness=0)
        vscroll = ttk_boot.Scrollbar(creds_outer, orient=VERTICAL, command=canvas.yview)
        creds_frame = ttk_boot.Frame(canvas)
        creds_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=creds_frame, anchor="nw")
        canvas.configure(yscrollcommand=vscroll.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        vscroll.pack(side=RIGHT, fill=Y)

        self.env_entries = {}
        fields = [
            ("Google API Key", "GOOGLE_API_KEY"),
            ("Google CSE ID", "GOOGLE_CSE_ID"),
            ("Bing API Key", "BING_API_KEY"),
            ("SerpAPI Key", "SERPAPI_KEY"),
            ("SendGrid API Key", "SENDGRID_API_KEY"),
            ("SMTP Host", "SMTP_HOST"),
            ("SMTP Port", "SMTP_PORT"),
            ("SMTP User", "SMTP_USER"),
            ("SMTP Password / App Password", "SMTP_PASSWORD"),
        ]

        for label_text, key in fields:
            row = ttk_boot.Frame(creds_frame)
            row.pack(fill=X, pady=4)
            ttk_boot.Label(row, text=label_text, width=30, anchor=W).pack(side=LEFT, padx=(0,5))
            ent = ttk_boot.Entry(row)
            ent.pack(side=LEFT, fill=X, expand=YES)
            self.env_entries[key] = ent

        ttk_boot.Button(creds_frame, text="💾 Save Credentials to .env", bootstyle="success", command=self.save_env_settings).pack(anchor=E, pady=10)

        # Load existing .env values into fields
        self.load_env_settings()
        
        # About section
        about_frame = ttk_boot.Labelframe(self.settings_tab, text="ℹ️ About", bootstyle="info", padding=20)
        about_frame.pack(fill=X, padx=10, pady=10)
        
        ttk_boot.Label(about_frame, text="JobGoblin - Lead Finder", font=("Helvetica", 14, "bold"), foreground="#00AA00").pack(pady=5)
        ttk_boot.Label(about_frame, text="🟢 Created by NERDY BIRD IT 🟢", font=("Helvetica", 11, "bold"), foreground="#00DD00").pack(pady=3)
        ttk_boot.Label(about_frame, text="📧 nerdybirdit@gmail.com", font=("Helvetica", 10), foreground="#00FF00").pack(pady=2)
        ttk_boot.Label(about_frame, text="📱 WhatsApp: +1 (412) 773-4245", font=("Helvetica", 10), foreground="#00FF00").pack(pady=2)
        ttk_boot.Label(about_frame, text="Version 2.0 - December 2025", foreground="#00AA00").pack(pady=2)
        ttk_boot.Label(about_frame, text="Professional job scraping and email campaign tool", foreground="#00CC00").pack(pady=2)
        
    # === HELPER METHODS ===
    
    def update_max_results_label(self, value):
        """Update the max results label"""
        self.max_results_label.config(text=str(int(float(value))))

    def send_support_message(self):
        """Send support email to developer"""
        from_email = self.support_from_email.get().strip()
        subject = self.support_subject.get().strip() or "Support Request"
        body = self.support_message.get(1.0, tk.END).strip()

        if not from_email or not body:
            messagebox.showerror("Missing Info", "Please enter your email and a message.")
            return

        self.support_status.config(text="Sending...", bootstyle="info")
        self.root.update_idletasks()

        # Recipient fixed
        to_email = "nerdybirdit@gmail.com"

        # Try SendGrid first
        sg_key = os.getenv("SENDGRID_API_KEY")
        sent = False
        error_msg = ""
        if sg_key:
            try:
                import sendgrid
                from sendgrid.helpers.mail import Mail
                sg = sendgrid.SendGridAPIClient(api_key=sg_key)
                mail = Mail(
                    from_email=from_email,
                    to_emails=to_email,
                    subject=subject,
                    plain_text_content=body,
                )
                resp = sg.send(mail)
                if resp.status_code < 300:
                    sent = True
            except Exception as e:
                error_msg = f"SendGrid error: {e}"

        # Fallback to SMTP
        if not sent:
            host = os.getenv("SMTP_HOST", "")
            port = int(os.getenv("SMTP_PORT", "587") or 587)
            user = os.getenv("SMTP_USER", "")
            pwd = os.getenv("SMTP_PASSWORD", "")
            if host and user and pwd:
                try:
                    msg = MIMEText(body)
                    msg["Subject"] = subject
                    msg["From"] = from_email
                    msg["To"] = to_email
                    ctx = ssl.create_default_context()
                    with smtplib.SMTP(host, port, timeout=20) as server:
                        server.starttls(context=ctx)
                        server.login(user, pwd)
                        server.sendmail(from_email, [to_email], msg.as_string())
                    sent = True
                except Exception as e:
                    error_msg = f"SMTP error: {e}"
            else:
                error_msg = "No SendGrid or SMTP credentials configured."

        if sent:
            self.support_status.config(text="Sent!", bootstyle="success")
            messagebox.showinfo("Sent", "Your message was sent to support.")
            self.support_message.delete(1.0, tk.END)
        else:
            self.support_status.config(text="Failed", bootstyle="danger")
            messagebox.showerror("Send Failed", error_msg or "Could not send message.")

    def load_env_settings(self):
        """Load .env values into the settings form"""
        env_path = ".env"
        if not os.path.exists(env_path):
            return
        try:
            data = {}
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    data[k.strip()] = v.strip()
            for key, entry in self.env_entries.items():
                if key in data:
                    entry.delete(0, tk.END)
                    entry.insert(0, data[key])
        except Exception as e:
            messagebox.showwarning("Env Load", f"Could not load .env: {e}")

    def save_env_settings(self):
        """Persist API/email credentials to .env"""
        env_path = ".env"
        env_data = {}

        # Load existing values
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        env_data[k.strip()] = v.strip()
            except Exception:
                pass

        # Update with form values
        for key, entry in self.env_entries.items():
            val = entry.get().strip()
            if val:
                env_data[key] = val
            elif key in env_data:
                # Remove empty fields from file
                env_data.pop(key, None)

        # Write back
        try:
            with open(env_path, "w", encoding="utf-8") as f:
                f.write("# Auto-generated by GUI settings\n")
                for k, v in env_data.items():
                    f.write(f"{k}={v}\n")
            messagebox.showinfo("Saved", ".env updated successfully")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not write .env: {e}")
    
    def select_all_engines(self):
        """Select all search engines"""
        for var in self.engine_vars.values():
            var.set(True)
    
    def deselect_all_engines(self):
        """Deselect all search engines"""
        for var in self.engine_vars.values():
            var.set(False)
    
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.delete(0, tk.END)
            self.output_dir.insert(0, directory)
    
    def start_scraping(self):
        """Start the scraping process in a background thread"""
        
        # Validate inputs
        keywords = self.keywords_entry.get().strip()
        if not keywords:
            messagebox.showerror("Error", "Please enter at least one keyword")
            return
        
        # Get selected engines
        selected_engines = [engine for engine, var in self.engine_vars.items() if var.get()]
        if not selected_engines:
            messagebox.showerror("Error", "Please select at least one search engine")
            return
        
        # Update UI state
        self.scraping = True
        self.start_btn.config(state=DISABLED)
        self.stop_btn.config(state=NORMAL)
        self.progress_bar.start()
        self.status_label.config(text="🔍 Scraping in progress...")
        self.clear_results()
        
        # Start scraping in background thread
        thread = threading.Thread(target=self.run_scraper, daemon=True)
        thread.start()
    
    def run_scraper(self):
        """Run the actual scraping process"""
        start_time = time.time()
        
        try:
            # Get parameters
            keywords = [k.strip() for k in self.keywords_entry.get().split(',') if k.strip()]
            locations = [l.strip() for l in self.locations_entry.get().split(',') if l.strip()]
            engines = [engine for engine, var in self.engine_vars.items() if var.get()]
            max_per_query = int(self.max_results.get())
            extract_emails = self.extract_emails_var.get()
            send_emails = self.send_emails_var.get()
            
            self.results = []
            
            # Expand queries
            queries = []
            for kw in keywords:
                if locations:
                    for loc in locations:
                        queries.append(f"{kw} {loc}")
                else:
                    queries.append(kw)
            
            self.update_status(f"Running {len(queries)} queries across {len(engines)} engines...")
            
            # Web engines
            WEB_ENGINES = {"duckduckgo", "google_cse", "bing", "serpapi", "linkedin", "glassdoor", "ziprecruiter"}
            SITE_ENGINES = {"indeed", "greenhouse", "lever", "simplyhired"}
            
            # Run web engines
            for idx, query in enumerate(queries, 1):
                if not self.scraping:
                    break
                    
                for eng in engines:
                    if not self.scraping:
                        break
                        
                    if eng in WEB_ENGINES:
                        self.update_status(f"[{idx}/{len(queries)}] Querying {eng}: {query}")
                        
                        # Handle site-filtered engines
                        if eng in ("linkedin", "glassdoor", "ziprecruiter"):
                            site_map = {
                                "linkedin": "site:linkedin.com/jobs ",
                                "glassdoor": "site:glassdoor.com/Job ",
                                "ziprecruiter": "site:ziprecruiter.com/jobs "
                            }
                            if "serpapi" in ENGINE_FUNCS:
                                fn = ENGINE_FUNCS["serpapi"]
                                modified_query = site_map[eng] + query
                                results = fn(modified_query, max_results=max_per_query, verbose=False)
                            else:
                                continue
                        else:
                            fn = ENGINE_FUNCS.get(eng)
                            if fn:
                                results = fn(query, max_results=max_per_query, verbose=False)
                            else:
                                continue
                        
                        filtered = [normalize_record(r) for r in results if is_relevant(r.get("title", ""), r.get("snippet", ""), keywords, 1.0)]
                        self.results.extend(filtered)
                        self.update_stats(len(self.results), 0, int(time.time() - start_time))
                        
                        time.sleep(1.2)  # Throttle
            
            # Run site engines
            for eng in engines:
                if not self.scraping:
                    break
                    
                if eng in SITE_ENGINES:
                    for kw in keywords:
                        if not self.scraping:
                            break
                            
                        locs = locations if locations else [""]
                        for loc in locs:
                            if not self.scraping:
                                break
                                
                            self.update_status(f"[site] {eng} kw='{kw}' loc='{loc}'")
                            
                            if eng == "indeed":
                                results = indeed_search(kw, loc, max_results=max_per_query, verbose=False)
                            elif eng == "greenhouse":
                                results = greenhouse_search(kw, loc, max_results=max_per_query, verbose=False)
                            elif eng == "lever":
                                results = lever_search(kw, loc, max_results=max_per_query, verbose=False)
                            elif eng == "simplyhired":
                                results = simplyhired_search(kw, loc, max_results=max_per_query, verbose=False)
                            else:
                                results = []
                            
                            filtered = [normalize_record(r) for r in results if is_relevant(r.get("title", ""), r.get("snippet", ""), keywords, 1.0)]
                            self.results.extend(filtered)
                            self.update_stats(len(self.results), 0, int(time.time() - start_time))
                            
                            time.sleep(1.2)
            
            # Dedupe
            seen = set()
            unique_results = []
            for r in self.results:
                url = r.get('url')
                if url and url not in seen:
                    seen.add(url)
                    unique_results.append(r)
            self.results = unique_results
            
            # Extract emails
            if extract_emails and self.scraping:
                self.update_status(f"📧 Extracting emails from {len(self.results)} job postings...")
                company_emails = extract_from_job_results(self.results, verbose=False)
                self.extracted_emails = filter_and_dedupe_emails(company_emails)
                self.update_stats(len(self.results), len(self.extracted_emails), int(time.time() - start_time))
                
                # Save emails to CSV
                email_mgr = EmailManager("output", verbose=False)
                email_mgr.export_emails_to_csv(self.extracted_emails, "output/found_emails.csv")
            
            # Display results
            self.display_results()
            
            # Save to archive
            self.save_to_archive(keywords, locations, engines, len(self.results), len(self.extracted_emails))
            
            # Save outputs
            self.auto_save_results()
            
            # Send emails if requested
            if send_emails and self.extracted_emails and self.scraping:
                self.update_status("📧 Sending emails...")
                sender = EmailSender(verbose=False)
                stats = sender.send_emails_from_csv("output/found_emails.csv", limit_per_run=50)
                messagebox.showinfo("Email Sending", f"Sent: {stats['sent']}\nFailed: {stats['failed']}\nSkipped: {stats['skipped']}")
            
            self.update_status("✅ Scraping completed successfully!")
            
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Scraping Error", f"An error occurred:\n{str(e)}")
        
        finally:
            self.root.after(0, self.scraping_finished)
    
    def stop_scraping(self):
        """Stop the scraping process"""
        self.scraping = False
        self.update_status("⛔ Stopping...")
    
    def scraping_finished(self):
        """Called when scraping is finished"""
        self.scraping = False
        self.start_btn.config(state=NORMAL)
        self.stop_btn.config(state=DISABLED)
        self.progress_bar.stop()
    
    def update_status(self, message):
        """Update status label (thread-safe)"""
        self.root.after(0, lambda: self.status_label.config(text=message))
    
    def update_stats(self, jobs, emails, elapsed):
        """Update statistics display (thread-safe)"""
        self.root.after(0, lambda: self.stats_jobs.config(text=f"Jobs Found: {jobs}"))
        self.root.after(0, lambda: self.stats_emails.config(text=f"Emails Found: {emails}"))
        self.root.after(0, lambda: self.stats_time.config(text=f"Time: {elapsed}s"))
    
    def display_results(self):
        """Display scraping results in the text area"""
        self.root.after(0, self._display_results_ui)
    
    def _display_results_ui(self):
        """Update UI with results (must run in main thread)"""
        self.results_text.delete(1.0, tk.END)
        
        if not self.results:
            self.results_text.insert(tk.END, "No results found.\n")
            return
        
        for idx, result in enumerate(self.results, 1):
            self.results_text.insert(tk.END, f"\n{'='*80}\n")
            self.results_text.insert(tk.END, f"[{idx}] ")
            self.results_text.insert(tk.END, f"{result.get('title', 'No Title')}\n", "title")
            self.results_text.insert(tk.END, f"🔗 URL: {result.get('url', 'N/A')}\n", "url")
            self.results_text.insert(tk.END, f"🔍 Engine: {result.get('engine', 'N/A')}\n", "engine")
            if result.get('snippet'):
                self.results_text.insert(tk.END, f"📝 {result['snippet'][:200]}...\n")
        
        if self.extracted_emails:
            self.results_text.insert(tk.END, f"\n\n{'='*80}\n")
            self.results_text.insert(tk.END, "📧 EXTRACTED EMAILS\n", "email")
            self.results_text.insert(tk.END, f"{'='*80}\n")
            
            for idx, (email, info) in enumerate(self.extracted_emails.items(), 1):
                domains = ', '.join(list(info.get('domains', []))[:3])
                self.results_text.insert(tk.END, f"\n[{idx}] ", "email")
                self.results_text.insert(tk.END, f"{email}\n", "email")
                self.results_text.insert(tk.END, f"    Domains: {domains}\n")
                self.results_text.insert(tk.END, f"    Sources: {len(info.get('sources', []))}\n")
    
    def clear_results(self):
        """Clear results display"""
        self.results_text.delete(1.0, tk.END)
        self.results = []
        self.extracted_emails = {}
        self.update_stats(0, 0, 0)
    
    def save_results(self):
        """Save results to files"""
        if not self.results:
            messagebox.showinfo("Save Results", "No results to save")
            return
        
        try:
            self.auto_save_results()
            messagebox.showinfo("Save Results", f"Saved {len(self.results)} jobs to:\n\n- output/web_jobs_ultimate.json\n- output/web_jobs_ultimate.txt\n- output/found_emails.csv")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save results:\n{str(e)}")
    
    def auto_save_results(self):
        """Automatically save results with timestamped files"""
        os.makedirs("output", exist_ok=True)
        
        # Create timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON
        with open("output/web_jobs_ultimate.json", 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        # Save TXT (main file)
        lines = []
        for r in self.results:
            lines.append(f"{r.get('title','')} | {r.get('url','')} | {r.get('engine','')}")
        
        with open("output/web_jobs_ultimate.txt", 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        # Save timestamped TXT file for this scrape (organized by date/time)
        timestamped_filename = f"output/scrape_{timestamp}.txt"
        with open(timestamped_filename, 'w', encoding='utf-8') as f:
            f.write(f"JobGoblin - Scraped Results\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Jobs: {len(self.results)}\n")
            f.write(f"Total Emails: {len(self.extracted_emails)}\n")
            f.write("="*80 + "\n\n")
            
            for idx, job in enumerate(self.results, 1):
                f.write(f"[{idx}] {job.get('title', 'No Title')}\n")
                f.write(f"URL: {job.get('url', 'N/A')}\n")
                f.write(f"Engine: {job.get('engine', 'N/A')}\n")
                if job.get('snippet'):
                    f.write(f"Description: {job['snippet']}\n")
                f.write("\n" + "-"*80 + "\n\n")
            
            # Add emails section if extracted
            if self.extracted_emails:
                f.write("\n" + "="*80 + "\n")
                f.write("EXTRACTED EMAILS\n")
                f.write("="*80 + "\n\n")
                for idx, (email, info) in enumerate(self.extracted_emails.items(), 1):
                    domains = ', '.join(list(info.get('domains', []))[:3])
                    f.write(f"[{idx}] {email}\n")
                    f.write(f"    Domains: {domains}\n")
                    f.write(f"    Sources: {len(info.get('sources', []))}\n\n")
        
        self.update_status(f"✅ Saved timestamped results to: {timestamped_filename}")
    
    def export_jobs_to_txt(self):
        """Export scraped jobs to a custom TXT file"""
        if not self.results:
            messagebox.showwarning("No Results", "No jobs to export. Please run a scrape first.")
            return
        
        # Ask user for filename
        filename = filedialog.asksaveasfilename(
            title="Save Jobs As",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"job_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"JobGoblin - Scraped Job Results\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Jobs: {len(self.results)}\n")
                f.write("="*80 + "\n\n")
                
                for idx, job in enumerate(self.results, 1):
                    f.write(f"[{idx}] {job.get('title', 'No Title')}\n")
                    f.write(f"URL: {job.get('url', 'N/A')}\n")
                    f.write(f"Engine: {job.get('engine', 'N/A')}\n")
                    if job.get('snippet'):
                        f.write(f"Description: {job['snippet']}\n")
                    f.write("\n" + "-"*80 + "\n\n")
            
            messagebox.showinfo("Export Successful", f"Exported {len(self.results)} jobs to:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export jobs:\n{str(e)}")
    
    def email_jobs_to_user(self):
        """Email scraped jobs to a user-specified email address"""
        if not self.results:
            messagebox.showwarning("No Results", "No jobs to email. Please run a scrape first.")
            return
        
        # Create dialog for email input
        dialog = tk.Toplevel(self.root)
        dialog.title("Email Job Results")
        dialog.geometry("500x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"500x250+{x}+{y}")
        
        ttk_boot.Label(dialog, text="📧 Send Job Results via Email", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        # Recipient email
        ttk_boot.Label(dialog, text="Recipient Email:").pack(anchor=W, padx=20, pady=(10, 0))
        recipient_entry = ttk_boot.Entry(dialog, width=50)
        recipient_entry.pack(padx=20, pady=5)
        
        # Subject
        ttk_boot.Label(dialog, text="Subject:").pack(anchor=W, padx=20, pady=(10, 0))
        subject_entry = ttk_boot.Entry(dialog, width=50)
        subject_entry.insert(0, f"JobGoblin Results - {len(self.results)} Jobs Found")
        subject_entry.pack(padx=20, pady=5)
        
        def send_email():
            recipient = recipient_entry.get().strip()
            subject = subject_entry.get().strip()
            
            if not recipient:
                messagebox.showerror("Error", "Please enter a recipient email address")
                return
            
            # Validate email format (basic)
            if '@' not in recipient or '.' not in recipient.split('@')[1]:
                messagebox.showerror("Error", "Please enter a valid email address")
                return
            
            try:
                dialog.destroy()
                
                # Create email body
                body = f"""JobGoblin - Scraped Job Results
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Jobs: {len(self.results)}

{'='*80}\n\n"""
                
                for idx, job in enumerate(self.results, 1):
                    body += f"[{idx}] {job.get('title', 'No Title')}\n"
                    body += f"URL: {job.get('url', 'N/A')}\n"
                    body += f"Engine: {job.get('engine', 'N/A')}\n"
                    if job.get('snippet'):
                        body += f"Description: {job['snippet'][:200]}...\n"
                    body += "\n" + "-"*80 + "\n\n"
                
                # Try SendGrid first, then SMTP
                try:
                    from sendgrid import SendGridAPIClient
                    from sendgrid.helpers.mail import Mail
                    
                    sendgrid_key = os.getenv('SENDGRID_API_KEY')
                    from_email = os.getenv('FROM_EMAIL', 'nerdybirdit@gmail.com')
                    
                    if sendgrid_key:
                        message = Mail(
                            from_email=from_email,
                            to_emails=recipient,
                            subject=subject,
                            plain_text_content=body
                        )
                        sg = SendGridAPIClient(sendgrid_key)
                        response = sg.send(message)
                        messagebox.showinfo("Email Sent", f"Job results sent successfully to {recipient}!")
                        return
                except Exception as sg_error:
                    pass  # Fall through to SMTP
                
                # Fallback to SMTP
                smtp_user = os.getenv('SMTP_USER')
                smtp_pass = os.getenv('SMTP_PASS')
                smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
                smtp_port = int(os.getenv('SMTP_PORT', '587'))
                
                if not smtp_user or not smtp_pass:
                    messagebox.showerror("Email Error", 
                        "Email credentials not configured.\n\n"
                        "Please set up SendGrid API or SMTP credentials in Settings tab.")
                    return
                
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = smtp_user
                msg['To'] = recipient
                
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls(context=context)
                    server.login(smtp_user, smtp_pass)
                    server.send_message(msg)
                
                messagebox.showinfo("Email Sent", f"Job results sent successfully to {recipient}!")
            
            except Exception as e:
                messagebox.showerror("Email Error", f"Failed to send email:\n{str(e)}")
        
        # Buttons
        btn_frame = ttk_boot.Frame(dialog)
        btn_frame.pack(pady=20)
        
        send_btn = ttk_boot.Button(btn_frame, text="Send Email", command=send_email, bootstyle="success", width=15)
        send_btn.pack(side=LEFT, padx=10)
        
        cancel_btn = ttk_boot.Button(btn_frame, text="Cancel", command=dialog.destroy, bootstyle="danger", width=15)
        cancel_btn.pack(side=LEFT, padx=10)
    
    def load_archive(self):
        """Load scrape archive from file"""
        if os.path.exists(self.archive_file):
            try:
                with open(self.archive_file, 'r', encoding='utf-8') as f:
                    self.archive_data = json.load(f)
            except:
                self.archive_data = []
        else:
            self.archive_data = []
        
        self.refresh_archive_display()
        self.refresh_archive_dropdown()
    
    def save_to_archive(self, keywords, locations, engines, jobs_count, emails_count):
        """Save current scrape to archive"""
        # Convert sets to lists for JSON serialization
        serializable_emails = {}
        for email, info in self.extracted_emails.items():
            serializable_emails[email] = {
                'email': email,
                'domains': list(info.get('domains', [])),  # Convert set to list
                'sources': list(info.get('sources', [])),
                'job_titles': list(info.get('job_titles', []))  # Convert set to list
            }
        
        entry = {
            'id': len(self.archive_data) + 1,
            'timestamp': datetime.now().isoformat(),
            'keywords': keywords,
            'locations': locations,
            'engines': engines,
            'jobs_found': jobs_count,
            'emails_found': emails_count,
            'results': self.results[:100],
            'extracted_emails': serializable_emails,
            'all_results': self.results
        }
        
        self.archive_data.append(entry)
        
        # Save to file
        with open(self.archive_file, 'w', encoding='utf-8') as f:
            json.dump(self.archive_data, f, indent=2)
        
        self.refresh_archive_display()
        self.refresh_archive_dropdown()
    
    def refresh_archive_display(self):
        """Refresh the archive treeview"""
        # Clear existing items
        for item in self.archive_tree.get_children():
            self.archive_tree.delete(item)
        
        # Add archive entries
        for entry in reversed(self.archive_data):  # Most recent first
            self.archive_tree.insert(
                "",
                tk.END,
                text=entry['id'],
                values=(
                    datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M:%S"),
                    ', '.join(entry.get('keywords', [])),
                    ', '.join(entry.get('locations', []))[:50],
                    ', '.join(entry.get('engines', []))[:50],
                    entry.get('jobs_found', 0),
                    entry.get('emails_found', 0)
                )
            )
    
    def filter_archive(self):
        """Filter archive based on search term"""
        search_term = self.archive_search.get().lower()
        
        # Clear existing items
        for item in self.archive_tree.get_children():
            self.archive_tree.delete(item)
        
        # Add filtered entries
        for entry in reversed(self.archive_data):
            # Search in keywords, locations, and engines
            searchable = ' '.join(entry.get('keywords', []) + entry.get('locations', []) + entry.get('engines', [])).lower()
            
            if search_term in searchable or not search_term:
                self.archive_tree.insert(
                    "",
                    tk.END,
                    text=entry['id'],
                    values=(
                        datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M:%S"),
                        ', '.join(entry.get('keywords', [])),
                        ', '.join(entry.get('locations', []))[:50],
                        ', '.join(entry.get('engines', []))[:50],
                        entry.get('jobs_found', 0),
                        entry.get('emails_found', 0)
                    )
                )
    
    def view_archive_details(self, event):
        """View details of selected archive entry"""
        selection = self.archive_tree.selection()
        if not selection:
            return
        
        item = self.archive_tree.item(selection[0])
        entry_id = int(item['text'])
        
        # Find entry in archive
        entry = next((e for e in self.archive_data if e['id'] == entry_id), None)
        if not entry:
            return
        
        # Store current archive entry for email manager to use
        self.current_archive_entry = entry
        self.current_archive_id = entry_id
        
        # Display details
        self.archive_details.delete(1.0, tk.END)
        
        details = f"""
{'='*80}
SCRAPE DETAILS - ID: {entry['id']}
{'='*80}

Date & Time: {datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M:%S")}
Keywords: {', '.join(entry.get('keywords', []))}
Locations: {', '.join(entry.get('locations', []))}
Engines: {', '.join(entry.get('engines', []))}
Jobs Found: {entry.get('jobs_found', 0)}
Emails Found: {entry.get('emails_found', 0)}

{'='*80}
ALL JOB LINKS & TITLES:
{'='*80}

"""
        self.archive_details.insert(tk.END, details)
        
        # Show all results with links and titles
        all_results = entry.get('all_results', entry.get('results', []))
        for idx, result in enumerate(all_results, 1):
            result_text = f"[{idx}] {result.get('title', 'No Title')}\n    🔗 {result.get('url', 'N/A')}\n    Engine: {result.get('engine', 'N/A')}\n\n"
            self.archive_details.insert(tk.END, result_text)
        
        # Add extracted emails section if emails were found
        if entry.get('emails_found', 0) > 0 and entry.get('extracted_emails'):
            self.archive_details.insert(tk.END, f"\n{'='*80}\nEXTRACTED EMAILS (ALL):\n{'='*80}\n\n")
            
            emails = entry.get('extracted_emails', {})
            for idx, (email, info) in enumerate(list(emails.items()), 1):
                domains = ', '.join(list(info.get('domains', []))[:3])
                email_text = f"[{idx}] {email}\n    Domains: {domains}\n    Sources: {len(info.get('sources', []))}\n\n"
                self.archive_details.insert(tk.END, email_text)
        elif entry.get('emails_found', 0) == 0:
            self.archive_details.insert(tk.END, f"\n{'='*80}\nNO EMAILS FOUND\n{'='*80}\n")

    
    def clear_archive(self):
        """Clear the entire archive"""
        if messagebox.askyesno("Clear Archive", "Are you sure you want to clear all archive data?"):
            self.archive_data = []
            if os.path.exists(self.archive_file):
                os.remove(self.archive_file)
            self.refresh_archive_display()
            self.archive_details.delete(1.0, tk.END)
            messagebox.showinfo("Archive Cleared", "Archive has been cleared")
    
    def send_emails_action(self):
        """Send emails from the email tab"""
        if not os.path.exists("output/found_emails.csv"):
            messagebox.showinfo("No Emails", "No emails found. Run a scrape with email extraction first.")
            return
        
        if messagebox.askyesno("Send Emails", "Send emails to extracted contacts?\n\nMaximum 50 emails per day will be sent."):
            try:
                sender = EmailSender(verbose=True)
                stats = sender.send_emails_from_csv("output/found_emails.csv", limit_per_run=50)
                messagebox.showinfo("Email Sending Complete", f"Sent: {stats['sent']}\nFailed: {stats['failed']}\nSkipped: {stats['skipped']}")
                self.refresh_email_stats()
            except Exception as e:
                messagebox.showerror("Email Error", f"Failed to send emails:\n{str(e)}")
    
    def view_email_csv(self):
        """View the emails CSV file"""
        csv_file = "output/found_emails.csv"
        if not os.path.exists(csv_file):
            messagebox.showinfo("No CSV", "No emails CSV found. Run a scrape with email extraction first.")
            return
        
        self.email_list_text.delete(1.0, tk.END)
        
        try:
            import csv
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.email_list_text.insert(tk.END, "📧 EXTRACTED EMAILS FROM CSV\n")
                self.email_list_text.insert(tk.END, "="*80 + "\n\n")
                
                for idx, row in enumerate(reader, 1):
                    self.email_list_text.insert(tk.END, f"[{idx}] {row.get('email', '')}\n")
                    self.email_list_text.insert(tk.END, f"    Domains: {row.get('domains', '')}\n")
                    self.email_list_text.insert(tk.END, f"    Job Titles: {row.get('job_titles', '')}\n")
                    self.email_list_text.insert(tk.END, f"    First Seen: {row.get('first_seen', '')}\n\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV:\n{str(e)}")
    
    def refresh_email_stats(self):
        """Refresh email statistics"""
        try:
            # Count emails in CSV
            email_count = 0
            if os.path.exists("output/found_emails.csv"):
                import csv
                with open("output/found_emails.csv", 'r', encoding='utf-8') as f:
                    email_count = sum(1 for _ in csv.DictReader(f))
            
            # Get daily stats
            email_mgr = EmailManager("output", verbose=False)
            stats = email_mgr.get_daily_stats()
            
            self.email_stats_total.config(text=f"Total Emails: {email_count}")
            self.email_stats_sent_today.config(text=f"Sent Today: {stats['emails_sent_today']}/{stats['daily_limit']}")
            self.email_stats_remaining.config(text=f"Remaining: {stats['remaining']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh stats:\n{str(e)}")
    
    def reset_email_limit(self):
        """Reset the daily email limit"""
        if messagebox.askyesno("Reset Limit", "Reset the daily email limit?\n\nThis will allow you to send 50 more emails today."):
            try:
                email_mgr = EmailManager("output", verbose=False)
                email_mgr.reset_daily_limit()
                self.refresh_email_stats()
                messagebox.showinfo("Limit Reset", "Daily email limit has been reset")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset limit:\n{str(e)}")
    
    def refresh_archive_dropdown(self):
        """Refresh the archive dropdown with current archives"""
        archive_options = []
        for entry in reversed(self.archive_data):
            archive_id = entry.get('id')
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M")
            keywords = ', '.join(entry.get('keywords', []))[:40]
            label = f"[ID {archive_id}] {timestamp} - {keywords}"
            archive_options.append(label)
        
        self.archive_dropdown['values'] = archive_options
        
        if archive_options:
            self.archive_dropdown.current(0)  # Select first/most recent
    
    def load_archive_emails(self):
        """Load emails from selected archive into email manager display"""
        if not self.archive_dropdown.get():
            messagebox.showwarning("No Selection", "Please select an archive first")
            return
        
        # Extract archive ID from dropdown selection
        dropdown_value = self.archive_dropdown.get()
        try:
            archive_id = int(dropdown_value.split('[ID ')[1].split(']')[0])
        except:
            messagebox.showerror("Error", "Could not parse archive ID")
            return
        
        # Find the archive entry
        entry = next((e for e in self.archive_data if e['id'] == archive_id), None)
        if not entry:
            messagebox.showerror("Error", "Archive not found")
            return
        
        # Store current archive and emails
        self.current_archive_entry = entry
        self.current_archive_id = archive_id
        self.current_archive_emails = entry.get('extracted_emails', {})
        
        # Display emails in the email list
        self.email_list_text.delete(1.0, tk.END)
        
        if not self.current_archive_emails:
            self.email_list_text.insert(tk.END, "No emails found in this archive")
            return
        
        # Display all emails from archive
        self.email_list_text.insert(tk.END, f"Emails from Archive ID {archive_id}\n")
        self.email_list_text.insert(tk.END, f"Total: {len(self.current_archive_emails)} unique emails\n")
        self.email_list_text.insert(tk.END, "="*80 + "\n\n")
        
        for idx, (email, info) in enumerate(self.current_archive_emails.items(), 1):
            domains = ', '.join(list(info.get('domains', []))[:3])
            sources = len(info.get('sources', []))
            email_text = f"[{idx}] {email}\n    Domains: {domains}\n    Found in: {sources} job listings\n\n"
            self.email_list_text.insert(tk.END, email_text)
        
        messagebox.showinfo("Loaded", f"Loaded {len(self.current_archive_emails)} emails from archive {archive_id}")
    
    def send_email_from_archive(self):
        """Send emails to contacts from selected archive with custom message"""
        if not self.current_archive_emails:
            messagebox.showwarning("No Emails", "Please load emails from an archive first using 'Load Emails from Selected Archive'")
            return
        
        # Create dialog to compose email
        dialog = tk.Toplevel(self.root)
        dialog.title("Compose Email to Contacts")
        dialog.geometry("700x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"700x600+{x}+{y}")
        
        ttk_boot.Label(dialog, text="📧 Email Message to Send", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        # Recipient count
        ttk_boot.Label(dialog, text=f"Recipients: {len(self.current_archive_emails)} emails", font=("Helvetica", 10)).pack(pady=5)
        
        # Subject
        ttk_boot.Label(dialog, text="Subject:").pack(anchor=W, padx=20, pady=(10, 0))
        subject_entry = ttk_boot.Entry(dialog, width=60)
        subject_entry.insert(0, "JobGoblin - Lead Finder Results")
        subject_entry.pack(padx=20, pady=5)
        
        # Message body
        ttk_boot.Label(dialog, text="Message Body:").pack(anchor=W, padx=20, pady=(10, 0))
        message_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, font=("Courier", 10), height=15)
        message_text.pack(padx=20, pady=5, fill=BOTH, expand=YES)
        
        # Default message
        default_message = """Hello,

We've identified potential job opportunities that match your criteria. 

Please review the details below for more information.

Best regards,
JobGoblin Lead Finder
"""
        message_text.insert(1.0, default_message)
        
        # Button frame
        button_frame = ttk_boot.Frame(dialog)
        button_frame.pack(pady=10)
        
        def send():
            subject = subject_entry.get().strip()
            message = message_text.get(1.0, tk.END).strip()
            
            if not subject:
                messagebox.showerror("Error", "Please enter a subject")
                return
            
            if not message:
                messagebox.showerror("Error", "Please enter a message body")
                return
            
            # Check daily limit
            email_mgr = EmailManager("output", verbose=False)
            stats = email_mgr.get_daily_stats()
            
            email_list = list(self.current_archive_emails.keys())
            emails_to_send = min(len(email_list), stats['remaining'])
            
            if emails_to_send == 0:
                messagebox.showerror("Limit Reached", f"Daily limit reached. You can send {stats['remaining']} more emails today.")
                return
            
            # Confirm sending
            if not messagebox.askyesno("Confirm Send", f"Send email to {emails_to_send} contacts?\n\nLimit: {stats['emails_sent_today']}/{stats['daily_limit']} sent today"):
                return
            
            # Send emails
            dialog.destroy()
            self.send_emails_to_list(email_list[:emails_to_send], subject, message)
        
        send_btn = ttk_boot.Button(button_frame, text="Send Email", command=send, bootstyle="success", width=18)
        send_btn.pack(side=LEFT, padx=5)
        
        cancel_btn = ttk_boot.Button(button_frame, text="Cancel", command=dialog.destroy, bootstyle="danger", width=18)
        cancel_btn.pack(side=LEFT, padx=5)
    
    def send_emails_to_list(self, email_list, subject, message):
        """Send emails to a list of email addresses"""
        sender = EmailSender(verbose=True)
        sent_count = 0
        failed_count = 0
        
        for idx, email in enumerate(email_list, 1):
            try:
                self.update_status(f"📧 Sending email {idx}/{len(email_list)} to {email}...")
                
                success = sender.send_email(email, subject, message)
                
                if success:
                    sent_count += 1
                    email_mgr = EmailManager("output", verbose=False)
                    email_mgr.mark_email_sent(email, email, subject, "success")
                else:
                    failed_count += 1
                
                self.root.update()
                time.sleep(0.5)  # Throttle to avoid rate limiting
            
            except Exception as e:
                failed_count += 1
                if self.scraping:  # Only show error if still running
                    self.update_status(f"❌ Failed to send to {email}: {str(e)}")
        
        # Show results
        messagebox.showinfo("Send Complete", f"Sent: {sent_count}\nFailed: {failed_count}\n\nEmails have been tracked in your sending history.")
        self.update_status("Ready")
        self.refresh_email_stats()



def main():
    """Main entry point for GUI application"""
    # Create themed root window with green/slime theme
    root = ttk_boot.Window(themename="darkly")  # Dark base with ability to customize
    
    # Apply JobGoblin green/slime color scheme
    style = ttk_boot.Style()
    
    # Override colors for slime/green aesthetic
    colors = {
        'bg': '#1a1a1a',           # Dark background
        'fg': '#00FF00',           # Neon lime green
        'accent': '#00DD00',       # Bright green accent
        'highlight': '#00AA00',    # Darker green for highlights
        'slime': '#0FFF50',        # Slime green
    }
    
    app = JobScraperGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
