
def solution_1(clients):
    # pizzas = clients[0][0]
    ingredients = {}
    for c in clients:
        for l in c[0]:
            ingredients[l] = ingredients[l] + 1 if l in ingredients else 1
        for d in c[1]:
            ingredients[d] = ingredients[d] - 1 if d in ingredients else -1
    pizza = []
    for k, v in ingredients.items():
        if v > 0:
            pizza.append(k)
    return pizza


def calc_score(pizza, clients):
    score = 0
    for c in clients:
        l_n = 0
        for l in c[0]:
            if l in pizza:
                l_n += 1
        if l_n < len(c[0]):
            continue
        d_n = 0
        for d in c[1]:
            if d in pizza:
                d_n += 1
        if d_n == 0:
            score += 1
    return score


def read_input(file_name):
    with open(file_name, "r") as f:
        n = int(f.readline())
        clients = []
        for i in range(n):
            likes = [s for s in f.readline().split()][1:]
            dislikes = [s for s in f.readline().split()][1:]
            clients.append((likes, dislikes))
    return clients


def write_output(file_out, pizza):
    with open(file_out, "w") as f:
        f.write("%d %s\n" % (len(pizza), " ".join(pizza)))


def process_one_file(in_file, out_file, solution):
    clients = read_input(in_file)
    pizza = solution(clients)
    score = calc_score(pizza, clients)
    print("%s Score: %d" % (in_file, score))
    write_output(out_file, pizza)
    return score


if __name__ == "__main__":
    total_score = 0
    files = [
        ("a_an_example.in.txt", "a_an_example.out", solution_1),
        ("b_basic.in.txt", "b_basic.out", solution_1),
        ("c_coarse.in.txt", "c_coarse.out", solution_1),
        ("d_difficult.in.txt", "d_difficult.out", solution_1),
        ("e_elaborate.in.txt", "e_elaborate.out", solution_1)
    ]
    for (f_in, f_out, f) in files:
        total_score += process_one_file(f_in, f_out, f)
    print(f"Total: {total_score}")
