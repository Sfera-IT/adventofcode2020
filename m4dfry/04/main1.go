package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

func main() {
	input, _ := ioutil.ReadFile("input")
	valid := 0

	for _, s := range strings.Split(strings.TrimSpace(string(input)), "\n\n") {
		check := true
		for _, f := range []string{"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"} {
			if ok := strings.Contains(s, f); !ok {
				check = false
			}
		}
		if check {
			valid++
		}
	}
	fmt.Println(valid)
}
