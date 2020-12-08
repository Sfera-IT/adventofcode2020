<?php

/**
 * 12.36 12.51
 */

$data = file_get_contents('8_dic.txt');
$rows = explode("\n", $data);



$acc = 0;
$already_executed_rows = [];

for ($i = 0; $i < $rows; $i++) {
    if (in_array($i, $already_executed_rows))
        break;
    $already_executed_rows[] = $i;
    command($rows[$i], $i);

}
echo $acc;


function command($row, &$index) {
    global $acc;

    $commands = explode(" ", $row);
    $command = $commands[0];
    $qt = intval($commands[1]);

    switch ($command) {
        case "acc":
            $acc += $qt;
            break;
        case "jmp":
            $index += $qt-1;
            break;
        case "nop":

            break;
    }
}