#! /usr/bin/python

from functools import reduce
import math
import datetime
import random
random.seed(datetime.datetime.now())


def get_delivery_score(delivery, pizzas):
    if not delivery:
        return 0
    ingredients_len = len(set(reduce(lambda p1, p2: p1 + p2, [pizzas[i] for i in delivery])))
    return ingredients_len * ingredients_len


def optimize(deliveries, pizzas):
    def get_next_exchange(deliveries):
        d1 = random.randint(0, len(deliveries) - 1)
        p1 = random.randint(0, len(deliveries[d1]) - 1)
        d2 = random.randint(0, len(deliveries) - 1)
        while d2 == d1:
            d2 = random.randint(0, len(deliveries) - 1)
        p2 = random.randint(0, len(deliveries[d2]) - 1)
        return (d1, p1), (d2, p2)

    def get_exchange_delta(exchange, deliveries, pizzas):
        d1, p1 = exchange[0]
        d2, p2 = exchange[1]
        orig_score1 = get_delivery_score(deliveries[d1], pizzas)
        orig_score2 = get_delivery_score(deliveries[d2], pizzas)
        new_d1 = deliveries[d1].copy()
        new_d2 = deliveries[d2].copy()
        tmp = new_d1[p1]
        new_d1[p1] = new_d2[p2]
        new_d2[p2] = tmp
        new_score1 = get_delivery_score(new_d1, pizzas)
        new_score2 = get_delivery_score(new_d2, pizzas)
        delta = (orig_score1 + orig_score2) - (new_score1 + new_score2)
        return delta

    def swap(deliveries, exchange):
        d1, p1 = exchange[0]
        d2, p2 = exchange[1]
        tmp = deliveries[d1][p1]
        deliveries[d1][p1] = deliveries[d2][p2]
        deliveries[d2][p2] = tmp
        return deliveries

    def get_swap_probability(delta, i):
        return math.exp(float(-delta) / i)

    max_score = sum(map(lambda d: get_delivery_score(d, pizzas), deliveries))
    score = max_score
    print(f"Init score: {max_score}")
    for i in range(1, 1000000):
        exchange = get_next_exchange(deliveries)
        delta = get_exchange_delta(exchange, deliveries, pizzas)
        if delta <= 0:
            swap(deliveries, exchange)
            score -= delta
        # else:
        #     if random.random() < get_swap_probability(delta, i):
        #         swap(deliveries, exchange)
        #         score -= delta
        if max_score < score:
            max_score = score
    print(f"Max score {max_score}")
    return deliveries


def solve_problem(pizzas, T2, T3, T4):
    deliveries = []
    t2, t3, t4 = 0, 0, 0
    i = 0
    indexes = list(range(0, len(pizzas)))
    indexes = sorted(indexes, key=lambda i: len(pizzas[i]), reverse=True)
    # random.shuffle(indexes)
    while i < len(indexes):
        if t2 < T2 and i < len(pizzas) - 1:
            deliveries.append(indexes[i:i+2])
            i += 2
            t2 += 1
            continue
        if t3 < T3 and i < len(pizzas) - 2:
            deliveries.append(indexes[i:i+3])
            i += 3
            t3 += 1
            continue
        if t4 < T4 and i < len(pizzas) - 3:
            deliveries.append(indexes[i:i+4])
            i += 4
            t4 += 1
            continue
        i += 1
    return optimize(deliveries, pizzas)


def solve_problem2(pizzas, T2, T3, T4):

    class DeliveriesPool:
        def __init__(self, team_size, team_count):
            self.team_size = team_size
            self.team_count = team_count
            self.is_full = False
            self.deliveries = [[] for i in range(team_count)]

        def add_pizza(self, p_idx, dry_run=False):
            if self.is_full:
                return False, 0
            max_possible_delta = len(pizzas[p_idx]) * len(pizzas[p_idx])
            idx = -1
            max_delta = -1
            for i in range(len(self.deliveries)):
                d = self.deliveries[i]
                if len(d) < self.team_size:
                    new_d = d.copy()
                    new_d.append(p_idx)
                    delta = get_delivery_score(new_d, pizzas) - get_delivery_score(d, pizzas)
                    if delta > max_delta:
                        max_delta = delta
                        idx = i
                        if max_delta == max_possible_delta:
                            break
            if idx == -1:
                self.is_full = True
                return False, 0
            if not dry_run:
                self.deliveries[idx].append(p_idx)
            return True, max_delta

        def get_deliveries(self):
            res = []
            p_to_merge = []
            for d in self.deliveries:
                if len(d) == self.team_size:
                    res.append(d)
                else:
                    p_to_merge += d
            i = 0
            while i <= len(p_to_merge) - self.team_size:
                res.append(p_to_merge[i:i + self.team_size])
                i += self.team_size
            return res

    d2 = DeliveriesPool(2, T2)
    d3 = DeliveriesPool(3, T3)
    d4 = DeliveriesPool(4, T4)
    pools = [d2, d3, d4]

    indexes = list(range(0, len(pizzas)))
    indexes = sorted(indexes, key=lambda i: len(pizzas[i]), reverse=True)

    for i in indexes:
        idx = -1
        max_score = 0
        for j in range(len(pools)):
            added, score = pools[j].add_pizza(indexes[i], dry_run=True)
            if added:
                if idx == -1:
                    idx = j
                if score > max_score:
                    max_score = score
                    idx = j
        if idx == -1:
            break
        pools[idx].add_pizza(indexes[i])

    deliveries = [d for pool in pools for d in pool.get_deliveries()]
    return optimize(deliveries, pizzas) if len(deliveries) > 1 else deliveries


def read_input(file_name):
    with open(file_name, "r") as f:
        (M, T2, T3, T4) = [int(c) for c in f.readline().split()]
        pizzas = []
        for i in range(0, M):
            pizzas.append([s for s in f.readline().split()][1:])
        return pizzas, T2, T3, T4


def write_output(deliveries, file_out):
    with open(file_out, "w") as f:
        f.write("%d\n" % len(deliveries))
        for d in deliveries:
            f.write(str(len(d)) + " " + " ".join([str(i) for i in d]) + "\n")


def check_and_calc_score(deliveries, pizzas, T2, T3, T4):
    if len(deliveries) > T2 + T3 + T4:
        raise RuntimeError("Too much deliveries")
    t = [T2, T3, T4]
    p = set()
    score = 0
    for d in deliveries:
        if t[len(d) - 2] <= 0:
            raise RuntimeError(f"For {len(d)} size team there are more deliveries than allowed")
        t[len(d) - 2] -= 1
        ingredients = set()
        for i in d:
            if i in p:
                raise RuntimeError(f"Duplication of pizza {i}")
            p.add(i)
            ingredients = ingredients.union(pizzas[i])
        score += len(ingredients) * len(ingredients)
    return score


def main(in_file, out_file):
    (pizzas, T2, T3, T4) = read_input(in_file)
    deliveries = solve_problem(pizzas, T2, T3, T4)
    score = check_and_calc_score(deliveries, pizzas, T2, T3, T4)
    print("%s Score: %d" % (in_file, score))
    write_output(deliveries, out_file)
    return score


if __name__ == "__main__":
    score = 0
    files = {
        # "a_example": "a.out",
        "b_little_bit_of_everything.in": "b.out",
        "c_many_ingredients.in": "c.out",
        "d_many_pizzas.in": "d.out",
        "e_many_teams.in": "e.out"
    }
    for f_in, f_out in files.items():
        score += main(f_in, f_out)
    print(f"Total: {score}")
