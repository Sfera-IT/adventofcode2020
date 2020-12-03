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

    var map = [];

    readIn.forEach(line => {
        map.push(line.split(''));
    });

    var moreSlopes = [];
    moreSlopes.push(treeSlope(map, 3, 1));
    console.log("Tree:", moreSlopes[0]);

    moreSlopes.push(treeSlope(map, 1, 1));
    moreSlopes.push(treeSlope(map, 5, 1));
    moreSlopes.push(treeSlope(map, 7, 1));
    moreSlopes.push(treeSlope(map, 1, 2));

    console.log("More Tree:", moreSlopes.reduce( (a, b) => a * b ) );
      
}

function treeSlope(map, right, down) {
    let countTree = 0;
    const lineLength = map[0].length;
    let posRight = right;

    for (let i = down; i < map.length; i=i+down) {
        if (map[i][posRight] == '#') {
            countTree++;
        }
        posRight = (posRight + right) % lineLength
    }
    return countTree;
}


run();