<?php

/**
 * 12.36 12.51 13.06
 * 30 minuti totali
 * di cui 15 il primo a 15 il secondo
 *
 */

$data = file_get_contents('8_dic.txt');
$rows = explode("\n", $data);



$acc = 0;
$jumpIndexes = [];
$already_executed_rows = [];

for ($i = 0; $i < $rows; $i++) {
    if (in_array($i, $already_executed_rows))
        break;
    $already_executed_rows[] = $i;
    command($rows[$i], $i);

}

$jumpReverse = array_reverse($jumpIndexes);

foreach ($jumpReverse as $jumpToJump) {
    // rieseguo il programma
    $acc = 0;
    $jumpIndexes = [];
    $already_executed_rows = [];

    for ($i = 0; $i < count($rows); $i++) {
        if (in_array($i, $already_executed_rows))
            break;
        $already_executed_rows[] = $i;
        if ($i != $jumpToJump)
            command($rows[$i], $i);

    }

    $maxIndex = count($rows);
    echo "Acc is: $acc and Index Is $i on $maxIndex. \n";
}


function command($row, &$index) {
    global $acc;
    global $jumpIndexes;

    $commands = explode(" ", $row);
    $command = $commands[0];
    $qt = intval($commands[1]);

    switch ($command) {
        case "acc":
            $acc += $qt;
            break;
        case "jmp":
            $jumpIndexes[] = $index;
            $index += $qt-1;
            break;
        case "nop":

            break;
    }
}