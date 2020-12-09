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
    let numbers: HashSet<u64> = read_lines("data.txt")
        .unwrap()
        .filter_map(|s| s.unwrap().parse::<u64>().ok())
        .collect();

    for n in &numbers {
        for m in &numbers {
            let peer = (2020u64 - *n).checked_sub(*m);
            if let Some(peer) = peer {
                if numbers.contains(&peer) {
                    println!("{} * {} * {} = {}", n, m, peer, n * m * peer);
                    return;
                }
            }
        }
    }
}
