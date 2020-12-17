fn elfgame(history: &mut Vec<usize>) {
    let last = history[history.len() - 1];
    let mut next = 0;
    for i in (0..(history.len()-1)).rev() {
        if last == history[i] {
            next = history.len() - i - 1;
            break;
        }
    }
    history.push(next);
}

fn main() {
    let mut history = vec![10,16,6,0,1,17];

    while history.len() < 2020 {
        elfgame(&mut history);
    }

    println!("ELF: {}", history[history.len() - 1]);
}
