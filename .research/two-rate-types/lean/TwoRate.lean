/-
  Soundness of the dependence-free two-rate rules for the Boolean fragment.

  Self-contained (Lean 4 core only, no Mathlib).  Probabilities are natural
  numbers over a common denominator: a joint law of all observations at one
  latent valuation is a finite list of (weight, outcome) pairs, and the
  probability of an event is the total weight of the outcomes satisfying it.
  Nothing is assumed about the joint law: the observations of different
  primitives may be arbitrarily dependent.  Rules are stated without the
  `min 1` cap, which only weakens them (any mass is at most the total).

  Theorem `sound`: for every latent valuation `t`, every joint law `d`, and
  every expression `e` (sharing and constants allowed), if each primitive
  meets its declared conditional rates then `e` meets the rates computed by
  `ty`.  Quantifying over every `t` is the supremum over latent valuations.
-/

namespace TwoRate

/-- Mass of the event `P` under the weighted outcome list `d`. -/
def mass {Ω : Type} : List (Nat × Ω) → (Ω → Bool) → Nat
  | [], _ => 0
  | (w, x) :: rest, P => (if P x then w else 0) + mass rest P

theorem mass_le_of_imp {Ω : Type} (d : List (Nat × Ω)) (P Q : Ω → Bool)
    (h : ∀ x, P x = true → Q x = true) : mass d P ≤ mass d Q := by
  induction d with
  | nil => simp [mass]
  | cons hd tl ih =>
    obtain ⟨w, x⟩ := hd
    simp only [mass]
    have hx := h x
    cases hP : P x <;> cases hQ : Q x <;> simp_all <;> omega

theorem mass_le_add_of_imp {Ω : Type} (d : List (Nat × Ω)) (P Q R : Ω → Bool)
    (h : ∀ x, P x = true → Q x = true ∨ R x = true) :
    mass d P ≤ mass d Q + mass d R := by
  induction d with
  | nil => simp [mass]
  | cons hd tl ih =>
    obtain ⟨w, x⟩ := hd
    simp only [mass]
    have hx := h x
    cases hP : P x <;> cases hQ : Q x <;> cases hR : R x <;> simp_all <;> omega

theorem mass_false {Ω : Type} (d : List (Nat × Ω)) : mass d (fun _ => false) = 0 := by
  induction d with
  | nil => rfl
  | cons hd tl ih => obtain ⟨w, x⟩ := hd; simp [mass, ih]

/-- Boolean core: primitives are indices; reusing an index shares the bit. -/
inductive Expr where
  | prim : Nat → Expr
  | const : Bool → Expr
  | neg : Expr → Expr
  | and : Expr → Expr → Expr
  | or : Expr → Expr → Expr
  | xor : Expr → Expr → Expr
  | ite : Expr → Expr → Expr → Expr

/-- Evaluation given a value for each primitive (exact or observed). -/
def eval : Expr → (Nat → Bool) → Bool
  | .prim i, v => v i
  | .const b, _ => b
  | .neg e, v => !(eval e v)
  | .and a b, v => eval a v && eval b v
  | .or a b, v => eval a v || eval b v
  | .xor a b, v => eval a v != eval b v
  | .ite c a b, v => if eval c v then eval a v else eval b v

structure Rates where
  eps : Nat
  omg : Nat

/-- The dependence-free two-rate rules. -/
def ty (r : Nat → Rates) : Expr → Rates
  | .prim i => r i
  | .const _ => ⟨0, 0⟩
  | .neg e => ⟨(ty r e).omg, (ty r e).eps⟩
  | .and a b => ⟨max (ty r a).eps (ty r b).eps, (ty r a).omg + (ty r b).omg⟩
  | .or a b => ⟨(ty r a).eps + (ty r b).eps, max (ty r a).omg (ty r b).omg⟩
  | .xor a b =>
      ⟨max ((ty r a).eps + (ty r b).eps) ((ty r a).omg + (ty r b).omg),
       max ((ty r a).eps + (ty r b).omg) ((ty r a).omg + (ty r b).eps)⟩
  | .ite c a b =>
      ⟨max ((ty r a).eps + (ty r c).omg) ((ty r b).eps + (ty r c).eps),
       max ((ty r a).omg + (ty r c).omg) ((ty r b).omg + (ty r c).eps)⟩

/-- The semantic judgment `e : Bool[eps, omg]` at one latent valuation `t`
    and one joint law `d` of observations `o`. -/
def Holds {Ω : Type} (d : List (Nat × Ω)) (o : Ω → Nat → Bool) (t : Nat → Bool)
    (e : Expr) (rt : Rates) : Prop :=
  (eval e t = false → mass d (fun x => eval e (o x)) ≤ rt.eps) ∧
  (eval e t = true → mass d (fun x => !(eval e (o x))) ≤ rt.omg)

theorem le_max_of_le_left {a b c : Nat} (h : a ≤ b) : a ≤ max b c :=
  Nat.le_trans h (Nat.le_max_left b c)

theorem le_max_of_le_right {a b c : Nat} (h : a ≤ c) : a ≤ max b c :=
  Nat.le_trans h (Nat.le_max_right b c)

theorem sound {Ω : Type} (r : Nat → Rates) (t : Nat → Bool) (d : List (Nat × Ω))
    (o : Ω → Nat → Bool)
    (hp : ∀ i, (t i = false → mass d (fun x => o x i) ≤ (r i).eps) ∧
               (t i = true → mass d (fun x => !(o x i)) ≤ (r i).omg)) :
    ∀ e, Holds d o t e (ty r e) := by
  intro e
  induction e with
  | prim i => exact hp i
  | const b =>
    constructor
    · intro h
      simp only [eval] at h
      subst h
      simp [eval, ty, mass_false]
    · intro h
      simp only [eval] at h
      subst h
      simp [eval, ty, mass_false]
  | neg e ih =>
    obtain ⟨ih0, ih1⟩ := ih
    constructor
    · intro h
      simp only [eval, Bool.not_eq_false'] at h
      simpa [eval, ty] using ih1 h
    · intro h
      simp only [eval, Bool.not_eq_true'] at h
      simpa [eval, ty] using ih0 h
  | and a b iha ihb =>
    obtain ⟨ha0, ha1⟩ := iha
    obtain ⟨hb0, hb1⟩ := ihb
    constructor
    · intro h
      simp only [eval, ty]
      cases hta : eval a t
      · have := mass_le_of_imp d (fun x => eval a (o x) && eval b (o x))
          (fun x => eval a (o x)) (by intro x hx; simp at hx; exact hx.1)
        exact le_max_of_le_left (Nat.le_trans this (ha0 hta))
      · have htb : eval b t = false := by simp [eval, hta] at h; exact h
        have := mass_le_of_imp d (fun x => eval a (o x) && eval b (o x))
          (fun x => eval b (o x)) (by intro x hx; simp at hx; exact hx.2)
        exact le_max_of_le_right (Nat.le_trans this (hb0 htb))
    · intro h
      simp only [eval, Bool.and_eq_true] at h
      simp only [eval, ty]
      have := mass_le_add_of_imp d (fun x => !(eval a (o x) && eval b (o x)))
        (fun x => !(eval a (o x))) (fun x => !(eval b (o x)))
        (by intro x hx; cases ea : eval a (o x) <;> cases eb : eval b (o x) <;> simp_all)
      have h1 := ha1 h.1
      have h2 := hb1 h.2
      omega
  | or a b iha ihb =>
    obtain ⟨ha0, ha1⟩ := iha
    obtain ⟨hb0, hb1⟩ := ihb
    constructor
    · intro h
      simp only [eval, Bool.or_eq_false_iff] at h
      simp only [eval, ty]
      have := mass_le_add_of_imp d (fun x => eval a (o x) || eval b (o x))
        (fun x => eval a (o x)) (fun x => eval b (o x))
        (by intro x hx; simpa using hx)
      have h1 := ha0 h.1
      have h2 := hb0 h.2
      omega
    · intro h
      simp only [eval, ty]
      cases hta : eval a t
      · have htb : eval b t = true := by simp [eval, hta] at h; exact h
        have := mass_le_of_imp d (fun x => !(eval a (o x) || eval b (o x)))
          (fun x => !(eval b (o x))) (by intro x hx; simp at hx; simp [hx.2])
        exact le_max_of_le_right (Nat.le_trans this (hb1 htb))
      · have := mass_le_of_imp d (fun x => !(eval a (o x) || eval b (o x)))
          (fun x => !(eval a (o x))) (by intro x hx; simp at hx; simp [hx.1])
        exact le_max_of_le_left (Nat.le_trans this (ha1 hta))
  | xor a b iha ihb =>
    obtain ⟨ha0, ha1⟩ := iha
    obtain ⟨hb0, hb1⟩ := ihb
    constructor
    · intro h
      simp only [eval, ty]
      cases hta : eval a t <;> cases htb : eval b t <;> simp [eval, hta, htb] at h
      · -- both exact values 0: an observed 1 needs an observed 1 somewhere
        have := mass_le_add_of_imp d (fun x => eval a (o x) != eval b (o x))
          (fun x => eval a (o x)) (fun x => eval b (o x))
          (by intro x hx; cases ea : eval a (o x) <;> cases eb : eval b (o x) <;> simp_all)
        have h1 := ha0 hta
        have h2 := hb0 htb
        exact le_max_of_le_left (by omega)
      · -- both exact values 1
        have := mass_le_add_of_imp d (fun x => eval a (o x) != eval b (o x))
          (fun x => !(eval a (o x))) (fun x => !(eval b (o x)))
          (by intro x hx; cases ea : eval a (o x) <;> cases eb : eval b (o x) <;> simp_all)
        have h1 := ha1 hta
        have h2 := hb1 htb
        exact le_max_of_le_right (by omega)
    · intro h
      simp only [eval, ty]
      cases hta : eval a t <;> cases htb : eval b t <;> simp [eval, hta, htb] at h
      · -- exact (0,1)
        have := mass_le_add_of_imp d (fun x => !(eval a (o x) != eval b (o x)))
          (fun x => eval a (o x)) (fun x => !(eval b (o x)))
          (by intro x hx; cases ea : eval a (o x) <;> cases eb : eval b (o x) <;> simp_all)
        have h1 := ha0 hta
        have h2 := hb1 htb
        exact le_max_of_le_left (by omega)
      · -- exact (1,0)
        have := mass_le_add_of_imp d (fun x => !(eval a (o x) != eval b (o x)))
          (fun x => !(eval a (o x))) (fun x => eval b (o x))
          (by intro x hx; cases ea : eval a (o x) <;> cases eb : eval b (o x) <;> simp_all)
        have h1 := ha1 hta
        have h2 := hb0 htb
        exact le_max_of_le_right (by omega)
  | ite c a b ihc iha ihb =>
    obtain ⟨hc0, hc1⟩ := ihc
    obtain ⟨ha0, ha1⟩ := iha
    obtain ⟨hb0, hb1⟩ := ihb
    constructor
    · intro h
      simp only [eval, ty]
      cases htc : eval c t
      · -- condition exactly 0: else-branch exact value is 0
        have htb : eval b t = false := by simp [eval, htc] at h; exact h
        have := mass_le_add_of_imp d
          (fun x => if eval c (o x) then eval a (o x) else eval b (o x))
          (fun x => eval b (o x)) (fun x => eval c (o x))
          (by intro x hx; cases ec : eval c (o x) <;> simp_all)
        have h1 := hb0 htb
        have h2 := hc0 htc
        exact le_max_of_le_right (by omega)
      · -- condition exactly 1: then-branch exact value is 0
        have hta : eval a t = false := by simp [eval, htc] at h; exact h
        have := mass_le_add_of_imp d
          (fun x => if eval c (o x) then eval a (o x) else eval b (o x))
          (fun x => eval a (o x)) (fun x => !(eval c (o x)))
          (by intro x hx; cases ec : eval c (o x) <;> simp_all)
        have h1 := ha0 hta
        have h2 := hc1 htc
        exact le_max_of_le_left (by omega)
    · intro h
      simp only [eval, ty]
      cases htc : eval c t
      · have htb : eval b t = true := by simp [eval, htc] at h; exact h
        have := mass_le_add_of_imp d
          (fun x => !(if eval c (o x) then eval a (o x) else eval b (o x)))
          (fun x => !(eval b (o x))) (fun x => eval c (o x))
          (by intro x hx; cases ec : eval c (o x) <;> simp_all)
        have h1 := hb1 htb
        have h2 := hc0 htc
        exact le_max_of_le_right (by omega)
      · have hta : eval a t = true := by simp [eval, htc] at h; exact h
        have := mass_le_add_of_imp d
          (fun x => !(if eval c (o x) then eval a (o x) else eval b (o x)))
          (fun x => !(eval a (o x))) (fun x => !(eval c (o x)))
          (by intro x hx; cases ec : eval c (o x) <;> simp_all)
        have h1 := ha1 hta
        have h2 := hc1 htc
        exact le_max_of_le_left (by omega)

/-- Corollary in the form of the brief: the supremum over latent valuations.
    For all valuations at which `e` is exactly 0, the false-positive mass is
    bounded by the derived eps (and dually for omg). -/
theorem sound_sup {Ω : Type} (r : Nat → Rates) (law : (Nat → Bool) → List (Nat × Ω))
    (o : Ω → Nat → Bool)
    (hp : ∀ t i, (t i = false → mass (law t) (fun x => o x i) ≤ (r i).eps) ∧
                 (t i = true → mass (law t) (fun x => !(o x i)) ≤ (r i).omg))
    (e : Expr) :
    (∀ t, eval e t = false → mass (law t) (fun x => eval e (o x)) ≤ (ty r e).eps) ∧
    (∀ t, eval e t = true → mass (law t) (fun x => !(eval e (o x))) ≤ (ty r e).omg) :=
  ⟨fun t => (sound r t (law t) o (hp t) e).1, fun t => (sound r t (law t) o (hp t) e).2⟩

/-- Sanity check: the AND-FPR rule is `max`, not the all-negative product. -/
example : (ty (fun _ => ⟨2, 10⟩) (.and (.prim 0) (.prim 1))).eps = 2 := rfl

end TwoRate
