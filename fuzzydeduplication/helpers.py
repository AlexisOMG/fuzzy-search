import re
from typing import Any, Dict, Hashable, List, Callable, Tuple, Set

from fuzzydeduplication.distances.levenshtein import levenshtein_distance_memopt

def clean_address(address: str) -> str:
  # Список слов и сокращений для удаления
  words_to_remove = [
    "улица", "ул\\. ?", "проспект", "пр-т\\. ?", "пр\\. ?", "бульвар", "б-р\\. ?", "переулок", "пер\\. ?", "набережная", "наб\\. ?",
    "шоссе", "площадь", "пл\\. ?", "дом", "д\\. ?", "квартира", "кв\\. ?", "корпус", "корп\\. ?", "строение", "стр\\. ?", "область",
    "обл\\. ?", "город", "г\\. ?", "поселок", "пос\\. ?", "деревня", "дер\\. ?",
    "street", "st\\. ?", "avenue", "ave\\. ?", "boulevard", "blvd\\. ?", "alley", "al\\. ?", "drive", "dr\\. ?",
    "square", "sq\\. ?", "house", "h\\. ?", "apartment", "apt\\. ?", "building", "bldg\\. ?", "county", "co\\. ?",
    "city", "ct\\. ?", "village", "vil\\. ?", "township", "twp\\. ?", "road", "rd\\. ?"
  ]

  # Создаем регулярное выражение из списка слов и сокращений
  pattern = r'\b(?:{})\b'.format('|'.join(words_to_remove))

  # Заменяем найденные слова и сокращения на пустую строку
  cleaned_address = re.sub(pattern, '', address, flags=re.IGNORECASE)

  # Удаляем лишние пробелы и возвращаем очищенную строку
  return re.sub(r'\s+', ' ', cleaned_address).strip()

def concat_fields(r: Dict[Hashable, Any], column_names: List[str]):
  s = ''
  for k in column_names:
    if r[k] is not None and isinstance(r[k], str) and r[k] != '':
      s += r[k]
  return s

def to_str(column_names: List[str]) -> Callable[[Dict[Hashable, Any]], str]:
  return lambda r: concat_fields(r, column_names)

def get_key(x: str) -> str:
    # Формируем ключ из значений полей
    return  '-'.join([x.split('-')[0], x.split('-')[1]])

def get_stats(
  res: List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]], 
  expected_res: Dict[str, Set[str]],
  id_key: str = 'rec_id'
) -> Tuple[int, int, int, float, float, float]:
  tp = 0
  fp = 0
  fn = 0
  res_by_ids = {}
  for (a, b) in res:
    a_id = a[id_key]
    b_id = b[id_key]
    if a_id == b_id:
      print(f'ERROR: {a_id}, {b_id}')
      continue
    a_key = get_key(a_id)
    b_key = get_key(b_id)
    if a_key != b_key:
      # print(f'ERROR: {a_id}, {b_id}, {sim}')
      fp += 1
      continue
    if a_key not in res_by_ids:
      res_by_ids[a_key] = set()
    res_by_ids[a_key].add(a_id)
    res_by_ids[a_key].add(b_id)
  for key in expected_res:
    if key not in res_by_ids:
      if len(expected_res[key]) > 1:
        # print(f'ERROR: not found {key}')
        fn += len(expected_res[key])
      continue
    # if len(expected_res[key]) != len(res_by_ids[key]):
    #   print(f'ERROR: not full {key}')
    fn += len(expected_res[key]) - len(res_by_ids[key])
    tp += len(res_by_ids[key])
  precision = 0
  if tp + fp != 0:
    precision = tp / (tp + fp)
  recall = 0
  if tp + fn != 0:
    recall = tp / (tp + fn)
  f1 = 0
  if precision + recall != 0:
    f1 = 2 * precision * recall / (precision + recall)
  return tp, fp, fn, precision, recall, f1

def res_stats(res: List[Tuple[Dict[Hashable, Any], Dict[Hashable, Any]]], expected_res) -> None:
  tp, fp, fn, precision, recall, f1 = get_stats(res, expected_res)
  print(f'tp: {tp}, fp: {fp}, fn: {fn}')
  print(f'precision: {precision}')
  print(f'recall: {recall}')
  print(f'f1: {f1}')

def full_lev_dist(a: Dict[Hashable, Any], b: Dict[Hashable, Any], column_names: List[str]) -> int:
  a_s = ''
  b_s = ''
  for k in column_names:
    if a[k] is not None and isinstance(a[k], str) and a[k] != '' and b[k] is not None and isinstance(b[k], str) and b[k] != '':
      a_s += a[k]
      b_s += b[k]
  return levenshtein_distance_memopt(a_s, b_s)

def get_lev_dist(column_names: List[str]) -> Callable[[Dict[Hashable, Any], Dict[Hashable, Any]], int]:
  return lambda a, b: full_lev_dist(a, b, column_names)
