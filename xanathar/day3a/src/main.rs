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

fn main() {
    let (mut x, mut y) = (0, 0);
    let map = Map::read_from_file("map.txt");
    let mut tree_count = 0;

    loop {
        match map.at(x, y) {
            Cell::Snow => (),
            Cell::Tree => tree_count += 1,
            Cell::Goal => break,
        }
        x += 3;
        y += 1;
    }

    println!("Trees: {}", tree_count);
}
