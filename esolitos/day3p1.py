
f = open("input/3.txt", "r")

tree_char='#'

col = 0
tree_count = 0

for row in f:
  char = row[col]
  if char == tree_char:
    tree_count += 1

  # Get the number of columns
  num_cols = len(row.strip())
  # Get the current character position
  # Use modulo to ensure we can "overflow" the col count
  col = ((col + 3) % num_cols) 

print(f"Trees: {tree_count}")

f.close()