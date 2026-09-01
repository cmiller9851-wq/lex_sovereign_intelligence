class LogicTheorist:
    """A zero-dependency, pure Python symbolic inference engine 
    modeled after the 1955-1956 Logic Theorist (Newell, Simon, Shaw).
    """
    def __init__(self):
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
        """Unifies a pattern containing variables (?p) against an expression."""
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
        """Applies variable bindings to a logical expression tree."""
        if isinstance(pattern, str) and pattern.startswith("?"):
            return bindings.get(pattern, pattern)
        if isinstance(pattern, tuple):
            return tuple(self._substitute(elem, bindings) for elem in pattern)
        return pattern

    def _has_free_vars(self, expr):
        """Detects uninstantiated pattern variables."""
        if isinstance(expr, str) and expr.startswith("?"):
            return True
        if isinstance(expr, tuple):
            return any(self._has_free_vars(e) for e in expr)
        return False

    def prove_by_substitution(self, target_proposition):
        """Heuristic Method 1: Direct Axiom Matching & Substitution."""
        for theorem in self.proven_theorems:
            bindings = self._unify(theorem, target_proposition)
            if bindings is not None:
                return theorem, bindings
        return None

    def prove_by_detachment(self, target_proposition, depth=0, max_depth=3, path=None):
        """Heuristic Method 2: Modus Ponens Detachment with Cycle Protection."""
        if path is None:
            path = set()
        if depth >= max_depth:
            return False

        for theorem in list(self.proven_theorems):
            if theorem == ("IMPLIES", ("OR", "?p", "?p"), "?p"):
                continue

            if isinstance(theorem, tuple) and theorem[0] == "IMPLIES":
                antecedent, consequent = theorem[1], theorem[2]
                bindings = self._unify(consequent, target_proposition)
                
                if bindings is not None:
                    sub_goal = self._substitute(antecedent, bindings)
                    if self._has_free_vars(sub_goal) or sub_goal in path:
                        continue
                    
                    new_path = path | {sub_goal}
                    if self.prove_by_substitution(sub_goal) or \
                       self.prove_by_detachment(sub_goal, depth + 1, max_depth, new_path) or \
                       self.prove_by_chaining(sub_goal, depth + 1, max_depth, new_path):
                        if target_proposition not in self.proven_theorems:
                            self.proven_theorems.append(target_proposition)
                        return True
        return False

    def prove_by_chaining(self, target_proposition, depth=0, max_depth=3, path=None):
        """Heuristic Method 3: Bidirectional Chaining & Transitivity."""
        if path is None:
            path = set()
        if depth >= max_depth:
            return False

        if not (isinstance(target_proposition, tuple) and target_proposition[0] == "IMPLIES"):
            return False

        a_target, c_target = target_proposition[1], target_proposition[2]

        # Mode 1: Top-Level Implication Transitivity
        for theorem in list(self.proven_theorems):
            if isinstance(theorem, tuple) and theorem[0] == "IMPLIES":
                bindings = self._unify(theorem[1], a_target)
                if bindings is not None:
                    b_intermediate = self._substitute(theorem[2], bindings)
                    if self._has_free_vars(b_intermediate):
                        extra_bindings = self._unify(theorem[2], c_target, bindings.copy())
                        if extra_bindings is not None:
                            b_intermediate = self._substitute(theorem[2], extra_bindings)

                    sub_goal = ("IMPLIES", b_intermediate, c_target)
                    if not self._has_free_vars(b_intermediate) and sub_goal not in path:
                        new_path = path | {sub_goal}
                        if self.prove_by_substitution(sub_goal) or \
                           self.prove_by_detachment(sub_goal, depth + 1, max_depth, new_path) or \
                           self.prove_by_chaining(sub_goal, depth + 1, max_depth, new_path):
                            if target_proposition not in self.proven_theorems:
                                self.proven_theorems.append(target_proposition)
                            return True

        # Mode 2: Nested Implication Chaining H -> (X -> Y)
        if isinstance(c_target, tuple) and c_target[0] == "IMPLIES":
            x_target, y_target = c_target[1], c_target[2]
            for theorem in list(self.proven_theorems):
                if isinstance(theorem, tuple) and theorem[0] == "IMPLIES":
                    # Left Chaining (X -> M)
                    bl = self._unify(theorem[1], x_target)
                    if bl is not None:
                        m = self._substitute(theorem[2], bl)
                        sub_goal = ("IMPLIES", a_target, ("IMPLIES", m, y_target))
                        if not self._has_free_vars(m) and sub_goal not in path:
                            new_path = path | {sub_goal}
                            if self.prove_by_substitution(sub_goal) or \
                               self.prove_by_detachment(sub_goal, depth + 1, max_depth, new_path) or \
                               self.prove_by_chaining(sub_goal, depth + 1, max_depth, new_path):
                                if target_proposition not in self.proven_theorems:
                                    self.proven_theorems.append(target_proposition)
                                return True

                    # Right Chaining (M -> Y)
                    br = self._unify(theorem[2], y_target)
                    if br is not None:
                        m = self._substitute(theorem[1], br)
                        sub_goal = ("IMPLIES", a_target, ("IMPLIES", x_target, m))
                        if not self._has_free_vars(m) and sub_goal not in path:
                            new_path = path | {sub_goal}
                            if self.prove_by_substitution(sub_goal) or \
                               self.prove_by_detachment(sub_goal, depth + 1, max_depth, new_path) or \
                               self.prove_by_chaining(sub_goal, depth + 1, max_depth, new_path):
                                if target_proposition not in self.proven_theorems:
                                    self.proven_theorems.append(target_proposition)
                                return True
        return False

    def prove(self, target_proposition):
        """Orchestrates heuristic search layers to prove target propositions."""
        res = self.prove_by_substitution(target_proposition)
        if res:
            print(f"SUCCESS (Substitution): {target_proposition}")
            if target_proposition not in self.proven_theorems:
                self.proven_theorems.append(target_proposition)
            return True

        initial_path = {target_proposition}
        if self.prove_by_detachment(target_proposition, path=initial_path):
            print(f"SUCCESS (Detachment): {target_proposition}")
            return True

        if self.prove_by_chaining(target_proposition, path=initial_path):
            print(f"SUCCESS (Chaining): {target_proposition}")
            return True

        print(f"FAILED: {target_proposition}")
        return False


if __name__ == "__main__":
    lt = LogicTheorist()

    # Pre-requisite Commutative Lemmata
    lt.prove(("IMPLIES", ("OR", "A", "C"), ("OR", "C", "A")))
    lt.prove(("IMPLIES", ("OR", "C", "B"), ("OR", "B", "C")))

    # Target: Right-Sided Disjunction
    target_right = (
        "IMPLIES",
        ("IMPLIES", "A", "B"),
        ("IMPLIES", ("OR", "A", "C"), ("OR", "B", "C"))
    )
    lt.prove(target_right)
