# Pure Python Logic Theorist with Variable-Safe Chaining Engine

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

    def _has_free_vars(self, expr):
        """Returns True if expression contains uninstantiated ? variables."""
        if isinstance(expr, str) and expr.startswith("?"):
            return True
        if isinstance(expr, tuple):
            return any(self._has_free_vars(e) for e in expr)
        return False

    def prove_by_substitution(self, target_proposition):
        for theorem in self.proven_theorems:
            bindings = self._unify(theorem, target_proposition)
            if bindings is not None:
                return theorem, bindings
        return None

    def prove_by_detachment(self, target_proposition, depth=0, max_depth=1):
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
                    if self._has_free_vars(sub_goal):
                        continue
                    
                    print(f"  [Detachment] Sub-goal generated: {sub_goal}")
                    if self.prove_by_substitution(sub_goal) or self.prove_by_detachment(sub_goal, depth + 1, max_depth):
                        if target_proposition not in self.proven_theorems:
                            self.proven_theorems.append(target_proposition)
                        return True
        return False

    def prove_by_chaining(self, target_proposition):
        """Forward Chaining (Syllogism): Given A -> C, find A -> B and prove B -> C."""
        if not (isinstance(target_proposition, tuple) and target_proposition[0] == "IMPLIES"):
            return False

        a_target, c_target = target_proposition[1], target_proposition[2]

        for theorem in list(self.proven_theorems):
            if isinstance(theorem, tuple) and theorem[0] == "IMPLIES":
                bindings = self._unify(theorem[1], a_target)
                if bindings is not None:
                    b_intermediate = self._substitute(theorem[2], bindings)
                    
                    # Discard candidate if intermediate state contains uninstantiated variables
                    if self._has_free_vars(b_intermediate):
                        continue

                    sub_goal = ("IMPLIES", b_intermediate, c_target)
                    print(f"  [Chaining] Intermediate state found: {b_intermediate}")
                    print(f"  [Chaining] Sub-goal generated: {sub_goal}")

                    if self.prove_by_substitution(sub_goal) or self.prove_by_detachment(sub_goal):
                        if target_proposition not in self.proven_theorems:
                            self.proven_theorems.append(target_proposition)
                        return True
        return False

    def prove(self, target_proposition):
        # Strategy 1: Substitution
        result = self.prove_by_substitution(target_proposition)
        if result:
            src_theorem, bindings = result
            print(f"PROOF SUCCESSFUL (Substitution):")
            print(f"  Target:   {target_proposition}")
            print(f"  Matched:  {src_theorem}\n")
            if target_proposition not in self.proven_theorems:
                self.proven_theorems.append(target_proposition)
            return True

        # Strategy 2: Detachment
        print(f"Direct match failed for target: {target_proposition}")
        print("Initiating Detachment Search...")
        if self.prove_by_detachment(target_proposition):
            print(f"PROOF SUCCESSFUL (Detachment)\n")
            return True

        # Strategy 3: Chaining
        print("Initiating Chaining Search...")
        if self.prove_by_chaining(target_proposition):
            print(f"PROOF SUCCESSFUL (Chaining)\n")
            return True

        print(f"PROOF FAILED: Could not deduce target\n")
        return False


if __name__ == "__main__":
    lt = LogicTheorist()

    # Step 1: Prove A -> (B v A)
    step_1 = ("IMPLIES", "A", ("OR", "B", "A"))
    lt.prove(step_1)

    # Step 2: Prove (B v A) -> (A v B)
    step_2 = ("IMPLIES", ("OR", "B", "A"), ("OR", "A", "B"))
    lt.prove(step_2)

    # Step 3: Target requiring Chaining: Prove A -> (A v B)
    # Uses Theorem 1 [A -> (B v A)] to generate sub-goal [(B v A) -> (A v B)], matching Theorem 2.
    target_chain = ("IMPLIES", "A", ("OR", "A", "B"))
    lt.prove(target_chain)
