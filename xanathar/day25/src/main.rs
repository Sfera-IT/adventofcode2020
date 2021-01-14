fn transform_subject(subject: u64, loopsize: u64) -> u64 {
    let mut num = 1;

    for _ in 1..=loopsize {
        num = (num * subject) % 20201227;
    }

    num
}

fn find_loop_size(subject: u64, target: u64) -> u64 {
    let mut num = 1;

    for loopsize in 1..(std::u32::MAX as u64) {
        num = (num * subject) % 20201227;

        if num == target {
            return loopsize;
        }
    }

    panic!("not found");
}

fn main() {
    const INITIAL_SUBJECT:u64 = 7;
    const CARD_PUBLIC_KEY:u64 = 10705932;
    const DOOR_PUBLIC_KEY:u64 = 12301431;

    let door_loop_size = find_loop_size(INITIAL_SUBJECT, DOOR_PUBLIC_KEY);
    println!("door_loop_size = {}", door_loop_size);

    let card_loop_size = find_loop_size(INITIAL_SUBJECT, CARD_PUBLIC_KEY);
    println!("card_loop_size = {}", card_loop_size);

    let secret1 = transform_subject(CARD_PUBLIC_KEY, door_loop_size);
    let secret2 = transform_subject(DOOR_PUBLIC_KEY, card_loop_size);

    println!("secrets: {} == {}", secret1, secret2);
}
