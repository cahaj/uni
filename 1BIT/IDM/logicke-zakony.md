Generated with Claude Sonnet 5.5

# Logické zákony pro důkazy o množinách

Značení: p, q, r jsou výroky (např. „x ∈ A“), ¬ je negace, ∧ konjunkce, ∨ disjunkce, ⇒ implikace, ⇔ ekvivalence.

## 1. Definice množinových operací (převod na logiku)

| Množinová operace | Logický zápis |
| --- | --- |
| x ∈ A ∩ B | x ∈ A ∧ x ∈ B |
| x ∈ A ∪ B | x ∈ A ∨ x ∈ B |
| x ∈ A \\ B | x ∈ A ∧ x ∉ B |
| x ∈ A △ B | (x ∈ A ∧ x ∉ B) ∨ (x ∈ B ∧ x ∉ A), tedy „přesně jedno z nich“ (xor) |
| (x, y) ∈ A × B | x ∈ A ∧ y ∈ B |
| x ∉ A | ¬(x ∈ A) |

Každý důkaz rovnosti množin se tak převede na ověření logické ekvivalence.

## 2. Distributivní zákony

- p ∧ (q ∨ r) ⇔ (p ∧ q) ∨ (p ∧ r)
- p ∨ (q ∧ r) ⇔ (p ∨ q) ∧ (p ∨ r)

Platí obě, zleva i zprava (vytýkání i roznásobení). Druhá je méně intuitivní, ale pro množiny je potřeba stejně často.

## 3. De Morganovy zákony

- ¬(p ∧ q) ⇔ ¬p ∨ ¬q
- ¬(p ∨ q) ⇔ ¬p ∧ ¬q

Nezbytné u rozdílů typu A \\ (B ∪ C) a A \\ (B ∩ C), protože x ∉ B ∪ C znamená ¬(x ∈ B ∨ x ∈ C).

## 4. Komutativita, asociativita, idempotence

- p ∧ q ⇔ q ∧ p, p ∨ q ⇔ q ∨ p
- (p ∧ q) ∧ r ⇔ p ∧ (q ∧ r), stejně pro ∨
- p ∧ p ⇔ p, p ∨ p ⇔ p

Idempotence se hodí třeba při „zdvojení“ x ∉ C, jako v příkladu 2 (a), kde se x ∉ C objevovalo u obou částí: (p ∧ r) ∨ (q ∧ r).

## 5. Absorpce

- p ∧ (p ∨ q) ⇔ p
- p ∨ (p ∧ q) ⇔ p

To je přesně logické jádro příkladů 1 (a) a (b).

## 6. Dvojitá negace a vlastnosti negace

- ¬¬p ⇔ p
- p ∧ ¬p ⇔ 0 (spor, nepravda), p ∨ ¬p ⇔ 1 (tautologie)
- p ∧ 1 ⇔ p, p ∨ 0 ⇔ p, p ∧ 0 ⇔ 0, p ∨ 1 ⇔ 1

Důležité pro hledání, že množina vychází prázdná (např. 1 (g): x ∈ A \\ B a x ∈ B \\ A vede na x ∉ B ∧ x ∈ B, spor).

## 7. Implikace a ekvivalence

- p ⇒ q ⇔ ¬p ∨ q (převod implikace na disjunkci)
- p ⇒ q ⇔ ¬q ⇒ ¬p (obměna, kontrapozice)
- ¬(p ⇒ q) ⇔ p ∧ ¬q
- p ⇔ q ⇔ (p ⇒ q) ∧ (q ⇒ p)

Poslední je přesně to, proč rovnost množin dokazujeme dvěma inkluzemi.

## 8. Zjednodušení a zavedení (pravidla pro jednosměrné kroky)

- p ∧ q ⇒ p (zjednodušení konjunkce)
- p ⇒ p ∨ q (zavedení disjunkce)
- z p a q plyne p ∧ q (zavedení konjunkce)
- z p a p ⇒ q plyne q (modus ponens)
- z p ∨ q a ¬p plyne q (disjunktivní sylogismus)

## 9. Rozbor případů jako implikace

Pravidlo „z (p ∨ q), (p ⇒ s) a (q ⇒ s) plyne s“ lze psát čistě formulí:

((p ⇒ s) ∧ (q ⇒ s)) ⇔ ((p ∨ q) ⇒ s)

Tím se rozbor případů nahradí jednou implikací.

## 10. Kvantifikátory (pro obecné postupy)

- X ⊆ Y ⇔ ∀x: (x ∈ X ⇒ x ∈ Y)
- X = Y ⇔ ∀x: (x ∈ X ⇔ x ∈ Y)
- ¬∀x φ ⇔ ∃x ¬φ (užitečné pro protipříklady: stačí najít jeden prvek, který rovnost porušuje)

## 11. Pro kartézské součiny

Pro dvojici (x, y) rozepisuj složky zvlášť:

(x, y) ∈ A × (B ∪ C) ⇔ x ∈ A ∧ (y ∈ B ∨ y ∈ C) ⇔ (x ∈ A ∧ y ∈ B) ∨ (x ∈ A ∧ y ∈ C)

To je distributivita ∧ vůči ∨, použitá na složky.

## Praktický postup

1. Zvolit libovolné x (u součinů dvojici (x, y)).
2. Převést množinovou notaci na logickou (tabulka 1).
3. Upravit levou stranu pomocí zákonů (distributivita, De Morgan, absorpce…).
4. Dojít k pravé straně a převést zpět na množiny.
5. Pokud rovnost neplatí, najít konkrétní prvek, který splňuje jednu stranu a druhou ne (protipříklad), nebo ukázat, že se logické formule liší pro nějaké ohodnocení p, q, r.

**Tip:** pro rychlou kontrolu, zda rovnost platí, sestav **pravdivostní tabulku** pro p = „x ∈ A“, q = „x ∈ B“, r = „x ∈ C“. Pokud mají obě strany pro všech 8 ohodnocení stejnou hodnotu, rovnost platí.
