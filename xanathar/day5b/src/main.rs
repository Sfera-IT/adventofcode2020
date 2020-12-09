use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn decode_binary(s: &str, one: char, zero: char) -> u32 {
    let mut val = 0;

    for c in s.chars() {
        match c {
            c if c == one => val = (val << 1) | 1,
            c if c == zero => val <<= 1,
            _ => panic!("invalid char in {}, expected {} or {}", s, one, zero),
        }
    }

    val
}

fn decode_boarding_pass(s: &str) -> u32 {
    // BFBBBBBLLR
    let (rowstr, seatstr) = s.split_at(s.len() - 3);
    let row = decode_binary(rowstr, 'B', 'F');
    let seat = decode_binary(seatstr, 'R', 'L');
    row * 8 + seat
}

fn main() {
    let mut occupied = [false; 1024];

    for seat in read_lines("boards.txt").unwrap().map(|s| decode_boarding_pass(&s.unwrap())) {
        occupied[seat as usize] = true;
    }

    for seat in 1..1023 {
        if !occupied[seat] && occupied[seat + 1] && occupied[seat - 1] {
            println!("maybe it's seat {}", seat);
        }
    }
}
