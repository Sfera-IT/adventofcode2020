use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

enum OpCode {
    Acc,
    Jmp,
    Nop,
}

struct Instr {
    opcode: OpCode,
    arg: i32,
    exec_cnt: u32,
}

impl Instr {
    pub fn parse(s: &str) -> Instr {
        let (opcode, arg) = s.split_at(3);

        let opcode = match opcode {
            "acc" => OpCode::Acc,
            "jmp" => OpCode::Jmp,
            "nop" => OpCode::Nop,
            _ => panic!("Invalid opcode: {}", opcode),
        };

        let arg = arg.trim();
        let arg = arg.parse::<i32>().unwrap_or_else(|_| panic!("arg parse failed {}", arg));

        Instr {
            opcode,
            arg,
            exec_cnt: 0,
        }
    }
}

fn main() {
    let mut program: Vec<Instr> = read_lines("code.txt")
        .unwrap()
        .map(|s| Instr::parse(&s.unwrap()))
        .collect();

    let mut acc: i32 = 0;
    let mut pc: i32 = 0;

    loop {
        if program[pc as usize].exec_cnt != 0 {
            println!("Loop found; acc is {}", acc);
            break;
        }

        program[pc as usize].exec_cnt += 1;

        match program[pc as usize].opcode {
            OpCode::Acc => { acc += program[pc as usize].arg; pc += 1; }
            OpCode::Nop => pc += 1,
            OpCode::Jmp => pc += program[pc as usize].arg,
        }
    }
}
