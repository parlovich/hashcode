
def solve_d(data):
    D, book_scores, book_counts, libs = data

    books_index = {}
    for i in range(0, len(libs)):
        for b in libs[i][2]:
            a = books_index.get(b)
            if a:
                a.add(i)
            else:
                books_index[b] = set([i])

    # libs_graph = []
    # for i in range(0, len(libs)):
    #     a = set()
    #     for b in libs[i][2]:
    #         a.update(books_index[b])
    #     libs_graph.append(a - set([i]))


    # cluster_id = 0
    # clusters = [-1] * len(libs)
    # for i in range(0, len(libs)):
    #     if clusters[i] != -1:
    #         continue
    #     clusters[i] = cluster_id
    #     visit = libs_graph[i]
    #     while visit:
    #         j = visit.pop()
    #         clusters[j] = cluster_id
    #         visit.update(filter(lambda x: clusters[x] == -1, libs_graph[j]))
    #     cluster_id += 1

    added_books = set()
    added_libs = set()
    # idx = sorted(range(0, len(libs)), key=lambda x: len(libs[x][2]), reverse=True)[0]
    # _add_to_result(res, added_books, added_libs, idx, libs)
    # while True:
    #     score = 0
    #     lib_idx = -1
    #     for i in libs_graph[idx]:
    #         if i in added_libs:
    #             continue
    #         cur_score = _calc_score(added_books, libs[i])
    #         if cur_score > score:
    #             score = cur_score
    #             lib_idx = i
    #     if lib_idx == -1:
    #         break
    #     _add_to_result(res, added_books, added_libs, lib_idx, libs)
    #     idx = lib_idx

    # for i in range(0, len(book_scores)):
    #     if added_libs.intersection(books_index[i]):
    #         continue
    #     lib_idx = -1
    #     score = 1000000
    #     for j in books_index[i]:
    #         cur_score = len(libs[j][2].intersection(books_index[i]))
    #         if cur_score < score:
    #             score = cur_score
    #             lib_idx = j
    #     _add_to_result(res, added_books, added_libs, lib_idx, libs)
    #
    # if len(res) > len(libs) / 2:
    #     res = sorted(res, key=lambda l: libs[l[0]][3], reverse=True)

    added_libs = range(0, int(len(libs) / 2))
    added_books = set()
    book_counts = [0] * len(book_scores)
    for i in added_libs:
        added_books.update(libs[i][2])
        for j in libs[i][2]:
            book_counts[j] += 1

    for i in range(int(len(libs) / 2), len(libs)):
        add_books = libs[i][2] - added_books
        if not add_books:
            continue
        for j in range(0, len(added_libs)):
            remove_books = set()
            for b in libs[added_libs[j]][2]:
                if book_counts[b] == 1:
                    remove_books.add(b)
            # if (len(add_books) + len(remove_books.intersection(libs[i][2]))) > len(remove_books):
            if len(add_books) > len(remove_books):
                # Swap: replace added_libs[j] with i
                for b in libs[added_libs[j]][2]:
                    book_counts[b] -= 1
                for b in libs[i][2]:
                    book_counts[b] += 1
                for b in remove_books:
                    added_books.remove(b)
                added_books.update(libs[i][2])
                added_libs[j] = i
                break

    res = []
    for i in added_libs:
        res.append((i, list(libs[i][2])),)

    return res


def _add_to_result(res, added_books, added_libs, i, libs):
    res.append((i, list(libs[i][2])),)
    added_books.update(libs[i][2])
    added_libs.add(i)


def _calc_score(added_books, lib):
    return len(lib[2] - added_books)

