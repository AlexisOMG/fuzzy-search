class SimilarityMetric:

  def similarity(self, s: str, t: str) -> float:
    raise NotImplementedError()

  def distance(self, s: str, t: str) -> int:
    raise NotImplementedError()