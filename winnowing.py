import hashlib

def remove_spaces(s):
    return s.replace(" ", "")

def n_grams(string, n):
  string = remove_spaces(string)
  return [string[i:i + n] for i in range(len(string) - n + 1)]

def hash_n_gram(n_gram):
    return int(hashlib.sha1(n_gram.encode('utf-8')).hexdigest(), 16)

def min_hash_window(hashes, w):
    return min(enumerate(hashes), key=lambda x: x[1], start=max(0, len(hashes) - w))

def winnowing(string, k, w):
    # Step 1: Generate k-grams
    k_grams = n_grams(string, k)

    # Step 2: Hash k-grams
    k_gram_hashes = [hash_n_gram(k_gram) for k_gram in k_grams]

    # Step 3: Generate min-hashes for each window
    fingerprints = set()
    prev_min_idx = -1
    for i in range(len(k_gram_hashes) - w + 1):
        window = k_gram_hashes[i:i + w]
        min_idx, min_hash = min(enumerate(window), key=lambda x: x[1])
        min_idx += i
        if min_idx != prev_min_idx:
            fingerprints.add(min_hash)
            prev_min_idx = min_idx

    return fingerprints



def winnowing_similarity(string1, string2, k, w):
    fingerprints1 = winnowing(string1, k, w)
    fingerprints2 = winnowing(string2, k, w)

    print(f"fingerprints1: {fingerprints1}")
    print(f"fingerprints2: {fingerprints2}")

    intersection = fingerprints1.intersection(fingerprints2)
    union = fingerprints1.union(fingerprints2)

    return len(intersection) / len(union)


# Example usage:
string1 = "Егоров Алексей Николаевич"
string2 = "Егороф Алексей Николаевич"
k = 2
w = 3

similarity = winnowing_similarity(string1, string2, k, w)
print(f"Winnowing similarity: {similarity}")
