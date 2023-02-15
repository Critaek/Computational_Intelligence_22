import pickle

def save_cache(cache):
    with open("Cache/dict.pkl", "wb") as f:
        pickle.dump(cache, f)

def load_cache():
    try:
        with open("Cache/dict.pkl", "rb") as f:
            print("Loading cache...")
            cache = pickle.load(f)
            return cache
    except OSError as e:
        print("No cache found!")
        return None