<?php

/**
 * 10.20 - 10.24
 *
 *
 */
$data = file_get_contents('./9_dic.txt');
$rows = explode("\n", $data);

$preamble = 25;

for ($i = $preamble; $i < count($rows); $i++) {
    $val = $rows[$i];

    $valid = false;
    for ($j = $i-$preamble; $j < $i; $j++) {
        for ($k = $i-$preamble; $k < $i; $k++) {
            if ($i == $k)
                continue;

            if (($rows[$j] + $rows[$k]) == $val) {
                $valid = true;
            }
        }
    }

    if ($valid == false)
        die($val);
}