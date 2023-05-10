import re

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
