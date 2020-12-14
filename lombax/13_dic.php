<?php

$data = file_get_contents('./13_dic.txt');

$rows = explode("\n", $data);

$minDeparture = $rows[0];
$buses = explode(",", $rows[1]);

//remove x

$buses = array_filter($buses, function ($v) {
    if ($v == "x")
        return false;

    return true;
});


$busArray = [];
foreach ($buses as $bus) {
    $busArray[$bus] = 0;
    while ($busArray[$bus] < $minDeparture) {
        $busArray[$bus] += $bus;
    }
}

asort($busArray);

$keys = array_keys($busArray);
$values = array_values($busArray);

$diff = $values[0] - $minDeparture;
$res = $diff * $keys[0];
echo $diff;