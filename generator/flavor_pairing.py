import numpy as np

WORD_EMBED_VALS = np.load('generator/flavors/ingred_word_emb.npy', allow_pickle=True).item()
INGRED_CATEGORIES = np.load('generator/flavors/ingred_categories.npy', allow_pickle=True).item()
INGREDIENT_LIST = sorted(WORD_EMBED_VALS.keys())

def similarity(n1, n2):
    """Returns the similarity between two ingredients based on our data."""
    v1 = WORD_EMBED_VALS[n1]
    v2 = WORD_EMBED_VALS[n2]
    return np.dot(v1, v2)