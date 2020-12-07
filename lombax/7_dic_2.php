<?php

$data = file_get_contents('./7_dic.txt');
$regex = "/(.*) bags contain (?:([0-9]* \w* \w*) (?:bag[s]?[\.]?[,]?[ ]?)*)(?:([0-9]* \w* \w*) (?:bag[s]?[\.]?[,]?[ ]?)*)?(?:([0-9]* \w* \w*) (?:bag[s]?[\.]?[,]?[ ]?)*)?(?:([0-9]* \w* \w*) (?:bag[s]?[\.]?[,]?[ ]?)*)?(?:([0-9]* \w* \w*) (?:bag[s]?[\.]?[,]?[ ]?)*)?(?:([0-9]* \w* \w*) (?:bag[s]?[\.]?[,]?[ ]?)*)?(?:([0-9]* \w* \w*) (?:bag[s]?[\.]?[,]?[ ]?)*)?(?:([0-9]* \w* \w*) (?:bag[s]?[\.]?[,]?[ ]?)*)?/";

$rows = explode("\n", $data);

$splitted = [];
$bags = [];
foreach ($rows as $row) {
    $res = [];
    $split = preg_match_all($regex, $row, $res);
    $splitted[] = $split;

    $color = $res[1][0];
    $contains = [];

    $stop = false;
    $i = 2;
    while ($stop == false) {
        $v = $res[$i][0];
        if ($v != "") {
            $vsplit = explode(" ", $v);
            $vnumber = $vsplit[0];
            $vcolor = $vsplit[1]." ".$vsplit[2];
            $contains[] = [$vnumber, $vcolor];
            $i++;
        } else {
            $stop = true;
        }
    }

    $bags[$color] = $contains;
}

$stop = false;
$count = count_child('shiny gold');
var_dump($bags);

function count_child($bagColor) {
    GLOBAL $bags;

    if (!isset($bags[$bagColor]))
        return 0;

    $bagContent = $bags[$bagColor];

    $count = 0;
    foreach ($bagContent as $bagDetails) {
        $count += $bagDetails[0];
        $count += $bagDetails[0] * count_child($bagDetails[1]);
    }

    return $count;

}


echo $count;