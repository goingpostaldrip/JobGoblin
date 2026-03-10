# JobGoblin Working - Job Scraper Botasaurus
# Add filtering and enrichment logic here if needed for future enhancements.

def filter_jobs(jobs, keyword):
    return [job for job in jobs if keyword.lower() in job.get('title','').lower()]
