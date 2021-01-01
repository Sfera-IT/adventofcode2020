<?php

$data = file_get_contents('./20_dic.txt');
$tiles_raw = explode("\n\n", $data);

$tiles = [];

// init tiles
$tileMap = [];
foreach ($tiles_raw as $tile_raw) {
    $tile = explode("\n", $tile_raw);

    $newTile = [];
    foreach ($tile as $row) {
        $newTile[] = str_split($row);
    }

    $id = array_shift($newTile); // remove first line
    $id = str_replace(":", "", str_replace("Tile ", "", implode("", $id)));

    $newTile = new Tile($id, $newTile);
    $tiles[] = $newTile;
    $tileMap[$id] = $newTile;
}

// find common members
$associationMap = [];
$rightAssociationMap = [];
$bottomAssociationMap = [];

for ($i = 0; $i < count($tiles); $i++) {
    for ($j = 0; $j < count($tiles); $j++) {
        $t1 = $tiles[$i];
        $t2 = $tiles[$j];

        if ($t1->id != $t2->id) {

            if ($t1->hasCommonBorders($t2)) {
                $associationMap[$t1->id][] = $t2->id;
            }
        }
    }
}

// start to create matrix from corners
uasort($associationMap, function($a, $b) {
    return (count($a) <=> count($b));
});

$firstCornerID = array_keys($associationMap)[0];
$firstCorner = $tileMap[$firstCornerID];

// create matrix

$squareSize = sqrt(count($tiles));
$matrix[0][0] = $firstCorner;
$previous = $firstCorner;
$firstOfTheLine = $firstCorner;
$tileMapTemp = $tileMap;

$i = 0;
$j = 1;

while (true) {

    $rightFound = false;
    foreach ($tileMapTemp as $tile) {
        $res = $previous->attachRight($tile);

        if ($res) {
            $matrix[$i][$j] = $res;
            $previous = $res;
            $j++;
            $rightFound = true;
            break;
        }
    }

    if ($rightFound) {
        // remove the previous tile from $tiles
        unset($tileMapTemp[$previous->id]);
    } else {
        // not found, posso essere al bordo (lo capisco dal valore di $j)
        // oppure sono nella strada sbagliata, riavvolgo

        if ($j == $squareSize) {
            // sono al bordo, cambio riga
            $i++;

            if ($i == $squareSize && $j == $squareSize) {
                // FINITO
                break;
            }

            $j = 0;

            $bottomFound = false;
            foreach ($tileMapTemp as $tile) {
                $res = $firstOfTheLine->attachBottom($tile);

                if ($res) {
                    $matrix[$i][$j] = $res;
                    $firstOfTheLine = $res;
                    $previous = $res;
                    $bottomFound = true;
                    $j++;
                    break;
                }
            }
            if (!$bottomFound) {
                // devo riavvolgere e girare il primo
                $firstCorner->nextMode();
                $matrix[0][0] = $firstCorner;
                $i = 0;
                $j = 1;
                $previous = $firstCorner;
                $firstOfTheLine = $firstCorner;
                $tileMapTemp = $tileMap;
            }
        } else {
            // devo riavvolgere e girare il primo
            $firstCorner->nextMode();
            $matrix[0][0] = $firstCorner;
            $i = 0;
            $j = 1;
            $previous = $firstCorner;
            $firstOfTheLine = $firstCorner;
            $tileMapTemp = $tileMap;
        }
    }
}

// print the big tile removing borders
$bigTile = "";

foreach ($matrix as $row) {
    for ($i = 1; $i < 9; $i++) {
        foreach ($row as $singleTile) {
            $tile = $singleTile->get();
            $tileReduced = array_slice($tile[$i], 1, -1);
            $bigTile .= "".implode("", $tileReduced);
        }
        $bigTile .= "\n";
    }
}

// create a new big tile class
$bigTile = rtrim($bigTile);

$tile = explode("\n", $bigTile);

$newTile = [];
foreach ($tile as $row) {
    $newTile[] = str_split($row);
}

$newBigTile = new Tile(10000, $newTile);

$monster = '                  # 
#    ##    ##    ###
 #  #  #  #  #  #   ';

// find the central line of the monster (all occurrences) then check top and bottom
$candidateMonster = '/(?=(#....##....##....###))/'; // qui uso un lookahead altrimenti non becca gli overlapping https://stackoverflow.com/questions/22454032/preg-match-all-how-to-get-all-combinations-even-overlapping-ones
$candidateMonsterTop = '/..................#./';
$candidateMonsterBottom = '/.#..#..#..#..#..#.../';

$monsterMatches = 0;
for($mode = 0; $mode <= 7; $mode++) {
    $bigTileString = $newBigTile->print();

    $matches = [];
    $candidates = preg_match_all($candidateMonster, $bigTileString, $matches);

    if (count($matches) > 0) {
        foreach ($matches[1] as $match) {
            $pos = strpos($bigTileString, $match);
            $upperPos = $pos - count($newBigTile->get()[0]) - 1;
            $lowerPos = $pos + count($newBigTile->get()[0]) + 1;

            $upperSubstr = substr($bigTileString, $upperPos, strlen($candidateMonsterTop)-2);
            $lowerSubstr = substr($bigTileString, $lowerPos, strlen($candidateMonsterBottom)-2);

            $match1 = preg_match($candidateMonsterTop, $upperSubstr);
            $match2 = preg_match($candidateMonsterBottom, $lowerSubstr);

            if ($match1 && $match2)
                $monsterMatches++;
        }

        if ($monsterMatches) {
            break;
        }
    }

    $newBigTile->nextMode();
}

$monsterItems = substr_count($monster, '#');
$remove = $monsterItems * $monsterMatches;

$t = substr_count($bigTileString, '#');
$total = substr_count($bigTileString, '#') - $remove;

echo "found $monsterMatches monsters, there is a total of $t # and removing $remove \n";

echo $total;

class Tile
{

    protected $originalTile = [];
    protected $tile = [];
    public $id = 0;


    public $modes = []; // 0 original, 1 +90 clockw, 2 +180, 3 +270, 4 original flip hr, 5 +90, 6 +180, 7 +270
    public $sides = []; // array of arrays, [$mode][$side]. 0 top, 1 right, 2 bottom, 3 left
    /**
     * Association contains
     *
     * [
     *  'this_id' => xxx,
     * 'other_id' => xxx,
     * 'this_mode' => xxx,
     * 'other_mode' => xxx,
     * 'this_side' => xxx,
     * 'other_side' => xxx,
     * ]
     */
    public $associations = [];
    public $rightAssociations = [];
    public $bottomAssociations = [];

    protected $actualMode = 0;
    protected $blocked = false;


    public function __construct(int $id, array $tile)
    {
        $this->id = $id;
        $this->tile = $tile;
        $this->originalTile = $this->tile;

        for($i = 0; $i <= 7; $i++) {
            $this->modes[$i] = $this->tile;
            $this->borders[$i] = $this->createBorders();
            $this->nextMode();
        }
    }

    public function get(): array {
        return $this->tile;
    }

    public function print() : string {
        $output = "";
        foreach ($this->tile as $row) {
            $output .= implode("", $row)."\n";
        }

        $output = rtrim($output);

        return $output;
    }

    public function getBorders(int $mode) : array
    {
        return $this->borders[$mode];
    }


    public function isCorner() {
        if (count($this->associations) == 2)
            return true;
        return false;
    }

    public function isSide() {
        if (count($this->associations) == 3)
            return true;
        return false;
    }

    public function isCentral() {
        if (count($this->associations) == 4)
            return true;
        return false;
    }

    public function isBlocked() : bool
    {
        return $this->blocked;
    }

    /**
     * @return int
     */
    public function getActualMode(): int
    {
        return $this->actualMode;
    }


    protected function rotate90() {
        if (!$this->blocked) {
            $matrix = $this->tile;
            $height = count($matrix);
            $width = count($matrix[0]);
            $mat90 = array();

            for ($i = 0; $i < $width; $i++) {
                for ($j = 0; $j < $height; $j++) {
                    $mat90[$height - $i - 1][$j] = $matrix[$height - $j - 1][$i];
                }
            }

            $mat90 = array_values($mat90); // reset keys

            $this->tile = $mat90;

        } else {
            throw new \Exception('Trying to rotate a locked tile');
        }
    }

    protected function flipHorizontal() {
        if (!$this->blocked) {
            $tile = $this->tile;
            $newTile = [];
            foreach ($tile as $tilerow) {
                $newTile[] = array_reverse($tilerow);
            }
            $this->tile = $newTile;
        } else {
            throw new \Exception('Trying to flip a locked tile');
        }
    }

    public function nextMode() : int {

        if (!$this->blocked) {
            if ($this->actualMode == 7)
            {
                // come back to 0 original tile
                $this->tile = $this->originalTile;
                $this->actualMode = 0;
            } else if ($this->actualMode == 3){
                // come back to 0 original tile and then flip
                $this->tile = $this->originalTile;
                $this->flipHorizontal();
                $this->actualMode++;
            } else {
                $this->rotate90();
                $this->actualMode++;
            }

            return $this->actualMode;
        } else {
            throw new \Exception('Trying to next mode a locked tile');
        }

    }

    protected function createBorders() : array
    {
        $version = $this->tile;
        $borders = [];
        $borders[0] = $version[0];                      // top
        $borders[1] = [];                               // right (top-to-bottom)
        $borders[2] = $version[count($version)-1];      // bottom
        $borders[3] = [];                               // left (top-to-bottom)

        for ($i = 0; $i < count($version); $i++) {
            $borders[3][] = $version[$i][0];
            $borders[1][] = $version[$i][count($version)-1];
        }

        return $borders;

    }

    public function getRightTile() {
        $association = array_filter($this->rightAssociations, function ($v) {
            if ($v['this_side'] == 1 && $v['this_mode'] == $this->actualMode)
                return true;
            return false;
        });

        $association = array_values($association);

        if (count($association) > 1)
        {
            throwException('Troppe associazioni a destra, errore');
        }

        if (count($association) == 1)
        {
            return $association[0]['other_id'];
        } else {
            return null;
        }

    }

    public function getBottomTile() {
        $association = array_filter($this->bottomAssociations, function ($v) {
            if ($v['this_side'] == 2 && $v['this_mode'] == $this->actualMode)
                return true;
            return false;
        });

        if (count($association) > 1)
        {
            throwException('Troppe associazioni sotto, errore');
        }

        if (count($association) == 1)
        {
            return $association[0]['other_id'];
        } else {
            return null;
        }

    }


    public function hasCommonBorders($newTile) {

        /**
         * @var $t1 Tile
         * @var $t2 Tile
         */
        $t1 = $this;
        $t2 = $newTile;

        for($t1Mode = 0; $t1Mode <= 7; $t1Mode++) {
            for($t2Mode = 0; $t2Mode <= 7; $t2Mode++) {

                for ($i = 0; $i <= 3; $i++) {
                    for ($j = 0; $j <= 3; $j++) {
                        $t1Borders = $t1->getBorders($t1Mode);
                        $t2Borders = $t2->getBorders($t2Mode);
                        if ($t1Borders[$i] == $t2Borders[$j]) {
                            $t1->associations[] = [
                                'this_id' => $t1->id,
                                'other_id' => $t2->id,
                                'this_mode' => $t1Mode,
                                'other_mode' => $t2Mode,
                                'this_side' => $i,
                                'other_side' => $j,
                            ];

                            // block them
                            $t1->actualMode = $t1Mode;
                            $t1->tile = $t1->modes[$t1Mode];
                            $t2->actualMode = $t2Mode;
                            $t2->tile = $t2->modes[$t2Mode];

                            return true;
                        }
                    }
                }
            }
        }

        return false;
    }
    
    public function attachRight(Tile $rightCandidate)
    {
        $t1 = $this;
        $t2 = $rightCandidate;

        if ($t1->id == $t2->id)
            return false;

        $t1Borders = $t1->getBorders($t1->getActualMode());
        $t1RightBorder = $t1Borders[1];

        for($mode = 0; $mode <= 7; $mode++) {
            $t2Borders = $t2->getBorders($t2->getActualMode());
            $t2LeftBorder = $t2Borders[3];

            if ($t1RightBorder == $t2LeftBorder) {
                return $t2;
            }

            $t2->nextMode();
        }

        return false;
    }

    public function attachBottom(Tile $rightCandidate)
    {
        $t1 = $this;
        $t2 = $rightCandidate;

        if ($t1->id == $t2->id)
            return false;

        $t1Borders = $t1->getBorders($t1->getActualMode());
        $t1BottomBorder = $t1Borders[2];

        for($mode = 0; $mode <= 7; $mode++) {
            $t2Borders = $t2->getBorders($t2->getActualMode());
            $t2TopBorder = $t2Borders[0];

            if ($t1BottomBorder == $t2TopBorder) {
                return $t2;
            }

            $t2->nextMode();
        }

        return false;
    }
}