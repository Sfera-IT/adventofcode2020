<?php
$tot = 2020;
echo "*<br>";

$file = file_get_contents('./../data/1.txt');
$numbers = explode(PHP_EOL, $file);

$cnt = count($numbers);
$candidates = [];

for ($i = 0; $i < $cnt; $i++) {
    for ($j = 0; $j < $cnt; $j++) {
        $tmp = $numbers[$i] + $numbers[$j];

        if ($tmp == $tot) {
            $candidates[] = [$numbers[$i], $numbers[$j]];
        }
    }
}
print_r($candidates); // 1704 * 316
echo 1704*316;
die();

$conts = file_get_contents('1.txt');
$cont = explode(";", $conts);
$numbers = array();
foreach ($cont as $num) {
    $numbers[] = intval($num);
}
$removed = array_pop($numbers);
// print_r($numbers);
// $mins = array();
// foreach ($numbers as $number) {
//     if ($number < 1853)
//         $mins[] = $number;
// }
$tot = count($numbers) - 1;
$tots = array();
foreach ($numbers as $item) {
    for ($i = 0; $i <= $tot; $i++) {
        #echo $item." ".$mins[$i];
        if ($item + $numbers[$i] < $SUM) {
            $tots[] = $item + $numbers[$i];
        }
        if ($item + $numbers[$i] == $SUM) {
            $res = $item * $numbers[$i];
            echo $res;
            echo "<br>";
        }
    }
}

// $tots = array();
// foreach ($numbers as $item) {
//     for ($i = 0; $i <= $tot; $i++) {
//         #echo $item." ".$mins[$i];
//         if ($item + $numbers[$i] == $SUM2) {
//             $res = $item * $numbers[$i];
//             echo $item ." ". $numbers[$i];
//             echo "<br>";
//         }
//     }
// }

// print_r($tots);
echo $res;
echo "**<br>";
echo "615 903 502";
echo "278783190";
foreach ($tots as $item) {
    for ($i = 0; $i <= $tot; $i++) {
        // echo $item . " + " . $numbers[$i] . " + " . $numbers[$k] . "=" . $item + $numbers[$i] + $numbers[$k]."<br>";
        if ($item + $numbers[$i] == $SUM) {
            echo $item . " + " . $numbers[$i] . "=" . $item + $numbers[$i] . "<br>";
            // $res = $item * $numbers[$i];
            // echo "########" . $res . "#########";
        }
    }
}
