package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strings"
)

var end string = `(\s+|$)`
var res = []*regexp.Regexp{
	regexp.MustCompile(`byr:(19[2-9]\d|200[0-2])` + end),
	regexp.MustCompile(`iyr:(201\d|2020)` + end),
	regexp.MustCompile(`eyr:(202\d|2030)` + end),
	regexp.MustCompile(`hgt:((1[5-8]\d|19[0-3])cm|(59|6\d|7[0-6])in)` + end),
	regexp.MustCompile(`hcl:#[\da-f]{6}` + end),
	regexp.MustCompile(`ecl:(amb|blu|brn|gry|grn|hzl|oth)` + end),
	regexp.MustCompile(`pid:\d{9}` + end),
}

func main() {
	input, _ := ioutil.ReadFile("input")
	valid := 0

	for _, s := range strings.Split(strings.TrimSpace(string(input)), "\n\n") {
		check := true
		for _, re := range res {
			if !re.MatchString(s) {
				check = false
			}
		}
		if check {
			valid++
		}

	}
	fmt.Println(valid)
}
