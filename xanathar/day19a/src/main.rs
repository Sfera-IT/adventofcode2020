#![allow(clippy::needless_range_loop)]

use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;
use regex::Regex;
use lazy_static::lazy_static;
use std::collections::HashSet;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

type RuleSet = [Rule];

#[derive(Clone, PartialEq, Debug)]
enum Rule {
    Nope,
    Match(char),
    Sequence(Vec<usize>),
    Either(Vec<usize>, Vec<usize>),
}

impl Rule {
    fn new(line: &str) -> (usize, Self) {
        lazy_static! {
            static ref RE_CHR: Regex = Regex::new(r###"^(?P<id>\d+): "(?P<chr>\w+)"$"###).unwrap();
        }
        lazy_static! {
            static ref RE_SEQ: Regex = Regex::new(r"^(?P<id>\d+): (?P<rest>.+)$").unwrap();
        }

        println!("{}", line);

        if line.contains('\"') {
            RE_CHR.captures(line).map(|cap| {
                (cap.name("id").map(|value| value.as_str()).unwrap().parse::<usize>().unwrap(),
                Rule::Match(cap.name("chr").map(|value| value.as_str()).unwrap().chars().next().unwrap()))
            }).unwrap()
        } else {
            RE_SEQ.captures(line).map(|cap| {
                let id = cap.name("id").map(|value| value.as_str()).unwrap().parse::<usize>().unwrap();
                let rest = cap.name("rest").map(|value| value.as_str()).unwrap();

                let mut s = rest.as_bytes();
                let mut v1 = Vec::new();
                let mut v2 = Vec::new();
                let mut v = &mut v1;

                loop {
                    let (ns, token) = Rule::extract_token(s);
                    s = &ns;

                    if token.is_empty() {
                        break;
                    }

                    if token == "|" {
                        v = &mut v2;
                    } else {
                        let n = token.parse::<usize>().unwrap();
                        v.push(n);
                    }
                }

                if v2.is_empty() {
                    Some((id, Rule::Sequence(v1)))
                } else {
                    Some((id, Rule::Either(v1, v2)))
                }
            }).unwrap().unwrap()
        }
    }

    fn extract_token(mut src: &[u8]) -> (&[u8], String) {
        let mut token = String::new();

        while !src.is_empty() && src[0] == b' ' { src = &src[1..]; }

        while !src.is_empty() && src[0] != b' ' {
            token.push(src[0] as char);
            src = &src[1..];
        }

        (src, token)
    }

    fn expand_sequence(rules: &[usize], ruleset: &RuleSet) -> Vec<String> {
        let mut v = vec![String::new()];

        for rule in rules {
            let exp = ruleset[*rule].expand_pattern(&ruleset);

            if exp.len() == 1 {
                for s in v.iter_mut() {
                    s.push_str(&exp[0]);
                }
            } else {
                let mut new = Vec::<String>::new();
                for origs in v.iter() {
                    for news in exp.iter() {
                        new.push(format!("{}{}", origs, news));
                    }
                }
                v = new;
            }
        }

        v
    }

    fn expand_pattern(&self, ruleset: &RuleSet) -> Vec<String> {
        match self {
            Rule::Nope => panic!(),
            Rule::Match(c) => vec![format!("{}", c)],
            Rule::Sequence(rules) => Rule::expand_sequence(&rules, ruleset),
            Rule::Either(a, b) => {
                let mut v = Rule::expand_sequence(&a, ruleset);
                v.extend(Rule::expand_sequence(&b, ruleset));
                v
            },
        }
    }
}

fn main() {
    let mut rules = Vec::with_capacity(200);

    for _ in 0..200 {
        rules.push(Rule::Nope);
    }

    for line in read_lines("rules.txt").unwrap() {
        let (id, rule) = Rule::new(&line.unwrap());
        rules[id] = rule;
    }

    let map = rules[0].expand_pattern(&rules).iter().cloned().collect::<HashSet<String>>();

    let count = read_lines("patterns.txt").unwrap()
        .filter(|p| map.contains(p.as_ref().unwrap()))
        .count();

    println!("count = {}", count);
}
