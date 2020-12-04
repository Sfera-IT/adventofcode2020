<?php
$file = file_get_contents('./2_dic.txt');

$lines = explode("\n", $file);


$totExercise1 = 0;
$totExercise2 = 0;
foreach ($lines as $line) {

    $items = explode(" ", $line);

    $policy = explode("-", $items[0]);
    $policy_from = $policy[0];
    $policy_to = $policy[1];
    $letter = substr($items[1], 0 , 1);
    $password = $items[2];

    $count = substr_count($password, $letter);

    if ($count <= $policy_to && $count >= $policy_from) {
        $totExercise1++;
    }

    // -----
    // Exercise 2


    $l = substr($password, $policy_from-1, 1);
    $l .= substr($password, $policy_to-1, 1);
    $count2 = substr_count($l, $letter);

    echo "Password is: ".$password." and we found $l in index $policy_from and $policy_to \n";
    if ($count2 == 1)
        $totExercise2++;

}

echo $totExercise1;
echo "\n";
echo $totExercise2;