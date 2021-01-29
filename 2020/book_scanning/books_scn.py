import sys
import random


def solve_problem_d(data):
    D, book_scores, libs = data
    max_score = 0
    max_r = {
        "score": 0,
        "libs": []
             }

    def _get_result_score(r):
        res = []
        for i in r:
            res.append((i, (list(libs[i][2]))),)
        score = calc_score(data, res)
        if score > max_r["score"]:
            max_r["score"] = score
            max_r["libs"] = r[:]

        return res, score

    def _calc_added_books(r):
        b = set()
        b_c = [0] * len(book_scores)
        for i in r:
            b.update(libs[i][2])
            for j in libs[i][2]:
                b_c[j] += 1
        return b, b_c

    def _update_added_books(b, b_c, r_i, a_i):
        for i in libs[r_i][2]:
            b_c[i] -= 1
            if b_c[i] == 0:
                b.remove(i)
        b.update(libs[a_i][2])
        for i in libs[a_i][2]:
            b_c[i] += 1
        return b, b_c

    def _get_removed_books(b_c, lib_id):
        bks = set()
        for b in libs[lib_id][2]:
            if b_c[b] == 1:
                bks.add(b)
        return bks

    # s  = sorted(range(0, len(libs)), key=lambda x: len(libs[x][2]), reverse=True)
    # r = s[:int(len(libs) / 2)]
    # nr = s[int(len(libs) / 2):]
    added_books = set()
    r = []
    nr = []
    for i in range(0, int(len(libs) / 2)):
        i1, i2 = ((2 * i, 2 * i + 1) if len(set(libs[2 * i][2]) - added_books) > len(set(libs[2 * i + 1][2]) - added_books)
                  else (2 * i + 1, 2 * i))
        # i1, i2 = ((2 * i, 2 * i + 1) if len(libs[2 * i][2]) > len(libs[2 * i + 1][2])
        #           else (2 * i + 1, 2 * i))
        r.append(i1)
        nr.append(i2)
        added_books.update(libs[i1][2])

    added_books, book_counts = _calc_added_books(r)
    res, score = _get_result_score(r)
    print(score)

    for n in range(0, 500):
        for i in range(0, len(r)):
            removed = _get_removed_books(book_counts, r[i])
            add_c = len(libs[nr[i]][2] - added_books)
            rem_c = len(removed - libs[nr[i]][2])
            if add_c > rem_c or (add_c == rem_c and len(libs[r[i]][2]) > len(libs[nr[i]][2])):
                t = nr[i]
                nr[i] = r[i]
                r[i] = t
                added_books, book_counts = _update_added_books(added_books, book_counts, nr[i], r[i])
                res, score = _get_result_score(r)
                print(score)

    for n in range(0, 100):
        random.shuffle(nr)
        for i in range(0, len(r)):
            removed = _get_removed_books(book_counts, r[i])
            add_c = len(libs[nr[i]][2] - added_books)
            rem_c = len(removed - libs[nr[i]][2])
            if add_c > rem_c or (add_c == rem_c and len(libs[r[i]][2]) > len(libs[nr[i]][2])):
            # if len(libs[nr[i]][2] - added_books) >= len(removed - libs[nr[i]][2]):
                t = nr[i]
                nr[i] = r[i]
                r[i] = t
                added_books, book_counts = _update_added_books(added_books, book_counts, nr[i], r[i])
                res, score = _get_result_score(r)
                print(score)

    # for i in range(0, len(r)):
    #     k = -1
    #     removed = _get_removed_books(book_counts, r[i])
    #     for j in range(0, len(nr)):
    #         if len(libs[nr[j]][2] - added_books) > len(removed - libs[nr[j]][2]):
    #             k = j
    #             break
    #     if k > -1:
    #         t = nr[k]
    #         nr[k] = r[i]
    #         r[i] = t
    #         added_books, book_counts = _update_added_books(added_books, book_counts, nr[k], r[i])
    #         res, score = _get_result_score(r)
    #         print(score)

    # for i in range(0, len(nr)):
    #     if not libs[nr[i]][2] - added_books:
    #         continue
    #     max_delta = 0
    #     idx = -1
    #     for j in range(0, len(r)):
    #         t = r[j]
    #         r[j] = i
    #         rr, s = _get_result_score(r)
    #         if s - score > max_delta:
    #             max_delta = s - score
    #             idx = j
    #         r[j] = t
    #     if idx > -1:
    #         r[idx] = i
    #         res, score = _get_result_score(r)
    #         print(score)
    return _get_result_score(sorted(max_r["libs"], key=lambda x: len(libs[x][2]), reverse=True))[0]


def solve_problem(data):
    D, book_scores, libs = data
    result = []
    add_next_lib_to_result(data, D, set(), set(), result)
    return result


def get_books_order(book_scores, scanned_books, lib):
    days_to_signup, book_per_day, book_ids, total_score = lib
    return sorted(book_ids - scanned_books, key=lambda i: book_scores[i], reverse=True)


def calc_lib_score(days_left, book_scores, scanned_books, lib):
    days_to_signup, book_per_day, book_ids, total_score = lib
    # score = total_score
    score = 0

    if days_to_signup >= days_left:
        return 0, None

    # for i in book_ids & scanned_books:
    #     score -= book_scores[i]
    sorted_books = sorted(book_ids - scanned_books, key=lambda i: book_scores[i], reverse=True)
    if len(sorted_books) > (days_left - days_to_signup) * book_per_day:
        sorted_books = sorted_books[:(days_left - days_to_signup) * book_per_day]

    for i in sorted_books:
        score += book_scores[i]

    score /= days_to_signup
    if sorted_books:
        score += (len(book_scores) - len(sorted_books) - len(scanned_books)) / 10

    return score, sorted_books


def add_next_lib_to_result(data, days_left, scanned_books, added_libs, result):
    D, book_scores, libs = data
    if days_left < 1:
        return
    score = 0
    lib_id = -1
    books = None
    idxs = set(range(0, len(libs))) - added_libs
    for i in random.sample(idxs, int(len(idxs)/5)) if len(idxs) > 100 else idxs:
        cur_score, cur_books = calc_lib_score(days_left, book_scores, scanned_books, libs[i])
        if cur_score > score:
            score = cur_score if cur_score > score else score
            books = cur_books
            lib_id = i
    if lib_id >= 0:
        # books = get_books_order(book_scores, scanned_books, libs[lib_id])
        result.append((lib_id, books),)
        added_libs.add(lib_id)
        scanned_books.update(books)
        add_next_lib_to_result(data, days_left - libs[lib_id][0], scanned_books, added_libs, result)


def calc_score(data, results):
    """
    Calc score of the solution
    :param data: initial input data
    :param results: array of libs: (lib_id, books_ids[])

    """
    D, book_scores, libs = data

    scanned_books = set()
    signup_days = 0
    libs_in_scan = []
    lib_next_idx = 0
    for d in range(0, D):
        if signup_days == 0 and lib_next_idx < len(results):
            # If no signup in process then add another one more library for scanning
            r_lib = results[lib_next_idx]
            lib_id = r_lib[0]
            lib = libs[lib_id]
            signup_days = lib[0]
            libs_in_scan.append((lib_next_idx, lib, -signup_days),)
            lib_next_idx += 1
        signup_days -= 1
        # scan books for one day
        new_libs_in_scan = []
        for l in libs_in_scan:
            lib_idx, lib, scan_day = l
            books = results[lib_idx][1]
            books_per_day = lib[1]
            if scan_day >= 0:
                start_idx = scan_day * books_per_day
                if start_idx < len(books):
                    for i in range(start_idx, start_idx + books_per_day if start_idx + books_per_day < len(books) else len(books)):
                        scanned_books.add(books[i])
            scan_day += 1
            if scan_day * books_per_day < len(books):
                new_libs_in_scan.append((lib_idx, lib, scan_day),)
        libs_in_scan = new_libs_in_scan

    if libs_in_scan:
        print ("WARN: more libs/books in the result than it can be scanned")

    score = 0
    for b in scanned_books:
        score += book_scores[b]
    return score


def write_output(out_file, results):
    with open(out_file, "w") as f:
        f.write("%d\n" % len(results))
        for lib in results:
            f.write("%d %d\n" % (lib[0], len(lib[1])))
            f.write("%s\n" % " ".join([str(i) for i in lib[1]]))


def read_input_data(file_name):
    """
    Reads input file
    :return: (D, book_scores, libs)
    D:
        number of days
    book_scores:
        array of book scores, score of book i = book_scores[i]
    libs: array
        (days_to_signup, book_per_day, book_ids)
    """
    with open(file_name, "r") as f:
        B, L, D = [int(c) for c in f.readline().split()]
        book_scores = [int(c) for c in f.readline().split()]
        libs = []
        for i in range(0, L):
            n, signup, b_per_day = [int(c) for c in f.readline().split()]
            books = set([int(c) for c in f.readline().split()])
            t_score = 0
            for b in books:
                t_score += book_scores[b]
            libs.append((signup, b_per_day, books, t_score))
        return D, book_scores, libs


if __name__ == "__main__":
    limit = sys.getrecursionlimit()
    sys.setrecursionlimit(30000)

    files = [
        # ("a_example.txt", "a_example.out"),
        # ("b_read_on.txt", "b_read_on.out"),
        # ("e_so_many_books.txt", "e_so_many_books.out"),
        # ("f_libraries_of_the_world.txt", "f_libraries_of_the_world.out"),
        # ("c_incunabula.txt", "c_incunabula.out"),
        ("d_tough_choices.txt", "d_tough_choices.out"),
    ]
    total_score = 0
    for f_in, f_out in files:
        print("Read %s..." % f_in)
        data = read_input_data(f_in)
        if f_in.startswith("d"):
            results = solve_problem_d(data)
        else:
            results = solve_problem(data)
        score = calc_score(data, results)
        print("Score: %s" % score)
        write_output(f_out, results)
        total_score += score
    print("Total: %d" % total_score)
