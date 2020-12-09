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
    let numbers: HashSet<u32> = read_lines("data.txt")
        .unwrap()
        .filter_map(|s| s.unwrap().parse::<u32>().ok())
        .collect();

    for n in &numbers {
        let peer = 2020 - n;
        if numbers.contains(&peer) {
            println!("{} * {} = {}", n, peer, n * peer);
            break;
        }
    }
}
