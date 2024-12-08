from serpapi import GoogleSearch
import os
import hashlib
from datetime import datetime

class ScholarToBibtex:
    def __init__(self, serpapi_key, output_dir, user_id):
        self.serpapi_key = serpapi_key
        self.output_dir = output_dir
        self.user_id = user_id

    def get_publications(self):
        """Fetch all publications for a given author ID using SerpAPI with pagination."""
        all_articles = []
        start = 0
        batch_size = 100

        while True:
            params = {
                "api_key": self.serpapi_key,
                "engine": "google_scholar_author",
                "author_id": self.user_id,
                "start": start,
                "num": batch_size,
                "sort": "pubdate"
            }

            search = GoogleSearch(params)
            results = search.get_dict()
            articles = results.get('articles', [])
            
            if not articles:
                break
                
            all_articles.extend(articles)
            start += batch_size
            print(f"Fetched {len(all_articles)} publications...")
            
        return all_articles

    def create_bibtex_entry(self, article):
        """Convert a single article to BibTeX format."""
        first_author = article['authors'].split(',')[0].strip()
        last_name = first_author.split()[-1].lower()
        year = article.get('year', 'XXXX')
        
        title_hash = hashlib.md5(article['title'].encode()).hexdigest()[:4]
        citation_key = f"{last_name}{year}_{title_hash}"
        
        title = article['title'].replace('{', '\\{').replace('}', '\\}')
        authors = article['authors'].replace(' and ', ' AND ')
        
        entry = [
            f"@article{{{citation_key},",
            f"  title = {{{title}}},",
            f"  author = {{{authors}}},",
            f"  year = {{{year}}},",
        ]
        
        if 'publication' in article:
            entry.append(f"  journal = {{{article['publication']}}},")
        
        if 'cited_by' in article:
            entry.append(f"  note = {{Cited by {article['cited_by']['value']}}},")
        
        if 'link' in article:
            entry.append(f"  url = {{{article['link']}}},")
        
        entry.append("}")
        return '\n'.join(entry)

    def update_citations(self):
        """Update the citations file."""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Get publications
            publications = self.get_publications()
            
            if not publications:
                return {"status": "warning", "message": "No publications found"}
            
            # Convert to BibTeX
            bibtex_entries = [self.create_bibtex_entry(article) for article in publications]
            
            # Write to file
            output_file = os.path.join(self.output_dir, 'citations.bib')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(bibtex_entries))
            
            return {
                "status": "success",
                "message": f"Updated {len(publications)} citations",
                "timestamp": datetime.now().isoformat(),
                "file_path": output_file
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            } 