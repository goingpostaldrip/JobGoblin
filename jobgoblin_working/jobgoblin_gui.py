from proxy_manager import ProxyManager
from ddg_proxy_client import ddg_search
from search_engines import startpage_search, serpapi_search, google_cse_search, bing_search
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from site_indeed import indeed_search
from site_greenhouse import greenhouse_search
from site_lever import lever_search
from site_simplyhired import simplyhired_search
from site_remoteok import remoteok_search
from site_weworkremotely import weworkremotely_search
from site_remotive import remotive_search

class JobScraperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JobGoblin - Ultimate Job Scraper")
        self.geometry("900x600")
        self.create_widgets()

    def create_widgets(self):
        keyword_frame = ttk.LabelFrame(self, text="Keywords")
        keyword_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(keyword_frame, text="Enter keywords:").pack(side="left", padx=5)
        self.keyword_entry = ttk.Entry(keyword_frame, width=40)
        self.keyword_entry.pack(side="left", padx=5)
        self.keyword_entry.insert(0, "Python Developer")
        ttk.Button(keyword_frame, text="Search", command=self.start_search).pack(side="left", padx=5)

        self.results_frame = ttk.LabelFrame(self, text="Results")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_box = tk.Text(self.results_frame, height=20)
        self.results_box.pack(fill="both", expand=True)

        self.status_bar = ttk.Label(self, text="Ready", relief="sunken", anchor="w")
        self.status_bar.pack(fill="x", side="bottom")

        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate", maximum=7)
        self.progress.pack(fill="x", padx=10, pady=5)

    def start_search(self):
        keyword = self.keyword_entry.get().strip()
        self.results_box.delete("1.0", tk.END)
        self.results_box.insert(tk.END, f"Searching for jobs: {keyword}\n")
        self.status_bar.config(text="Searching...")
        self.progress['value'] = 0
        threading.Thread(target=self.run_search, args=(keyword,), daemon=True).start()

    def run_search(self, keyword):
        import logging
        logging.basicConfig(filename='jobgoblin_working/output/gui_log.txt', level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(message)s')
        results = []

if __name__ == '__main__':
    app = JobScraperApp()
    app.mainloop()
