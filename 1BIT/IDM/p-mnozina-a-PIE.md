# Potenční množina a princip inkluze a exkluze (PIE)

Studijní materiál k sadě 04, příklady 1 až 11. Dirichletův princip (příklady 12 až 15) tu není.

## 1. Potenční množina

### Definice a základní fakta

Potenční množina P(A) je množina **všech podmnožin** množiny A.

- X ∈ P(A) ⇔ X ⊆ A.
- |P(A)| = 2^|A|. Každý prvek buď do podmnožiny patří, nebo ne, takže máme 2 · 2 · … · 2 možností.
- ∅ ∈ P(A) a A ∈ P(A) platí **vždy**, pro každou množinu A.
- P(∅) = {∅}. Ta má 1 prvek, ne 0.

### Hlavní past: ∈ versus ⊆

Prvky množiny P(A) jsou **množiny**. Proto platí:

- {5} ∈ P(M) znamená totéž co {5} ⊆ M, tedy 5 ∈ M.
- {{5}} ⊆ P(M) znamená, že {5} ∈ P(M), tedy opět 5 ∈ M.
- {∅} ∈ P(M) znamená {∅} ⊆ M, tedy ∅ ∈ M. (Pozor, prvkem M je prázdná množina, ne „nic“.)

### Jak vypisovat prvky P(A)

Postupuj podle **velikosti podmnožin**, abys na žádnou nezapomněl:

1. podmnožina velikosti 0: ∅,
2. velikosti 1: jednoprvkové,
3. velikosti 2, a tak dále, až celá množina A.

Kontrola: počet vypsaných musí být 2^|A|. Počty podle velikosti odpovídají kombinačním číslům, pro |A| = 3 je to 1, 3, 3, 1.

Pokud jsou prvky A samy množiny (příklad 1c), **obal každý prvek do složených závorek jako celek**. Pro A = {{⋆}, {1,2}, ∆} jsou prvky a = {⋆}, b = {1,2}, c = ∆. Vypiš podmnožiny množiny {a, b, c} a pak za a, b, c dosaď zpět. Například podmnožina {a} je {{⋆}}, podmnožina {a, c} je {{⋆}, ∆}.

### Užitečné vztahy

- P(A) ∩ P(B) = P(A ∩ B).
- P(A) ∪ P(B) ⊆ P(A ∪ B), ale rovnost **obecně neplatí**. Příklad: A = {1}, B = {2}. Pak {1,2} ∈ P(A ∪ B), ale {1,2} ∉ P(A) ∪ P(B).
- A ⊆ B ⇔ P(A) ⊆ P(B).

### Vzorové příklady

**Příklad 2: |P(M)| = 4, {{5}} ⊆ P(M), {∅} ∈ P(M). Určete M.**

1. 2^|M| = 4, takže |M| = 2.
2. {{5}} ⊆ P(M) dává {5} ∈ P(M), tedy 5 ∈ M.
3. {∅} ∈ P(M) dává ∅ ∈ M.
4. M má právě dva prvky, a to 5 a ∅. Tedy **M = {∅, 5}**.

**Příklad 3: |P(P(P(∅)))|.**

Postupuj zevnitř. P(∅) = {∅} má 1 prvek. P(P(∅)) má 2^1 = 2 prvky. P(P(P(∅))) má 2^2 = **4** prvky.

**Příklad 4: platí P(A \\ B) = P(A) \\ P(B)?**

Neplatí. Doporučený postup je najít protipříklad a ověřit obě inkluze. Vezmi A = {1,2}, B = {2}.

- A \\ B = {1}, tedy P(A \\ B) = {∅, {1}}.
- P(A) = {∅, {1}, {2}, {1,2}}, P(B) = {∅, {2}}, tedy P(A) \\ P(B) = {{1}, {1,2}}.
- Inkluze ⊆ neplatí: ∅ ∈ P(A \\ B), ale ∅ ∉ P(A) \\ P(B).
- Inkluze ⊇ neplatí: {1,2} ∈ P(A) \\ P(B), ale {1,2} ∉ P(A \\ B).

Obecné vysvětlení: prázdná množina je v P(A \\ B) vždy, ale v P(A) \\ P(B) nikdy, protože je v P(B). Proto ⊆ neplatí nikdy. P(A) \\ P(B) obsahuje podmnožiny A, které nejsou podmnožinami B. Ty mohou obsahovat prvky z B, takže nemusí ležet v A \\ B.

## 2. Princip inkluze a exkluze

### Vzorce

Dvě množiny: |A ∪ B| = |A| + |B| − |A ∩ B|.

Tři množiny: |A ∪ B ∪ C| = |A| + |B| + |C| − |A ∩ B| − |A ∩ C| − |B ∩ C| + |A ∩ B ∩ C|.

Čtyři množiny: + jednotlivé (4 členy), − dvojité (6 členů), + trojité (4 členy), − čtyřnásobný (1 člen).

Obecně: znaménko u k-násobných průniků je (−1)^(k+1) a počet členů je C(n, k).

**Verze s doplňkem** (to, co zůstane po vyškrtání):

|U \\ (A₁ ∪ … ∪ Aₙ)| = |U| − |sjednocení|.

### Počet násobků v intervalu

- Počet násobků čísla x v {1, …, N} je ⌊N / x⌋.
- Počet násobků x v intervalu \[a, b\] je ⌊b / x⌋ − ⌊(a−1) / x⌋.
- Průnik násobků x a y je množina násobků **nsn(x, y)**, ne součinu. Například násobky 4 i 6 jsou násobky 12, ne 24.
- Pro více čísel: průnik je množina násobků nsn všech zúčastněných čísel.

### Zkratka 1: vyřaď čísla, která jsou násobkem jiného

Pokud je číslo y násobkem čísla x, pak A\_y ⊆ A\_x, takže A\_y můžeš z výpočtu úplně vynechat. Příspěvky takového čísla se v PIE vzájemně vyruší. Tím se často zmenší tři množiny na dvě.

Pozor, vyřadit lze jen číslo, které je násobkem **jednoho** z ostatních. Například 6 nelze vyřadit kvůli tomu, že 6 = nsn(2, 3).

### Zkratka 2: periodicita pro nesoudělná čísla

Pokud jsou čísla navzájem nesoudělná (například 2, 3, 5, 7), je jejich nsn rovno součinu M = 210 a vzor škrtání se opakuje po každých M číslech. V jednom bloku zůstane M · (1 − 1/2)(1 − 1/3)(1 − 1/5)(1 − 1/7) = 48 čísel. Celé bloky tedy započítáš násobením a zbytek dopočítáš zvlášť (nebo klasickým PIE).

### Vzorové příklady (příklad 5)

Ve všech případech počítáme, kolik čísel z 1, …, 1000 **zůstane**, tedy 1000 − |sjednocení|.

**5a) čísla 2, 6, 18.** Násobky 6 i 18 jsou násobky 2. Zbývá jen 2: 1000 − 500 = **500**.

**5b) čísla 4, 6, 32.** Násobky 32 jsou násobky 4, takže zbývají 4 a 6. |A₄| = 250, |A₆| = 166, |A₄ ∩ A₆| = |A₁₂| = 83. Sjednocení: 250 + 166 − 83 = 333. Zbyde 1000 − 333 = **667**.

**5c) čísla 5, 18, 30.** Násobky 30 jsou násobky 5, takže zbývají 5 a 18. |A₅| = 200, |A₁₈| = 55, nsn(5, 18) = 90, takže |A₉₀| = 11. Sjednocení: 200 + 55 − 11 = 244. Zbyde 1000 − 244 = **756**.

**5d) čísla 2, 6, 15.** Násobky 6 jsou násobky 2, takže zbývají 2 a 15. |A₂| = 500, |A₁₅| = 66, nsn(2, 15) = 30, takže |A₃₀| = 33. Sjednocení: 500 + 66 − 33 = 533. Zbyde 1000 − 533 = **467**.

**5e) čísla 2, 3, 5, 7.** Čísla jsou nesoudělná, použij periodicitu. Jeden blok 210 čísel dá 48 zbylých. Platí 1000 = 4 · 210 + 160, takže 4 · 48 = 192 plus počet zbylých v 1, …, 160. Zbylá čísla v 1, …, 160 jsou 1, prvočísla od 11 do 157 a složená čísla složená jen z prvočísel ≥ 11 (nejmenší je 11² = 121). Dopočet dá 36, celkem 192 + 36 = **228**. Alternativně použij plný PIE se čtyřmi množinami (15 členů) a dostaneš totéž.

### Čísla bez čtvercového (kubického) dělitele (příklady 6 a 7)

Zadání: kolik čísel n < 100 není dělitelných druhou (třetí) mocninou žádného čísla většího než 1. Čísla n < 100 jsou 1, …, 99, tedy N = 99.

**Klíčová úvaha:** stačí vyloučit dělitelnost mocninami **prvočísel**. Je-li n dělitelné k², kde k > 1, pak je dělitelné i p², kde p je prvočíselný dělitel k.

**Příklad 6 (druhé mocniny).** Prvočíselné čtverce ≤ 99: 4, 9, 25, 49.

- |A₄| = 24, |A₉| = 11, |A₂₅| = 3, |A₄₉| = 2.
- Průniky: 4 a 9 dávají nsn 36, takže ⌊99/36⌋ = 2. Ostatní dvojice mají nsn ≥ 100 (4 · 25 = 100, 4 · 49 = 196, 9 · 25 = 225, …), tedy 0.
- Sjednocení: 24 + 11 + 3 + 2 − 2 = 38.
- Výsledek: 99 − 38 = **61**.

**Příklad 7 (třetí mocniny).** Prvočíselné krychle ≤ 99: 8, 27 (další 125 je moc velké).

- |A₈| = 12, |A₂₇| = 3, nsn = 216 > 99, takže průnik 0.
- Sjednocení: 15. Výsledek: 99 − 15 = **84**.

### Permutace s vynechanými písmeny (příklady 8 až 11)

**Zadání:** Máme 16 různých písmen. Kolik pořadí (permutací) je takových, že z nich nelze vynecháním některých písmen dostat žádné z daných slov? Tedy žádné ze slov není **podposloupností** permutace (písmena slova jsou v permutaci ve stejném pořadí, ne nutně těsně za sebou).

**Základní fakt:** Pokud je dáno m konkrétních písmen, počet permutací 16 písmen, ve kterých jsou tato písmena v jednom předepsaném pořadí, je **16! / m!**. Všech m! pořadí těchto písmen je stejně pravděpodobných.

**Postup:**

1. Označ A\_i množinu permutací, ve kterých se i-té slovo vyskytuje jako podposloupnost.
2. |A\_i| = 16! / (počet písmen slova i)!.
3. U průniku A\_i ∩ A\_j sjednoť písmena obou slov (sdílená písmena počítej **jednou**). Zjisti, kolik pořadí těchto písmen vyhovuje oběma požadavkům současně. Označme to e a počet sjednocených písmen m. Pak |A\_i ∩ A\_j| = e · 16! / m!.
4. Výsledek je 16! − |A₁ ∪ A₂| = 16! − |A₁| − |A₂| + |A₁ ∩ A₂|.

**Pozor na rozpory:** pokud slova na sdílených písmenech vyžadují protichůdné pořadí, je průnik **prázdný**.

**Příklad 8: DEN, NOC.** |A\_DEN| = |A\_NOC| = 16!/3!. Sdílené písmeno je N. Z D < E < N a N < O < C plyne D < E < N < O < C, což je jediné pořadí 5 písmen, takže e = 1 a |průnik| = 16!/5!.

Výsledek: **16! − 2 · 16!/3! + 16!/5!**.

**Příklad 9: HOP, PONK.** |A\_HOP| = 16!/3!, |A\_PONK| = 16!/4!. Slovo HOP chce O před P, slovo PONK chce P před O. To je spor, takže průnik je prázdný.

Výsledek: **16! − 16!/3! − 16!/4!**.

**Příklad 10: BOK, MONK.** |A\_BOK| = 16!/3!, |A\_MONK| = 16!/4!. Sdílená písmena O a K. Z B < O < K a M < O < N < K plyne, že B a M jsou před O (v libovolném pořadí), pak O, N, K. Sjednocených písmen je 5 (B, M, O, N, K) a vyhovují 2 pořadí (B před M, nebo M před B). Takže e = 2 a |průnik| = 2 · 16!/5!.

Výsledek: **16! − 16!/3! − 16!/4! + 2 · 16!/5!**.

**Příklad 11: HLOD, HOP.** |A\_HLOD| = 16!/4!, |A\_HOP| = 16!/3!. Sdílená písmena H a O. Z H < L < O < D a H < O < P plyne H < L < O, a pak D a P jsou za O v libovolném pořadí. Sjednocených písmen je 5 (H, L, O, D, P) a vyhovují 2 pořadí, takže |průnik| = 2 · 16!/5!.

Výsledek: **16! − 16!/3! − 16!/4! + 2 · 16!/5!**.

## 3. Jak poznat typ příkladu

| Zadání | Postup |
| --- | --- |
| Vypiš prvky P(A) | podmnožiny podle velikosti, kontrola počtu 2^n |
| Urči M z podmínek na P(M) |  |
| P(P(…)) | postupně zevnitř: 2^(předchozí počet) |
| Platí rovnost množin s P? | zkus malé množiny, ověř obě inkluze, vždy zvaž ∅ |
| Kolik čísel zůstane po vyškrtnutí násobků | doplněk k PIE, nejdřív vyřaď násobky jiných čísel |
| Čísla bez čtvercového (kubického) dělitele | PIE na prvočíselné čtverce (krychle) |
| Permutace, kde se nevyskytuje žádné slovo | PIE, |

## 4. Kontrolní seznam před odevzdáním

1. Je každý násobek něčeho jiného ze zadání? Vyřaď ho.
2. Použil jsem **nsn**, ne součin?
3. Počítám správný interval? U „n < 100“ je to 1 až 99.
4. Střídají se znaménka (+, −, +, −)?
5. Odpovídá počet členů v každé sumě kombinačnímu číslu C(n, k)?
6. U permutací: spor v pořadí? Kolik pořadí splňuje obě slova? Počítám sdílená písmena jen jednou?
7. Končím odečtením od celku (1000, 99, 16!), pokud se ptají na to, co **zůstane**?
