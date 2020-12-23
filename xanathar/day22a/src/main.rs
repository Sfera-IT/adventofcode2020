use std::collections::VecDeque;

fn play_round(deck1: &mut VecDeque<u32>, deck2: &mut VecDeque<u32>) {
    let card1 = deck1.pop_front().unwrap();
    let card2 = deck2.pop_front().unwrap();

    if card1 > card2 {
        deck1.push_back(card1);
        deck1.push_back(card2);
    } else {
        deck2.push_back(card2);
        deck2.push_back(card1);
    }
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

fn main() {
    let mut deck1 = VecDeque::from(vec![50, 19, 40, 22, 7, 4, 3, 16, 34, 45, 46, 39, 44, 32, 20, 29, 15, 35, 41, 2, 21, 28, 6, 26, 48]);
    let mut deck2 = VecDeque::from(vec![14, 9, 37, 47, 38, 27, 30, 24, 36, 31, 43, 42, 11, 17, 18, 10, 12, 5, 33, 25, 8, 23, 1, 13, 49]);

    while !deck1.is_empty() && !deck2.is_empty() {
        play_round(&mut deck1, &mut deck2);
    }

    let score = if deck1.is_empty() { calc_score(deck2) } else { calc_score(deck1) };
    println!("{}", score);
}
