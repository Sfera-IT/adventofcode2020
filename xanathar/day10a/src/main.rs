use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;
use std::collections::BTreeSet;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn main() {
    let numbers: BTreeSet<u32> = read_lines("jolts.txt")
        .unwrap()
        .filter_map(|s| s.unwrap().parse::<u32>().ok())
        .collect();

    let (mut last, mut one, mut two, mut three) = (0, 0, 0, 1);

    for n in numbers {
        match n - last {
            1 => one += 1,
            2 => two += 1,
            3 => three += 1,
            _ => panic!("wtf?"),
        }
        last = n;
    }

    println!("1:{} 2:{} 3:{}  [1*3]={}", one, two, three, one*three);
}
