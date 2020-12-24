use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::{Iterator, FromIterator};
use std::collections::HashSet;
use regex::Regex;
use lazy_static::lazy_static;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Debug)]
struct Recipe {
    ingredients: HashSet<String>,
    allergens: HashSet<String>,
}

impl Recipe {
    fn parse(line: &str) -> Self {
        lazy_static! {
            static ref RE: Regex = Regex::new(r"^(?P<ingredients>[a-z ]+) \(contains (?P<allergens>[a-z, ]+)\)$").unwrap();
        }

        let cap = RE.captures(line).unwrap();
        let ingredient_list = cap.name("ingredients").unwrap().as_str();
        let allergen_list = cap.name("allergens").unwrap().as_str();

        let ingredients = ingredient_list.split(' ').map(|p| p.to_string()).collect::<HashSet<String>>();
        let allergens = allergen_list.split(", ").map(|p| p.to_string()).collect::<HashSet<String>>();

        Recipe { ingredients, allergens }
    }
}

#[derive(Debug, Clone)]
struct Ingredient {
    name: String,
    potential_allergens: HashSet<String>,
    allergen: Option<String>,
}


fn main() {
    let recipes = read_lines("recipes.txt").unwrap().map(|s| Recipe::parse(&s.unwrap())).collect::<Vec<Recipe>>();
    let allergens = recipes.iter().flat_map(|r| r.allergens.iter()).cloned().collect::<Vec<String>>();
    let ingredients = recipes.iter().flat_map(|r| r.ingredients.iter()).cloned().collect::<HashSet<String>>();
    let mut ingredients = ingredients.iter().map(|i| Ingredient {
        name: i.clone(),
        potential_allergens: HashSet::from_iter(allergens.iter().cloned()),
        allergen: None,
    }).collect::<Vec<Ingredient>>();

    for r in &recipes {
        for a in &r.allergens {
            for i in &mut ingredients {
                if !r.ingredients.contains(&i.name) {
                    i.potential_allergens.remove(a);
                }
            }
        }
    }

    loop {
        let mut reduce_allergen = None;
        for i in &mut ingredients {
            if i.allergen.is_none() && i.potential_allergens.len() == 1 {
                let allergen = i.potential_allergens.iter().next().unwrap();
                reduce_allergen = Some(allergen.clone());
                i.allergen = Some(allergen.clone());
                break;
            }
        }
        if let Some(a) = reduce_allergen {
            for i in &mut ingredients {
                if i.allergen.is_none() {
                    i.potential_allergens.remove(&a);
                }
            }
        } else {
            break;
        }
    }

    let mut canonical = ingredients.iter().filter(|i| i.allergen.is_some()).cloned().collect::<Vec<Ingredient>>();

    canonical.sort_unstable_by_key(|i| i.allergen.clone());

    let mut first = true;
    for i in &canonical {
        if first {
            first = false;
        } else {
            print!(",");
        }
        print!("{}", i.name);
    }
    println!();
}
