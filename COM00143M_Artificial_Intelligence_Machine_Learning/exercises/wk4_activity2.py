import forward_chaining

"""
Horn clauses

A = [1, 1] is Safe
B = [1, 2] is Safe
C = [2, 1] is Safe
D = [2, 2] is Safe
E = [3, 1] is Safe
F = [3, 2] is Safe

G = [1, 1] is Stench
H = [1, 2] is Stench
I = [2, 1] is Stench
J = [2, 2] is Stench
K = [3, 1] is Stench
L = [3, 2] is Stench

M = [1, 1] is Wumpus
N = [1, 2] is Wumpus
O = [2, 1] is Wumpus
P = [2, 2] is Wumpus
Q = [3, 1] is Wumpus
R = [3, 2] is Wumpus
"""

def main():
    fc = forward_chaining.ForwardChaining()

    # 1,1 is stench 
    # 2, 1 is safe
    # 2, 2 is stench
    fc.add_clause([ord("G")])
    fc.add_clause([ord("C")])
    fc.add_clause([ord("J")])

    # if 1,1 is stench and 2,2 is stench, then 1,2 is wumpus
    # G ^ J = N
    # -G v -J v N
    fc.add_clause([-ord("G"), -ord("J"), -ord("N")])

    ret = fc.forward_chaining(ord("R") + 1)
    print(f"Result = {ret}")


if __name__ == '__main__':
    raise SystemExit(main())
