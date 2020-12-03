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
        ret.push(parseInt(line));
    }

    return ret;
}


async function run() {
    const readIn = await processLineByLine();

    readIn.forEach(el1 => {
        //console.log("debug:", el1)
        readIn.forEach(el2 => {
            if ((el1 + el2) == 2020) {
                console.log(el1, el2, (el1 * el2))
            }
        });
    });
}

async function run2() {
    const readIn = await processLineByLine();

    readIn.forEach(el1 => {
        readIn.forEach(el2 => {
            readIn.forEach(el3 => {
                if ((el1 + el2 + el3) == 2020) {
                    console.log(el1, el2, el3, (el1 * el2 * el3))
                }
            });
        });
    });
}

run2();