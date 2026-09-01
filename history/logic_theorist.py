class LogicTheorist:
    def __init__(self):
        # Core Axioms from Principia Mathematica (represented as nested tuples)
        self.axioms = [
            ("IMPLIES", ("OR", "?p", "?p"), "?p"),                      # Axiom 1.2: (p v p) -> p
            ("IMPLIES", "?q", ("OR", "?p", "?q")),                      # Axiom 1.3: q -> (p v q)
            ("IMPLIES", ("OR", "?p", "?q"), ("OR", "?q", "?p")),          # Axiom 1.4: (p v q) -> (q v p)
            ("IMPLIES", 
                ("IMPLIES", "?p", "?q"), 
                ("IMPLIES", ("OR", "?r", "?p"), ("OR", "?r", "?q"))
            )                                                           # Axiom 1.6: (p -> q) -> ((r v p) -> (r v q))
        ]
        self.proven_theorems = list(self.axioms)

    def _unify(self, pattern, expr, bindings=None):
        """Attempts to match a target pattern against a known theorem structure."""
        if bindings is None:
            bindings = {}

        if isinstance(pattern, str) and pattern.startswith("?"):
            if pattern in bindings:
                return bindings if bindings[pattern] == expr else None
            new_bindings = bindings.copy()
            new_bindings[pattern] = expr
            return new_bindings

        if type(pattern) != type(expr):
            return None

        if isinstance(pattern, tuple):
            if len(pattern) != len(expr) or pattern[0] != expr[0]:
                return None
            for p_sub, e_sub in zip(pattern[1:], expr[1:]):
                bindings = self._unify(p_sub, e_sub, bindings)
                if bindings is None:
                    return None
            return bindings

        return bindings if pattern == expr else None

    def prove_by_substitution(self, target_proposition):
        """Heuristic Method 1: Direct Substitution Search"""
        for theorem in self.proven_theorems:
            bindings = self._unify(theorem, target_proposition)
            if bindings is not None:
                return theorem, bindings
        return None

    def prove(self, target_proposition):
        result = self.prove_by_substitution(target_proposition)
        if result:
            src_theorem, bindings = result
            print(f"PROOF SUCCESSFUL:")
            print(f"  Target:   {target_proposition}")
            print(f"  Matched:  {src_theorem}")
            print(f"  Bindings: {bindings}\n")
            if target_proposition not in self.proven_theorems:
                self.proven_theorems.append(target_proposition)
            return True
        
        print(f"PROOF FAILED: Target {target_proposition} could not be deduced.")
        return False


if __name__ == "__main__":
    lt = LogicTheorist()

    # Theorem 2.01: (A v A) -> A
    target_1 = ("IMPLIES", ("OR", "A", "A"), "A")
    lt.prove(target_1)

    # Theorem 2.02: B -> (A v B)
    target_2 = ("IMPLIES", "B", ("OR", "A", "B"))
    lt.prove(target_2)
