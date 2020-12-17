use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;
use regex::Regex;
use lazy_static::lazy_static;
use std::ops::RangeInclusive;
use std::collections::HashSet;

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

fn is_ticket_valid(t: &Ticket, rules: &[Rule]) -> bool {
    for n in t.0.iter() {
        let mut match_found = false;
        for r in rules {
            if r.range1.contains(n) || r.range2.contains(n) {
                match_found = true;
                break;
            }
        }
        if !match_found {
            return false
        }
    }

    true
}

struct Field {
    set: HashSet<String>,
    reduced: Option<String>,
}

fn reduce_fields(fields: &mut Vec<Field>) -> bool {
    let found = {
        let min_val = fields.iter_mut()
                        .filter(|f| f.reduced.is_none())
                        .min_by_key(|f| f.set.len());

        let mut min_val = match min_val {
            None => return false,
            Some(v) => v,
        };

        if min_val.set.len() != 1 {
            // assumes at least one field has only one possibility
            panic!("Cannot easily reduce");
        }

        let found = min_val.set.iter().next().unwrap().clone();
        min_val.reduced = Some(found.clone());
        found
    };

    for f in fields.iter_mut() {
        if f.reduced.is_none() {
            f.set.remove(&found);
        }
    }

    true
}

fn main() {
    let rules = read_lines("rules.txt")
        .unwrap()
        .filter_map(|s| Rule::new(&s.unwrap()))
        .collect::<Vec<Rule>>();

    let tickets = read_lines("tickets.txt")
        .unwrap()
        .map(|s| Ticket(s.unwrap().split(',').map(|tkn| tkn.parse::<u32>().unwrap()).collect()))
        .filter(|t| is_ticket_valid(t, &rules))
        .collect::<Vec<Ticket>>();

    let mut fields = tickets[0].0.iter()
                    .map(|_| rules.iter().map(|r| r.name.clone()).collect::<HashSet<String>>())
                    .map(|h| Field { set: h, reduced: None })
                    .collect::<Vec<Field>>();

    for t in tickets {
        for (index, value) in t.0.iter().enumerate() {
            for r in &rules {
                if !r.range1.contains(value) && !r.range2.contains(value) {
                    fields[index].set.remove(&r.name);
                }
            }
        }
    }

    while reduce_fields(&mut fields) {}

    let my_ticket = vec![127,83,79,197,157,67,71,131,97,193,181,191,163,61,53,89,59,137,73,167];

    let mut product = 1;
    for (idx, field) in fields.iter().enumerate() {
        let name = field.reduced.as_deref().unwrap();
        if name.starts_with("departure") {
            product *= my_ticket[idx] as u64;
        }
    }
    println!("Product: {}", product);
}
