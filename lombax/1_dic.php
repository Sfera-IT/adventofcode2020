<?php

/**
 *
 *
 * --- Day 1: Report Repair ---

After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical island. Surely, Christmas will go on without you.

The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little picture of a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of them, but somehow, you'll need to find fifty of these coins by the time you arrive so you can pay the deposit on your room.

To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456
In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?

To begin, get your puzzle input.
 *
 *
 *
 *
 * --- Part Two ---

The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?
 *
 *
 *
 *
 */

$numbers = [
    '1583',
    '1295',
    '1747',
    '1628',
    '1756',
    '1992',
    '1984',
    '1990',
    '2006',
    '1626',
    '1292',
    '1561',
    '1697',
    '1249',
    '2001',
    '1822',
    '1715',
    '1951',
    '1600',
    '1615',
    '1769',
    '1825',
    '1335',
    '1987',
    '1745',
    '1660',
    '1952',
    '1437',
    '1348',
    '1968',
    '615',
    '1847',
    '476',
    '1346',
    '1357',
    '1838',
    '1955',
    '1750',
    '1831',
    '2003',
    '1730',
    '1696',
    '1257',
    '1581',
    '866',
    '1765',
    '1691',
    '1995',
    '1977',
    '1988',
    '1713',
    '1599',
    '1300',
    '1892',
    '1550',
    '2002',
    '1694',
    '1930',
    '1998',
    '1564',
    '1704',
    '1398',
    '864',
    '1480',
    '1578',
    '1946',
    '1850',
    '1964',
    '1914',
    '1860',
    '1979',
    '1857',
    '1969',
    '1675',
    '1967',
    '2009',
    '1950',
    '1834',
    '783',
    '1935',
    '1963',
    '1659',
    '1314',
    '1647',
    '1671',
    '1706',
    '1734',
    '1965',
    '1666',
    '316',
    '1657',
    '1663',
    '1373',
    '1719',
    '1778',
    '1559',
    '1869',
    '1958',
    '1986',
    '1845',
    '1643',
    '1783',
    '1670',
    '1445',
    '1758',
    '2008',
    '1680',
    '1251',
    '1982',
    '1420',
    '1621',
    '1997',
    '1785',
    '1994',
    '1376',
    '1944',
    '1771',
    '1844',
    '96',
    '467',
    '1954',
    '903',
    '1368',
    '1305',
    '1589',
    '1970',
    '1980',
    '1521',
    '1775',
    '1629',
    '1796',
    '1985',
    '1957',
    '1669',
    '1637',
    '1606',
    '1766',
    '1972',
    '1956',
    '1685',
    '1235',
    '58',
    '1996',
    '1959',
    '1788',
    '1273',
    '1378',
    '1233',
    '1470',
    '1584',
    '1741',
    '1327',
    '1763',
    '1989',
    '1665',
    '1667',
    '1975',
    '1862',
    '1791',
    '1229',
    '1873',
    '1761',
    '1754',
    '1882',
    '1642',
    '1971',
    '1777',
    '1580',
    '1648',
    '1678',
    '1266',
    '1645',
    '502',
    '1717',
    '1723',
    '1244',
    '1370',
    '1898',
    '1755',
    '1708',
    '1983',
    '1901',
    '844',
    '1239',
    '1290',
    '1879',
    '1656',
    '1966',
    '1929',
    '1993',
    '1743',
    '1909',
    '1451',
    '2000',
    '1978',
    '1938',
    '1707',
    '1337',
    '1362',
    '1263'
];

$cnt = count($numbers);
$candidates = [];

for ($i = 0; $i < $cnt; $i++) {
    for ($j = 0; $j < $cnt; $j++) {
        $tmp = $numbers[$i] + $numbers[$j];

        if ($tmp == 2020) {
            $candidates[] = [$numbers[$i], $numbers[$j]];
        }
    }
}
var_dump($candidates); // 1704 * 316

$candidates = [];

for ($i = 0; $i < $cnt; $i++) {
    for ($j = 0; $j < $cnt; $j++) {
        for ($k = 0; $k < $cnt; $k++) {
            $tmp = $numbers[$i] + $numbers[$j]+ $numbers[$k];

            if ($tmp == 2020) {
                $candidates[] = [$numbers[$i], $numbers[$j], $numbers[$k]];
            }
        }

    }
}

var_dump($candidates); // 502 615 903