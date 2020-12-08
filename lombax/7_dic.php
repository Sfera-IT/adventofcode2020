<?php

// refactory secondo metodo di Sharpedge

$regex1 = "/(.*) contain (.*)/";
$regex2 = "/\d (.*?)s?(?:,|$)/";

$data = file_get_contents('./7_dic.txt');
$rows = explode("\n", $data);

$items = [];
foreach ($rows as $row) {
    preg_match_all($regex1, $row, $matches);
    preg_match_all($regex2, implode("\n", $matches[2]), $matches2);
    $items[$matches[1][0]] = $matches2[1];
}

$stack = ['shiny gold bag'];
$res = [];
$i = 0;
while (count($stack) > 0) {
    foreach ($items as $bag => $contains) {
        foreach ($contains as $singleContains) {
            if (strpos($singleContains, $stack[0]) !== false) {
                $stack[] = substr($bag, 0, -1); //remove last s
                $res[] = $bag;
            }
        }

    }

    $i++;

    array_shift($stack);
}

$final = array_unique($res);

echo count($final);

// ---- EX 2

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

echo "\n";

echo $count;