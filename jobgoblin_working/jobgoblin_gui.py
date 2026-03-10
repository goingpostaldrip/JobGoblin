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
        scraper_list = [
            (indeed_search, 'Indeed'),
            (greenhouse_search, 'Greenhouse'),
            (lever_search, 'Lever'),
            (simplyhired_search, 'SimplyHired'),
            (remoteok_search, 'RemoteOK'),
            (weworkremotely_search, 'WeWorkRemotely'),
            import tkinter as tk
            from tkinter import messagebox, filedialog
            import ttkbootstrap as ttk_boot
            from ttkbootstrap.constants import *
            import threading
            import os
            from site_indeed import indeed_search
            from site_greenhouse import greenhouse_search
            from site_lever import lever_search
            from site_simplyhired import simplyhired_search
            from site_remoteok import remoteok_search
            from site_weworkremotely import weworkremotely_search
            from site_remotive import remotive_search

            class JobScraperGUI:
                    self.proxy_manager = ProxyManager()
                    self.proxy_manager.load_proxies(os.path.join(os.path.dirname(__file__), 'proxies.json'))
                def __init__(self, root):
                    self.root = root
                    self.root.title("JobGoblin - Lead Finder")
                    self.root.geometry("1200x800")
                    self.results = []
                    self.setup_ui()

                def setup_ui(self):
                    self.notebook = ttk_boot.Notebook(self.root)
                    self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

                    self.scraper_tab = ttk_boot.Frame(self.notebook)
                    self.notebook.add(self.scraper_tab, text="🟢 Job Scraper")

                    self.archive_tab = ttk_boot.Frame(self.notebook)
                    self.notebook.add(self.archive_tab, text="🟢 Scrape Archive")

                    self.email_tab = ttk_boot.Frame(self.notebook)
                    self.notebook.add(self.email_tab, text="🟢 Email Manager")

                    self.proxy_tab = ttk_boot.Frame(self.notebook)
                    self.notebook.add(self.proxy_tab, text="🔗 Proxy Management")

                    self.help_tab = ttk_boot.Frame(self.notebook)
                    self.notebook.add(self.help_tab, text="🟢 Help & Support")

                    self.settings_tab = ttk_boot.Frame(self.notebook)
                    self.notebook.add(self.settings_tab, text="⚙️ Settings")

                    self.developer_tab = ttk_boot.Frame(self.notebook)
                    self.notebook.add(self.developer_tab, text="👨‍💻 Developer")

                    self.setup_scraper_tab()

                def setup_scraper_tab(self):
                    keywords_frame = ttk_boot.Labelframe(self.scraper_tab, text="🔑 Keywords", bootstyle="primary", padding=10)
                    keywords_frame.pack(fill=X, pady=5)
                    ttk_boot.Label(keywords_frame, text="Enter keywords (comma-separated):").pack(anchor=W)
                    self.keywords_entry = ttk_boot.Entry(keywords_frame, width=40)
                    self.keywords_entry.pack(fill=X, pady=5)
                    self.keywords_entry.insert(0, "Python Developer, Data Scientist")

                    locations_frame = ttk_boot.Labelframe(self.scraper_tab, text="📍 Locations", bootstyle="info", padding=10)
                    locations_frame.pack(fill=X, pady=5)
                    ttk_boot.Label(locations_frame, text="Enter locations (comma-separated):").pack(anchor=W)
                    self.locations_entry = ttk_boot.Entry(locations_frame, width=40)
                    self.locations_entry.pack(fill=X, pady=5)
                    self.locations_entry.insert(0, "New York, Remote")

                    engines_frame = ttk_boot.Labelframe(self.scraper_tab, text="🌐 Search Engines", bootstyle="success", padding=10)
                    engines_frame.pack(fill=X, pady=5)
                    self.engine_vars = {}
                    engine_names = [
                        "DuckDuckGo", "Startpage", "SerpAPI", "Google CSE", "Bing", "Indeed", "Greenhouse", "Lever", "SimplyHired", "RemoteOK", "WeWorkRemotely", "Remotive"
                    ]
                    for name in engine_names:
                        var = tk.BooleanVar(value=True)
                        self.engine_vars[name] = var
                        ttk_boot.Checkbutton(engines_frame, text=name, variable=var, bootstyle="success-round").pack(side=LEFT, padx=2)

                    search_btn = ttk_boot.Button(keywords_frame, text="Search", command=self.start_search, bootstyle="success")
                    search_btn.pack(pady=5)

                    self.results_frame = ttk_boot.Labelframe(self.scraper_tab, text="Results", bootstyle="info", padding=10)
                    self.results_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
                    self.results_box = tk.Text(self.results_frame, height=20)
                    self.results_box.pack(fill=BOTH, expand=True)

                def start_search(self):
                    keywords = self.keywords_entry.get().strip()
                    locations = self.locations_entry.get().strip()
                    selected_engines = [name for name, var in self.engine_vars.items() if var.get()]
                    self.results_box.delete("1.0", tk.END)
                    self.results_box.insert(tk.END, f"Searching for jobs: {keywords} in {locations} using {', '.join(selected_engines)}\n")
                    threading.Thread(target=self.run_search, args=(keywords, locations, selected_engines), daemon=True).start()

                def run_search(self, keywords, locations, selected_engines):
                    results = []
                    engine_map = {
                        "DuckDuckGo": ddg_search,
                        "Startpage": startpage_search,
                        "SerpAPI": serpapi_search,
                        "Google CSE": google_cse_search,
                        "Bing": bing_search,
                        "Indeed": indeed_search,
                        "Greenhouse": greenhouse_search,
                        "Lever": lever_search,
                        "SimplyHired": simplyhired_search,
                        "RemoteOK": remoteok_search,
                        "WeWorkRemotely": weworkremotely_search,
                        "Remotive": remotive_search,
                    }
                    proxy = self.proxy_manager.get_proxy()
                    for engine in selected_engines:
                        scraper = engine_map.get(engine)
                        if scraper:
                            try:
                                jobs = scraper(keywords, locations, 5, True, proxy=proxy)
                                for job in jobs:
                                    job['source'] = engine
                                    results.append(job)
                            except Exception as e:
                                self.results_box.insert(tk.END, f"[{engine}] Error: {e}\n")
                        else:
                            self.results_box.insert(tk.END, f"[{engine}] API integration missing.\n")
                    if not results:
                        self.results_box.insert(tk.END, "No jobs found.\n")
                    else:
                        for job in results:
                            self.results_box.insert(tk.END, f"[{job['source']}] {job.get('title','')} at {job.get('company','')} ({job.get('location','')})\n{job.get('url','')}\n\n")

            if __name__ == "__main__":
                root = ttk_boot.Window(themename="superhero")
                app = JobScraperGUI(root)
                root.mainloop()
