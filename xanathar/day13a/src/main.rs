use std::iter::Iterator;

fn main() {
    fn wait(time: u64, bus: u64) -> u64 {
        bus - (time % bus)
    }

    let time = 1002632;
    let buses = vec![23,0,0,0,0,0,0,0,0,0,0,0,0,41,0,0,0,0,0,0,0,0,0,829,0,0,0,0,0,0,0,0,0,0,0,0,13,17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,29,0,677,0,0,0,0,0,37,0,0,0,0,0,0,0,0,0,0,0,0,19];

    let bus = buses.iter().filter(|b| **b != 0).min_by(|a, b| wait(time, **a).cmp(&wait(time, **b))).unwrap();
    println!("BUS = {}  WAIT = {}  RES = {}", bus, wait(time, *bus), bus * wait(time, *bus));
}
