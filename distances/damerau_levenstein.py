from distances.similarity_metric import SimilarityMetric

def damerau_levenshtein_distance_1(A, B):
  n = len(A)
  m = len(B)

  F = [[0] * (m + 1) for i in range(n + 1)]

  for i in range(n + 1):
    F[i][0] = i

  for j in range(m + 1):
    F[0][j] = j

  for i in range(1, n + 1):
    for j in range(1, m + 1):
      F[i][j] = min(F[i - 1][j], F[i][j - 1]) + 1
      F[i][j] = min(F[i][j], F[i - 1][j - 1] + int(A[i - 1] != B[j - 1]))
      if i >= 2 and j >= 2 and A[i - 2:i] == B[j - 2:j][::-1]:
        F[i][j] = min(F[i][j], F[i - 2][j - 2] + 1)

  return F[n][m]

def damerau_levenshtein_distance(s, t, delete_cost=1, insert_cost=1, replace_cost=1, transpose_cost=1):
    m, n = len(s), len(t)
    
    if s == "":
      return n
    elif t == "":
      return m
    
    inf = (m + n) * max(delete_cost, insert_cost, replace_cost, transpose_cost)
    d = [[inf] * (n + 2) for _ in range(m + 2)]
    
    for i in range(m + 1):
      d[i + 1][1] = i * delete_cost
      d[i + 1][0] = inf
        
    for j in range(n + 1):
      d[1][j + 1] = j * insert_cost
      d[0][j + 1] = inf
        
    last_position = {}
    for letter in (s + t):
      last_position[letter] = 0
        
    for i in range(1, m + 1):
      last = 0
      for j in range(1, n + 1):
        i_ = last_position[t[j - 1]]
        j_ = last
        
        c = replace_cost
        if s[i - 1] == t[j - 1]:
          d[i + 1][j + 1] = d[i][j]
          last = j
          c = 0
        else:
          d[i + 1][j + 1] = min(d[i][j] + c, d[i + 1][j] + insert_cost, d[i][j + 1] + delete_cost)
            
        d[i + 1][j + 1] = min(
          d[i + 1][j + 1], 
          d[i_][j_] + (i - i_ - 1) * delete_cost + transpose_cost + (j - j_ - 1) * insert_cost
        )
          
      last_position[s[i - 1]] = i
        
    return d[m][n]

def damerau_levenshtein_distance_memopt(s: str, t: str) -> int:
  m, n = len(s), len(t)
  if m == 0:
      return n
  if n == 0:
      return m

  prev_prev_row = [0] * (n + 1)
  prev_row = [0] * (n + 1)
  current_row = [0] * (n + 1)

  for j in range(n + 1):
    prev_row[j] = j

  for i in range(1, m + 1):
    current_row[0] = i

    for j in range(1, n + 1):
      cost = 0 if s[i - 1] == t[j - 1] else 1
      current_row[j] = min(
        prev_row[j] + 1,
        current_row[j - 1] + 1,
        prev_row[j - 1] + cost
      )

      if i > 1 and j > 1 and s[i - 1] == t[j - 2] and s[i - 2] == t[j - 1]:
        current_row[j] = min(current_row[j], prev_prev_row[j - 2] + cost)

    prev_prev_row, prev_row, current_row = prev_row, current_row, prev_prev_row

  return prev_row[n]

def damerau_levenshtein_similarity(s: str, t: str) -> float:
  distance = damerau_levenshtein_distance_memopt(s, t)
  return 1 - distance / max(len(s), len(t))

class DamerauLevenshteinMetric(SimilarityMetric):

  def distance(self, s: str, t: str) -> float:
    return damerau_levenshtein_distance_memopt(s, t)
  
  def similarity(self, s: str, t: str) -> float:
    return damerau_levenshtein_similarity(s, t)

