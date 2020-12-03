package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	file, _ := os.Open("input")
	defer file.Close()

	var tMap []string

	treeMultiplier := 1
	slopes := [][]int{
		{1, 1},
		{3, 1},
		{5, 1},
		{7, 1},
		{1, 2},
	}

	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		tMap = append(tMap, scanner.Text())
	}

	lineLength := len(tMap[0])
	lineCount := len(tMap)

	for i := 0; i < 5; i++ {
		posX := 0
		posY := 0
		treeCounter := 0

		for (posY + slopes[i][1]) <= lineCount {
			if tMap[posY][posX] == '#' {
				treeCounter++
			}

			posX = (posX + slopes[i][0]) % lineLength
			posY += slopes[i][1]
		}

		fmt.Println(treeCounter)
		treeMultiplier *= treeCounter
	}
	fmt.Println(treeMultiplier)
}
