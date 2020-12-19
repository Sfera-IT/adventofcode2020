use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::iter::Iterator;
use std::collections::VecDeque;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Copy, Clone, Debug)]
enum Token {
    Num(i64),
    Add,
    Mul,
    SubExpr,
    SubExprClose,
}

enum Ast {
    Num(i64),
    Add(Box<Ast>, Box<Ast>),
    Mul(Box<Ast>, Box<Ast>),
}

fn lexer_flush(cur: &mut String, res: &mut VecDeque<Token>) {
    if !cur.is_empty() {
        res.push_back(Token::Num(cur.parse::<i64>().unwrap()));
        cur.clear();
    }
}

fn lexer(expr: &str) -> VecDeque<Token> {
    let mut cur = String::new();
    let mut res = VecDeque::new();

    for c in expr.chars() {
        match c {
            c if c.is_numeric() => cur.push(c),
            '+' => {
                lexer_flush(&mut cur, &mut res);
                res.push_back(Token::Add);
            }
            '*' => {
                lexer_flush(&mut cur, &mut res);
                res.push_back(Token::Mul);
            }
            '(' => {
                lexer_flush(&mut cur, &mut res);
                res.push_back(Token::SubExpr);
            }
            ')' => {
                lexer_flush(&mut cur, &mut res);
                res.push_back(Token::SubExprClose);
            }
            ' ' => lexer_flush(&mut cur, &mut res),
            _ => panic!("Unexpected char: '{}'", c),
        }
    }

    lexer_flush(&mut cur, &mut res);

    res
}

fn parse_right_hand(mut tokens: &mut VecDeque<Token>) -> Box<Ast> {
    match tokens.pop_front() {
        Some(Token::Num(n)) => Box::new(Ast::Num(n)),
        Some(Token::SubExpr) => {
            let sub_expr = parse_expr(&mut tokens);
            parse_expect_close(&mut tokens);
            sub_expr
        }
        Some(t) => panic!("unexpected token {:?} - rh expected", t),
        None => panic!("unexpected termination - rh expected"),
    }
}

fn parse_make_op(op: Token, left: Box<Ast>, right: Box<Ast>) -> Box<Ast> {
    match op {
        Token::Add => Box::new(Ast::Add(left, right)),
        Token::Mul => Box::new(Ast::Mul(left, right)),
        _ => panic!("unexpected token {:?}", op)
    }
}

fn parse_is_op(op: Option<&Token>) -> bool {
    match op {
        Some(Token::Add) | Some(Token::Mul) => true,
        _ => false
    }
}

fn parse_expect_close(tokens: &mut VecDeque<Token>) {
    match tokens.pop_front() {
        Some(Token::SubExprClose) => (),
        Some(t) => panic!("unexpected token {:?} - ')' expected", t),
        None => panic!("unexpected termination - ')' expected"),
    }
}

fn parse_expr(mut tokens: &mut VecDeque<Token>) -> Box<Ast> {
    let token = tokens.pop_front();

    let (mut result, mut root_result_token) = match token {
        Some(Token::Num(n)) => {
            let mut left = Box::new(Ast::Num(n));

            match tokens.pop_front() {
                Some(op) => {
                    left = parse_make_op(op, left, parse_right_hand(&mut tokens));
                    (left, op)
                },
                None => panic!("unexpected termination - operator expected"),
            }
        },
        Some(Token::SubExpr) => {
            let parsed = parse_expr(&mut tokens);
            parse_expect_close(&mut tokens);
            (parsed, Token::SubExpr)
        }
        _ => unimplemented!()
    };

    while parse_is_op(tokens.front()) {
        let new_op = tokens.pop_front().unwrap();

        match (root_result_token, new_op) {
            (Token::SubExpr, _) | (Token::Add, Token::Add) | (_, Token::Mul) => {
                result = parse_make_op(new_op, result, parse_right_hand(&mut tokens));
                root_result_token = new_op;
            },
            (Token::Mul, Token::Add) => {
                if let Ast::Mul(left, right) = *result {
                    result = parse_make_op(Token::Mul, left, parse_make_op(Token::Add, right, parse_right_hand(&mut tokens)));
                    root_result_token = Token::Mul;
                } else {
                    panic!()
                }
            },
            (_, _) => panic!("unexpected pattern"),
        }
    }

    result
}

fn solve_ast(ast: &Ast) -> i64 {
    match ast {
        Ast::Num(n) => *n,
        Ast::Mul(a, b) => solve_ast(&a) * solve_ast(&b),
        Ast::Add(a, b) => solve_ast(&a) + solve_ast(&b),
    }
}

fn calc(expr: &str) -> i64 {
    let mut tokens = lexer(expr);
    let ast = parse_expr(&mut tokens);
    solve_ast(&ast)
}

fn main() {
    let sum: i64 = read_lines("math.txt")
        .unwrap()
        .map(|s| s.unwrap())
        .filter(|s| !s.is_empty())
        .map(|s| calc(&s))
        .sum();

    println!("SUM: {}", sum);
}

mod tests {
    #![cfg(test)]
    use super::*;

    #[test]
    fn test_expr1() {
        assert_eq!(calc("2 + 3"), 5);
    }

    #[test]
    fn test_expr2() {
        assert_eq!(calc("2 + 3 + 4"), 9);
    }

    #[test]
    fn test_expr3() {
        assert_eq!(calc("(2 + 3 + 4)"), 9);
    }

    #[test]
    fn test_expr4() {
        assert_eq!(calc("(2 + 3) + 4"), 9);
    }

    #[test]
    fn test_expr5() {
        assert_eq!(calc("2 + (3 + 4)"), 9);
    }

    #[test]
    fn test_expr6() {
        assert_eq!(calc("2 + (3 * 4)"), 14);
    }

    #[test]
    fn test_expr7() {
        assert_eq!(calc("2 + 3 * 4"), 20);
    }

    #[test]
    fn test_expr8() {
        assert_eq!(calc("(2 + 3) * 4"), 20);
    }

    #[test]
    fn test_expr9() {
        assert_eq!(calc("2 * 3 + 4"), 14);
    }
}
