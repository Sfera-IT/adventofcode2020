use std::iter::Iterator;

struct CupsGame {
    current: u32,
    cups: Vec<u32>,
    moves: u32,
}

impl CupsGame {
    fn new(cups: Vec<u32>) -> Self {
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

        println!();
        println!("-- move {} --", self.moves);

        print!("cups:");
        for i in 0..self.cups.len() {
            if self.cups[i] == self.current {
                print!(" ({})", self.cups[i]);
            } else {
                print!(" {}", self.cups[i]);
            }
        }
        println!();

        let curidx = self.find(self.current).unwrap();

        let nextidx = (curidx + 1) % self.cups.len();
        let pick1 = self.cups.remove(nextidx);
        let nextidx = nextidx % self.cups.len();
        let pick2 = self.cups.remove(nextidx);
        let nextidx = nextidx % self.cups.len();
        let pick3 = self.cups.remove(nextidx);

        println!("pick up: {}, {}, {}", pick1, pick2, pick3);

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

        println!("destination: {}", self.cups[insert_idx]);

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

        print!("cups:");
        for i in 0..self.cups.len() {
            if self.cups[i] == self.current {
                print!(" ({})", self.cups[i]);
            } else {
                print!(" {}", self.cups[i]);
            }
        }

        println!();
        print!("solution: ");
        let mut index = self.find(1).unwrap() + 1;
        while self.cups[index % self.cups.len()] != 1 {
            print!("{}", self.cups[index % self.cups.len()]);
            index += 1;
        }
        println!();
        println!();
    }
}

fn main() {
    let mut game = CupsGame::new(vec![3,8,9,5,4,7,6,1,2]);

    for _ in 0..100 {
        game.play_move();
    }

    game.fin();
}
