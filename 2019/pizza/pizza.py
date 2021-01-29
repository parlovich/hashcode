#! /usr/bin/python

import sys
import copy

M_INT = 1
T_INT = 2


class SliceType:
    BIG = "big"
    SMALL = "small"
    GOOD = "good"


class PizzaSlicer:

    def __init__(self, pizza, L, H):
        self.pizza = copy.deepcopy(pizza)
        self.R = len(pizza)
        self.C = len(pizza[0])
        self.L = L
        self.H = H

    @staticmethod
    def _slice_size(slice):
        R, C = slice[0], slice[1]
        return (abs(R[0] - R[1]) + 1) * (abs(C[0] - C[1]) + 1)

    def _check_slice_type(self, slice):
        if self._slice_size(slice) > self.H:
            return SliceType.BIG
        T, M = 0, 0
        R, C = slice[0], slice[1]
        for i in range(R[0], R[1] + 1):
            for j in range(C[0], C[1] + 1):
                if self.pizza[i][j] == M_INT:
                    M += 1
                elif self.pizza[i][j] == T_INT:
                    T += 1
                else:
                    return SliceType.BIG
                if T >= self.L and M >= self.L:
                    return SliceType.GOOD
        return SliceType.GOOD if T >= self.L and M >= self.L \
            else SliceType.SMALL

    def _cut_slice(self, cur_slice):
        state = self._check_slice_type(cur_slice)
        if state == SliceType.BIG:
            return None
        if state == SliceType.GOOD:
            return cur_slice
        # Try to grow slice
        R, C = cur_slice[0], cur_slice[1]
        cur_slice = None
        cur_size = 0
        # right
        if C[1] < self.C - 1:
            next_slice = self._cut_slice((R, (C[0], C[1] + 1)))
            if next_slice:
                next_size = self._slice_size(next_slice)
                if not cur_slice or next_size > cur_size:
                    cur_slice = next_slice
                    cur_size = next_size
        # down
        if R[1] < self.R - 1:
            next_slice = self._cut_slice(((R[0], R[1] + 1), C))
            if next_slice:
                next_size = self._slice_size(next_slice)
                if not cur_slice or next_size > cur_size:
                    cur_slice = next_slice
                    cur_size = next_size
        # left
        # if C[0] > 0:
        #     next_slice = self._cut_slice((R, (C[0] - 1, C[1])))
        #     if next_slice:
        #         next_size = self._slice_size(next_slice)
        #         if not cur_slice or next_size > cur_size:
        #             cur_slice = next_slice
        #             cur_size = next_size
        # # up
        # if R[0] > 0:
        #     next_slice = self._cut_slice(((R[0] - 1, R[1]), C))
        #     if next_slice:
        #         next_size = self._slice_size(next_slice)
        #         if not cur_slice or next_size > cur_size:
        #             cur_slice = next_slice
        #             cur_size = next_size

        return cur_slice

    def _extend_slice(self, orig_slice, new_slice=None):
        if new_slice:
            # check if candidate slice is validity
            if self._slice_size(new_slice) > self.H:
                return None
            for i in range(new_slice[0][0], new_slice[0][1] + 1):
                for j in range(new_slice[1][0], new_slice[1][1] + 1):
                    if (i < orig_slice[0][0] or i > orig_slice[0][1] or
                            j < orig_slice[1][0] or j > orig_slice[1][1]) and \
                            self.pizza[i][j] == 0:
                        return None
            cur_slice = new_slice
        else:
            cur_slice = orig_slice
        cur_size = self._slice_size(cur_slice)

        # go down
        if cur_slice[0][1] < self.R - 1:
            next_slice = self._extend_slice(orig_slice, ((cur_slice[0][0], cur_slice[0][1] + 1), cur_slice[1]))
            if next_slice:
                next_size = self._slice_size(next_slice)
                if next_size > cur_size:
                    cur_slice = next_slice
                    cur_size = next_size
        # go right
        if cur_slice[1][1] < self.C - 1:
            next_slice = self._extend_slice(orig_slice, (cur_slice[0], (cur_slice[1][0], cur_slice[1][1] + 1)))
            if next_slice:
                next_size = self._slice_size(next_slice)
                if next_size > cur_size:
                    cur_slice = next_slice
                    cur_size = next_size
        # go up
        if cur_slice[0][0] > 0:
            next_slice = self._extend_slice(orig_slice, ((cur_slice[0][0] - 1, cur_slice[0][1]), cur_slice[1]))
            if next_slice:
                next_size = self._slice_size(next_slice)
                if next_size > cur_size:
                    cur_slice = next_slice
                    cur_size = next_size
        # go left
        if cur_slice[1][0] > 0:
            next_slice = self._extend_slice(orig_slice, (cur_slice[0], (cur_slice[1][0] - 1, cur_slice[1][1])))
            if next_slice:
                next_size = self._slice_size(next_slice)
                if next_size > cur_size:
                    cur_slice = next_slice
                    cur_size = next_size

        self._fill_in_slice_area(cur_slice)
        return cur_slice

    def _fill_in_slice_area(self, slice):
        R, C = slice[0], slice[1]
        for i in range(R[0], R[1] + 1):
            for j in range(C[0], C[1] + 1):
                self.pizza[i][j] = 0

    def cut(self):
        slices = []
        # Cut Small slices
        for r in range(0, self.R):
            for c in range(0, self.C):
                if self.pizza[r][c] != 0:
                    slice = self._cut_slice(((r, r), (c, c)))
                    if slice:
                        slices.append(slice)
                        self._fill_in_slice_area(slice)
        # extend slices
        if slices:
            for i in range(0, len(slices)):
                slices[i] = self._extend_slice(slices[i])
                self._fill_in_slice_area(slices[i])
        return slices


def read_input_data(file_name):
    with open(file_name, "r") as f:
        (R, C, L, H) = [int(c) for c in f.readline().split()]
        pizza = []
        for i in range(0, R):
            pizza.append([T_INT if c == 'T' else M_INT for c in f.readline().strip()])
        return pizza, L, H


def print_slices(slices, file_out):
    with open(file_out, "w") as f:
        f.write("%d\n" % len(slices))
        for s in slices:
            f.write("%d %d %d %d\n" % (s[0][0], s[1][0], s[0][1], s[1][1]))


def check_slices_calc_score(pizza, slices, L, H):
    tmp_pizza = copy.deepcopy(pizza)
    score = 0
    for slice in slices:
        T, M, size = 0, 0, 0
        for i in range(slice[0][0], slice[0][1] + 1):
            for j in range(slice[1][0], slice[1][1] + 1):
                score += 1
                size += 1
                val = tmp_pizza[i][j]
                if val == 0:
                    raise RuntimeError("slices overlap")
                elif val == T_INT:
                    T += 1
                elif val == M_INT:
                    M += 1
                tmp_pizza[i][j] = 0
        if size > H:
            raise RuntimeError("slice is to big: slice %s, size: %d" % (slice, size))
        if T < L:
            raise RuntimeError("Too few tomatoes: slice %s" % slice)
        if M < L:
            raise RuntimeError("Too few mushrooms: slice %s" % slice)

    return score


def main(in_file, out_file):
    (pizza, L, H) = read_input_data(in_file)
    slicer = PizzaSlicer(pizza, L, H)
    slices = slicer.cut()
    score = check_slices_calc_score(pizza, slices, L, H)
    print "%s Score: %d" % (in_file, score)
    print_slices(slices, out_file)
    return score


if __name__ == "__main__":
    score = 0
    files = {
        "a_example.in": "a_example.out",
        "b_small.in": "b_small.out",
        "c_medium.in": "c_medium.out",
        "d_big.in": "d_big.out"
    }
    for f_in, f_out in files.items():
        score += main(f_in, f_out)
    print "Total: %d" % score

    # if len(sys.argv) < 2:
    #     print "No file name"
    # else:
    #     main(sys.argv[1])
