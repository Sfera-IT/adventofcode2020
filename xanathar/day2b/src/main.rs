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

#[derive(Debug, Clone, PartialEq)]
struct Password {
    letter: u8,
    pos1: usize,
    pos2: usize,
    password: Box<[u8]>,
}

impl Password {
    pub fn new(line: &str) -> Option<Password> {
        lazy_static! {
            // 5-6 v: vvvgvb
            static ref RE: Regex = Regex::new(r"^(?P<pos1>\d+)-(?P<pos2>\d+) (?P<chr>[a-z]): (?P<pwd>[a-z]+)$").unwrap();
        }

        RE.captures(line).map(|cap| {
            Password {
                pos1: cap.name("pos1").map(|value| value.as_str()).unwrap().parse::<usize>().unwrap() - 1,
                pos2: cap.name("pos2").map(|value| value.as_str()).unwrap().parse::<usize>().unwrap() - 1,
                letter: cap.name("chr").map(|value| value.as_str()).unwrap().chars().next().unwrap() as u8,
                password: Box::from(cap.name("pwd").map(|value| value.as_str()).unwrap().as_bytes()),
            }
        })
    }

    pub fn valid(&self) -> bool {
        let inp1 = self.pos1 < self.password.len() && self.password[self.pos1] == self.letter;
        let inp2 = self.pos2 < self.password.len() && self.password[self.pos2] == self.letter;

        inp1 ^ inp2
    }
}

fn main() {
    let valid_passwords = read_lines("data.txt")
        .unwrap()
        .filter_map(|s| Password::new(&s.unwrap()))
        .filter(|p| p.valid())
        .count();

    println!("Valid password: {}", valid_passwords);
}
