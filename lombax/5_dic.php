<?php
/**
 * 12.55 - 13.09 - 13.14
 *
 */

$file = file_get_contents('./5_dic.txt');
$fileRows = explode("\n", $file);

$max = 0;
$ids = [];
foreach ($fileRows as $fileRow) {

    $code = $fileRow;
    $start = 0;
    $end = 127;

    for ($i = 0; $i < 7; $i++) {
        // first 7 letters

        if ($code[$i] == "F")
        {
            // start invariato
            $end = intdiv($end-$start, 2) + $start;
        } else if ($code[$i] == "B") {
            $start = intdiv($end-$start, 2) + 1 + $start;
            // end invariato
        } else {
            echo "non dovrebbe accadere \n";
        }
    }

    if ($start != $end) {
        die("non dovrebbe accadere nemmeno questo");
    }

    $row = $start;


    $start = 0;
    $end = 7;
    for ($i = 7; $i < 10; $i++) {
        if ($code[$i] == "L")
        {
            // start invariato
            $end = intdiv($end-$start, 2) + $start;
        } else if ($code[$i] == "R") {
            $start = intdiv($end-$start, 2) + 1 + $start;
            // end invariato
        } else {
            echo "non dovrebbe accadere \n";
        }
    }

    $column = $start;
    $id = $row*8+$column;

    echo "Row: $row Column: $column Id: $id \n";

    if ($max < $id)
        $max = $id;

    $ids[] = $id;
}

// ex 1
echo $max;

// ex 2

sort($ids);

$min = min($ids);
$max = max($ids);

$candidates = [];
for ($i = $min; $i < $max; $i++) {
    if (!in_array($i, $ids)) {
        $candidates[] = $i;
    }
}

var_dump($candidates);