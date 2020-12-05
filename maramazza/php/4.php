<?php
$res1 = 0;
$resOK = 0;
$rules = array('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid');
/*

byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.

*/

function checkValue($field, $value)
{
    switch ($field) {
        case 'byr':
            if (strlen($value) == 4) {
                if ((int)$value >= 1920 && (int)$value <= 2002)
                    return true;
                else
                    return false;
            } else {
                return false;
            }
            break;
        case 'iyr':
            if (strlen($value) == 4) {
                if ((int)$value >= 2010 && (int)$value <= 2020)
                    return true;
                else
                    return false;
            } else {
                return false;
            }
            break;
        case 'eyr':
            if (strlen($value) == 4) {
                if ((int)$value >= 2020 && (int)$value <= 2030)
                    return true;
                else
                    return false;
            } else {
                return false;
            }
            break;
        case 'hgt':
            break;
        case 'hcl':
            break;
        case 'ecl':
            break;
        case 'pid':
            break;
    }
}

$content = file_get_contents('./../data/4.txt');
$rows = preg_split("#\n\s*\n#Uis", $content);

$passports = array();
foreach ($rows as $row) {
    $passports[] = preg_split("/ /", str_replace("\n", " ", $row));
}
$tot = count($passports);
$check = array();
foreach ($passports as $key => $passport) {
    $elems = count($passport);
    for ($i = 0; $i < $elems; $i++) {
        $check[$key][] = substr($passport[$i], 0, 3);
    }
    $diff = array_diff($rules, $check[$key]);
    if (!$diff or ((count($diff) == 1) && (in_array('cid', $diff)))) {
        $res1++;
        print_r($passport);
    }
}
echo "res1: " . $res1;
