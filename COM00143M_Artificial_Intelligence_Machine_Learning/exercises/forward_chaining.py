import sys

class ForwardChaining:
    def __init__(self):
        self.clauses = []

    def forward_chaining(self, n):
        # model[i] = truth value of variable i
        model = [False] * (n + 1)

        # Sanity check clauses
        for clause in self.clauses:
            pos_lits = 0
            for lit in clause:
                assert -n <= lit <= n, "Found reference to variable larger than n."
                if lit > 0:
                    pos_lits += 1
            assert pos_lits <= 1, "At most one positive literal is allowed in each clause."

        # Iterate until fixpoint
        fixpoint = False

        while not fixpoint:
            fixpoint = True

            for clause in self.clauses:
                # Check all negative literals
                all_true = True
                for lit in clause:
                    if lit < 0 and not model[-lit]:
                        all_true = False
                        break

                if all_true:
                    # Check for positive literal
                    goal_clause = True
                    for lit in clause:
                        if lit > 0:
                            goal_clause = False
                            if not model[lit]:
                                model[lit] = True
                                fixpoint = False
                                print(f"Inferred {lit} with clause {clause}")
                            break

                    if goal_clause:
                        print(f"No models satisfy all clauses simultaneously. False goal clause: {clause}")
                        return False

        print("Model:")
        for i in range(1, len(model)):
            print(f"Variable {i} = {model[i]}")

        return True

    def add_clause(self, clause):
        self.clauses.append(clause)

    def reset_clauses(self):
        self.clauses.clear()

    @staticmethod
    def example():
        # Example from AIMA Figure 7.16
        # Symbols A, B, L, M, P, Q are numbered 1..6.
        fc = ForwardChaining()

        fc.add_clause([-5, 6])
        fc.add_clause([-3, -4, 5])
        fc.add_clause([-2, -3, 4])
        fc.add_clause([-1, -5, 3])
        fc.add_clause([-1, -2, 3])
        fc.add_clause([1])
        fc.add_clause([2])

        model_exists = fc.forward_chaining(6)
        print("Model exists:", model_exists)


if __name__ == "__main__":
    ForwardChaining.example()
