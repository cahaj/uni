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

## 12. Pravidla pro práci s kvantifikátory (rozšíření kapitoly 10)

U důkazů o relacích se místo množinových operací objevují hlavně kvantifikátory: definice složení obsahuje „existuje y“, definice vlastností obsahuje „pro všechna x, y, z“. Tato kapitola navazuje na kapitolu 10 a rozvádí ji.

### 12.1 Základní pojmy

- **∀x φ(x)**: pro každé x platí φ(x).
- **∃x φ(x)**: existuje aspoň jedno x, pro které platí φ(x).
- **∃!x φ(x)**: existuje právě jedno takové x (používá se u zobrazení).
- Proměnná za kvantifikátorem je **vázaná**, lze ji přejmenovat: ∃y φ(y) ⇔ ∃t φ(t). Tohle se hodí, když se v jednom důkazu objeví dvě různá „y“.
- Kvantifikátor se vždy vztahuje na **celou formuli za ním**. Zápis ∀x (p ⇒ q) není totéž co (∀x p) ⇒ q.

### 12.2 Negace kvantifikátorů

| Negace | Převod |
| --- | --- |
| ¬∀x φ | ∃x ¬φ |
| ¬∃x φ | ∀x ¬φ |
| ¬∀x ∃y φ | ∃x ∀y ¬φ (každý kvantifikátor se otočí, negace se přesune dovnitř) |
| ¬∀x (p ⇒ q) | ∃x (p ∧ ¬q) (kombinace s pravidlem ¬(p ⇒ q) ⇔ p ∧ ¬q z kapitoly 7) |

**Použití u vlastností relací (negace = protipříklad):**

- R není reflexivní: ∃x: ¬(xRx), tedy chybí smyčka.
- R není symetrická: ∃x, y: xRy ∧ ¬(yRx).
- R není antisymetrická: ∃x, y: xRy ∧ yRx ∧ x ≠ y.
- R není tranzitivní: ∃x, y, z: xRy ∧ yRz ∧ ¬(xRz).
- Rovnost X = Y neplatí: ∃x: ¬(x ∈ X ⇔ x ∈ Y), tedy existuje prvek, který leží v jedné množině a ve druhé ne.

### 12.3 Rozdělení kvantifikátorů přes spojky

| Pravidlo | Platí? |
| --- | --- |
| ∀x (φ ∧ ψ) ⇔ ∀x φ ∧ ∀x ψ | ano, oběma směry |
| ∃x (φ ∨ ψ) ⇔ ∃x φ ∨ ∃x ψ | ano, oběma směry (použito v úloze 10 a) |
| ∃x (φ ∧ ψ) ⇒ ∃x φ ∧ ∃x ψ | jen jedním směrem |
| ∀x φ ∨ ∀x ψ ⇒ ∀x (φ ∨ ψ) | jen jedním směrem |

Proč opačné směry selhávají: pravá strana „∃x φ ∧ ∃x ψ“ dovoluje, aby každá z formulí byla splněna jiným x, zatímco levá strana „∃x (φ ∧ ψ)“ chce jedno x pro obě. Podobně u ∀ a ∨.

- Protipříklad k ∃ a ∧: na ℤ je ∃x (x je sudé ∧ x je liché) nepravdivé, ale ∃x (x je sudé) ∧ ∃x (x je liché) pravdivé.
- Protipříklad k ∀ a ∨: na ℤ platí ∀x (x je sudé ∨ x je liché), ale neplatí ∀x (x je sudé) ani ∀x (x je liché).

**Tohle je přesně důvod, proč je v úloze 11 u průniku jen inkluze „⊆“.** Průnik odpovídá ∧, a ∃ se přes ∧ nerozdělí oběma směry.

### 12.4 Vytknutí části, která na x nezávisí

Pokud formule ψ **neobsahuje proměnnou x**, platí:

- ∃x (φ(x) ∧ ψ) ⇔ (∃x φ(x)) ∧ ψ
- ∃x (φ(x) ∨ ψ) ⇔ (∃x φ(x)) ∨ ψ
- ∀x (φ(x) ∧ ψ) ⇔ (∀x φ(x)) ∧ ψ
- ∀x (φ(x) ∨ ψ) ⇔ (∀x φ(x)) ∨ ψ

Pozor: v definici složení \[x,y\] ∈ S ∧ \[y,z\] ∈ R obsahují **oba** členy proměnnou y, takže vytknout nelze. Naopak \[y,z\] ∈ R spolu s ∃x by vytknout šlo.

### 12.5 Pořadí kvantifikátorů

- Stejné kvantifikátory lze zaměnit: ∀x ∀y φ ⇔ ∀y ∀x φ a ∃x ∃y φ ⇔ ∃y ∃x φ. (Použito v 10 e, kde se zaměňuje ∃y a ∃i.)
- Různé kvantifikátory **nelze** zaměnit: ∃y ∀x φ ⇒ ∀x ∃y φ platí jen jedním směrem.
- Příklad na ℕ: ∀x ∃y (y > x) je pravda (ke každému čísle existuje větší), ale ∃y ∀x (y > x) je nepravda (neexistuje číslo větší než všechna).

### 12.6 Prázdné případy

- ∀x ∈ ∅ φ(x) je **vždy pravdivé** (není co porušit).
- ∃x ∈ ∅ φ(x) je **vždy nepravdivé** (není co vybrat).
- Proto je prázdná relace symetrická, antisymetrická, tranzitivní i ireflexivní, a relace {\[1,2\]} je tranzitivní (neexistuje navazující dvojice, takže není co ověřovat).

### 12.7 Pravidla pro vedení důkazu

| Cíl nebo situace | Co udělat |
| --- | --- |
| **Dokázat ∀x φ(x)** | Napsat „Nechť x je libovolné.“ Dokázat φ(x) bez dalších předpokladů o x. Žádná konkrétní hodnota. |
| **Dokázat ∃x φ(x)** | Najít konkrétního svědka a ověřit, že pro něj φ platí. (U složení: svědek je prostřední prvek y.) |
| **Použít předpoklad ∀x φ(x)** | Dosadit do něj libovolný konkrétní prvek, který potřebuješ (instanciace). |
| **Použít předpoklad ∃y φ(y)** | Napsat „Nechť y je takový prvek.“ Je pevné, ale neznámé. Nesmí mít jméno, které už v důkazu jinak existuje. |
| **Vyvrátit ∀x φ(x)** | Najít jeden protipříklad (viz negace v 12.2). |
| **Vyvrátit ∃x φ(x)** | Dokázat ∀x ¬φ(x). |
| **Z φ(a) odvodit ∃x φ(x)** | Zavedení ∃: konkrétní prvek a je svědkem. |
| **Dokázat ∀x (p ⇒ q)** | Zvolit libovolné x, **předpokládat p**, odvodit q. |

## 13. Definice pro důkazy z 5. sady

Všechny důkazy z úloh 10 a 11 se dělají tak, že se definice rozepíše do logiky (jako v kapitole 1) a pak se použijí zákony z kapitol 2 až 12. Proto je potřeba znát přesné znění definic.

### 13.1 Relace a operace s nimi

| Pojem | Definice (logický zápis) |
| --- | --- |
| **Relace R** (z A do B) | R ⊆ A × B, a xRy ⇔ \[x,y\] ∈ R |
| **Rovnost relací** | R = S ⇔ ∀x, y: (\[x,y\] ∈ R ⇔ \[x,y\] ∈ S) |
| **Inkluze relací** | R ⊆ S ⇔ ∀x, y: (\[x,y\] ∈ R ⇒ \[x,y\] ∈ S) |
| **Sjednocení / průnik** | \[x,y\] ∈ R ∪ S ⇔ \[x,y\] ∈ R ∨ \[x,y\] ∈ S; průnik analogicky s ∧ |
| **Rozdíl** | \[x,y\] ∈ R \\ S ⇔ \[x,y\] ∈ R ∧ \[x,y\] ∉ S |
| **Doplněk R̄** (vůči univerzu A × B) | \[x,y\] ∈ R̄ ⇔ \[x,y\] ∉ R |
| **Inverzní relace R⁻¹** | \[x,y\] ∈ R⁻¹ ⇔ \[y,x\] ∈ R |
| **Složení R ∘ S** (podle sbírky: nejdřív S, potom R) | \[x,z\] ∈ R ∘ S ⇔ ∃y: \[x,y\] ∈ S ∧ \[y,z\] ∈ R |
| **Sjednocení systému ⋃ Sᵢ** (i ∈ I) | \[x,y\] ∈ ⋃ Sᵢ ⇔ ∃i ∈ I: \[x,y\] ∈ Sᵢ |
| **Průnik systému ⋂ Sᵢ** (i ∈ I) | \[x,y\] ∈ ⋂ Sᵢ ⇔ ∀i ∈ I: \[x,y\] ∈ Sᵢ |
| **Mocnina Rⁿ** | R¹ = R, Rⁿ⁺¹ = R ∘ Rⁿ |
| **Tranzitivní uzávěr R⁺** | R⁺ = R ∪ R² ∪ R³ ∪ …, tedy \[a,b\] ∈ R⁺ ⇔ ∃n ≥ 1: \[a,b\] ∈ Rⁿ |

Pozor na tři věci:

1. Při skládání dává **složení pořadí zprava doleva**. Kdo zamění R a S, dostane špatný důkaz i špatný výsledek.
2. Doplněk má smysl jen vzhledem k předem danému univerzu. U relace R ⊆ A × B je to A × B.
3. Rovnost relací se dokazuje stejně jako rovnost množin, jen prvky jsou dvojice.

### 13.2 Vlastnosti relace na množině M (s kvantifikátory)

| Vlastnost | Definice |
| --- | --- |
| Reflexivní | ∀x ∈ M: xRx |
| Ireflexivní | ∀x ∈ M: ¬(xRx) |
| Symetrická | ∀x, y ∈ M: (xRy ⇒ yRx) |
| Antisymetrická | ∀x, y ∈ M: (xRy ∧ yRx ⇒ x = y) |
| Tranzitivní | ∀x, y, z ∈ M: (xRy ∧ yRz ⇒ xRz) |
| Ekvivalence | reflexivní ∧ symetrická ∧ tranzitivní |
| Uspořádání | reflexivní ∧ antisymetrická ∧ tranzitivní |
| Třída ekvivalence prvku a | \[a\] = {x ∈ M : xRa} |
| Rozklad M | systém množin Bᵢ ⊆ M, kde Bᵢ ≠ ∅, Bᵢ ∩ Bⱼ = ∅ pro i ≠ j a ⋃ Bᵢ = M |
| Supremum a ∨ b | nejmenší prvek mezi horními závorami a i b (jedinečný) |
| Infimum a ∧ b | největší prvek mezi dolními závorami a i b (jedinečný) |
| Svazově uspořádaná množina | uspořádaná množina, kde ∀a, b ∃ supremum i infimum |

### 13.3 Zobrazení (úlohy 27 až 29)

| Pojem | Definice |
| --- | --- |
| **Zobrazení f z A do B** | relace f ⊆ A × B, pro kterou ∀x ∈ A ∃!y ∈ B: \[x,y\] ∈ f |
| **Obraz množiny C ⊆ A** | f(C) = {y : ∃x ∈ C: \[x,y\] ∈ f} |
| **Vzor množiny D ⊆ B** | f⁻¹(D) = {x ∈ A : ∃y ∈ D: \[x,y\] ∈ f}, u zobrazení tedy {x : f(x) ∈ D} |
| **Prosté** (injekce) | ∀x₁, x₂: f(x₁) = f(x₂) ⇒ x₁ = x₂ |
| **Na** (surjekce) | ∀y ∈ B ∃x ∈ A: f(x) = y |
| **Vzájemně jednoznačné** (bijekce) | prosté a na |

Zobrazení musí mít **každý prvek A jako první složku právě jedné dvojice**. Právě proto selže relace x² + y² = 1 na ℝ: pro x = 0 vychází y = 1 i y = −1, a pro x = 2 nevychází žádné y.

## 14. Šablony důkazů a vzorové důkazy

### 14.1 Tři šablony

**A) Rovnost relací R = S (dvěma inkluzemi):**

1. (⊆) Nechť \[x,z\] ∈ R je libovolná dvojice. Rozepiš definici, upravuj řetězem implikací (kapitoly 2 až 9 a 12) a dojdi k \[x,z\] ∈ S.
2. (⊇) Totéž opačně.
3. Závěr: R = S.

Pokud je každý krok ekvivalence (⇔), stačí jeden řetěz a obě inkluze naráz. Řetěz ⇔ ale používej jen tehdy, když jsi u každého kroku jistý, že platí oběma směry.

**B) Inkluze R ⊆ S:** jen první polovina šablony A. Používá se u úlohy 11 (a), (b), (c).

**C) Důkaz, že inkluze neplatí oběma směry (protipříklad):** zvol malé konkrétní relace (několik dvojic), spočítej obě strany a ukaž dvojici, která je na jedné straně a na druhé ne.

### 14.2 Co použít kde (nápověda k úloze 10 a 11)

| Úloha | Klíčové pravidlo |
| --- | --- |
| 10 (a) složení a sjednocení | ∃ se rozdělí přes ∨ (12.3), distributivita (kap. 2) |
| 10 (b) inverze složení | přejmenování y, komutativita ∧ (kap. 4), definice R⁻¹ |
| 10 (c) inverze rozdílu | definice R⁻¹ a rozdílu, žádné kvantifikátory |
| 10 (d) doplněk a inverze, dvojitá inverze | definice R̄ a R⁻¹, ¬¬p ⇔ p (kap. 6) |
| 10 (e) systém relací | zaměnění ∃y a ∃i (12.5), definice ⋃ |
| 11 (a), (b) průnik | ∃ nad ∧ jde jen jedním směrem (12.3) |
| 11 (c) rozdíl složení | negace ∃ (12.2) a instanciace (12.7) |

### 14.3 Vzorový důkaz 10 (b): (R ∘ S)⁻¹ = S⁻¹ ∘ R⁻¹

Každý krok je ekvivalence, takže stačí jeden řetěz. Nechť \[x,z\] je libovolná dvojice.

| Krok | Tvrzení | Důvod |
| --- | --- | --- |
| 1 | \[x,z\] ∈ (R ∘ S)⁻¹ |  |
| 2 | \[z,x\] ∈ R ∘ S | definice inverze |
| 3 | ∃y: \[z,y\] ∈ S ∧ \[y,x\] ∈ R | definice složení |
| 4 | ∃y: \[y,z\] ∈ S⁻¹ ∧ \[x,y\] ∈ R⁻¹ | definice inverze (dvakrát) |
| 5 | ∃y: \[x,y\] ∈ R⁻¹ ∧ \[y,z\] ∈ S⁻¹ | komutativita ∧ |
| 6 | \[x,z\] ∈ S⁻¹ ∘ R⁻¹ | definice složení (nejdřív R⁻¹, potom S⁻¹) |

### 14.4 Vzorový důkaz 10 (c): (R \\ S)⁻¹ = R⁻¹ \\ S⁻¹

| Krok | Tvrzení | Důvod |
| --- | --- | --- |
| 1 | \[x,y\] ∈ (R \\ S)⁻¹ |  |
| 2 | \[y,x\] ∈ R \\ S | definice inverze |
| 3 | \[y,x\] ∈ R ∧ \[y,x\] ∉ S | definice rozdílu |
| 4 | \[x,y\] ∈ R⁻¹ ∧ \[x,y\] ∉ S⁻¹ | definice inverze (dvakrát) |
| 5 | \[x,y\] ∈ R⁻¹ \\ S⁻¹ | definice rozdílu |

### 14.5 Vzorový důkaz 10 (e), první rovnost: R ∘ (⋃ Sᵢ) = ⋃ (R ∘ Sᵢ)

| Krok | Tvrzení | Důvod |
| --- | --- | --- |
| 1 | \[x,z\] ∈ R ∘ (⋃ Sᵢ) |  |
| 2 | ∃y: \[x,y\] ∈ ⋃ Sᵢ ∧ \[y,z\] ∈ R | definice složení |
| 3 | ∃y: (∃i: \[x,y\] ∈ Sᵢ) ∧ \[y,z\] ∈ R | definice ⋃ |
| 4 | ∃y ∃i: \[x,y\] ∈ Sᵢ ∧ \[y,z\] ∈ R | i se v druhém členu nevyskytuje, lze ho vytknout (12.4) |
| 5 | ∃i ∃y: \[x,y\] ∈ Sᵢ ∧ \[y,z\] ∈ R | zaměnění stejných kvantifikátorů (12.5) |
| 6 | ∃i: \[x,z\] ∈ R ∘ Sᵢ | definice složení |
| 7 | \[x,z\] ∈ ⋃ (R ∘ Sᵢ) | definice ⋃ |

### 14.6 Vzorový důkaz 11 (a): R ∘ (S₁ ∩ S₂) ⊆ R ∘ S₁ ∩ R ∘ S₂

Nechť \[x,z\] ∈ R ∘ (S₁ ∩ S₂). Pak existuje y s \[x,y\] ∈ S₁ ∩ S₂ a \[y,z\] ∈ R, tedy \[x,y\] ∈ S₁ ∧ \[x,y\] ∈ S₂ ∧ \[y,z\] ∈ R. **Stejné y** ukazuje, že \[x,z\] ∈ R ∘ S₁ a zároveň \[x,z\] ∈ R ∘ S₂. To je \[x,z\] ∈ R ∘ S₁ ∩ R ∘ S₂.

**Protipříklad pro opačný směr.** Nechť S₁ = {\[1,2\]}, S₂ = {\[1,3\]}, R = {\[2,4\], \[3,4\]}.

- S₁ ∩ S₂ = ∅, takže R ∘ (S₁ ∩ S₂) = ∅.
- R ∘ S₁ = {\[1,4\]} (přes y = 2) a R ∘ S₂ = {\[1,4\]} (přes y = 3), jejich průnik je {\[1,4\]}.

Pravá strana obsahuje \[1,4\], levá ne, rovnost neplatí. Dvojici \[1,4\] zde svědčí **různá y** (2 pro S₁ a 3 pro S₂), což je přesně slabina z 12.3.

### 14.7 Vzorový důkaz 11 (c): R ∘ S₁ \\ R ∘ S₂ ⊆ R ∘ (S₁ \\ S₂)

Nechť \[x,z\] ∈ R ∘ S₁ \\ R ∘ S₂, tedy \[x,z\] ∈ R ∘ S₁ a \[x,z\] ∉ R ∘ S₂.

1. Z \[x,z\] ∈ R ∘ S₁ plyne: nechť y je takový prvek, že \[x,y\] ∈ S₁ a \[y,z\] ∈ R (eliminace ∃, 12.7).
2. Z \[x,z\] ∉ R ∘ S₂ plyne po negaci ∃ (12.2): ∀t: ¬(\[x,t\] ∈ S₂ ∧ \[t,z\] ∈ R).
3. Dosadíme t = y (instanciace). Protože \[y,z\] ∈ R, musí platit \[x,y\] ∉ S₂.
4. Tedy \[x,y\] ∈ S₁ \\ S₂ a \[y,z\] ∈ R, což je \[x,z\] ∈ R ∘ (S₁ \\ S₂).

**Protipříklad pro opačný směr.** Nechť S₁ = {\[1,2\], \[1,3\]}, S₂ = {\[1,3\]}, R = {\[2,4\], \[3,4\]}. Pak S₁ \\ S₂ = {\[1,2\]} a R ∘ (S₁ \\ S₂) = {\[1,4\]}. Ale R ∘ S₁ = {\[1,4\]} a R ∘ S₂ = {\[1,4\]}, takže jejich rozdíl je prázdný. Dvojice \[1,4\] je na pravé straně a na levé ne.

### 14.8 Kontrolní seznam před odevzdáním důkazu

1. Je zřejmé, co je dokazováno (rovnost nebo jen inkluze)? U rovnosti jsou obě inkluze?
2. Je u každého kroku uveden **důvod** (definice nebo zákon z této sbírky)?
3. Je složení psáno ve správném pořadí (nejdřív druhá relace)?
4. Nezaměňují se kvantifikátory jiného druhu (∃ a ∀) a nerozdělují se ∃ přes ∧ nebo ∀ přes ∨ oběma směry?
5. Je „libovolné“ x skutečně libovolné, tedy nebylo mu mezitím přiřazeno konkrétní číslo?
6. U tvrzení „neplatí“ je uveden **konkrétní protipříklad**, u kterého je spočtena každá strana zvlášť?
