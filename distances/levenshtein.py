from distances.similarity_metric import SimilarityMetric

def levenshtein_distance(s, t, k):
  if abs(len(s) - len(t)) > k:
    return float('inf')
  
  if len(s) > len(t):
    s, t = t, s
  
  d = [0] * (len(s) + 1)
  
  for j in range(1, len(t) + 1):
    prev = d[0]
    d[0] = j
    for i in range(1, len(s) + 1):
      old = d[i]
      cost = (s[i - 1] != t[j - 1])
      d[i] = min(min(d[i - 1], d[i]) + 1, prev + cost)
      prev = old
  
  return d[len(s)]

def levenshtein_distance_memopt(s: str, t: str) -> int:
  m, n = len(s), len(t)

  if n > m:
    s, t = t, s
    m, n = n, m
  
  v0 = list(range(n + 1))
  v1 = [0] * (n + 1)

  for i in range(m):
    v1[0] = i + 1

    for j in range(n):
      deletion_cost = v0[j + 1] + 1
      insertion_cost = v1[j] + 1
      if s[i] == t[j]:
        substitution_cost = v0[j]
      else:
        substitution_cost = v0[j] + 1

      v1[j + 1] = min(deletion_cost, insertion_cost, substitution_cost)

    v0, v1 = v1, v0

  return v0[n]

def levenstein_similarity(s: str, t: str) -> float:
  distance = levenshtein_distance_memopt(s, t)
  return 1 - distance / max(len(s), len(t))

class LevenshteinMetric(SimilarityMetric):
  def distance(self, s: str, t: str) -> int:
    return levenshtein_distance_memopt(s, t)
  
  def similarity(self, s: str, t: str) -> float:
    return levenstein_similarity(s, t)

