<?php
$res1 = 0;
$res2 = 0;

$file = file_get_contents('./../data/2.txt');
$lines = explode(PHP_EOL, $file);

foreach ($lines as $line) {
    $values = explode(" ", $line);
    $rules = explode("-", $values[0]);
    $min = $rules[0];
    $max = $rules[1];
    $value = substr($values[1], 0, 1);
    $password = $values[2];

    $risultato = substr_count($password, $value);

    if (($risultato >= $min) and ($risultato <= $max)) {
        $res1++;
    }

    $char = substr($password, $min - 1, 1);
    $char .= substr($password, $max - 1, 1);
    $check = substr_count($char, $value);

    if ($check == 1)
        $res2++;
}
echo "*";
echo "\n";
echo $res1;
echo "\n";
echo "**";
echo "\n";
echo $res2;
