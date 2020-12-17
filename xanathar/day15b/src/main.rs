#![allow(clippy::needless_range_loop)]
use std::collections::HashMap;

struct ElfGameState {
    last: u64,
    turn: u64,
    history: HashMap<u64, u64>,
}

impl ElfGameState {
    fn new() -> Self {
        ElfGameState {
            last: 0,
            turn: 0,
            history: HashMap::new(),
        }
    }

    fn initial(&mut self, init: Vec<u64>) {
        for t in 0..(init.len() - 1) {
            self.history.insert(init[t], (t + 1) as u64);
        }

        self.turn = (init.len() - 1) as u64;
        self.last = self.play_round(init[init.len() - 1]);
    }

    fn play_round(&mut self, next_val: u64) -> u64 {
        self.turn += 1;

        let next = match self.history.get(&next_val) {
            Some(t) => self.turn - t,
            None => 0,
        };

        self.history.insert(next_val, self.turn);
        next
    }

    fn play(&mut self) {
        self.last = self.play_round(self.last);
    }

    fn len(&self) -> u64 {
        self.turn + 1
    }

    fn last(&self) -> u64 {
        self.last
    }
}

fn main() {
    let mut game = ElfGameState::new();
    game.initial(vec![10,16,6,0,1,17]);

    while game.len() < 30000000 {
        game.play();
    }

    println!("ELF: {}", game.last());
}
