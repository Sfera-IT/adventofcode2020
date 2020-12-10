use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Copy, Clone, PartialEq, Debug)]
enum Cell {
    Snow,
    Tree,
    Goal,
}

struct Map {
    cells: Box<[Box<[Cell]>]>,
    width: usize,
    height: usize,
}

impl Map {
    fn parse_cell_line(line: &str) -> Box<[Cell]> {
        line.chars()
            .filter_map(|c| match c {
                '.' => Some(Cell::Snow),
                '#' => Some(Cell::Tree),
                _ => None,
            }).collect::<Box<[Cell]>>()
    }

    pub fn read_from_file(filename: &str) -> Map {
        let cells: Box<[Box<[Cell]>]> = read_lines(filename)
            .unwrap()
            .map(|s| Map::parse_cell_line(&s.unwrap()))
            .collect();

        if cells.len() == 0 {
            panic!("empty map");
        }

        let width = cells[0].len();
        let height = cells.len();

        for l in cells.iter() {
            if l.len() != width {
                panic!("width");
            }
        }

        Map {
            cells,
            width,
            height,
        }
    }

    pub fn at(&self, x: usize, y: usize) -> Cell {
        if y >= self.height {
            Cell::Goal
        } else {
            self.cells[y][x % self.width]
        }
    }
}

fn calc_slope(dx: usize, dy: usize) -> u64 {
    let (mut x, mut y) = (0, 0);
    let map = Map::read_from_file("map.txt");
    let mut tree_count = 0;

    loop {
        match map.at(x, y) {
            Cell::Snow => (),
            Cell::Tree => tree_count += 1,
            Cell::Goal => break,
        }
        x += dx;
        y += dy;
    }

    tree_count
}


fn main() {
    // Right 1, down 1.
    let s1 = calc_slope(1, 1);
    // Right 3, down 1. (This is the slope you already checked.)
    let s2 = calc_slope(3, 1);
    // Right 5, down 1.
    let s3 = calc_slope(5, 1);
    // Right 7, down 1.
    let s4 = calc_slope(7, 1);
    // Right 1, down 2.
    let s5 = calc_slope(1, 2);

    println!("{}*{}*{}*{}*{} = {}", s1, s2, s3, s4, s5, s1*s2*s3*s4*s5);
}
