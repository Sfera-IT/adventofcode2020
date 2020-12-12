use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

enum Instruction {
    North(i64),
    South(i64),
    East(i64),
    West(i64),
    Forward(i64),
    TurnCw,
    TurnCcw,
    Reverse,
}

impl Instruction {
    pub fn parse(s: &str) -> Instruction {
        let (instr, len) = s.split_at(1);
        let len = len.parse::<i64>().unwrap();

        match (instr, len) {
            ("N", l) => Instruction::North(l),
            ("S", l) => Instruction::South(l),
            ("E", l) => Instruction::East(l),
            ("W", l) => Instruction::West(l),
            ("F", l) => Instruction::Forward(l),
            ("L", 0) | ("R", 0) => Instruction::Forward(0),
            ("L", 180) | ("R", 180) => Instruction::Reverse,
            ("L", 90) | ("R", 270) => Instruction::TurnCcw,
            ("L", 270) | ("R", 90) => Instruction::TurnCw,
            _ => panic!("Can't read {}", s),
        }
    }
}


fn main() {
    let route: Vec<Instruction> = read_lines("route.txt")
        .unwrap()
        .map(|s| Instruction::parse(&s.unwrap()))
        .collect();

    let mut x: i64 = 0;
    let mut y: i64 = 0;
    let mut dx: i64 = 1;
    let mut dy: i64 = 0;

    for i in route {
        match i {
            Instruction::North(v) => y -= v,
            Instruction::South(v) => y += v,
            Instruction::East(v) => x += v,
            Instruction::West(v) => x -= v,
            Instruction::Forward(v) => { x += dx * v; y += dy * v; },
            Instruction::TurnCw => {
                let (ndx, ndy) = match (dx, dy) {
                    (1, 0) => (0, 1),
                    (0, 1) => (-1, 0),
                    (-1, 0) => (0, -1),
                    (0, -1) => (1, 0),
                    _ => panic!("wtf"),
                };
                dx = ndx; dy = ndy;
            },
            Instruction::TurnCcw => {
                let (ndx, ndy) = match (dx, dy) {
                    (0, 1) => (1, 0),
                    (-1, 0) => (0, 1),
                    (0, -1) => (-1, 0),
                    (1, 0) => (0, -1),
                    _ => panic!("wtf"),
                };
                dx = ndx; dy = ndy;
            },
            Instruction::Reverse => { dx = -dx; dy = -dy; },
        }
    }

    println!("x: {}, y: {}, tot: {}", x, y, x.abs() + y.abs());
}
