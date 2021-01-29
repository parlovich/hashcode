#! /usr/bin/python

import sys
import copy


def solve_problem(m, types):
    pizzas = [types[0]]
    max_sum = types[0]

    s = {}
    for i in range(len(types)):
        s[types[i]] = i

    t = types
    for i in range(len(t)):
        p = [t[i]]
        m_s = t[i]
        for j in range(len(t)):
            if i == j:
                continue
            if (m - m_s) in s.keys() and (m - m_s) not in p:
                p += [m - m_s]
                break
            if (m_s + t[j]) < m:
                p += [t[j]]
                m_s += t[j]
            else:
                break

        if m >= m_s > max_sum:
            pizzas = p
            max_sum = m_s
        if max_sum == m:
            break

    pizzas = [s[n] for n in pizzas]
    return pizzas


def calc_score(pizzas, types):
    score = 0
    for p in pizzas:
        score += types[p]
    return score


def read_input(file_name):
    with open(file_name, "r") as f:
        (m, n) = [int(c) for c in f.readline().split()]
        types = [int(c) for c in f.readline().split()]
        return m, types


def write_output(file_out, pizzas):
    with open(file_out, "w") as f:
        f.write("%d\n" % len(pizzas))
        if pizzas:
            f.write(str(pizzas[0]))
            for i in range(1, len(pizzas)):
                f.write(" ")
                f.write(str(pizzas[i]))
            f.write("\n")


def process_one_file(in_file, out_file):
    (m, types) = read_input(in_file)
    pizzas = solve_problem(m, types)
    score = calc_score(pizzas, types)
    if score > m:
        raise RuntimeError("Score %d is bigger than max %d".format(score, m))
    print("%s Score: %d" % (in_file, score))
    write_output(out_file, pizzas)
    return score


if __name__ == "__main__":
    total_score = 0
    files = [
        ("a_example.in", "a_example.out"),
        ("b_small.in", "b_small.out"),
        ("c_medium.in", "c_medium.out"),
        ("d_quite_big.in", "d_quite_big.out"),
        ("e_also_big.in", "e_also_big.out")
    ]
    for (f_in, f_out) in files:
        total_score += process_one_file(f_in, f_out)
    print "Total: %d" % total_score
