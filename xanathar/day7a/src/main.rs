use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;
use std::collections::{HashMap, HashSet, VecDeque};
use regex::Regex;
use lazy_static::lazy_static;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Default)]
struct Rule {
    color: String,
    contains: HashMap<String, u32>,
}

impl Rule {
    fn parse(line: &str) -> Rule {
        lazy_static! {
            static ref RE_COLOR: Regex = Regex::new(r"^(?P<color>\w+ \w+) bags contain").unwrap();
        }
        lazy_static! {
            static ref RE_CONTAINS: Regex = Regex::new(r"(?P<num>\d+) (?P<color>\w+ \w+) bags?[,.]\s?").unwrap();
        }

        let color = RE_COLOR.captures(line)
            .unwrap()
            .name("color")
            .unwrap()
            .as_str()
            .to_string();

        let mut contains = HashMap::new();

        for cap in RE_CONTAINS.captures_iter(line) {
            let num = cap.name("num").map(|v| v.as_str().parse::<u32>().unwrap()).unwrap();
            let color = cap.name("color").map(|v| v.as_str().to_string()).unwrap();
            contains.insert(color, num);
        }

        Rule {
            color,
            contains,
        }
    }
}

fn main() {
    let rules: HashMap<String, Rule> = read_lines("rules.txt")
        .unwrap()
        .map(|s| Rule::parse(&s.unwrap()))
        .map(|r| (r.color.clone(), r))
        .collect();

    let mut pending = VecDeque::new();
    let mut set = HashSet::new();
    pending.push_back("shiny gold");

    while let Some(bag) = pending.pop_front() {
        for rule in rules.values() {
            if rule.contains.contains_key(bag) {
                set.insert(rule.color.clone());
                pending.push_back(&rule.color);
                println!("{} -> {}", rule.color, bag);
            }
        }
    }

    println!("Set size= {}", set.len());
}
