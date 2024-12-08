import os
from serpapi.google_search import GoogleSearch
from dotenv import load_dotenv
import re
from urllib.parse import urlparse, parse_qs
import hashlib

def extract_author_id(url):
    """Extract the author ID from a Google Scholar URL."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get('user', [None])[0]

def get_publications(author_id, api_key):
    """Fetch all publications for a given author ID using SerpAPI with pagination."""
    all_articles = []
    start = 0
    batch_size = 100  # SerpAPI's max items per request

    while True:
        params = {
            "api_key": api_key,
            "engine": "google_scholar_author",
            "author_id": author_id,
            "start": start,
            "num": batch_size,
            "sort": "pubdate"  # Sort by publication year
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        articles = results.get('articles', [])
        
        if not articles:
            break
            
        all_articles.extend(articles)
        start += batch_size
        
        # Print progress
        print(f"Fetched {len(all_articles)} publications...")
        
    return all_articles

def create_bibtex_entry(article):
    """Convert a single article to BibTeX format."""
    # Create a unique citation key from first author's lastname, year, and title hash
    first_author = article['authors'].split(',')[0].strip()
    last_name = first_author.split()[-1].lower()
    year = article.get('year', 'XXXX')
    
    # Create a short hash from the title for uniqueness
    title_hash = hashlib.md5(article['title'].encode()).hexdigest()[:4]
    citation_key = f"{last_name}{year}_{title_hash}"
    
    # Clean the title
    title = article['title'].replace('{', '\\{').replace('}', '\\}')
    
    # Format authors
    authors = article['authors'].replace(' and ', ' AND ')
    
    # Build BibTeX entry
    entry = [
        f"@article{{{citation_key},",
        f"  title = {{{title}}},",
        f"  author = {{{authors}}},",
        f"  year = {{{year}}},",
    ]
    
    # Add optional fields if available
    if 'publication' in article:
        entry.append(f"  journal = {{{article['publication']}}},")
    
    if 'cited_by' in article:
        entry.append(f"  note = {{Cited by {article['cited_by']['value']}}},")
    
    if 'link' in article:
        entry.append(f"  url = {{{article['link']}}},")
    
    entry.append("}")
    return '\n'.join(entry)

def main():
    load_dotenv()
    api_key = os.getenv('SERPAPI_KEY')
    
    if not api_key:
        print("Error: SERPAPI_KEY not found in environment variables")
        print("Please create a .env file with your SerpAPI key: SERPAPI_KEY=your_key_here")
        return
    
    # Use fixed URL
    url = "https://scholar.google.com/citations?hl=en&user=ilO06uUAAAAJ&view_op=list_works&sortby=pubdate"
    author_id = extract_author_id(url)
    
    if not author_id:
        print("Error: Could not extract author ID from the URL")
        return
    
    try:
        # Fetch publications
        publications = get_publications(author_id, api_key)
        
        if not publications:
            print("No publications found")
            return
        
        # Convert to BibTeX
        bibtex_entries = [create_bibtex_entry(article) for article in publications]
        
        # Save to file
        output_file = f"scholar_{author_id}_publications.bib"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(bibtex_entries))
        
        print(f"Successfully saved {len(publications)} publications to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 