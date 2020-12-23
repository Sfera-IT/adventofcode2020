<?php

class Tile {

    private $originalMatrix;
    public $id;

    public $versions = [];
    public $borders = [];

    public function __construct($id, $originalMatrix)
    {
        $this->originalMatrix = $originalMatrix;
        $this->id = $id;

        $versions[0] = $originalMatrix;
        $versions[1] = $this->getRotated90($originalMatrix); // 90
        $versions[2] = $this->getRotated90($versions[1]); // 180
        $versions[3] = $this->getRotated90($versions[2]); // 270
        $versions[4] = $this->getFlippedHorizontal(); // horizontal flip
        $versions[5] = $this->getRotated90($versions[4]); // 90 hr flip
        $versions[6] = $this->getRotated90($versions[5]); // 180 hr flip
        $versions[7] = $this->getRotated90($versions[6]); // 270 hr flip
        $versions[8] = $this->getFlippedVertical(); // vertical flip
        $versions[9] = $this->getRotated90($versions[8]); // 90 v flip
        $versions[10] = $this->getRotated90($versions[9]); // 180 v flip
        $versions[11] = $this->getRotated90($versions[10]); // 270 v flip

        $this->versions = $versions;


        foreach ($this->versions as $version) {

            $borders = [];
            $borders[0] = $version[0];
            $borders[1] = [];
            $borders[2] = [];
            $borders[3] = $version[count($version)-1];

            for ($i = 0; $i < count($version); $i++) {
                $borders[1][] = $version[$i][0];
                $borders[2][] = $version[$i][count($version)-1];
            }

            $this->borders = array_merge($this->borders, $borders);
        }

        // rendo unici i bordi da confrontare, ma dato che php è scemo e array_unique sembra non funzionare su array di array
        // allora li converto in array di stringhe, li uniquizzo, resetto le chiavi e poi li riconverto in array di array
        $this->borders = array_map(
            function($v) {
                return implode("", $v);
            },
            $this->borders
        );

        $this->borders = array_unique($this->borders);
        $this->borders = array_values($this->borders); // reset keys

        $this->borders = array_map(
            function($v) {
                return str_split($v);
            },
            $this->borders
        );


    }

    private function getFlippedHorizontal() {
        $tile = $this->originalMatrix;
        $newTile = [];
        foreach ($tile as $tilerow) {
            $newTile[] = array_reverse($tilerow);
        }
        return $newTile;
    }

    private function getFlippedVertical() {
        $tile = $this->originalMatrix;
        $newTile = [];
        for ($i = count($tile) - 1; $i >= 0 ; $i--) {
            $tilerow = $tile[$i];
            $newTile[] = $tilerow;
        }
        return $newTile;
    }

    private function getRotated90($matrix) {
        $height = count($matrix);
        $width = count($matrix[0]);
        $mat90 = array();

        for ($i = 0; $i < $width; $i++) {
            for ($j = 0; $j < $height; $j++) {
                $mat90[$height - $i - 1][$j] = $matrix[$height - $j - 1][$i];
            }
        }

        $mat90 = array_values($mat90); // reset keys
        return $mat90;
    }


}


$data = file_get_contents('./20_dic.txt');
$tiles_raw = explode("\n\n", $data);

$tiles = [];

foreach ($tiles_raw as $tile_raw) {
    $tile = explode("\n", $tile_raw);

    $newTile = [];
    foreach ($tile as $row) {
        $newTile[] = str_split($row);
    }

    $id = array_shift($newTile); // remove first line
    $id = str_replace(":", "", str_replace("Tile ", "", implode("", $id)));

    $tiles[] = new Tile($id, $newTile);
}

$matchesPerTile = [];
$associations = [];
for ($i = 0; $i < count($tiles); $i++) {
    for ($j = 0; $j < count($tiles); $j++) {
        $t1 = $tiles[$i];
        $t2 = $tiles[$j];

        if ($t1->id != $t2->id) {

            if (has_common_members($t1, $t2)) {
                $associations[$t1->id][] = $t2->id;

                $matchesPerTile[$t1->id][] = $t2;
            }

        }
    }
}

// ordino dal minore al maggiore
uasort($associations, function($a, $b) {
    return (count($a) <=> count($b));
});

// prendo i primi 4, dovrebbero essere i corner
$corners = array_slice(array_keys($associations), 0, 4);
echo array_product($corners);


function has_common_members($t1, $t2) {

    for ($i = 0; $i < count($t1->borders); $i++) {
        for ($j = 0; $j < count($t2->borders); $j++) {
            if ($t1->borders[$i] == $t2->borders[$j]) {
                return true;
            }
        }
    }
    return false;
}