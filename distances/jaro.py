from distances.similarity_metric import SimilarityMetric

def jaro_distance(s: str, t: str) -> float:
  s_len, t_len = len(s), len(t)
  
  if s_len > t_len:
    s, t = t, s
    s_len, t_len = t_len, s_len

  match_distance = max(s_len, t_len) // 2 - 1

  s_matches, t_matches = [False] * s_len, [False] * t_len
  matches, transpositions = 0, 0

  for i in range(s_len):
    start, end = max(0, i - match_distance), min(i + match_distance + 1, t_len)
    for j in range(start, end):
      if t_matches[j]:
        continue
      if s[i] != t[j]:
        continue
      s_matches[i] = t_matches[j] = True
      matches += 1
      break

  if matches == 0:
    return 0.0

  k = 0
  for i in range(s_len):
    if not s_matches[i]:
      continue
    while not t_matches[k]:
      k += 1
    if s[i] != t[k]:
      transpositions += 1
    k += 1

  return (matches / s_len + matches / t_len + (matches - transpositions // 2) / matches) / 3


def jaro_winkler_similarity(s: str, t: str, p=0.1) -> float:
  jaro_dist = jaro_distance(s, t)

  if jaro_dist > 0.0:
    prefix = 0
    for i in range(min(len(s), len(t))):
      if s[i] == t[i]:
        prefix += 1
      else:
        break
    jaro_dist += (p * prefix * (1 - jaro_dist))

  return jaro_dist

class JaroWinklerMetric(SimilarityMetric):
  def __init__(self, p=0.1):
    self.p = p

  def similarity(self, s: str, t: str) -> float:
    return jaro_winkler_similarity(s, t, self.p)
