use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Debug)]
enum Instruction {
    North(i64),
    South(i64),
    East(i64),
    West(i64),
    Forward(i64),
    TurnCw(u64),
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
            ("L", 180) | ("R", 180) => Instruction::TurnCw(2),
            ("L", 90) | ("R", 270) => Instruction::TurnCw(3),
            ("L", 270) | ("R", 90) => Instruction::TurnCw(1),
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
    let mut wx: i64 = 10;
    let mut wy: i64 = -1;

    println!("{},{}  W:{},{}", x, y, wx, wy);

    for i in route {
        match i {
            Instruction::North(v) => wy -= v,
            Instruction::South(v) => wy += v,
            Instruction::East(v) => wx += v,
            Instruction::West(v) => wx -= v,
            Instruction::Forward(v) => { x += wx * v; y += wy * v; },
            Instruction::TurnCw(d) => {
                for _ in 1..=d {
                    let old_wx = wx;
                    wx = -wy;
                    wy = old_wx;
                }
            },
        }
        println!("{:?}", i);
        println!("{},{}  W:{},{}", x, y, wx, wy);
    }

    println!();
    println!("x: {}, y: {}, tot: {}", x, y, x.abs() + y.abs());
}
