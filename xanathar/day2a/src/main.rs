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
    letter: char,
    min: usize,
    max: usize,
    password: String,
}

impl Password {
    pub fn new(line: &str) -> Option<Password> {
        lazy_static! {
            // 5-6 v: vvvgvb
            static ref RE: Regex = Regex::new(r"^(?P<min>\d+)-(?P<max>\d+) (?P<chr>[a-z]): (?P<pwd>[a-z]+)$").unwrap();
        }

        RE.captures(line).map(|cap| {
            Password {
                min: cap.name("min").map(|value| value.as_str()).unwrap().parse::<usize>().unwrap(),
                max: cap.name("max").map(|value| value.as_str()).unwrap().parse::<usize>().unwrap(),
                letter: cap.name("chr").map(|value| value.as_str()).unwrap().chars().next().unwrap(),
                password: cap.name("pwd").map(|value| value.as_str()).unwrap().to_string(),
            }
        })
    }

    pub fn valid(&self) -> bool {
        let count = self.password.chars().filter(|c| *c == self.letter).count();

        count >= self.min && count <= self.max
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
