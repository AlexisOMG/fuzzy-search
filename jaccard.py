def jaccard_similarity(set1: set, set2: set) -> float:
  intersection = set1.intersection(set2)
  union = set1.union(set2)
  similarity = len(intersection) / len(union)
  return similarity