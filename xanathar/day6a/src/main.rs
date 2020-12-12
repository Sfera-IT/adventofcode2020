use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;
use std::collections::HashSet;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn main() {
    let mut values = Vec::new();
    let mut current = HashSet::new();

    for line in read_lines("custom.txt").unwrap().map(|s| s.unwrap()) {
        if line.is_empty() {
            values.push(current.len());
            current.clear();
        } else {
            for c in line.chars() {
                current.insert(c);
            }
        }
    }
    if !current.is_empty() {
        values.push(current.len());
    }

    println!("sum = {}", values.iter().sum::<usize>());
}
