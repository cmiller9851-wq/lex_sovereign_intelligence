# Pure Python Logic Theorist with Direct Substitution & Detachment Engine

class LogicTheorist:
    def __init__(self):
        # Core Axioms from Principia Mathematica
        self.axioms = [
            ("IMPLIES", ("OR", "?p", "?p"), "?p"),                      # Axiom 1.2
            ("IMPLIES", "?q", ("OR", "?p", "?q")),                      # Axiom 1.3
            ("IMPLIES", ("OR", "?p", "?q"), ("OR", "?q", "?p")),          # Axiom 1.4
            ("IMPLIES", 
                ("IMPLIES", "?p", "?q"), 
                ("IMPLIES", ("OR", "?r", "?p"), ("OR", "?r", "?q"))
            )                                                           # Axiom 1.6
        ]
        self.proven_theorems = list(self.axioms)

    def _unify(self, pattern, expr, bindings=None):
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

    def _substitute(self, pattern, bindings):
        if isinstance(pattern, str) and pattern.startswith("?"):
            return bindings.get(pattern, pattern)
        if isinstance(pattern, tuple):
            return tuple(self._substitute(elem, bindings) for elem in pattern)
        return pattern

    def prove_by_substitution(self, target_proposition):
        for theorem in self.proven_theorems:
            bindings = self._unify(theorem, target_proposition)
            if bindings is not None:
                return theorem, bindings
        return None

    def prove_by_detachment(self, target_proposition, depth=0, max_depth=2):
        if depth >= max_depth:
            return False

        for theorem in list(self.proven_theorems):
            if isinstance(theorem, tuple) and theorem[0] == "IMPLIES":
                antecedent, consequent = theorem[1], theorem[2]
                bindings = self._unify(consequent, target_proposition)
                
                if bindings is not None:
                    sub_goal = self._substitute(antecedent, bindings)
                    print(f"  [Depth {depth}] Detachment sub-goal generated: {sub_goal}")
                    
                    if self.prove_by_substitution(sub_goal) or self.prove_by_detachment(sub_goal, depth + 1, max_depth):
                        print(f"  [Depth {depth}] Detachment success for: {target_proposition}")
                        if target_proposition not in self.proven_theorems:
                            self.proven_theorems.append(target_proposition)
                        return True
        return False

    def prove(self, target_proposition):
        # Strategy 1: Direct Substitution Search
        result = self.prove_by_substitution(target_proposition)
        if result:
            src_theorem, bindings = result
            print(f"PROOF SUCCESSFUL (Substitution):")
            print(f"  Target:   {target_proposition}")
            print(f"  Matched:  {src_theorem}")
            print(f"  Bindings: {bindings}\n")
            if target_proposition not in self.proven_theorems:
                self.proven_theorems.append(target_proposition)
            return True

        # Strategy 2: Detachment (Modus Ponens) Search
        print(f"Direct match failed for: {target_proposition}")
        print("Initiating Detachment Search...")
        if self.prove_by_detachment(target_proposition):
            print(f"PROOF SUCCESSFUL (Detachment)\n")
            return True

        print(f"PROOF FAILED: Could not deduce {target_proposition}\n")
        return False


if __name__ == "__main__":
    lt = LogicTheorist()

    # Test Direct Substitution
    target_1 = ("IMPLIES", ("OR", "A", "A"), "A")
    lt.prove(target_1)

    # Test Detachment Engine
    target_2 = ("IMPLIES", ("OR", "B", "A"), ("OR", "A", "B"))
    lt.prove(target_2)
