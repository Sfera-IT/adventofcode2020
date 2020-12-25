use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashSet;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Copy, Clone, Debug, PartialEq)]
enum Dir {
    East,
    SouthEast,
    SouthWest,
    West,
    NorthWest,
    NorthEast,
}

#[derive(Copy, Clone, PartialEq, Hash, Eq)]
struct Pos(i32, i32);

impl Pos {
    pub fn walk(&self, dir: Dir) -> Self {
        let (west_ofs, east_ofs) = if (self.1 & 1) == 0 {
            (-1, 0)
        } else {
            (0, 1)
        };

        match dir {
            Dir::East => Pos(self.0 + 1, self.1),
            Dir::SouthEast => Pos(self.0 + east_ofs, self.1 - 1),
            Dir::SouthWest => Pos(self.0 + west_ofs, self.1 - 1),
            Dir::West => Pos(self.0 - 1, self.1),
            Dir::NorthWest => Pos(self.0 + west_ofs, self.1 + 1),
            Dir::NorthEast => Pos(self.0 + east_ofs, self.1 + 1),
        }
    }
}

fn flip_tile(hexmap: &mut HashSet::<Pos>, directions: &[Dir]) {
    let mut pos = Pos(0, 0);

    for d in directions {
        pos = pos.walk(*d);
    }

    if hexmap.contains(&pos) {
        hexmap.remove(&pos);
    } else {
        hexmap.insert(pos);
    }
}

fn parse_directions(mut dir_str: &[u8]) -> Vec<Dir> {
    let mut v = Vec::<Dir>::new();

    while !dir_str.is_empty() {
        match dir_str[0] {
            b'e' => { dir_str = &dir_str[1..]; v.push(Dir::East) },
            b'w' => { dir_str = &dir_str[1..]; v.push(Dir::West) },
            b'n' => {
                match dir_str[1] {
                    b'e' => v.push(Dir::NorthEast),
                    b'w' => v.push(Dir::NorthWest),
                    _ => panic!(),
                };
                dir_str = &dir_str[2..];
            },
            b's' => {
                match dir_str[1] {
                    b'e' => v.push(Dir::SouthEast),
                    b'w' => v.push(Dir::SouthWest),
                    _ => panic!(),
                };
                dir_str = &dir_str[2..];
            },
            _ => panic!(),
        }
    }

    v
}

fn main() {
    let mut hexmap = HashSet::<Pos>::new();

    for line in read_lines("input.txt").unwrap() {
        let directions = parse_directions(line.unwrap().as_bytes());
        flip_tile(&mut hexmap, &directions);
    }

    println!("Tiles: {} black", hexmap.len());
}
