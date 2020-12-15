#![allow(clippy::needless_range_loop)]

use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;
use std::collections::{HashMap};
use regex::Regex;
use lazy_static::lazy_static;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Debug)]
enum Instr {
    MemWr { addr: u64, val: u64 },
    Mask { overwrite: u64, floating: Vec<u64>, floating_mask: u64 },
}

impl Instr {
    fn parse(line: &str) -> Instr {
        lazy_static! {
            static ref RE_MEMWR: Regex = Regex::new(r"^mem\[(?P<addr>\d+)\] = (?P<val>\d+)$").unwrap();
        }

        if line.starts_with("mask = ") {
            let (_, mask) = line.split_at(7);

            // If the bitmask bit is 0, the corresponding memory address bit is unchanged.
            // If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
            // If the bitmask bit is X, the corresponding memory address bit is floating.
            let (mut overwrite, mut bitcnt, mut floating_mask) = (0, 36, 0);
            let mut floating = Vec::new();

            for c in mask.chars() {
                bitcnt -= 1;
                overwrite <<= 1;
                floating_mask <<= 1;
                match c {
                    '1' => overwrite |= 1,
                    '0' => (),
                    'X' => {
                        floating.push(1 << bitcnt);
                        floating_mask |= 1;
                    },
                    _ => panic!("Unexpected char in mask: {}", c),
                }
            }

            Instr::Mask { overwrite, floating: Instr::make_floating_vec(floating), floating_mask }
        } else {
            RE_MEMWR.captures(line).map(|cap| {
                Instr::MemWr {
                    addr: cap.name("addr").map(|value| value.as_str()).unwrap().parse::<u64>().unwrap(),
                    val: cap.name("val").map(|value| value.as_str()).unwrap().parse::<u64>().unwrap(),
                }
            }).unwrap()
        }
    }

    fn make_floating_vec(bits: Vec<u64>) -> Vec<u64> {
        let pow2 = 1 << bits.len();
        let mut res = Vec::with_capacity(pow2);

        for i in 0..pow2 {
            let mut val = 0;

            for bit in 0..bits.len() {
                let bitmask = 1 << bit;

                if (i & bitmask) != 0 {
                    val |= bits[bit];
                }
            }
            res.push(val);
        }

        res
    }
}

fn main() {
    let instrs: Vec<Instr> = read_lines("code.txt")
        .unwrap()
        .map(|s| Instr::parse(&s.unwrap()))
        .collect();
    let mut memory = HashMap::<u64, u64>::new();
    let empty_mask = Vec::new();

    let mut mask_overwrite = 0;
    let mut mask_float = &empty_mask;
    let mut mask_floatmask = 0;

    for i in &instrs {
        match i {
            Instr::Mask { overwrite, floating, floating_mask } => {
                mask_overwrite = *overwrite;
                mask_float = &floating;
                mask_floatmask = !floating_mask;
            },
            Instr::MemWr { addr, val } => {
                let addr = (addr | mask_overwrite) & mask_floatmask;
                for float in mask_float.iter() {
                    memory.insert(addr | float, *val);
                }
            },
        }
    }

    println!("SUM: {}", memory.values().sum::<u64>());
}
