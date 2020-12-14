use std::iter::Iterator;

fn main() {
    let buses = vec![23,0,0,0,0,0,0,0,0,0,0,0,0,41,0,0,0,0,0,0,0,0,0,829,0,0,0,0,0,0,0,0,0,0,0,0,13,17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,29,0,677,0,0,0,0,0,37,0,0,0,0,0,0,0,0,0,0,0,0,19];
    let pairs: Vec<(u64, u64)> = buses.iter()
        .enumerate()
        .filter_map(|(p, b)| if *b == 0 {
            None
        } else {
            Some(((*b - (p as u64 % *b)) % *b, *b))
        })
        .collect();

    let busproduct: u64 = buses.iter().filter(|n| **n != 0).product();

    let mut sols = 0;

    for (rem, num) in &pairs {
        let base = busproduct / num;
        let mut n = base;

        loop {
            if (n % num) == *rem {
                sols += n;
                break;
            }
            n += base;
        }
    }
    while sols > busproduct {
        sols -= busproduct;
    }

    println!("Result = {}", sols);
}
