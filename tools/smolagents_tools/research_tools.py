import feedparser
from urllib import parse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from smolagents.tools import Tool

class ArxivSearchTool(Tool):
    name = "arxiv_search"
    description = "Searches for research papers on arXiv based on keywords."

    inputs = {
        "keywords": {"type": "string", "description": "Keywords for search (e.g., 'machine learning', 'AI', 'climate change')"},
        "num_results": {"type": "integer", "description": "Number of results to return (default: 5)"}   
    }

    output_type = "array"

    def forward(self, keywords: list, num_results: int = 5) -> list:
        """Fetches and ranks arXiv papers using TF-IDF and Cosine Similarity.
        Args:
            keywords: List of keywords for search.
            num_results: Number of results to return.
        Returns:
            List of the most relevant papers based on TF-IDF ranking.
        """
        try:
            print(f"DEBUG: Searching arXiv papers with keywords: {keywords}")

            # Use a general keyword search
            query = "+AND+".join([f"all:{kw}" for kw in keywords])  
            query_encoded = parse.quote(query)
            url = f"http://export.arxiv.org/api/query?search_query={query_encoded}&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending"

            print(f"DEBUG: Query URL - {url}")

            feed = feedparser.parse(url)
            papers = []

            # Extract papers from arXiv
            for entry in feed.entries:
                papers.append({
                    "title": entry.title,
                    "authors": ", ".join(author.name for author in entry.authors),
                    "year": entry.published[:4],
                    "abstract": entry.summary,
                    "link": entry.link
                })

            if not papers:
                return [{"error": "No results found. Try different keywords."}]

            # Prepare TF-IDF Vectorization
            corpus = [paper["title"] + " " + paper["abstract"] for paper in papers]
            vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))  # Remove stopwords
            tfidf_matrix = vectorizer.fit_transform(corpus)

            # Transform Query into TF-IDF Vector
            query_str = " ".join(keywords)
            query_vec = vectorizer.transform([query_str])

            #Compute Cosine Similarity
            similarity_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

            #Sort papers based on similarity score
            ranked_papers = sorted(zip(papers, similarity_scores), key=lambda x: x[1], reverse=True)

            # Return the most relevant papers
            return [paper[0] for paper in ranked_papers[:num_results]]

        except Exception as e:
            print(f"ERROR: {str(e)}")
            return [{"error": f"Error fetching research papers: {str(e)}"}]