Generated with Claude Sonnet 5.5

# Relace: vlastnosti, ekvivalence a uspořádání

Studijní materiál k sadě úloh o relacích. Cíl: umět každou vlastnost **rozpoznat**, **dokázat** nebo **vyvrátit** a vědět, jak postupovat u typových zadání.

## 1. Základní pojmy

**Relace R na množině M** je libovolná podmnožina kartézského součinu M × M. Zápis xRy znamená totéž co \[x, y\] ∈ R.

Relaci lze zadat třemi způsoby a je dobré umět je mezi sebou převádět:

- **výčtem dvojic**: R = {\[1,1\], \[1,2\], \[2,1\]},
- **grafem se šipkami**: prvky jsou vrcholy, dvojice \[a, b\] je šipka a → b, dvojice \[a, a\] je smyčka,
- **tabulkou**: řádek = první prvek, sloupec = druhý prvek, na průsečíku je 1 nebo 0.

Pro úlohy je graf se šipkami nejpraktičtější, protože většinu vlastností z něj poznáš na první pohled.

**Slovníček (česky / slovensky ve sbírce):** uspořádání / usporiadanie, rozklad / rozklad, uzávěr / uzáver, zachovává / zachováva, svaz (zväz), svazově uspořádaná množina / zväzovo usporiadaná množina, tranzitivní / tranzitívna, reflexivní / reflexívna.

## 2. Pět základních vlastností

| Vlastnost | Definice | Jak ji poznáš v grafu | Jak ji vyvrátíš (stačí jeden případ) |
| --- | --- | --- | --- |
| **Reflexivní** | ∀x ∈ M: xRx | smyčka u každého vrcholu | najdi a, pro které \[a,a\] ∉ R |
| **Ireflexivní** | ∀x ∈ M: ¬(xRx) | žádná smyčka | najdi a, pro které \[a,a\] ∈ R |
| **Symetrická** | xRy ⇒ yRx | každá šipka má šipku zpět | najdi \[a,b\] ∈ R, ale \[b,a\] ∉ R |
| **Antisymetrická** | (xRy ∧ yRx) ⇒ x = y | mezi dvěma různými vrcholy nikdy šipky oběma směry | najdi a ≠ b s \[a,b\] ∈ R i \[b,a\] ∈ R |
| **Tranzitivní** | (xRy ∧ yRz) ⇒ xRz | ke každé cestě a → b → c existuje zkratka a → c | najdi \[a,b\], \[b,c\] ∈ R, ale \[a,c\] ∉ R |

### Pasti, které se opakují

1. **Reflexivní a ireflexivní nejsou protiklady.** Relace může mít smyčky jen u části prvků, a pak není ani jedna. Příklad (úl. 4c): R = {\[1,1\]} na M = {1,2,3,4} není reflexivní (chybí \[2,2\]) a není ireflexivní (má \[1,1\]). Je přitom tranzitivní.
2. **Symetrická a antisymetrická nejsou protiklady.** Identita {\[x,x\]} je obojí. Relace {\[1,2\],\[2,1\],\[1,3\]} není ani jedno: \[1,3\] nemá zpětnou šipku a dvojice 1, 2 jde oběma směry.
3. **Implikace s nesplněným předpokladem platí automaticky.** Relace R = {\[1,2\]} je tranzitivní, protože neexistuje cesta o dvou šipkách, takže není co ověřovat. Stejně je tranzitivní prázdná relace. Proto R ∘ R = ∅ ≠ R (úl. 8, 9).
4. **Tranzitivita zahrnuje i případ x = z.** Relace {\[1,2\],\[2,1\]} je symetrická, ale není tranzitivní: z 1R2 a 2R1 plyne 1R1, které chybí (úl. 6).
5. **Antisymetrie neříká „šipky nejsou oboustranné“ obecně**, jen mezi *různými* prvky. Smyčky \[a,a\] antisymetrii nevadí.

## 3. Jak vlastnosti ověřovat

### 3.1 Konečná relace (výčet)

- **Reflexivita:** projdi všechny prvky M a pro každý hledej \[a,a\]. Pozor na prvky, které se v R vůbec nevyskytují (například 4 v úl. 15).
- **Symetrie:** pro každou dvojici \[a,b\] hledej \[b,a\].
- **Antisymetrie:** hledej dvojici různých prvků a ≠ b, která jde oběma směry. Když žádná není, je relace antisymetrická.
- **Tranzitivita:** pro každou dvojici \[a,b\] projdi všechny dvojice \[b,c\], které na ni navazují, a ověř, že \[a,c\] ∈ R. Dělej to systematicky podle prvního prvku, jinak snadno nějakou cestu přehlédneš.

**Vzorový příklad (úl. 15).** M = {1,2,3,4}, R = {\[1,1\],\[1,2\],\[2,1\],\[2,2\],\[2,3\],\[3,2\],\[3,3\]}.

- reflexivní? Ne, chybí \[4,4\].
- symetrická? Ano: \[1,2\]↔\[2,1\], \[2,3\]↔\[3,2\], smyčky jsou samy sobě zpětné.
- tranzitivní? Ne: 1R2 a 2R3, ale \[1,3\] ∉ R.
- Závěr: **není ekvivalence**, a proto se hledají uzávěry (viz kapitola 4).

### 3.2 Relace na nekonečné množině (podmínka)

Tady nelze vypisovat. Platí pravidlo:

- **Vlastnost dokazuješ obecně** pro libovolné prvky.
- **Vlastnost vyvracíš jedním konkrétním protipříkladem.**

**Šablona důkazu tranzitivity:** Nechť x, y, z jsou libovolné a platí xRy a yRz. Ukážeme, že platí xRz. (Rozepíšu definici relace, spojím obě podmínky a dostanu podmínku pro dvojici x, z.)

**Vzorové příklady (úl. 16, relace na ℝ):**

- **x/y = 1.** Reflexivita selže pro x = 0, protože výraz 0/0 není definovaný. Není to ekvivalence.
- **|x − y| ≤ 1.** Reflexivní a symetrická ano, tranzitivní ne. Protipříklad: x = 0, y = 1, z = 2. Platí |0−1| ≤ 1 a |1−2| ≤ 1, ale |0−2| = 2 > 1. Není to ekvivalence.
- **|x| = |y|.** Reflexivita: |x| = |x|. Symetrie: z |x| = |y| plyne |y| = |x|. Tranzitivita: z |x| = |y| a |y| = |z| plyne |x| = |z|. Je to ekvivalence, třídy jsou dvojice {x, −x}.
- **x³ = y³.** Platí právě tehdy, když x = y (třetí mocnina je prostá). Relace je tedy identita, což je ekvivalence s jednoprvkovými třídami.

**Úl. 17 (a \~ b ⇔ 10a + b je prvočíslo):** reflexivita selže u a = 0, protože 00 = 0 není prvočíslo. Symetrie také selže: 2 \~ 3 (číslo 23 je prvočíslo), ale 3 \~ 2 ne (32 je sudé). Není to ekvivalence.

## 4. Uzávěry relace

**Uzávěr** relace R vůči vlastnosti je *nejmenší* relace, která R obsahuje a danou vlastnost má. Nejmenší znamená: přidáš jen to, co je nutné.

| Uzávěr | Konstrukce |
| --- | --- |
| **Reflexivní** ρ(R) | R ∪ {\[x,x\] : x ∈ M} |
| **Symetrický** | R ∪ R⁻¹ |
| **Tranzitivní** R⁺ | R ∪ R² ∪ R³ ∪ … = všechny dvojice \[a,b\], pro které v grafu vede cesta z a do b o aspoň jedné šipce |

Poznámky:

- R⁺ = R právě tehdy, když je R tranzitivní. Proto S = {\[1,2\]} splňuje S⁺ = S (úl. 7) a S = {\[1,2\],\[2,1\]} splňuje S⁺ ≠ S (úl. 6), protože S⁺ přidá \[1,1\] a \[2,2\].
- Dvojice \[x,x\] leží v R⁺ jen tehdy, když x leží na nějakém cyklu.
- Ekvivalenční uzávěr získáš tak, že přidáš symetrii, pak tranzitivitu a nakonec smyčky.

**Vzorový příklad (úl. 5).** R = {(1,3),(2,3),(3,4),(3,1),(4,2)}. V grafu vede cesta 1 → 3 → 4 → 2 → 3 → 1, takže se z každého z prvků 1, 2, 3, 4 dostaneš do každého (včetně sebe samého). Proto R⁺ = {1,2,3,4} × {1,2,3,4}, tedy všech 16 dvojic.

**Pokračování úl. 15.** ρ(R) = R ∪ {\[4,4\]}. R⁺ = R ∪ {\[1,3\],\[3,1\]}, symetrický uzávěr je R samotná. Ekvivalenční uzávěr je R ∪ {\[4,4\],\[1,3\],\[3,1\]}, který určuje rozklad {{1,2,3},{4}}.

## 5. Ekvivalence a rozklady

**Ekvivalence** je relace, která je **reflexivní, symetrická a tranzitivní.** Zapamatuj si zkratku **RST**.

**Třída ekvivalence** prvku a je množina \[a\] = {x : xRa}, tedy všechno, co je „stejné jako a“.

**Rozklad** množiny M je systém podmnožin (bloků), které jsou neprázdné, po dvou disjunktní a jejich sjednocení je celé M.

**Hlavní věta:** ekvivalence na M a rozklady M si jednoznačně odpovídají.

- Ekvivalence → rozklad: bloky jsou třídy ekvivalence.
- Rozklad → ekvivalence: \[x,y\] ∈ E ⇔ x a y leží ve stejném bloku.

**Úl. 14b.** Rozklad {{a},{b,c},{d}} dává E = {\[a,a\],\[b,b\],\[c,c\],\[d,d\],\[b,c\],\[c,b\]}. Každý blok přispěje všemi dvojicemi svých prvků (včetně dvojic \[x,x\]).

**Úl. 12 (všechny rozklady množiny {1,2,3,4}).** Systematicky podle tvaru bloků:

| Tvar bloků | Počet rozkladů |
| --- | --- |
| jeden blok 4 | 1 |
| bloky 3 + 1 | 4 |
| bloky 2 + 2 | 3 |
| bloky 2 + 1 + 1 | 6 |
| bloky 1 + 1 + 1 + 1 | 1 |
| **celkem** | **15** |

**Úl. 13 (rozklady ℤ).** Nejznámější je rozklad podle zbytku po dělení n: pro n = 3 jsou bloky {3m}, {3m+1}, {3m+2}. Další: nula, kladná a záporná čísla.

**Úl. 19 (E⁻¹ je ekvivalence).** Reflexivita: \[x,x\] ∈ E, tedy \[x,x\] ∈ E⁻¹. Symetrie: \[x,y\] ∈ E⁻¹ ⇒ \[y,x\] ∈ E ⇒ \[x,y\] ∈ E ⇒ \[y,x\] ∈ E⁻¹. Tranzitivita se ověří stejně, nebo stačí říct, že pro symetrickou E je E⁻¹ = E.

**Úl. 20 (E₁ ∘ E₂ nemusí být ekvivalence).** Protipříklad na X = {1,2,3}: E₁ má rozklad {{1,2},{3}}, E₂ má rozklad {{1},{2,3}}. Složením dostaneš E₁ ∘ E₂ = {\[1,1\],\[1,2\],\[2,1\],\[2,2\],\[2,3\],\[3,1\],\[3,2\],\[3,3\]}. Obsahuje \[3,1\], ale neobsahuje \[1,3\], takže symetrie selhala.

## 6. Uspořádání

**Uspořádání** (neostré, částečné) je relace, která je **reflexivní, antisymetrická a tranzitivní.** Zkratka **RAT**.

Porovnání s ekvivalencí: obě mají R a T, ale ekvivalence má symetrii a uspořádání antisymetrii. Relace, která je zároveň symetrická i antisymetrická, je podmnožinou identity.

| Pojem | Význam |
| --- | --- |
| **Ostré uspořádání** | ireflexivní a tranzitivní (například < na ℕ) |
| **Lineární (úplné) uspořádání** | uspořádání, ve kterém jsou každé dva prvky srovnatelné (xRy nebo yRx) |
| **Částečné uspořádání** | srovnatelné být nemusí, například ⊆ na P(X) pro |

**Příklady uspořádání:** ≤ na ℝ (lineární), ⊆ na P(X) (částečné), dělitelnost ∣ na ℕ (částečná).

**Úl. 18.** Relace A ∼ B ⇔ A ⊆ B na P(X) je reflexivní (A ⊆ A), antisymetrická (A ⊆ B a B ⊆ A dávají A = B) a tranzitivní. Není symetrická: ∅ ⊆ X, ale X ⊄ ∅. Je tedy uspořádání, ne ekvivalence.

**Úl. 22.** P(Y) \\ P(X) pro X = {1,2,3}, Y = {1,2,3,4} jsou právě podmnožiny Y obsahující prvek 4. Zúžení uspořádání na libovolnou podmnožinu je opět uspořádání (vlastnosti RAT se zúžením neztratí), takže stačí to takto zdůvodnit.

**Úl. 21 (R₁ ∘ R₂ nemusí být uspořádání).** Protipříklad na X = {1,2}: R₂ = {\[1,1\],\[2,2\],\[1,2\]} a R₁ = {\[1,1\],\[2,2\],\[2,1\]} jsou uspořádání. Složením vyjde R₁ ∘ R₂ = {\[1,1\],\[1,2\],\[2,1\],\[2,2\]}, které není antisymetrické.

### Hasseův diagram

Hasseův diagram je zjednodušený graf uspořádání. Postup:

1. Vynech všechny smyčky (reflexivita se předpokládá).
2. Vynech všechny šipky, které vyplývají z tranzitivity (zkratky a → c, pokud existuje cesta a → b → c).
3. Nakresli menší prvky dolů, větší nahoru, a vynech šipky (směr je dán polohou).

Na diagramu čteš: a ≤ b právě tehdy, když se z a dostaneš do b cestou směrem nahoru.

## 7. Svazově uspořádaná množina (úl. 23–26)

V uspořádané množině (M, ≤) pro dva prvky a, b platí:

- **horní závora** je prvek, který je ≥ a i ≥ b,
- **supremum** a ∨ b je nejmenší z horních závor (musí existovat a být jediné),
- **dolní závora** je prvek ≤ a i ≤ b,
- **infimum** a ∧ b je největší z dolních závor.

**Svazově uspořádaná množina** je uspořádaná množina, v níž mají **každé dva prvky supremum i infimum.**

### Jak postupovat u úlohy 23

1. **Dostaň R\*ᵢ.** Je to nejmenší reflexivní a tranzitivní relace obsahující Rᵢ, tedy: přidej smyčky a přidej všechny dvojice \[a,b\], kam vede cesta. Pro svaz stačí pracovat s grafem Rᵢ a „dosažitelností“, vypisovat všechny dvojice není nutné.
2. **Rychlý test (nutná podmínka):** konečný svaz má právě jeden největší a právě jeden nejmenší prvek. Pokud existují dva maximální prvky (prvky bez šipky ven) nebo dva minimální prvky (bez šipky dovnitř), svaz to není.
3. **Důkladný test:** u každé dvojice prvků najdi horní závory a zkontroluj, že mezi nimi je nejmenší. Totéž s dolními závorami. Zaměř se na dvojice nesrovnatelných prvků.

**Proč nestačí rychlý test:** R₆ má jeden nejmenší (a) i jeden největší (f) prvek, přesto svaz není. Prvky d a e mají dolní závory a, b, c, ale b a c jsou nesrovnatelné, takže mezi dolními závorami není největší a infimum neexistuje.

**Výsledky úlohy 23 s důvodem:**

- R₁, R₂, R₃, R₄, R₇ jsou svazy. Jsou to „rovnoběžné cesty“ s jedním začátkem a jedním koncem a nesrovnatelné prvky mají vždy společný nejbližší prvek nad sebou i pod sebou.
- R₅ svaz není: prvek c nemá žádný následník, takže c a f jsou dva maximální prvky a nemají společnou horní závoru.
- R₆ svaz není, viz výše.

### Dělitelnost (úl. 24, 25)

Relace m ∣ n znamená, že m dělí n. Na množině přirozených čísel platí: supremum dvou čísel je jejich **nejmenší společný násobek** a infimum je jejich **největší společný dělitel.** Množina X s dělitelností je tedy svaz, právě když pro každou dvojici z X leží její NSN i NSD zpět v X.

**Úl. 24.** X = {1,2,3,4,6,12}. Hasseův diagram: dole 1; nad ním 2 a 3; nad 2 je 4 a 6, nad 3 je 6; úplně nahoře 12 (nad 4 a 6). Nesrovnatelné dvojice mají NSN i NSD v X, například pro 4 a 6 je NSN = 12 a NSD = 2. Je to svaz.

**Úl. 25.** Hledáš a, b, c tak, aby M = {a, b, c, 2, 4, 8} byl svaz. Nejjednodušší cesta je zvolit řetěz (každé dva prvky jsou srovnatelné, tedy supremum a infimum jsou vždy jeden z nich). Například a, b, c = 1, 16, 32, nebo 1, 16, 64. Jiná volba často vyžaduje, aby se do M „vešly“ i další NSN a NSD (například přidání čísla 3 by vyžadovalo i 6 a 12).

**Úl. 26.** (P(M), ⊆) je svaz: supremum dvou množin je jejich sjednocení, infimum je průnik. Hasseův diagram pro 4prvkovou množinu má 16 vrcholů v 5 patrech (1, 4, 6, 4, 1 prvků) a hrany spojují množiny lišící se právě jedním prvkem.

## 8. Postup podle typu zadání

| Zadání | Postup |
| --- | --- |
| „Určete vlastnosti relace“ | Projdi všech pět vlastností. Každou buď dokaž obecně, nebo vyvrať jedním protipříkladem. |
| „Je to ekvivalence?“ | Ověř RST. Při první nesplněné vlastnosti skonči (jeden protipříklad stačí). Pokud je ekvivalence, najdi třídy a zapiš rozklad. |
| „Je to uspořádání?“ | Ověř RAT. U svazů pak hledej supremum a infimum každé dvojice. |
| „Najděte relaci, která je … ale není …“ | Začni nejmenší vhodnou relací a přidávej dvojice. Po každém přidání zkontroluj tranzitivitu. |
| „Určete uzávěr“ | Přidej jen to, co je nutné. Pro R⁺ prověř všechny cesty v grafu. |
| „Rozklad ↔ ekvivalence“ | Každý blok dá všechny dvojice svých prvků (včetně \[x,x\]). |

### Recepty pro úlohu 4 (M = {1,2,3,4})

- **Symetrická, reflexivní, není tranzitivní:** identita plus {\[1,2\],\[2,1\],\[1,3\],\[3,1\]}. Chybí \[2,3\] i \[3,2\], tedy tranzitivita selže.
- **Reflexivní, tranzitivní, není symetrická:** identita plus jedna jednosměrná dvojice, například \[1,2\].
- **Tranzitivní, není reflexivní ani ireflexivní:** jedna smyčka, například {\[1,1\]}.
- **Tranzitivní, není symetrická ani antisymetrická:** potřebuješ oboustrannou dvojici (kvůli tranzitivitě musí mít i smyčky) a jednosměrnou dvojici: {\[1,1\],\[2,2\],\[1,2\],\[2,1\],\[4,3\]}.

## 9. Časté chyby

1. Zapomenutá smyčka u prvku, který se v relaci jinak nevyskytuje (úl. 15, prvek 4).
2. Přehlédnutá cesta při kontrole tranzitivity. Pomáhá projít dvojice podle prvního prvku.
3. Záměna symetrie a antisymetrie. Antisymetrie se týká jen *různých* prvků.
4. Tvrzení „není reflexivní, takže je ireflexivní“. Neplatí.
5. Důkaz vlastnosti na jednom příkladu. Příklad stačí pouze k *vyvrácení*.
6. Při skládání relací zaměněné pořadí. V této sbírce je (R ∘ S): nejdřív S, potom R.
7. U svazů kontrola jen největšího a nejmenšího prvku (viz R₆).
8. Ekvivalence se zadanou podmínkou, kde je v obou stranách nedefinovaný výraz (například x/y při y = 0).

## 10. Cvičení na procvičení

U každé relace urči, které z vlastností R, I, S, A, T má, a zda jde o ekvivalenci nebo uspořádání. Klíč je pod úlohami.

1. M = {1,2,3}, R = {\[1,1\],\[2,2\],\[3,3\],\[1,2\],\[2,3\]}.
2. Na ℤ: x ∼ y ⇔ 3 ∣ (x − y).
3. Na ℕ: x R y ⇔ x < y.
4. Na ℝ: x R y ⇔ x − y ∈ ℚ.
5. Na ℤ: x R y ⇔ x − y je liché.
6. Na ℕ: x R y ⇔ x ∣ y.

### Klíč

1. Reflexivní, antisymetrická, není symetrická, **není tranzitivní** (1R2 a 2R3, ale \[1,3\] ∉ R). Není to ekvivalence ani uspořádání. Doplněním \[1,3\] vznikne uspořádání (řetěz 1 < 2 < 3).
2. Ekvivalence, tři třídy (zbytky 0, 1, 2).
3. Ireflexivní, antisymetrická (předpoklad nastane jen prázdně), tranzitivní. Je to ostré uspořádání, ne neostré.
4. Ekvivalence: reflexivita (0 ∈ ℚ), symetrie (opačné číslo k racionálnímu je racionální), tranzitivita (součet dvou racionálních čísel je racionální).
5. Ireflexivní (x − x = 0 je sudé), symetrická, není tranzitivní (1R2, 2R3, ale 1 − 3 = −2 je sudé), není antisymetrická (1R2 i 2R1).
6. Reflexivní, antisymetrická (na ℕ z m ∣ n a n ∣ m plyne m = n), tranzitivní, takže uspořádání. Není lineární (2 a 3 jsou nesrovnatelné).

## 11. Doplněk: řešení úlohy 4 přes tabulky

Tabulka (matice) relace má **řádek = první prvek**, **sloupec = druhý prvek**. Jednička na pozici (a, b) znamená \[a, b\] ∈ R, nula znamená, že dvojice v relaci není. Tabulka je pro konečné relace nejrychlejší způsob, jak vlastnosti ověřovat.

### Jak číst vlastnosti z tabulky

| Vlastnost | Co hledat v tabulce |
| --- | --- |
| Reflexivní | na úhlopříčce (levý horní → pravý dolní roh) jsou **samé jedničky** |
| Ireflexivní | na úhlopříčce jsou **samé nuly** |
| Symetrická | tabulka je **zrcadlově souměrná podle úhlopříčky**, pozice (a,b) a (b,a) mají stejnou hodnotu |
| Antisymetrická | mimo úhlopříčku **nikdy nejsou jedničky na obou pozicích (a,b) i (b,a)** |
| Tranzitivní | pro každou jedničku na pozici (a,b) musí být **každá jednička z řádku b také v řádku a** |

Poslední pravidlo je nejpraktičtější. Jednička (a,b) říká „z a se dostanu do b“. Řádek b ukazuje, kam se dostanu z b, a tam se musím dostat i přímo z a.

### 4a) Symetrická, reflexivní, ne tranzitivní

Ra = {\[1,1\], \[2,2\], \[3,3\], \[4,4\], \[1,2\], \[2,1\], \[1,3\], \[3,1\]}

|  | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| **1** | 1 | 1 | 1 | 0 |
| **2** | 1 | 1 | 0 | 0 |
| **3** | 1 | 0 | 1 | 0 |
| **4** | 0 | 0 | 0 | 1 |

- Úhlopříčka je samé 1, takže je reflexivní.
- Tabulka je souměrná podle úhlopříčky, takže je symetrická.
- Tranzitivita selže: pozice (2,1) je 1, řádek 1 má jedničky ve sloupcích 1, 2, 3, ale řádek 2 nemá jedničku ve sloupci 3. Chybí \[2,3\].

### 4b) Reflexivní, tranzitivní, ne symetrická

Rb = {\[1,1\], \[2,2\], \[3,3\], \[4,4\], \[1,2\]}

|  | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| **1** | 1 | 1 | 0 | 0 |
| **2** | 0 | 1 | 0 | 0 |
| **3** | 0 | 0 | 1 | 0 |
| **4** | 0 | 0 | 0 | 1 |

- Úhlopříčka je samé 1, takže je reflexivní.
- Pozice (1,2) je 1, ale (2,1) je 0, takže není symetrická.
- Tranzitivita: u jedničky (1,2) má řádek 2 jedinou jedničku ve sloupci 2, a ta je i v řádku 1. Ostatní jedničky leží na úhlopříčce a tam podmínka platí triviálně.

### 4c) Tranzitivní, ani reflexivní, ani ireflexivní

Rc = {\[1,2\], \[1,4\], \[2,2\], \[2,4\]}

|  | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| **1** | 0 | 1 | 0 | 1 |
| **2** | 0 | 1 | 0 | 1 |
| **3** | 0 | 0 | 0 | 0 |
| **4** | 0 | 0 | 0 | 0 |

- Úhlopříčka je 0, 1, 0, 0. Není tam samé 1 ani samé 0, takže relace není reflexivní ani ireflexivní.
- Tranzitivita: jednička (1,2) vede do řádku 2, který má jedničky ve sloupcích 2 a 4, a stejné jedničky má řádek 1. Jednička (1,4) vede do prázdného řádku 4. Totéž platí pro (2,2) a (2,4).

### 4d) Tranzitivní, ani symetrická, ani antisymetrická

Rd = {\[1,1\], \[1,2\], \[2,1\], \[2,2\], \[3,4\]}

|  | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| **1** | 1 | 1 | 0 | 0 |
| **2** | 1 | 1 | 0 | 0 |
| **3** | 0 | 0 | 0 | 1 |
| **4** | 0 | 0 | 0 | 0 |

- Pozice (3,4) je 1, ale (4,3) je 0, takže není symetrická.
- Pozice (1,2) i (2,1) jsou 1 při 1 ≠ 2, takže není antisymetrická.
- Tranzitivita: řádky 1 a 2 jsou stejné, takže podmínka mezi nimi platí oboustranně. Jednička (3,4) vede do prázdného řádku 4.

**Typická chyba:** kdyby v 4d chyběly smyčky \[1,1\] a \[2,2\], tabulka by měla v levém horním rohu nuly na úhlopříčce a tranzitivita by selhala. Jednička (1,2) vede do řádku 2, který má jedničku ve sloupci 1, ale pozice (1,1) je 0.
