#![allow(clippy::needless_range_loop)]
use std::collections::VecDeque;
use std::iter::Iterator;

struct History(Vec<u32>, Vec<u32>);

impl History {
    fn new(deck1: &VecDeque<u32>, deck2: &VecDeque<u32>) -> Self {
        let pl1 = deck1.iter().copied().collect::<Vec<u32>>();
        let pl2 = deck2.iter().copied().collect::<Vec<u32>>();
        History(pl1, pl2)
    }
    fn is_same(&self, deck1: &VecDeque<u32>, deck2: &VecDeque<u32>) -> bool {
        if deck1.len() != self.0.len() || deck2.len() != self.1.len() {
            return false;
        }

        for i in 0..deck1.len() {
            if deck1[i] != self.0[i] {
                return false;
            }
        }

        for i in 0..deck2.len() {
            if deck2[i] != self.1[i] {
                return false;
            }
        }

        true
    }
}

#[derive(Debug)]
enum Winner {
    Player1,
    Player2,
}

fn calc_score(mut deck: VecDeque<u32>) -> u64 {
    let mut sum = 0;
    let mut index = 0;

    while let Some(card) = deck.pop_back() {
        index += 1;
        sum += (card as u64) * index;
    }

    sum
}

fn play_game(start_deck1: Vec<u32>, start_deck2: Vec<u32>) -> (Winner, u64) {
    let mut history = Vec::<History>::new();
    let mut deck1 = VecDeque::from(start_deck1);
    let mut deck2 = VecDeque::from(start_deck2);

    loop {
        match play_round(&mut history, &mut deck1, &mut deck2) {
            None => (),
            Some(Winner::Player1) => return (Winner::Player1, calc_score(deck1)),
            Some(Winner::Player2) => return (Winner::Player2, calc_score(deck2)),
        }
    }
}

fn play_round(history: &mut Vec<History>, deck1: &mut VecDeque<u32>, deck2: &mut VecDeque<u32>) -> Option<Winner> {
    if deck1.is_empty() {
        return Some(Winner::Player2);
    }

    if deck2.is_empty() {
        return Some(Winner::Player1);
    }

    if history.iter().any(|h| h.is_same(&deck1, &deck2)) {
        return Some(Winner::Player1);
    }

    history.push(History::new(&deck1, &deck2));

    let card1 = deck1.pop_front().unwrap();
    let card2 = deck2.pop_front().unwrap();

    let winner = if (card1 as usize) <= deck1.len() && (card2 as usize) <= deck2.len() {
        let copydeck1 = deck1.iter().take(card1 as usize).copied().collect::<Vec<u32>>();
        let copydeck2 = deck2.iter().take(card2 as usize).copied().collect::<Vec<u32>>();

        play_game(copydeck1, copydeck2).0
    } else if card1 > card2 {
        Winner::Player1
    } else {
        Winner::Player2
    };

    match winner {
        Winner::Player1 => {
            deck1.push_back(card1);
            deck1.push_back(card2);
        },
        Winner::Player2 => {
            deck2.push_back(card2);
            deck2.push_back(card1);
        },
    }

    None
}

fn main() {
    let start_deck1 = vec![50, 19, 40, 22, 7, 4, 3, 16, 34, 45, 46, 39, 44, 32, 20, 29, 15, 35, 41, 2, 21, 28, 6, 26, 48];
    let start_deck2 = vec![14, 9, 37, 47, 38, 27, 30, 24, 36, 31, 43, 42, 11, 17, 18, 10, 12, 5, 33, 25, 8, 23, 1, 13, 49];

    let (winner, score) = play_game(start_deck1, start_deck2);

    println!("Win by {:?} with score of {}", winner, score);
}
