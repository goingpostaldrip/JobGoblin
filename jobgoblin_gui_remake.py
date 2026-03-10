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
        # Keyword input
        keyword_frame = ttk.LabelFrame(self, text="Keywords")
        keyword_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(keyword_frame, text="Enter keywords:").pack(side="left", padx=5)
        self.keyword_entry = ttk.Entry(keyword_frame, width=40)
        self.keyword_entry.pack(side="left", padx=5)
        self.keyword_entry.insert(0, "Python Developer")
        ttk.Button(keyword_frame, text="Search", command=self.start_search).pack(side="left", padx=5)

        # Results display
        self.results_frame = ttk.LabelFrame(self, text="Results")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_box = tk.Text(self.results_frame, height=20)
        self.results_box.pack(fill="both", expand=True)

    def start_search(self):
        keyword = self.keyword_entry.get().strip()
        self.results_box.delete("1.0", tk.END)
        self.results_box.insert(tk.END, f"Searching for jobs: {keyword}\n")
        threading.Thread(target=self.run_search, args=(keyword,), daemon=True).start()

    def run_search(self, keyword):
        results = []
        for scraper, label in [
            (indeed_search, 'Indeed'),
            (greenhouse_search, 'Greenhouse'),
            (lever_search, 'Lever'),
            (simplyhired_search, 'SimplyHired'),
            (remoteok_search, 'RemoteOK'),
            (weworkremotely_search, 'WeWorkRemotely'),
            (remotive_search, 'Remotive'),
        ]:
            attempts = 0
            max_attempts = 3
            while attempts < max_attempts:
                try:
                    jobs = scraper(keyword, '', 5, True)
                    for job in jobs:
                        job['source'] = label
                        results.append(job)
                    break
                except Exception as e:
                    self.results_box.insert(tk.END, f"[{label}] Error (attempt {attempts+1}): {e}\n")
                    attempts += 1
            else:
                self.results_box.insert(tk.END, f"[{label}] Failed after {max_attempts} attempts.\n")
        if not results:
            self.results_box.insert(tk.END, "No jobs found.\n")
        else:
            for job in results:
                self.results_box.insert(tk.END, f"[{job['source']}] {job.get('title','')} at {job.get('company','')} ({job.get('location','')})\n{job.get('url','')}\n\n")

if __name__ == "__main__":
    app = JobScraperApp()
    app.mainloop()
