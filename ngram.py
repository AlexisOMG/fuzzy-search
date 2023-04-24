def n_grams(string, n):
    return [string[i:i + n] for i in range(len(string) - n + 1)]


def dice_coefficient(set1: set, set2: set):
    intersection = set1.intersection(set2)
    return 2 * len(intersection) / (len(set1) + len(set2))


def n_gram_similarity(strings, target, n, threshold):
    # Step 1: Preprocessing
    n_gram_sets = [set(n_grams(string, n)) for string in strings]
    
    # Step 2: Indexing (inverted index)
    inverted_index = {}
    for idx, n_gram_set in enumerate(n_gram_sets):
        for n_gram in n_gram_set:
            if n_gram not in inverted_index:
                inverted_index[n_gram] = []
            inverted_index[n_gram].append(idx)
    
    # Step 3: Matching
    target_n_grams = set(n_grams(target, n))
    scores = [0.] * len(strings)
    for n_gram in target_n_grams:
        if n_gram in inverted_index:
            for idx in inverted_index[n_gram]:
                scores[idx] = dice_coefficient(n_gram_sets[idx], target_n_grams)

                

    # Step 4: Thresholding
    matches = [idx for idx, score in enumerate(scores) if score >= threshold]

    return matches


# Example usage:
strings = ["apple", "banana", "grape", "pineapple", "peach", "grapefruit"]
target = "papaya"
n = 2
threshold = 0.2

matching_indices = n_gram_similarity(strings, target, n, threshold)
print(f"Matching strings: {[strings[idx] for idx in matching_indices]}")
