/-
  The independence tightening of the AND false-negative rule, for product
  laws (Lean 4 core only).

  Two operands draw on disjoint sources, so at a fixed latent valuation the
  joint law of their observations is a product law `prod d1 d2`.  If both
  are exactly 1 and their false-negative masses are at most `a` (out of
  total `T1`) and `b` (out of total `T2`), the conjunction's false-negative
  mass, out of `T1 * T2`, satisfies

      err + a * b ≤ a * T2 + b * T1,

  i.e. err / (T1 T2) ≤ α + β − α β with α = a/T1, β = b/T2, which is
  1 − (1 − α)(1 − β).
-/

namespace TwoRateIndep

def mass {Ω : Type} : List (Nat × Ω) → (Ω → Bool) → Nat
  | [], _ => 0
  | (w, x) :: rest, P => (if P x then w else 0) + mass rest P

def total {Ω : Type} (d : List (Nat × Ω)) : Nat := mass d (fun _ => true)

/-- Product of two weighted outcome lists. -/
def prod {Ω₁ Ω₂ : Type} : List (Nat × Ω₁) → List (Nat × Ω₂) → List (Nat × (Ω₁ × Ω₂))
  | [], _ => []
  | (w, x) :: rest, d2 => (d2.map (fun p => (w * p.1, (x, p.2)))) ++ prod rest d2

theorem mass_append {Ω : Type} (d e : List (Nat × Ω)) (P : Ω → Bool) :
    mass (d ++ e) P = mass d P + mass e P := by
  induction d with
  | nil => simp [mass]
  | cons hd tl ih => obtain ⟨w, x⟩ := hd; simp [mass, ih]; omega

theorem mass_map_scale {Ω₁ Ω₂ : Type} (w : Nat) (x : Ω₁) (d2 : List (Nat × Ω₂))
    (P : Ω₁ → Bool) (Q : Ω₂ → Bool) :
    mass (d2.map (fun p => (w * p.1, (x, p.2)))) (fun z => P z.1 && Q z.2) =
      (if P x then w * mass d2 Q else 0) := by
  induction d2 with
  | nil => cases P x <;> simp [mass]
  | cons hd tl ih =>
    obtain ⟨v, y⟩ := hd
    simp only [List.map, mass] at *
    rw [ih]
    cases hP : P x <;> cases hQ : Q y <;> simp [Nat.mul_add]

theorem mass_prod {Ω₁ Ω₂ : Type} (d1 : List (Nat × Ω₁)) (d2 : List (Nat × Ω₂))
    (P : Ω₁ → Bool) (Q : Ω₂ → Bool) :
    mass (prod d1 d2) (fun z => P z.1 && Q z.2) = mass d1 P * mass d2 Q := by
  induction d1 with
  | nil => simp [prod, mass]
  | cons hd tl ih =>
    obtain ⟨w, x⟩ := hd
    simp only [prod, mass]
    rw [mass_append, mass_map_scale, ih]
    cases P x <;> simp [Nat.add_mul]

theorem mass_split {Ω : Type} (d : List (Nat × Ω)) (P : Ω → Bool) :
    mass d P + mass d (fun x => !(P x)) = total d := by
  induction d with
  | nil => simp [mass, total]
  | cons hd tl ih =>
    obtain ⟨w, x⟩ := hd
    simp only [total, mass] at *
    by_cases hP : P x = true
    · simp [hP]; omega
    · simp [hP]; omega

/-- The arithmetic core: with nA ≤ a ≤ T1 and nB ≤ b ≤ T2, where
    T1 = mA + nA and T2 = mB + nB,
    (T1 T2 − mA mB) + a b ≤ a T2 + b T1, stated without subtraction. -/
theorem core (mA nA mB nB a b : Nat) (ha : nA ≤ a) (hb : nB ≤ b)
    (haT : a ≤ mA + nA) (hbT : b ≤ mB + nB) :
    (mA + nA) * (mB + nB) + a * b ≤ mA * mB + (a * (mB + nB) + b * (mA + nA)) := by
  obtain ⟨α, rfl⟩ : ∃ α, a = nA + α := ⟨a - nA, by omega⟩
  obtain ⟨β, rfl⟩ : ∃ β, b = nB + β := ⟨b - nB, by omega⟩
  have hα : α ≤ mA := by omega
  have key : β * α ≤ β * mA := Nat.mul_le_mul_left β hα
  -- expand both sides into monomials, treated as atoms by omega
  simp only [Nat.add_mul, Nat.mul_add] at *
  have e1 : nA * nB = nB * nA := Nat.mul_comm _ _
  have e2 : α * nB = nB * α := Nat.mul_comm _ _
  have e3 : α * β = β * α := Nat.mul_comm _ _
  have e4 : nA * β = β * nA := Nat.mul_comm _ _
  have e5 : α * mB = mB * α := Nat.mul_comm _ _
  have e6 : nA * mB = mB * nA := Nat.mul_comm _ _
  have e7 : mA * nB = nB * mA := Nat.mul_comm _ _
  have e8 : mA * β = β * mA := Nat.mul_comm _ _
  omega

/-- Independent AND, false-negative side.  Operand observations are
    independent (product law); both operands are exactly 1; their
    false-negative masses are at most a and b.  Then the conjunction's
    false-negative mass err satisfies err + a b ≤ a T2 + b T1. -/
theorem and_omega_indep {Ω₁ Ω₂ : Type} (d1 : List (Nat × Ω₁)) (d2 : List (Nat × Ω₂))
    (A : Ω₁ → Bool) (B : Ω₂ → Bool) (a b : Nat)
    (hA : mass d1 (fun x => !(A x)) ≤ a) (hB : mass d2 (fun y => !(B y)) ≤ b)
    (haT : a ≤ total d1) (hbT : b ≤ total d2) :
    mass (prod d1 d2) (fun z => !(A z.1 && B z.2)) + a * b
      ≤ a * total d2 + b * total d1 := by
  have s1 := mass_split d1 A
  have s2 := mass_split d2 B
  have sp := mass_split (prod d1 d2) (fun z => A z.1 && B z.2)
  have tp : total (prod d1 d2) = total d1 * total d2 := by
    have := mass_prod d1 d2 (fun _ => true) (fun _ => true)
    simpa [total] using this
  have mp := mass_prod d1 d2 A B
  have c := core (mass d1 A) (mass d1 (fun x => !(A x))) (mass d2 B)
    (mass d2 (fun y => !(B y))) a b hA hB (by omega) (by omega)
  rw [s1, s2] at c
  have : mass (prod d1 d2) (fun z => !(A z.1 && B z.2)) + mass d1 A * mass d2 B
      = total d1 * total d2 := by omega
  omega

end TwoRateIndep
