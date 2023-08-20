from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

from .models import ItemData

all_items: list[ItemData] = []
vectorizer = TfidfVectorizer(min_df=1, analyzer="word", ngram_range=(1, 2))


def flatten(item: ItemData):
    values = [item.name, item.address]
    values.extend(item.description.values())
    values.extend(item.significance.values())
    return " ".join(values)


def init_fulltext(items: list[ItemData]):
    global all_items, vextorizer, site_tfidf, fulltexts
    all_items = items

    fulltexts = [flatten(item) for item in items]

    site_tfidf = vectorizer.fit_transform(fulltexts)


def query_all(query):
    query_tfidf = vectorizer.transform([query])
    similarity = cosine_similarity(query_tfidf, site_tfidf)
    return list(similarity[0])
