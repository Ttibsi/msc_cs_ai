import queue
import random
import threading

def producer(q):
    i = 0
    while i < 10:
        q.put(random.randint(0, 10))
        i += 1

def consumer(q):
    i = 0
    while i < 10:
        i += 1
        if q.qsize():
            print(q.get(block=True))
        else:
            print("No value found")


def bounding_box() -> int:
    q = queue.Queue()
    t1 = threading.Thread(target=producer, args=(q,))
    t2 = threading.Thread(target=consumer, args=(q,))
    t3 = threading.Thread(target=producer, args=(q,))
    t4 = threading.Thread(target=consumer, args=(q,))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    return 0

###

def sieve(high: int) -> int:
    values = [True] * (high)
    values[0] = False
    values[1] = False

    def strikethrough(values, step):
        for idx in range(high):
            if idx == 2 or idx == 3:
                continue
            if not idx % step:
                values[idx] = False

    twos = threading.Thread(target=strikethrough, args=(values, 2))
    threes = threading.Thread(target=strikethrough, args=(values, 3))
    fives = threading.Thread(target=strikethrough, args=(values, 5))

    twos.start()
    threes.start()
    fives.start()
    twos.join()
    threes.join()
    fives.join()

    for idx, v in enumerate(values):
        if v:
            print(idx)

    return 0


def main() -> int:
    # return bounding_box()
    return sieve(30)


if __name__ == "__main__":
    raise SystemExit(main())
