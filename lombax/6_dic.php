<?php
$file = file_get_contents('./6_dic.txt');
$groups = explode("\n\n", $file);


$total = 0;
foreach ($groups as $singleGroup) {
    $different = different($singleGroup);

    $total += $different;
}

echo $total;
echo "\n";



// ex 2
$total2 = 0;
foreach ($groups as $singleGroup) {
    $people = explode("\n", $singleGroup);

    $arr = str_split($people[0]);
    foreach ($people as $p) {
        $a = str_split($p);
        $arr = array_intersect($arr, $a);
    }

    $total2 += count($arr);
}

echo $total2;
function different($str) {
    $str = str_replace("\n", "", $str); // remove carriage return

    return count(array_unique( str_split( $str)));
}