f = open("input/3.txt", "r")
tree_char='#'

class RowAnalizer:
  row_length = 31
  tree_char = '#'
  
  def __init__(self, rythm: int, skip_rows: int = 0):
    self._rythm = rythm
    self._skip_rows = skip_rows
    self._next_pos = 0
    self._skip_count = skip_rows


  def hasTree(self, row: str) -> bool:
    return self.getChar(row) == self.tree_char


  def getChar(self, row: str) -> str or None:
    if not self.isValidRow():
      return None
    return row[self.getCol()]


  def getCol(self) -> int:
    pos = self._next_pos
    self._next_pos = (self._next_pos + self._rythm) % self.row_length
    return pos;


  def isValidRow(self) -> bool:
    if self._skip_count == self._skip_rows:
      self._skip_count = 0
      # print("^", end='')
      return True
    else:
      # print(".", end='')
      self._skip_count += 1
    return False


class Counter:
  def __init__(self, analyzer: RowAnalizer):
    self._occurrences = 0
    self._analyzer = analyzer
  
  def processRow(self, row: str):
    if self._analyzer.hasTree(row):
      self._occurrences += 1

  def getTotal(self) -> int:
    return self._occurrences;


col = 0
tree_count = 0

r1d1 = Counter(RowAnalizer(1))
r3d1 = Counter(RowAnalizer(3))
r5d1 = Counter(RowAnalizer(5))
r7d1 = Counter(RowAnalizer(7))
r1d2 = Counter(RowAnalizer(1, 1))

for row in f:
  r1d1.processRow(row)
  r3d1.processRow(row)
  r5d1.processRow(row)
  r7d1.processRow(row)
  r1d2.processRow(row)

# print(r1d1.getTotal())
# print(r3d1.getTotal())
# print(r5d1.getTotal())
# print(r7d1.getTotal())
# print(r1d2.getTotal())

tot = r1d1.getTotal() * r3d1.getTotal() * r5d1.getTotal() * r7d1.getTotal() * r1d2.getTotal()
print(f"\n---\n Grand: {tot}")

f.close()