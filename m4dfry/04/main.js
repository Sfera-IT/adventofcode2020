#!/usr/bin/node

const fs = require('fs');
const readline = require('readline');


async function processLineByLine() {
    const fileStream = fs.createReadStream('input');

    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });
    // Note: we use the crlfDelay option to recognize all instances of CR LF
    // ('\r\n') in input.txt as a single line break.

    var ret = [];

    for await (const line of rl) {
        ret.push(line);
    }

    return ret;
}

async function run() {
    const readIn = await processLineByLine();
    let res = 0;

    let passport = new Map();
    for (let i = 0; i < readIn.length; i++) {
        if (readIn[i] == "") {
            if (await checkPassportFirst(passport)) {
                res++;
            }

            passport = new Map();
        } else {
            const couples = readIn[i].split(" ")
            couples.forEach(couple => {
                const keyvalue = couple.split(':');
                passport[keyvalue[0].toString()] = keyvalue[1];
            });
        }
    }

    console.log("result:", res)
}

async function checkPassportFirst(pass) {
    const ruleValues = ['ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'];
    for (let i = 0; i < ruleValues.length; i++) {
        if (pass[ruleValues[i]] == null) {
            return false;
        }
    }
    return true;
}

async function checkPassport(pass) {
    const ruleValues = ['ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'];
    const colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'];

    for (let i = 0; i < ruleValues.length; i++) {
        if (pass[ruleValues[i]] == null) {
            return false;
        } else {
            const currentValue = pass[ruleValues[i]];
            let value = 0;
            switch (ruleValues[i]) {
                case 'byr':
                    value = parseInt(currentValue);
                    if (!(value >= 1920 && value <= 2002)) {
                        return false;
                    }
                    break;
                case 'iyr':
                    value = parseInt(currentValue);
                    if (!(value >= 2010 && value <= 2020)) {
                        return false;
                    }
                    break;
                case 'eyr':
                    value = parseInt(currentValue);
                    if (!(value >= 2020 && value <= 2030)) {
                        return false;
                    }
                    break;
                case 'hgt':
                    console.log(currentValue);
                    if (currentValue.includes("cm")) {
                        value = parseInt(currentValue.replace("cm", ""));
                        if (!(value >= 150 && value <= 193)) {
                            return false;
                        }
                    } else if (currentValue.includes("in")) {
                        value = parseInt(currentValue.replace("in", ""));
                        if (!(value >= 59 && value <= 76)) {
                            return false;
                        }
                    }
                    else {
                        return false;
                    }
                    break;
                /*
                    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
                    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
                    pid (Passport ID) - a nine-digit number, including leading zeroes.
                    cid (Country ID) - ignored, missing or not.
                */
                case 'hcl':
                    const rerr = /#[\da-f]{6}/;
                    if(!rerr.test(currentValue)){
                        return false;
                    }
                    break;
                case 'ecl':
                    if (!colors.includes(currentValue)) {
                        return false;
                    }
                    break;
                case 'pid':
                    const rorr = /[\d]{9}/;
                    if(!rorr.test(currentValue)){
                        return false;
                    }
                    break;
            }
        }
    }

    return true;
}


run();