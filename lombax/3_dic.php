<?php

$content = file_get_contents('./3_dic.txt');

$rows = explode("\n", $content);

$row = 0;
$col = 0;
$maxcol = strlen($rows[0]);
$maxrow = count($rows);


$trees = 0;
while (true) {
    $target = $rows[$row][$col];

    if ($target == "#")
        $trees++;

    increase($row, $col, $maxcol);

    if ($row >= $maxrow)
        break;
}

echo "\n Finish, total trees: $trees";

function increase(&$row, &$col, $maxcol) {
    $row += 1;
    $col += 3;
    if ($col >= $maxcol)
        $col = (($col % $maxcol));
}