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

#[derive(Debug, Clone, PartialEq, Default)]
struct Passport {
    byr: Option<String>,
    iyr: Option<String>,
    eyr: Option<String>,
    hgt: Option<String>,
    hcl: Option<String>,
    ecl: Option<String>,
    pid: Option<String>,
    cid: Option<String>,
}

impl Passport {
    pub fn new(lines: Vec<String>) -> Passport {
        lazy_static! {
            static ref RE: Regex = Regex::new(r"(?P<key>[a-z][a-z][a-z]):(?P<value>\S+)").unwrap();
        }

        let mut passport = Passport::default();

        for line in lines {
            for cap in RE.captures_iter(&line) {
                let key = cap.name("key").map(|v| v.as_str());
                let value = cap.name("value").map(|v| v.as_str().to_string());

                match key {
                    Some("byr") => passport.byr = value,
                    Some("iyr") => passport.iyr = value,
                    Some("eyr") => passport.eyr = value,
                    Some("hgt") => passport.hgt = value,
                    Some("hcl") => passport.hcl = value,
                    Some("ecl") => passport.ecl = value,
                    Some("pid") => passport.pid = value,
                    Some("cid") => passport.cid = value,
                    Some(key) => println!("Unknown key {}", key),
                    None => (),
                }
            }
        }

        passport
    }

    pub fn is_valid(&self) -> bool {
        self.byr.is_some() &&
            self.iyr.is_some() &&
            self.eyr.is_some() &&
            self.hgt.is_some() &&
            self.hcl.is_some() &&
            self.ecl.is_some() &&
            self.pid.is_some()
    }
}

fn read_passports(file: &str) -> Vec<Passport> {
    let passport_codes = read_lines(file)
        .unwrap()
        .map(|s| s.unwrap());

    let mut current: Vec<String> = Vec::new();
    let mut passports: Vec<Passport> = Vec::new();

    for l in passport_codes {
        if l.trim().is_empty() {
            passports.push(Passport::new(current));
            current = Vec::new();
        } else {
            current.push(l);
        }
    }

    if !current.is_empty() {
        passports.push(Passport::new(current));
    }

    passports
}

fn main() {
    let passports = read_passports("passports.txt");

    println!("valid passports: {}", passports.iter().filter(|p| p.is_valid()).count());
}
