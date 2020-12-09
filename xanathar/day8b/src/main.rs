use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Clone, Debug, Copy, PartialEq)]
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

enum ExecResult {
    Loop,
    Invalid,
    Completed(i32),
}

fn execute(program: &mut Vec<Instr>, flip: usize) -> ExecResult {
    let mut acc: i32 = 0;
    let mut pc: i32 = 0;

    loop {
        if (pc as usize) > program.len() {
            return ExecResult::Invalid;
        }

        if (pc as usize) == program.len() {
            return ExecResult::Completed(acc);
        }

        if program[pc as usize].exec_cnt != 0 {
            return ExecResult::Loop;
        }

        program[pc as usize].exec_cnt += 1;
        let flipped = (pc as usize) == flip;

        match (flipped, program[pc as usize].opcode) {
            (_, OpCode::Acc) => { acc += program[pc as usize].arg; pc += 1; }
            (false, OpCode::Nop) | (true, OpCode::Jmp) => pc += 1,
            (false, OpCode::Jmp) | (true, OpCode::Nop)  => pc += program[pc as usize].arg,
        }
    }
}

fn reset(program: &mut Vec<Instr>) {
    for i in program { i.exec_cnt = 0; }
}

fn main() {
    let mut program: Vec<Instr> = read_lines("code.txt")
        .unwrap()
        .map(|s| Instr::parse(&s.unwrap()))
        .collect();

    for iter in 0..program.len() {
        if program[iter].opcode == OpCode::Acc {
            continue;
        }

        match execute(&mut program, iter) {
            ExecResult::Loop | ExecResult::Invalid => reset(&mut program),
            ExecResult::Completed(acc) => {
                println!("Acc is {}", acc);
                break;
            }
        }
    }
}
