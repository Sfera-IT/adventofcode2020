use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;
use regex::Regex;
use lazy_static::lazy_static;
use std::ops::RangeInclusive;

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
        fn validate_number_field(val: Option<&str>, range: RangeInclusive<u32>) -> bool {
            if let Some(val) = val {
                if let Ok(val) = val.parse::<u32>() {
                    if range.contains(&val) {
                        return true;
                    }
                }
            }
            false
        }

        fn validate_regex(val: Option<&str>, regex: &Regex) -> bool {
            if let Some(val) = val {
                return regex.is_match(val);
            }
            false
        }

        // byr (Birth Year) - four digits; at least 1920 and at most 2002.
        if !validate_number_field(self.byr.as_deref(), 1920..=2002) {
            return false;
        }

        // iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        if !validate_number_field(self.iyr.as_deref(), 2010..=2020) {
            return false;
        }

        // eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        if !validate_number_field(self.eyr.as_deref(), 2020..=2030) {
            return false;
        }

        // hgt (Height) - a number followed by either cm or in:
        if let Some(hgt) = self.hgt.as_ref() {
            if hgt.len() <= 2 {
                return false;
            }

            let (val, unit) = hgt.split_at(hgt.len() - 2);

            match unit {
                //     If cm, the number must be at least 150 and at most 193.
                "cm" => if !validate_number_field(Some(val), 150..=193) {
                    return false;
                },
                //     If in, the number must be at least 59 and at most 76.
                "in" => if !validate_number_field(Some(val), 59..=76) {
                    return false;
                },
                _ => return false,
            }
        } else {
            return false;
        }

        // hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        lazy_static! {
            static ref RE_HCL: Regex = Regex::new(r"^#[0-9a-f]{6}$").unwrap();
        }
        if !validate_regex(self.hcl.as_deref(), &RE_HCL) {
            return false;
        }

        // ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        if let Some(ecl) = self.ecl.as_deref() {
            match ecl {
                "amb" | "blu" | "brn" | "gry" | "grn" | "hzl" | "oth" => (),
                _ => return false,
            }
        } else {
            return false;
        }

        // pid (Passport ID) - a nine-digit number, including leading zeroes.
        lazy_static! {
            static ref RE_PID: Regex = Regex::new(r"^[0-9]{9}$").unwrap();
        }
        if !validate_regex(self.pid.as_deref(), &RE_PID) {
            return false;
        }

        true
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
