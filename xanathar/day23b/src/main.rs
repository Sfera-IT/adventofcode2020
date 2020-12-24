use std::iter::Iterator;

// A proper solution would use a real ring to run.
// This takes around 3 hours to run.
// Implementing a real ring in Rust takes more than 3 hours,
// keeping 2 resources busy (me and my PC) rather than just one.
// Merry Christmas.

struct CupsGame {
    current: u32,
    cups: Vec<u32>,
    moves: u32,
}

impl CupsGame {
    fn new(mut cups: Vec<u32>) -> Self {

        let max = cups.iter().max().unwrap();

        for i in (max+1)..=1_000_000 {
            cups.push(i);
        }

        CupsGame {
            current: cups[0],
            cups,
            moves: 0,
        }
    }

    fn find(&self, num: u32) -> Option<usize> {
        for i in 0..self.cups.len() {
            if self.cups[i] == num {
                return Some(i);
            }
        }
        None
    }

    fn play_move(&mut self) {
        self.moves += 1;

        let curidx = self.find(self.current).unwrap();

        let nextidx = (curidx + 1) % self.cups.len();
        let pick1 = self.cups.remove(nextidx);
        let nextidx = nextidx % self.cups.len();
        let pick2 = self.cups.remove(nextidx);
        let nextidx = nextidx % self.cups.len();
        let pick3 = self.cups.remove(nextidx);

        let mut insert_idx = {
            let mut start = self.current;
            loop {
                start -= 1;
                if start == 0 {
                    break self.cups.iter().enumerate().max_by_key(|(_, e)| *e).map(|(i, _)| i).unwrap();
                } else if let Some(i) = self.find(start) {
                    break i;
                }
            }
        };

        insert_idx = (insert_idx + 1) % self.cups.len();

        self.cups.insert(insert_idx, pick3);
        self.cups.insert(insert_idx, pick2);
        self.cups.insert(insert_idx, pick1);

        let nextcuridx = (self.find(self.current).unwrap() + 1) % self.cups.len();
        self.current = self.cups[nextcuridx];
    }

    fn fin(&self) {
        println!();
        println!("-- final --");

        let idx1 = self.find(1).unwrap();
        let sol1 = self.cups[(idx1 + 1) % self.cups.len()] as u64;
        let sol2 = self.cups[(idx1 + 2) % self.cups.len()] as u64;

        println!("solution: {} * {} = {}", sol1, sol2, sol1 * sol2);

        println!();
    }
}

fn main() {
    let mut game = CupsGame::new(vec![3,8,9,5,4,7,6,1,2]);

    for it in 0..10_000_000 {
        game.play_move();

        if (it % 1000) == 0 {
            println!("[{} / 10000000] - {}%", it, (it as f32) / 100000.0);
        }
    }

    game.fin();
}
