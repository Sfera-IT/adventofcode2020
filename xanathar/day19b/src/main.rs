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

fn str_to_bin(s: &str) -> u8 {
    let mut r = 0;

    for c in s.chars() {
        r <<= 1;
        if c == 'a' {
            r |= 1;
        }
    }

    r
}

fn str_to_bin_vec(mut s: &str) -> Vec<u8> {
    let mut r = Vec::new();

    while !s.is_empty() {
        r.push(str_to_bin(&s[0..8]));
        s = &s[8..];
    }

    r
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

    // Examining the rules:
    // - pattern 42 and 31 are 8 chars long
    // - there is no intersection between 42 and 31
    // - all 256 patterns are covered by 42 and 31 (128 each)
    // - only rule 0 uses 8 and 11, more precisely 8 followed by 11
    // - which means, any number of 42, followed by a smaller number of 31

    // 0: 8 11
    // 8: 42 | 42 8
    // 11: 42 31 | 42 11 31

    let set31 = rules[31].expand_pattern(&rules).iter().map(|s| str_to_bin(s)).collect::<HashSet<u8>>();
    let set42 = rules[42].expand_pattern(&rules).iter().map(|s| str_to_bin(s)).collect::<HashSet<u8>>();

    assert_eq!(set31.len(), 128);
    assert_eq!(set42.len(), 128);
    assert_eq!(set31.intersection(&set42).count(), 0);
    assert_eq!(set31.union(&set42).count(), 256);

    let patterns = read_lines("patterns.txt").unwrap().map(|s| s.unwrap()).collect::<Vec<String>>();

    let mut matches = 0;
    let mut discarded = 0;

    for s in patterns.iter() {
        if s.is_empty() || (s.len() % 8) != 0 {
            discarded += 1;
            continue;
        }

        let v = str_to_bin_vec(s);

        let mut count42 = 0;
        let mut count31 = 0;
        let mut discard = false;

        for p in v.iter() {
            if set42.contains(p) {
                if count31 != 0 {
                    discard = true;
                    break;
                }
                count42 += 1;
            } else {
                count31 += 1;
            }
        }

        if count31 != 0 && count42 > count31 && !discard {
            matches += 1;
        } else {
            discarded += 1;
        }
    }

    println!("matches = {} -- discarded = {}", matches, discarded);
}
