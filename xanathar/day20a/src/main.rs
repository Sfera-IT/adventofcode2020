use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::{Iterator};
use std::collections::{VecDeque};
use regex::Regex;
use lazy_static::lazy_static;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Debug)]
struct Tile {
    id: u32,
    sides: [u32; 4],
}

impl Tile {
    fn parse(lines: &mut VecDeque<String>) -> Option<Self> {
        lazy_static! {
            static ref RE: Regex = Regex::new(r"^Tile (?P<id>\d+):$").unwrap();
        }

        let line = match lines.pop_front() {
            None => return None,
            Some(l) => l,
        };

        let cap = match RE.captures(&line) {
            None => return None,
            Some(l) => l,
        };

        let id = cap.name("id").unwrap().as_str().parse::<u32>().unwrap();

        let mut side_n = Vec::<u8>::new();
        let mut side_e = Vec::<u8>::new();
        let mut side_s = Vec::<u8>::new();
        let mut side_w = Vec::<u8>::new();

        loop {
            let line = match lines.pop_front() {
                Some(l) => Vec::from(l.as_bytes()),
                None => b"".to_vec(),
            };

            if !line.is_empty() {
                if side_n.is_empty() {
                    side_n = line.clone();
                }
                side_w.push(line[0]);
                side_e.push(line[line.len() - 1]);
                side_s = line.clone();
            } else {
                return Some(Tile {
                    id,
                    sides: Tile::calc_sides(side_n, side_e, side_s, side_w),
                });
            }
        }
    }

    fn calc_sides(n: Vec<u8>, e: Vec<u8>, s: Vec<u8>, w: Vec<u8>) -> [u32; 4] {
        let n = n.iter().fold(0, |a, c| a << 1 | if *c == b'#' { 1 } else { 0 });
        let e = e.iter().fold(0, |a, c| a << 1 | if *c == b'#' { 1 } else { 0 });
        let s = s.iter().fold(0, |a, c| a << 1 | if *c == b'#' { 1 } else { 0 });
        let w = w.iter().fold(0, |a, c| a << 1 | if *c == b'#' { 1 } else { 0 });

        [n, e, s, w]
    }

    fn xform(&self, xform: Xform) -> XformedTile {
        let sides = match xform {
            Xform::Flat   => [self.sides[0], self.sides[1], self.sides[2], self.sides[3]],
            Xform::Rot90  => rot(&self.sides),
            Xform::Rot180 => rot(&rot(&self.sides)),
            Xform::Rot270 => rot(&rot(&rot(&self.sides))),
            Xform::FlatFlipV   => flipv(&[self.sides[0], self.sides[1], self.sides[2], self.sides[3]]),
            Xform::Rot90FlipV  => flipv(&rot(&self.sides)),
            Xform::Rot180FlipV => flipv(&rot(&rot(&self.sides))),
            Xform::Rot270FlipV => flipv(&rot(&rot(&rot(&self.sides)))),
        };

        XformedTile {
            id: self.id,
            sides,
            xform,
        }
    }
}

fn rot(s: &[u32; 4]) -> [u32; 4] {
    [flip_side(s[3]), s[0], flip_side(s[1]), s[2]]
}

fn flipv(s: &[u32; 4]) -> [u32; 4] {
    [flip_side(s[0]), s[3], flip_side(s[2]), s[1]]
}

fn flip_side(v: u32) -> u32 {
    ((v & 0x1) << 9) |
    (((v >> 1) & 0x1) << 8) |
    (((v >> 2) & 0x1) << 7) |
    (((v >> 3) & 0x1) << 6) |
    (((v >> 4) & 0x1) << 5) |
    (((v >> 5) & 0x1) << 4) |
    (((v >> 6) & 0x1) << 3) |
    (((v >> 7) & 0x1) << 2) |
    (((v >> 8) & 0x1) << 1) |
    ((v >> 9) & 0x1)
}

#[derive(Copy, Clone, Debug)]
enum Xform {
    Flat,
    Rot90,
    Rot180,
    Rot270,
    FlatFlipV,
    Rot90FlipV,
    Rot180FlipV,
    Rot270FlipV,
}

static ALL_XFORMS: [Xform; 8] = [
    Xform::Flat,
    Xform::Rot90,
    Xform::Rot180,
    Xform::Rot270,
    Xform::FlatFlipV,
    Xform::Rot90FlipV,
    Xform::Rot180FlipV,
    Xform::Rot270FlipV,
];


#[derive(Clone)]
struct XformedTile {
    id: u32,
    sides: [u32; 4],
    xform: Xform,
}

struct Photo {
    tiles: Box<[Option<XformedTile>]>,
    size: usize,
}

impl Photo {
    fn new(size: usize) -> Self {
        Photo {
            tiles: vec![None; size * size].into_boxed_slice(),
            size,
        }
    }

    fn contains(&self, id: u32) -> bool {
        for t in self.tiles.iter() {
            if let Some(tt) = t {
                if tt.id == id {
                    return true;
                }
            }
        }
        false
    }

    fn get(&self, x: usize, y: usize) -> &Option<XformedTile> {
        &self.tiles[y * self.size + x]
    }

    fn set(&mut self, x: usize, y: usize, v: XformedTile) {
        self.tiles[y * self.size + x] = Some(v);
    }

    fn side_match(&self, new_side: u32, x: isize, y: isize, side_index: usize) -> bool {
        if x < 0 || y < 0 || x >= (self.size as isize) || y >= (self.size as isize) {
            return true;
        }

        let other = match self.get(x as usize, y as usize) {
            None => return true,
            Some(o) => o.sides[side_index],
        };

        other == new_side
    }

    fn try_set(&mut self, x: usize, y: usize, v: XformedTile) -> bool {
        let ix = x as isize;
        let iy = y as isize;

        if self.side_match(v.sides[0], ix, iy - 1, 2) &&
            self.side_match(v.sides[1], ix + 1, iy, 3) &&
            self.side_match(v.sides[2], ix, iy + 1, 0) &&
            self.side_match(v.sides[3], ix - 1, iy, 1)
        {
            self.set(x, y, v);
            true
        } else {
            false
        }
    }

    fn clear(&mut self, x: usize, y: usize) {
        self.tiles[y * self.size + x] = None;
    }

    fn free(&self) -> Option<(usize, usize)> {
        for y in 0..self.size {
            for x in 0..self.size {
                if self.get(x, y).is_none() {
                    return Some((x, y));
                }
            }
        }
        None
    }

    fn try_solve(&mut self, tiles: &[Tile], recurse: u32) -> bool {
        let (x, y) = match self.free() {
            Some((x, y)) => (x, y),
            None => return true,
        };

        for t in tiles {
            if self.contains(t.id) {
                continue;
            }

            for xform in ALL_XFORMS.iter() {
                let t = t.xform(*xform);
                if self.try_set(x, y, t.clone()) {
                    if self.try_solve(&tiles, recurse + 1) {
                        return true;
                    } else {
                        self.clear(x, y);
                    }
                 }
            }
        }

        false
    }

    fn print(&self) {
        for y in 0..self.size {
            for x in 0..self.size {
                print!("{:?}    ", match self.get(x, y) {
                    None => "????".to_string(),
                    Some(v) => format!("{}", v.id),
                });
            }
            println!();
        }
    }

    fn result(&self) -> u64 {
        let a = self.get(0, 0).as_ref().unwrap().id as u64;
        let b = self.get(0, self.size - 1).as_ref().unwrap().id as u64;
        let c = self.get(self.size - 1, 0).as_ref().unwrap().id as u64;
        let d = self.get(self.size - 1, self.size - 1).as_ref().unwrap().id as u64;
        a * b * c * d
    }
}

fn main() {
    let mut lines = read_lines("tiles.txt").unwrap().map(|s| s.unwrap()).collect::<VecDeque<String>>();
    let mut tiles = Vec::new();

    while let Some(t) = Tile::parse(&mut lines) {
        println!("Loaded tile {} : {:?}", t.id, t.sides);
        tiles.push(t);
    }

    let mut photo = Photo::new(12);

    println!("Solving...");

    let result = photo.try_solve(&tiles, 0);

    println!("Done? {}", result);

    if result {
        println!("SOLUTION: {}", photo.result());
    }

    println!();

    photo.print();
}
