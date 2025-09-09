## Inference Rules
| Rule               | Formulation    |
|--------------------|------------------------------------------|
| Modus Ponens (MP)  | P, P→Q ⟹ Q|
| Modus Tollens (MT) | ¬Q, P→Q ⟹ ¬P|
| Hyp. Syllogism (HS)| P→Q, Q→R ⟹ P→R|
| Disj. Syllogism (DS)| P∨Q, ¬P ⟹ Q  |
| Addition (Add)     | P ⟹ P∨Q       |
| Simplification (Simp)| P∧Q ⟹ P     |
| Conjunction (Conj) | P, Q ⟹ P∧Q    |
| Resolution (Res)   | (P∨Q), (¬P∨R) ⟹ Q∨R                     |

## Equivalence Laws
| Law                | Formulation    |
|--------------------|------------------------------------------|
| Identity           | P∧⊤≡P ; P∨⊥≡P |
| Domination         | P∨⊤≡⊤ ; P∧⊥≡⊥ |
| Idempotent         | P∨P≡P ; P∧P≡P |
| Double Negation    | ¬¬P≡P          |
| Commutative        | P∨Q≡Q∨P ; P∧Q≡Q∧P                       |
| Associative        | (P∨Q)∨R≡P∨(Q∨R) ; (P∧Q)∧R≡P∧(Q∧R)       |
| Distributive       | P∨(Q∧R)≡(P∨Q)∧(P∨R) ; P∧(Q∨R)≡(P∧Q)∨(P∧R)|
| De Morgan’s        | ¬(P∧Q)≡¬P∨¬Q ; ¬(P∨Q)≡¬P∧¬Q             |
| Absorption         | P∨(P∧Q)≡P ; P∧(P∨Q)≡P                   |
| Implication        | P→Q≡¬P∨Q ; ¬(P→Q)≡P∧¬Q                  |
| Biconditional      | P↔Q≡(P→Q)∧(Q→P)≡(P∧Q)∨(¬P∧¬Q)           |