#! /usr/bin/python

from functools import reduce
import math
import statistics
import datetime


class Street:
    def __init__(self, begin, end, name, length):
        self.begin = begin
        self.end = end
        self.name = name
        self.length = length


class Schedule:
    def __init__(self, intersection, streets):
        self.intersection = intersection
        self.streets = streets


# def optimize(deliveries, pizzas):
#     def get_next_exchange(deliveries):
#         d1 = random.randint(0, len(deliveries) - 1)
#         p1 = random.randint(0, len(deliveries[d1]) - 1)
#         d2 = random.randint(0, len(deliveries) - 1)
#         while d2 == d1:
#             d2 = random.randint(0, len(deliveries) - 1)
#         p2 = random.randint(0, len(deliveries[d2]) - 1)
#         return (d1, p1), (d2, p2)
#
#     def get_exchange_delta(exchange, deliveries, pizzas):
#         d1, p1 = exchange[0]
#         d2, p2 = exchange[1]
#         orig_score1 = get_delivery_score(deliveries[d1], pizzas)
#         orig_score2 = get_delivery_score(deliveries[d2], pizzas)
#         new_d1 = deliveries[d1].copy()
#         new_d2 = deliveries[d2].copy()
#         tmp = new_d1[p1]
#         new_d1[p1] = new_d2[p2]
#         new_d2[p2] = tmp
#         new_score1 = get_delivery_score(new_d1, pizzas)
#         new_score2 = get_delivery_score(new_d2, pizzas)
#         delta = (orig_score1 + orig_score2) - (new_score1 + new_score2)
#         return delta
#
#     def swap(deliveries, exchange):
#         d1, p1 = exchange[0]
#         d2, p2 = exchange[1]
#         tmp = deliveries[d1][p1]
#         deliveries[d1][p1] = deliveries[d2][p2]
#         deliveries[d2][p2] = tmp
#         return deliveries
#
#     def get_swap_probability(delta, i):
#         return math.exp(float(-delta) / i)
#
#     max_score = sum(map(lambda d: get_delivery_score(d, pizzas), deliveries))
#     score = max_score
#     print(f"Init score: {max_score}")
#     for i in range(1, 1000000):
#         exchange = get_next_exchange(deliveries)
#         delta = get_exchange_delta(exchange, deliveries, pizzas)
#         if delta <= 0:
#             swap(deliveries, exchange)
#             score -= delta
#         # else:
#         #     if random.random() < get_swap_probability(delta, i):
#         #         swap(deliveries, exchange)
#         #         score -= delta
#         if max_score < score:
#             max_score = score
#     print(f"Max score {max_score}")
#     return deliveries


def solve_problem(D, I, streets, paths, F):
    schedules = []
    intr = {}
    # s_l = {}
    # for s in streets:
    #     s_l[s.name] = s.length
    s_index = {}
    for s in streets:
        s_index[s.name] = s
    p_index = {}
    for p in paths:
        # p_l = 0
        # for s in p:
        #     p_l += s_l[s]
        # if p_l > D:
        #     continue
        for s in p:
            if s not in p_index:
                p_index[s] = 0
            p_index[s] += 1

    for s in streets:
        if s.end not in intr:
            intr[s.end] = set()
        if s.name in p_index:
            intr[s.end].add(s.name)

    for i, streets in intr.items():
        if streets:
            o = sorted(streets, key=lambda x: p_index[x], reverse=True)
            med = statistics.median([p_index[s] for s in o])
            arr = []
            for s in o:
                t = 1
                if p_index[s] - med > 3:
                    t = 2
                if p_index[s] - med > 5:
                    t = 3
                arr.append((s, t))

            schedules.append(Schedule(i, arr))
    return schedules


def read_input(file_name):
    with open(file_name, "r") as f:
        (D, I, S, V, F) = [int(c) for c in f.readline().split()]
        streets = []    # i1 i2 name length
        for i in range(S):
            (begin, end, name, length) = [s for s in f.readline().split()]
            streets.append(Street(int(begin), int(end), name, int(length)))
        paths = []  # n-streets [street names]
        for i in range(V):
            paths.append([s for s in f.readline().split()][1:])
        return D, I, streets, paths, F


def write_output(schedules, file_out):
    with open(file_out, "w") as f:
        f.write("%d\n" % len(schedules))
        for sch in schedules:
            f.write("%d\n" % sch.intersection)
            f.write("%d\n" % len(sch.streets))
            for s in sch.streets:
                f.write("%s %d\n" % s)


# def check_and_calc_score(deliveries, pizzas, T2, T3, T4):
#     if len(deliveries) > T2 + T3 + T4:
#         raise RuntimeError("Too much deliveries")
#     t = [T2, T3, T4]
#     p = set()
#     score = 0
#     for d in deliveries:
#         if t[len(d) - 2] <= 0:
#             raise RuntimeError(f"For {len(d)} size team there are more deliveries than allowed")
#         t[len(d) - 2] -= 1
#         ingredients = set()
#         for i in d:
#             if i in p:
#                 raise RuntimeError(f"Duplication of pizza {i}")
#             p.add(i)
#             ingredients = ingredients.union(pizzas[i])
#         score += len(ingredients) * len(ingredients)
#     return score


def main(in_file, out_file):
    (D, I, streets, paths, F) = read_input(in_file)
    schedules = solve_problem(D, I, streets, paths, F)
    # score = check_and_calc_score(deliveries, pizzas, T2, T3, T4)
    # print("%s Score: %d" % (in_file, score))
    write_output(schedules, out_file)
    return score


if __name__ == "__main__":
    score = 0
    files = {
        "a.txt": "a.out",
            "b.txt": "b.out",
            "c.txt": "c.out",
            "d.txt": "d.out",
            "e.txt": "e.out",
            "f.txt": "f.out"
    }
    for f_in, f_out in files.items():
        score += main(f_in, f_out)
    print(f"Total: {score}")
