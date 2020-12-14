use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;
use regex::Regex;
use lazy_static::lazy_static;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Copy, Clone, PartialEq, Debug)]
enum Instr {
    MemWr { addr: u16, val: u64 },
    Mask { or: u64, and: u64 },
}

impl Instr {
    fn parse(line: &str) -> Instr {
        lazy_static! {
            static ref RE_MEMWR: Regex = Regex::new(r"^mem\[(?P<addr>\d+)\] = (?P<val>\d+)$").unwrap();
        }

        if line.starts_with("mask = ") {
            let (_, mask) = line.split_at(7);
            let (mut and, mut or) = (0, 0);

            for c in mask.chars() {
                and <<= 1;
                or <<= 1;
                match c {
                    '1' => or |= 1,
                    '0' => (),
                    'X' => and |= 1,
                    _ => panic!("Unexpected char in mask: {}", c),
                }
            }

            Instr::Mask { or, and }
        } else {
            RE_MEMWR.captures(line).map(|cap| {
                Instr::MemWr {
                    addr: cap.name("addr").map(|value| value.as_str()).unwrap().parse::<u16>().unwrap(),
                    val: cap.name("val").map(|value| value.as_str()).unwrap().parse::<u64>().unwrap(),
                }
            }).unwrap()
        }
    }
}

fn main() {
    let instrs: Vec<Instr> = read_lines("code.txt")
        .unwrap()
        .map(|s| Instr::parse(&s.unwrap()))
        .collect();

    let mut memory: [u64; 65536] = [0; 65536];
    let mut mask_or = 0;
    let mut mask_and = 0;

    for i in instrs {
        match i {
            Instr::Mask { and, or } => {
                mask_and = and;
                mask_or = or;
            },
            Instr::MemWr { addr, val } => {
                memory[addr as usize] = (val & mask_and) | mask_or;
            },
        }
    }

    println!("SUM: {}", memory.iter().sum::<u64>());
}
