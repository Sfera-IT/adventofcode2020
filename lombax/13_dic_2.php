<?php

/**
 * Spiegazione Teorema Cinese Del Resto
 * http://utenti.quipo.it/base5/numeri/teorcinese.htm
 *
 */

$data = file_get_contents('./13_dic.txt');

$rows = explode("\n", $data);

$minDeparture = $rows[0];
$buses = explode(",", $rows[1]);


// creo un array di obiettivi
// ad esempio 67,7,59,61 first occurs at timestamp 754018.
// gli obiettivi saranno 0, 6, 57, 58 (primo a 0, secondo a val - 1, terzo a val - 2 etc...)
// calcolo però usando il modulo per evitare di andare sotto zero con valori piccoli (es se sono all'index -10 ma il valore è 5, avrei risultato -5 che non va bene)
// dove ci sono le x inserisco comunque 0 per preservare l'indice
$objectives = [];
foreach ($buses as $k => $v) {
    if ($v == "x") {
        $objectives[] = 0;
    } else {
        if ($k == 0) {
            $objectives[] = 0;
        } else {
            $objectives[] = $v - $k % $v;
        }

    }

}

// calcolo il prodotto di tutti i bus, mi serve perchè è un numero sicuramente divisibile per ogni bus
// lo calcolo con un loop per escludere facilmente le x
$product = 1;
foreach ($buses as $bus) {
    if ($bus != "x") {
        $product = $product * $bus;
    }
}


// itero su tutti i bus (dalla chiave minima alla massima)
// per ogni bus, verifico quante volte sta nel prodotto sopra calcolato e uso quel valore come base
// poi aggiungo quel valore base a se stesso ciclicamente, finchè quel valore % valore del bus == valore obiettivo
// per intenderci al primo ciclo il valore prodotto è 1687931, il bus è 67, quindi 1687931/67 genera valore base di 25193
// Ora sommo 25193 + 25193 + .... finchè il valore risultante modulo 67 non darà il valore obiettivo, che nell'array "objectives" è
// allo stesso index del bus. In questo caso zero.
// al prossimo giro il bus sarà X e non avrà un valore obiettivo
// al giro dopo il bus sarà 7 e il valore obiettivo sarà 5 (-2)
// al giro dopo il bus sarà 59 e il valore obiettivo sarà 56 (-3)
// etc
// quando trovo che il modulo corrisponde al valore obiettivo, inserisco in un array il valore ottenuo sommando ciclicamente e break
$subProducts = [];
for ($i = 0; $i <= max(array_keys($buses)); $i++) {
    $bus = $buses[$i];

    if ($bus != "x") {
        $subProduct = $product / $bus;
        $base = $subProduct;
        $nextObjective = $objectives[$i];

        while (true) {
            $subProduct += $base;

            $rest = $subProduct % $bus;
            //echo "$i, $bus, $rest, $nextObjective \n";
            if ($rest == $nextObjective) {
                $subProducts[] = $subProduct;
                break;
            }

        }
    }
}

// sommo tutti i subproduct
$prodSum = array_sum($subProducts);

// ora dalla somma dei subproduct, che è molto alta, rimuovo product ciclicamente finchè la somma rimanente non è
// immediatamente minore di product. Questo dovrebbe essere il numero che sto cercando
while ($prodSum > $product) {
    $prodSum -= $product;
}

echo $prodSum."\n";