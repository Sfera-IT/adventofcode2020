use std::collections::{HashSet, HashMap};
use std::iter::Iterator;


fn parse_line(y: i64, line: &str, grid: &mut HashSet<(i64, i64, i64, i64)>) {
    for (x, c) in line.chars().enumerate() {
        if c == '#' {
            grid.insert((x as i64, y, 0, 0));
        }
    }
}

fn evolve(grid: &mut HashSet<(i64, i64, i64, i64)>) {
    let mut to_be_removed = HashSet::new();
    let mut to_be_inserted = HashMap::new();

    for (x,y,z,w) in grid.iter().copied() {
        let mut neighbours = 0;

        for dx in -1..=1 {
            for dy in -1..=1 {
                for dz in -1..=1 {
                    for dw in -1..=1 {
                        if dx != 0 || dy != 0 || dz != 0 || dw != 0 {
                            let coords = (x + dx, y + dy, z + dz, w + dw);

                            if grid.contains(&coords) {
                                neighbours += 1;
                            } else {
                                let inactive_neighbours = to_be_inserted.entry(coords).or_insert(0);
                                *inactive_neighbours += 1;
                            }
                        }
                    }
                }
            }
        }

        if neighbours != 2 && neighbours != 3 {
            to_be_removed.insert((x, y, z, w));
        }
    }

    grid.retain(|p| !to_be_removed.contains(p));

    for ((x, y, z, w), n) in to_be_inserted.iter() {
        if *n == 3 {
            grid.insert((*x, *y, *z, *w));
        }
    }
}

fn main() {
    let mut grid = HashSet::new();

    parse_line(0, "#.##....", &mut grid);
    parse_line(1, ".#.#.##.", &mut grid);
    parse_line(2, "###.....", &mut grid);
    parse_line(3, "....##.#", &mut grid);
    parse_line(4, "#....###", &mut grid);
    parse_line(5, ".#.#.#..", &mut grid);
    parse_line(6, ".##...##", &mut grid);
    parse_line(7, "#..#.###", &mut grid);

    for _ in 0..6 {
        evolve(&mut grid);
    }

    println!("Result: {}", grid.len());
}
