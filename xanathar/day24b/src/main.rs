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

fn count_black_neighbours(pos: Pos, hexmap: &HashSet<Pos>) -> usize {
    let mut count = 0;

    if hexmap.contains(&pos.walk(Dir::East)) { count += 1; }
    if hexmap.contains(&pos.walk(Dir::NorthEast)) { count += 1; }
    if hexmap.contains(&pos.walk(Dir::NorthWest)) { count += 1; }
    if hexmap.contains(&pos.walk(Dir::SouthEast)) { count += 1; }
    if hexmap.contains(&pos.walk(Dir::SouthWest)) { count += 1; }
    if hexmap.contains(&pos.walk(Dir::West)) { count += 1; }

    count
}


fn art_exhib_day(hexmap: HashSet<Pos>) -> HashSet<Pos> {
    let mut newmap = HashSet::<Pos>::new();
    let mut whites = HashSet::new();

    for pos in hexmap.iter() {
        if !hexmap.contains(&pos.walk(Dir::East)) { whites.insert(pos.walk(Dir::East)); }
        if !hexmap.contains(&pos.walk(Dir::NorthEast)) { whites.insert(pos.walk(Dir::NorthEast)); }
        if !hexmap.contains(&pos.walk(Dir::NorthWest)) { whites.insert(pos.walk(Dir::NorthWest)); }
        if !hexmap.contains(&pos.walk(Dir::SouthEast)) { whites.insert(pos.walk(Dir::SouthEast)); }
        if !hexmap.contains(&pos.walk(Dir::SouthWest)) { whites.insert(pos.walk(Dir::SouthWest)); }
        if !hexmap.contains(&pos.walk(Dir::West)) { whites.insert(pos.walk(Dir::West)); }

        let black_neighbours = count_black_neighbours(*pos, &hexmap);
        if black_neighbours == 1 || black_neighbours == 2 {
            newmap.insert(*pos);
        }
    }

    for pos in whites.iter() {
        if count_black_neighbours(*pos, &hexmap) == 2 {
            newmap.insert(*pos);
        }
    }

    newmap
}



fn main() {
    let mut hexmap = HashSet::<Pos>::new();

    for line in read_lines("input.txt").unwrap() {
        let directions = parse_directions(line.unwrap().as_bytes());
        flip_tile(&mut hexmap, &directions);
    }

    println!("Tiles: {} black", hexmap.len());

    for day in 1..=100 {
        hexmap = art_exhib_day(hexmap);
        println!("Day {} : {} black", day, hexmap.len());
    }
}
