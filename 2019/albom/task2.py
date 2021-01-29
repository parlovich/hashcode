#! /usr/bin/python

import sys
import copy
import random
import multiprocessing


class Photo:
    def __init__(self, id, orientation, tags):
        self.id = id
        self.orientation = orientation
        self.tags = set(tags)


class Slide:
    def __init__(self, p1, p2=None):
        self.p1 = p1
        self.p2 = p2
        self.removed = False
        self.tags = self.p1.tags if not self.p2 else set().union(self.p1.tags, self.p2.tags)
        self.photos = [self.p1, self.p2] if self.p2 else [self.p1]


def create_index(slides):
    index = {}
    for s in slides:
        for t in s.tags:
            if t not in index:
                index[t] = set([s])
            else:
                index[t].add(s)
    return index


def remove_from_index(index, s):
    for t in s.tags:
        index.get(t).remove(s)


def calc_score(s1, s2):
    # in_s1 = len(s1.tags.difference(s2.tags))
    # in_s2 = len(s2.tags.difference(s1.tags))
    intersec = len(s1.tags.intersection(s2.tags))
    return min(len(s1.tags) - intersec, len(s2.tags) - intersec, intersec)


def find_next_index(s1, slides, index):
    s2 = None
    max_score = -1
    possible_max_score = int(len(s1.tags) / 2)
    candidates = set()
    for t in s1.tags:
        candidates = candidates.union(index.get(t))
    # candidates = filter(lambda x: not x.removed, candidates)
    # candidates = sorted(candidates, key=lambda x: len(x.tags))
    if candidates:
        candidates = list(candidates)
        s2 = candidates[0]
        max_score = calc_score(s1, s2)
        # idxs = range(1, len(candidates)) if len(candidates) < 1000 \
        #     else [random.randint(1, len(candidates) - 1) for i in range(1000)]
        for i in range(1, len(candidates)):
            if max_score >= possible_max_score:
                break
            if int(len(candidates[i].tags) / 2) <= max_score:
                continue
            tmp_score = calc_score(candidates[i], s1)
            if tmp_score > max_score:
                max_score = tmp_score
                s2 = candidates[i]

    if not s2:
        for s in slides:
            if not s.removed:
                s2 = s
                break
    if s2:
        remove_from_index(index, s2)

    return s2


def find_v(p, photos):
    idx = -1
    min_score = -1
    if photos:
        idx = 0
        min_score = len(p.tags.intersection(photos[idx].tags))
        for i in range(1, len(photos)):
            if min_score == 0:
                return idx
            l = len(p.tags.intersection(photos[i].tags))
            if l < min_score:
                idx = i
                min_score = l
    return idx


def read_input_data(file_name):
    photos = []
    with open(file_name, "r") as f:
        n = [int(c) for c in f.readline().split()][0]
        for i in range(0, n):
            p = f.readline().split()
            # we don't need vertical images with one tag
            if p[0] == 'V' and int(p[1]) < 2:
                continue
            photos.append(Photo(i, p[0], p[2:]))
    return photos


def print_out(slides, file_out):
    with open(file_out, "w") as f:
        f.write("%d\n" % len(slides))
        for s in slides:
            f.write("%s\n" % " ".join([str(p.id) for p in s.photos]))


def check_and_calc_score(slides):
    score = 0
    last = slides.pop()
    while slides:
        next = slides.pop()
        score += calc_score(last, next)
        last = next
    return score


def search_tree(p, photos):
    score = -1
    slides = []
    if not photos:
        return 0, [Slide(p)]
    for i in range(0, len(photos)):
        t_score, t_slides = search_tree(photos[i], photos[0:i] + photos[i + 1:])
        t_score += calc_score(p, photos[i])
        if t_score > score:
            score = t_score
            slides = t_slides

    return score, [Slide(p)] + slides


def main(in_file, out_file):
    photos = read_input_data(in_file)
    # index = create_index(photos)

    total = len(photos)
    p = photos.pop()
    result = search_tree(p, photos)
    # remove_from_index(index, p1)
    # while photos:

        # s2 = find_next_index(s1, slides, index)
        # if not s2:
        #     break
        # result.append(s2)
        # slides.remove(s2)
        # s2.removed = True
        # s1 = s2
        # print "\r{0}, total: {1}, complete: {2}".format(in_file, total, len(result)),

    # print_out(result, out_file)

    score = check_and_calc_score(result)
    print("\n%s Score: %d" % (in_file, score))
    return score


def worker(args):
    score = main(args[0], args[1])
    return score


if __name__ == "__main__":
    sys.setrecursionlimit(80000)
    files = {
        # "a_example.txt": "a_example2.out",
        "b_lovely_landscapes.txt": "b_lovely_landscapes2.out",
        # "c_memorable_moments.txt": "c_memorable_moments2.out",
        # "d_pet_pictures.txt": "d_pet_pictures2.out",
        # "e_shiny_selfies.txt": "e_shiny_selfies2.out"
    }
    # pool = multiprocessing.Pool(processes=4)
    # results = pool.map(worker, files.items())
    results = []
    for f_in, f_out in files.items():
        results.append(main(f_in, f_out))
    score = sum(results)
    print("Total: %d" % score)

    # if len(sys.argv) < 2:
    #     print "No file name"
    # else:
    #     main(sys.argv[1])
