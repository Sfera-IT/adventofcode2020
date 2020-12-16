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

struct Ticket(Vec<u32>);


#[derive(Debug, Clone, PartialEq)]
struct Rule {
    name: String,
    range1: RangeInclusive<u32>,
    range2: RangeInclusive<u32>,
}

impl Rule {
    pub fn new(line: &str) -> Option<Self> {
        lazy_static! {
            // 5-6 v: vvvgvb
            static ref RE: Regex = Regex::new(r"^(?P<name>[^:]+): (?P<min1>\d+)-(?P<max1>\d+) or (?P<min2>\d+)-(?P<max2>\d+)$").unwrap();
        }

        RE.captures(line).map(|cap| {
            Rule {
                name: cap.name("name").map(|value| value.as_str()).unwrap().to_string(),
                range1: RangeInclusive::new(
                    cap.name("min1").map(|value| value.as_str()).unwrap().parse::<u32>().unwrap(),
                    cap.name("max1").map(|value| value.as_str()).unwrap().parse::<u32>().unwrap(),
                ),
                range2: RangeInclusive::new(
                    cap.name("min2").map(|value| value.as_str()).unwrap().parse::<u32>().unwrap(),
                    cap.name("max2").map(|value| value.as_str()).unwrap().parse::<u32>().unwrap(),
                ),
            }
        })
    }
}

fn calc_ticket_error_rate(t: &Ticket, rules: &[Rule]) -> u32 {
    let mut error_rate = 0;

    for n in t.0.iter() {
        let mut match_found = false;
        for r in rules {
            if r.range1.contains(n) || r.range2.contains(n) {
                match_found = true;
                break;
            }
        }
        if !match_found {
            error_rate += n;
        }
    }

    error_rate
}

fn main() {
    let rules = read_lines("rules.txt")
        .unwrap()
        .filter_map(|s| Rule::new(&s.unwrap()))
        .collect::<Vec<Rule>>();

    let tickets = read_lines("tickets.txt")
        .unwrap()
        .map(|s| Ticket(s.unwrap().split(',').map(|tkn| tkn.parse::<u32>().unwrap()).collect()))
        .collect::<Vec<Ticket>>();

    let rate = tickets.iter().map(|t| calc_ticket_error_rate(t, &rules)).sum::<u32>();

    println!("rate: {}", rate);
}
