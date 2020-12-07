<?php

$data = file_get_contents('./7_dic.txt');

$rows = explode("\n", $data);

/**
 *
 *  FA SCHIFO NON GUARDARE QUESTO ESERCIZIO, LO DEVO RIFARE
 *  FA SCHIFO NON GUARDARE QUESTO ESERCIZIO, LO DEVO RIFARE
 *  FA SCHIFO NON GUARDARE QUESTO ESERCIZIO, LO DEVO RIFARE
 *  FA SCHIFO NON GUARDARE QUESTO ESERCIZIO, LO DEVO RIFARE
 *  FA SCHIFO NON GUARDARE QUESTO ESERCIZIO, LO DEVO RIFARE
 *  FA SCHIFO NON GUARDARE QUESTO ESERCIZIO, LO DEVO RIFARE
 *  FA SCHIFO NON GUARDARE QUESTO ESERCIZIO, LO DEVO RIFARE
 *
 *
 *
 *
 *
 */


// prima trovo i colori che possono contenere una shiny gold
$possible_colors = [];
foreach ($rows as $row) {
    // shiny gold deve essere presente nella stringa ma non in posizione zero
    if (strpos($row, "shiny gold") !== false && strpos($row, "shiny gold") !== 0) {
        // è presente, per trovare il colore che la contiene prendo le prime 2 parole e la aggiungo all'array
        $r_exploded = explode(" ", $row);
        $colors = $r_exploded[0]." ".$r_exploded[1];
        $possible_colors[] = $colors;
    }
}

$possible_colors_2 = [];
foreach ($possible_colors as $possibleColor) {
    foreach ($rows as $row) {
        if (strpos($row, $possibleColor) !== false && strpos($row, $possibleColor) !== 0) {
            $r_exploded = explode(" ", $row);
            $colors = $r_exploded[0]." ".$r_exploded[1];
            $possible_colors_2[] = $colors;
        }
    }
}

$possible_colors_3 = [];
foreach ($possible_colors_2 as $possibleColor) {
    foreach ($rows as $row) {
        if (strpos($row, $possibleColor) !== false && strpos($row, $possibleColor) !== 0) {
            $r_exploded = explode(" ", $row);
            $colors = $r_exploded[0]." ".$r_exploded[1];
            $possible_colors_3[] = $colors;
        }
    }
}

$possible_colors_4 = [];
foreach ($possible_colors_3 as $possibleColor) {
    foreach ($rows as $row) {
        if (strpos($row, $possibleColor) !== false && strpos($row, $possibleColor) !== 0) {
            $r_exploded = explode(" ", $row);
            $colors = $r_exploded[0]." ".$r_exploded[1];
            $possible_colors_4[] = $colors;
        }
    }
}

$possible_colors_5 = [];
foreach ($possible_colors_4 as $possibleColor) {
    foreach ($rows as $row) {
        if (strpos($row, $possibleColor) !== false && strpos($row, $possibleColor) !== 0) {
            $r_exploded = explode(" ", $row);
            $colors = $r_exploded[0]." ".$r_exploded[1];
            $possible_colors_5[] = $colors;
        }
    }
}

$possible_colors_6 = [];
foreach ($possible_colors_5 as $possibleColor) {
    foreach ($rows as $row) {
        if (strpos($row, $possibleColor) !== false && strpos($row, $possibleColor) !== 0) {
            $r_exploded = explode(" ", $row);
            $colors = $r_exploded[0]." ".$r_exploded[1];
            $possible_colors_6[] = $colors;
        }
    }
}

$possible_colors_7 = [];
foreach ($possible_colors_6 as $possibleColor) {
    foreach ($rows as $row) {
        if (strpos($row, $possibleColor) !== false && strpos($row, $possibleColor) !== 0) {
            $r_exploded = explode(" ", $row);
            $colors = $r_exploded[0]." ".$r_exploded[1];
            $possible_colors_7[] = $colors;
        }
    }
}

$possible_colors_8 = [];
foreach ($possible_colors_7 as $possibleColor) {
    foreach ($rows as $row) {
        if (strpos($row, $possibleColor) !== false && strpos($row, $possibleColor) !== 0) {
            $r_exploded = explode(" ", $row);
            $colors = $r_exploded[0]." ".$r_exploded[1];
            $possible_colors_8[] = $colors;
        }
    }
}

$possible_colors_9 = [];
foreach ($possible_colors_8 as $possibleColor) {
    foreach ($rows as $row) {
        if (strpos($row, $possibleColor) !== false && strpos($row, $possibleColor) !== 0) {
            $r_exploded = explode(" ", $row);
            $colors = $r_exploded[0]." ".$r_exploded[1];
            $possible_colors_9[] = $colors;
        }
    }
}


$merge = array_merge($possible_colors_2, $possible_colors, $possible_colors_3, $possible_colors_4, $possible_colors_5, $possible_colors_6, $possible_colors_7, $possible_colors_8, $possible_colors_9);
$unique = array_unique($merge);
echo count($unique);

//
//
//// $possible_colors ora contiene solo i colori che possono contenere all'interno una shiny gold
//// reitero
//
//$count = 0;
//foreach ($rows as $row) {
//    // smonto la riga, tolgo il primo colore e la rimonto
//    $r_exploded = explode(" ", $row);
//    array_shift($r_exploded);
//    array_shift($r_exploded);
//    $row_imploded = implode(" ", $r_exploded);
//
//    // per ogni possibile color, verifico che sia presente nella riga, se si può contenere una shiny gold
//    foreach ($possible_colors as $possibleColor) {
//        if (strpos($row_imploded, $possibleColor) !== false) {
//            $count += 1;
//            break;
//        }
//    }
//}

//echo $count;
