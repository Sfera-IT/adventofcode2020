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

const regex = /([0-9]+)\-([0-9]+)\s([a-z])\:\s([a-z]+)/;

async function run() {
    const readIn = await processLineByLine();

    var found1 = 0;
    var found2 = 0;
    var count = 0;
    
    readIn.forEach(el => {
        var ind = el.split(regex);
        var objIn = {
            min: parseInt(ind[1]),
            max: parseInt(ind[2]),
            char: ind[3],
            pass: ind[4],
        };

        var passSplitted = objIn.pass.split(objIn.char);
        var charFound = passSplitted.length - 1;
        if( charFound >= objIn.min && charFound <= objIn.max) {
            found1++;
        }

        let occur = 0;
        var ar = objIn.pass.split('');
        if (ar[objIn.min - 1] == objIn.char) {
            occur++;
        }
        if(ar[objIn.max - 1] == objIn.char) {
            occur++;
        }

        if(occur == 1) {
            found2++;
        }

        count++
    });
    
    console.log("Found 1:", found1, count);
    console.log("Found 2:", found2, count);
}


run();