use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn is_summable(val: u64, nums: &[u64]) -> bool {
    assert_eq!(nums.len(), 25);

    for i in 0..(nums.len() - 1) {
        for j in (i + 1)..nums.len() {
            if (nums[i] + nums[j]) == val {
                return true;
            }
        }
    }
    false
}

fn main() {
    let numbers: Vec<u64> = read_lines("xmas.txt")
        .unwrap()
        .filter_map(|s| s.unwrap().parse::<u64>().ok())
        .collect();

    for i in 25..numbers.len() {
        if !is_summable(numbers[i], &numbers[i-25..i]) {
            println!("The number of the beast is {}", numbers[i]);
        }
    }
}
