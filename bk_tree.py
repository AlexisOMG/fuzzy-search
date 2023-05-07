from typing import List, Tuple, Callable, Dict, Optional
from distances.levenshtein import levenshtein_distance_memopt

class BKTreeNode:
    def __init__(self, value: str):
        self.value: str = value
        self.children: Dict[int, BKTreeNode] = {}

    def insert(self, value: str, distance_func: Callable[[str, str], int]):
        distance = distance_func(self.value, value)
        if distance in self.children:
            self.children[distance].insert(value, distance_func)
        else:
            self.children[distance] = BKTreeNode(value)

    def query(self, value: str, max_distance: int, distance_func: Callable[[str, str], int]) -> List[Tuple[int, str]]:
        results: List[Tuple[int, str]] = []

        distance_to_value = distance_func(self.value, value)
        if distance_to_value <= max_distance:
            results.append((distance_to_value, self.value))

        for i in range(distance_to_value - max_distance, distance_to_value + max_distance + 1):
            child = self.children.get(i)
            if child:
                results.extend(child.query(value, max_distance, distance_func))

        return results


class BKTree:
    def __init__(self, distance_func: Callable[[str, str], int]):
        self.root: Optional[BKTreeNode] = None
        self.distance_func = distance_func

    def insert(self, value: str):
        if not self.root:
            self.root = BKTreeNode(value)
        else:
            self.root.insert(value, self.distance_func)

    def query(self, value: str, max_distance: int) -> List[Tuple[int, str]]:
        if not self.root:
            return []
        return self.root.query(value, max_distance, self.distance_func)


if __name__ == "__main__":
    words = ["apple", "banana", "orange", "grape", "watermelon", "pineapple"]
    tree = BKTree(levenshtein_distance_memopt)
    for word in words:
        tree.insert(word)

    query_word = "appla"
    max_distance = 4

    for word in words:
        distance = levenshtein_distance_memopt(query_word, word)
        print(f"Distance between '{query_word}' and '{word}': {distance}")

    results = tree.query(query_word, max_distance)
    print(f"Words within {max_distance} edit distance from '{query_word}':")
    for distance, word in results:
        print(f"{word} (distance: {distance})")
