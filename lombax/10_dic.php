<?php

/**
 * 11.27 - 11.36 - infinite
 *
 *
 */
$data = file_get_contents('./10_dic.txt');
$rows = explode("\n", $data);

$min = min($rows);
$max = max($rows);
$embedded = $max + 3;

$rows[] = 0;
sort($rows);
$rows[] = $embedded;

$differences = [];
$previous = 0;
foreach ($rows as $row) {
    $idx = $row - $previous;

    if (!isset($differences[$idx]))
        $differences[$idx] = 1;
    else
        $differences[$idx]++;

    $previous = $row;

}

echo $differences[1] * $differences[3];

// 2

$values = [];
$values[0] = 1;
for ($i = 0; $i < count($rows); $i++) {
    $n = $rows[$i];
    if ($i != 0) {
        $values[$n] = $values[$n - 1] + $values[$n - 2] + $values[$n - 3];
    }
}

echo "\n";
echo end($values);