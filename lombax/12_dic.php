<?php
/**
 * 15.27 - 16.00
 */
$data = file_get_contents('./12_dic.txt');
$rows = explode("\n", $data);

$ship = new Ship();

foreach ($rows as $row) {
    $action = substr($row, 0, 1);
    $number = substr($row, 1, strlen($row) - 1);
    $ship->doAction($action, $number);
}

echo $ship->manhattanDistance();


class Ship {

    public $x = 0;
    public $y = 0;

    public $direction = 1; // 0 north, 1 east, 2 south, 3 west, start by facing east

    public function manhattanDistance() {
        return abs($this->x) + abs($this->y);
    }

    public function doAction($action, $number) {


        switch ($action) {
            case "L":
            case "R":
                $this->direction = $this->calculateDirectionFromDirectionAndDegrees($this->direction, $action, $number);
                break;
            case "F":
                $this->moveForward($number, $this->direction);
                break;
            case "N":
                $this->moveForward($number, 0);
                break;
            case "E":
                $this->moveForward($number, 1);
                break;
            case "S":
                $this->moveForward($number, 2);
                break;
            case "W":
                $this->moveForward($number, 3);
                break;
        }
    }

    public function moveForward($units, $direction) {
        switch ($direction) {
            case 0:
                $this->y += $units;
                break;
            case 1:
                $this->x += $units;
                break;
            case 2:
                $this->y -= $units;
                break;
            case 3:
                $this->x -= $units;
                break;
        }
    }

    public function calculateDirectionFromDirectionAndDegrees($originalDirection, $newDirection, $degrees)
    {
        if ($newDirection == "L" && $degrees != 180) {
            $degrees += 180;
        }

        $add = ($degrees / 90);
        $newDirection = $originalDirection+$add;
        $newDirection = $newDirection % 4;

        return $newDirection;
    }

}