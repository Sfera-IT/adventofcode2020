use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Copy, Clone, Debug, PartialEq)]
enum Seat {
    Corridor,
    Empty,
    Occupied,
}

struct Ferry {
    layout: Box<[Seat]>,
    width: usize,
    height: usize,
}

impl Ferry {
    fn load(file: &str) -> Ferry {
        let lines = read_lines(file)
            .unwrap()
            .filter_map(|s| s.ok());

        let mut height = 0;
        let mut width = 0;
        let mut layout = Vec::new();

        for line in lines {
            if width == 0 {
                width = line.len();
            } else {
                assert_eq!(width, line.len());
            }
            height += 1;

            for c in line.chars() {
                layout.push(match c {
                    '.' => Seat::Corridor,
                    'L' => Seat::Empty,
                    '#' => Seat::Occupied,
                    c => panic!("unexpected: {}", c),
                });
            }
        }

        Ferry {
            width,
            height,
            layout: layout.into_boxed_slice(),
        }
    }

    fn at(&self, x: isize, y: isize) -> Option<Seat> {
        if x < 0 || y < 0 || x >= (self.width as isize) || y >= (self.height as isize) {
            None
        } else {
            Some(self.layout[(y as usize) * self.width + (x as usize)])
        }
    }

    fn ray(&self, mut x: isize, mut y: isize, dx: isize, dy: isize) -> Seat {
        loop {
            x += dx;
            y += dy;

            match self.at(x, y) {
                Some(Seat::Corridor) => (),
                Some(seat) => return seat,
                None => return Seat::Corridor,
            }
        }
    }

    fn evolve_single(&self, x: usize, y: usize) -> (Seat, bool) {
        // If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
        // If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
        // Otherwise, the seat's state does not change.

        let x = x as isize;
        let y = y as isize;
        let cur = self.at(x, y).unwrap_or(Seat::Corridor);
        let mut occupied = 0;

        for dy in -1..=1 {
            for dx in -1..=1 {
                if (dx != 0 || dy != 0) && self.ray(x, y, dx, dy) == Seat::Occupied {
                    occupied += 1;
                }
            }
        }

        let new = match (cur, occupied) {
            (Seat::Empty, o) if o == 0 => Seat::Occupied,
            (Seat::Occupied, o) if o >= 5 => Seat::Empty,
            (s, _) => s,
        };

        (new, new != cur)
    }

    fn evolve(&mut self) -> bool {
        let mut new = vec![Seat::Corridor; self.layout.len()];
        let mut changed = false;

        for y in 0..self.height {
            for x in 0..self.width {
                let (new_seat, has_changed) = self.evolve_single(x, y);
                new[(y as usize) * self.width + (x as usize)] = new_seat;
                changed |= has_changed;
            }
        }

        if changed {
            self.layout = new.into_boxed_slice();
        }

        changed
    }

    fn count_occupied(&self) -> usize {
        self.layout.iter().filter(|s| **s == Seat::Occupied).count()
    }
}


fn main() {
    let mut ferry = Ferry::load("ferry.txt");

    loop {
        if !ferry.evolve() {
            println!("Occupied: {}", ferry.count_occupied());
            break;
        }
    }
}
