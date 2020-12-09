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

fn calc_contained(rules: &HashMap<String, Rule>, color: &str) -> u32 {
    let rule = rules.get(color).unwrap();
    let mut count = 1;

    for (bag, qty) in &rule.contains {
        count += qty * calc_contained(rules, &bag);
    }

    count
}

fn main() {
    let rules: HashMap<String, Rule> = read_lines("rules.txt")
        .unwrap()
        .map(|s| Rule::parse(&s.unwrap()))
        .map(|r| (r.color.clone(), r))
        .collect();

    println!("Contains {} bags", calc_contained(&rules, "shiny gold") - 1);
}
