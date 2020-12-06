import re

class Passport:
  _req_fields = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    # Skip CID valisation,
    # makes Polar Credentials valid
    # 'cid',
  ]
  
  def __init__(self, raw: str):
    self._raw = raw
    self._data = {}


  def isValid(self) -> bool:
    for fname in self._req_fields:
      if (fname + ":") not in self._raw:
        print(f"Passport: {self._raw} \nMissing {fname}\n")
        return False
    return True




f = open("input/4.txt", "r")

data = re.sub(r'[\n\r]{2,}', '|', f.read().strip())

tot = valid = 0
raw = ""
for line in data.split('|'):
  tot += 1
  p = Passport(re.sub(r'[\r\n]+', ' ', line))

  if p.isValid():
    valid += 1


print(f"Valid: {valid} / {tot}")

f.close()