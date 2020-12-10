use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Debug)]
struct Adapter {
    jolts: u32,
    alts: u64,
}

fn main() {
    let mut numbers: Vec<Adapter> = read_lines("jolts.txt")
        .unwrap()
        .filter_map(|s| s.unwrap().parse::<u32>().ok())
        .map(|j| Adapter { jolts: j, alts: 0 })
        .collect();

    numbers.push(Adapter { jolts: 0, alts: 0 });
    numbers.sort_by(|a, b| a.jolts.partial_cmp(&b.jolts).unwrap());

    let last = numbers.len() - 1;
    numbers[last].alts = 1;

    for i in (0..numbers.len()).rev() {
        if i >= 1 && (numbers[i].jolts - numbers[i - 1].jolts) <= 3 {
            numbers[i - 1].alts += numbers[i].alts;
        }
        if i >= 2 && (numbers[i].jolts - numbers[i - 2].jolts) <= 3 {
            numbers[i - 2].alts += numbers[i].alts;
        }
        if i >= 3 && (numbers[i].jolts - numbers[i - 3].jolts) <= 3 {
            numbers[i - 3].alts += numbers[i].alts;
        }
    }

    println!("{:?}", numbers);
    println!("alternatives={}", numbers[0].alts);
}
