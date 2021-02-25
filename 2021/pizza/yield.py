
VALUES = ["a", "b", "c"]


def get_values():
    print("enter get_values")
    n = 0
    for v in range(2):
        n += 1
        print(f"yield {n}")
        yield n
    print("exit get_value")


if __name__ == "__main__":
    print("get generator")
    vals = get_values()
    for v in vals:
        print(f"value: {v}")
    for v in vals:
        print(f"value: {v}")
    print("exit")
