<?php

/**
 * 10.20 - 10.24 - 10.30
 * 
 *
 */
$data = file_get_contents('./9_dic.txt');
$rows = explode("\n", $data);

$find = 26134589;

$sum = 0;
$arr = [];
$prevI = 0;
for ($i = $prevI; $i < count($rows); $i++) {
   $sum += $rows[$i];
   $arr[] = $rows[$i];


   if ($sum == $find) {
       echo $sum."\n";
       echo min($arr)+max($arr);

       die('found');

   }

   if ($sum > $find) {
       $i = $prevI + 1;
       $prevI = $i;
       $sum = 0;
       $arr = [];
   }
}

echo "not found";