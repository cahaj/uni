Generated with Claude Sonnet 5.5

# IZP – půlsemestrální zkouška: studijní taháček

Půlsemestrálka obsahuje vždy čtyři typy úloh: oprava chybného kódu, doplnění kódu (ukazatele a struktury), soubory a argumenty programu a napsání celé funkce. Tahák shrnuje témata z přednášek 1–7, která k nim potřebuješ, a ukazuje, jak se v nich mohou proplétat.

## Mapa: která témata patří ke které úloze

Každá úloha prověřuje jiný výsek látky; zadání se ale mění jen v datech (jiný typ, pole místo čísla, matice místo pole).

| Úloha | Co se po tobě chce | Témata (týden výuky) |
| --- | --- | --- |
| 1. Oprava kódu | v krátké funkci přeškrtnout 2–4 chybné části a napsat opravu | datové typy a proměnné (1), řídicí konstrukce (2), výrazy (3), `scanf`/`printf` (4) |
| 2. Doplnění kódu | doplnit výrazy do volání funkcí a `printf` podle typů | pole a struktury (3), funkce (3–4), ukazatele (4, 7) |
| 3. Soubory a argumenty | doplnit podmínku na `argc` a volání `fscanf`/`fprintf` | soubory (3), standardní vstup a výstup (4), řetězce (3) |
| 4. Napsání funkce | hlavička i tělo funkce nad polem, řetězcem nebo maticí | funkce a vnořené cykly (4), pole (2–3), vektory a matice (6), dynamické struktury (7) |

**Možné varianty téhož:** `char` a řetězce místo `int`/`double`, matice místo pole, `fgets` místo `fscanf`, vnořená struktura, `malloc` na vstupu funkce.

## Základy: typy, specifikátory, limity, operátory

Kdykoli se čte nebo vypisuje, musí formátovací specifikátor přesně odpovídat typu proměnné. Rozdíl mezi `printf` a `scanf` je největší zdroj chyb.

| Typ | `printf` | `scanf` | Poznámka |
| --- | --- | --- | --- |
| `int` | `%d` / `%i` | `%d` (`%i` pozná i `0x…`, `0…`) |  |
| `unsigned int` | `%u` | `%u` |  |
| `long` / `long long` | `%ld` / `%lld` | `%ld` / `%lld` |  |
| `float` | `%f` | `%f` |  |
| `double` | `%f` (i `%lf`) | **`%lf`** | `scanf("%f")` do `double` je chyba |
| `long double` | `%Lf` | `%Lf` |  |
| `char` | `%c` | `%c` | `%c` nepřeskočí mezeru; `" %c"` ano |
| řetězec `char[]` | `%s` | `%s` | bez `&`, pole už je adresa |
| `size_t` | `%zu` | `%zu` | výsledek `sizeof`, `strlen` |
| ukazatel | `%p` | – |  |
| znak `%` | `%%` | – |  |
| hex / oktalově | `%x` / `%o` | `%x` / `%o` |  |
| exponent | `%e`, `%g` | `%e`, `%g` |  |

**`printf` dostává hodnotu, `scanf` adresu.** Návratová hodnota `scanf`/`fscanf` = počet úspěšně načtených položek (`EOF` na konci vstupu).

```c
int i; double d; char s[20];
scanf("%d", &i);       // ✓
scanf("%lf", &d);      // ✓
scanf("%19s", s);      // ✓ bez &, s omezením délky

scanf("%d", &d);       // ✗ špatný specifikátor
scanf("%lf", d);       // ✗ chybí &
scanf("%f", &d);       // ✗ %f je pro float
printf("%d\n", d);     // ✗ špatný specifikátor pro double
printf("%i\n", &i);    // ✗ vypisuje adresu, ne hodnotu
```

**Limity** (`<limits.h>`, `<float.h>`): `INT_MAX`, `INT_MIN`, `DBL_MAX` (největší konečné `double`), `-DBL_MAX` (nejnižší), `DBL_MIN` (⚠ nejmenší **kladné**, ne nejzápornější). Při hledání maxima se startuje z nejnižší možné hodnoty nebo z prvního prvku, při hledání minima z nejvyšší.

**Operátory a výrazy:**

- `/` mezi dvěma `int` je celočíselné dělení (`1/2 == 0`, `1.0/2 == 0.5`), `%` je zbytek jen pro celá čísla.
- `i++` vrací starou hodnotu, `++i` novou; `=` přiřazuje, `==` porovnává.
- `&&` a `||` se vyhodnocují zleva a zkráceně: `i < n && a[i] > 0` je bezpečné, obráceně ne.
- `abs` je pro `int`, `fabs` pro `double` (`<math.h>`), `labs` pro `long`.
- Přetypování: `(double)a / b`, ne `(double)(a / b)`.
- **C23:** `bool`, `true`, `false` jsou klíčová slova, `#include <stdbool.h>` není nutný; `nullptr` je nová konstanta ukazatele (`NULL` stále funguje).

## Podmínky a cykly: syntax a chyby k opravě

```c
if (a > b) { ... } else if (a == b) { ... } else { ... }

while (podmínka) { ... }

do {
    ...
} while (podmínka);                    // středník na konci je povinný

for (int i = 0; i < n; i++) { ... }    // inicializace; podmínka; krok

for (int i = 0; i < r; i++)            // vnořené cykly: každý má vlastní čítač
    for (int j = 0; j < c; j++) { ... }

switch (x) { case 1: ...; break; default: ...; }   // bez break propadává dál
```

U úlohy „oprav chyby“ se chyby dělí do pěti skupin. Projdi kód vždy postupně přes všechny:

| Skupina | Příklad chybného zápisu | Oprava |
| --- | --- | --- |
| Typ a specifikátor | `scanf("%d", &x)` pro `double x` | `%lf` |
| Chybějící `&`, `*`, `->` | `scanf("%d", x)` | `&x` |
| Špatné klíčové slovo nebo středník | `} for (i < n);` · `} while (i < n)` · `while (i < n);` | `} while (i < n);` · doplnit `;` · smazat `;` |
| Špatná logika | `if (a = b)` · `>` místo `<` · `i <= n` u pole délky `n` | `==` · opačné porovnání · `i < n` |
| Špatná počáteční hodnota | součet z `1`, součin z `0`, maximum z `0` při záporných datech | součet z `0`, součin z `1`, maximum z prvního prvku nebo z nejnižší hodnoty |

Další časté chyby: chybějící `return`, chybějící `i++` (nekonečný cyklus), použití proměnné před inicializací, `=` místo `==`, dělení `int / int` tam, kde je čekáno desetinné číslo, špatný návratový typ funkce.

**Běžné vzory:**

```c
int soucet = 0, pocet = 0;                       // počítání a sčítání
for (int i = 0; i < n; i++) {
    if (a[i] > 0) { soucet += a[i]; pocet++; }
}

while (scanf("%d", &x) == 1) { ... }            // čtení až do konce vstupu
```

## Pole, řetězce a matice

```c
int a[5] = {1, 2, 3};         // zbytek se doplní nulami; platné indexy 0 až 4
int m[3][4];                  // matice 3 řádky × 4 sloupce: m[řádek][sloupec]
char s[] = "ahoj";            // 5 bajtů: 'a','h','o','j','\0'
char t[10] = "ahoj";          // zbytek vyplněn '\0'
```

- Pole se do funkce předává jako adresa prvního prvku, funkce **nezná délku**; předává se zvlášť (`len`). Uvnitř funkce vrací `sizeof(arr)` velikost ukazatele, ne pole.
- `int a[]` a `int *a` jsou jako parametr totéž. Změna prvku pole ve funkci se projeví i venku, změna obyčejného parametru ne (předává se kopie).
- U matic jako parametru se musí znát počet sloupců: `void f(int r, int c, int m[r][c])` (pořadí: rozměry **před** polem) nebo `void f(int m[][4], int r)`.
- Řetězec je pole `char` ukončené `'\0'`. Pole musí být o 1 větší, než je text.

| Funkce (`<string.h>`) | Co dělá | Pozor |
| --- | --- | --- |
| `strlen(s)` | délka bez `'\0'` | vrací `size_t` |
| `strcmp(a, b)` | `0` při shodě | `a == b` porovnává adresy, ne text |
| `strcpy(dst, src)` | kopíruje včetně `'\0'` | cílové pole musí být dost velké |
| `strcat(dst, src)` | připojí na konec | totéž |
| `fgets(s, n, f)` | načte řádek včetně `'\n'` | `n` = velikost pole |

```c
for (int i = 0; s[i] != '\0'; i++) { ... }    // průchod řetězcem bez strlen
for (int i = 0; i < r; i++)                   // průchod maticí po řádcích
    for (int j = 0; j < c; j++) soucet += m[i][j];

a[5]                  // ✗ pole délky 5 končí indexem 4
if (s == "ahoj")      // ✗ porovnání adres, správně strcmp(s, "ahoj") == 0
char c = "a";         // ✗ "a" je řetězec, správně 'a'
m[i, j]               // ✗ správně m[i][j]
```

## Funkce, ukazatele a struktury

Tato úloha je skládačka: máš určit, **jakého typu je výraz** v každém kroku, a podle toho zvolit `.`, `->`, `[]`, `&` nebo `*`. Vždy si u každé proměnné napiš její typ.

```c
typedef struct { double x, y; } Bod;                 // struktura se jménem Bod
typedef struct { Bod* body; int pocet; } Obrazec;    // pole bodů + jeho délka
```

| Výraz | Typ výrazu | Platí, když |
| --- | --- | --- |
| `o` | `Obrazec` | proměnná je struktura |
| `po` | `Obrazec*` | ukazatel na strukturu |
| `o.pocet`, `po->pocet` | `int` | `.` pro strukturu, `->` pro ukazatel |
| `po->body` | `Bod*` | člen je ukazatel (= pole) |
| `po->body[i]` | `Bod` | `[i]` už dereferuje, dál tečka |
| `po->body[i].x` | `double` |  |
| `&po->body[i]` | `Bod*` | adresa prvku |
| `&po->body[i].x` | `double*` | `.` a `[]` mají přednost před `&` |
| `*(po->body + i)` | `Bod` | totéž co `po->body[i]` |
| `p[i]` |  | totéž co `*(p + i)` |

`p->x` je zkratka za `(*p).x`. Priorita: `.`, `->`, `[]` vážou silněji než unární `&` a `*`; `*p.x` znamená `*(p.x)`.

**Předávání parametrů:**

- Hodnotou (`Bod b`, `int n`): funkce dostane kopii, změna se venku neprojeví.
- Adresou (`Bod* b`, `int* n`): funkce může změnit původní hodnotu přes `b->x = 1.0;` či `*n = 5;`.
- Parametr typu `T*` voláš s `&promenna`; parametr typu `T` voláš s hodnotou, nikoli s adresou.

```c
void zvetsi(int* n) { *n += 1; }      // výstupní parametr
int k = 3;
zvetsi(&k);                           // ✓ k je nyní 4

zvetsi(k);                            // ✗ předáno int, očekáván int*
printf("%d", n);                      // ✗ uvnitř funkce n je adresa, správně *n
b.x                                   // ✗ pokud je b ukazatel, správně b->x
obr->body[i]->x                       // ✗ body[i] není ukazatel, správně obr->body[i].x
obr->body[obr->pocet]                 // ✗ poslední prvek má index pocet - 1
```

**Sady funkcí volající jedna druhou:** u každého volání zkontroluj tři věci: (1) co funkce očekává (typ parametru), (2) co jí posíláš (typ výrazu), (3) co vypisuje `printf` (specifikátor sedí s typem výrazu po dereferenci).

## Soubory, stdin a argumenty programu

**`int main(int argc, char* argv[])`**: `argc` je počet argumentů **včetně názvu programu**, `argv[0]` je název programu, `argv[1]` první skutečný argument, `argv[argc - 1]` poslední. Pro N skutečných argumentů je potřeba `argc >= N + 1`. Všechny `argv[i]` jsou řetězce.

| Převod řetězce | Funkce (`<stdlib.h>`) |
| --- | --- |
| na `int` | `atoi(argv[1])` nebo `strtol` |
| na `double` | `atof(argv[1])` nebo `strtod` |

| Režim `fopen` | Význam |
| --- | --- |
| `"r"` | čtení, soubor musí existovat |
| `"w"` | zápis, vytvoří nebo **smaže obsah** |
| `"a"` | připisování na konec |
| `"r+"`, `"w+"` | čtení i zápis |

`fopen` vrací `FILE*`, při neúspěchu `NULL`. Každý úspěšně otevřený soubor se zavírá pomocí `fclose`. Zavírá se jen to, co se podařilo otevřít.

| Standardní proud | Souborový ekvivalent | Poznámka |
| --- | --- | --- |
| `scanf(fmt, ...)` | `fscanf(f, fmt, ...)` | `scanf` = `fscanf(stdin, ...)` |
| `printf(fmt, ...)` | `fprintf(f, fmt, ...)` | `printf` = `fprintf(stdout, ...)` |
| `getchar()` | `fgetc(f)` | vrací `int`, na konci `EOF` |
| `fgets(s, n, stdin)` | `fgets(s, n, f)` | čte řádek, vrací `NULL` na konci |
| – | `fprintf(stderr, ...)` | chybové hlášky |

**Soubor je první argument** u `fscanf`, `fprintf`, `fgetc` a `fclose`; formát je druhý, adresy či hodnoty následují. **Výjimka:** `fgets(s, n, f)` má soubor až na třetím místě.

```c
int main(int argc, char* argv[])
{
    if (argc < 2)                          // kolik argumentů je potřeba + 1
        return 1;
    FILE* f = fopen(argv[1], "r");
    if (f != NULL) {
        int x;
        while (fscanf(f, "%d", &x) == 1) { ... }     // čtení do konce souboru
        fclose(f);
    }
    return 0;                              // 0 = úspěch, nenulová = chyba
}
```

**Pasti:**

```c
if (argc < 1)                      // ✗ vždy nepravda: argc je alespoň 1
fscanf("%d", &x);                  // ✗ chybí FILE* na prvním místě
fscanf(f, "%d", x);                // ✗ chybí &
fprintf(f, "%d", &x);              // ✗ & je navíc, vypisuje se hodnota
fscanf(argv[1], "%d", &x);         // ✗ argv[1] je název souboru, ne FILE*
while (!feof(f)) { fscanf(...); }  // ✗ zpracuje poslední položku dvakrát; testuj návratovou hodnotu
char* s; fscanf(f, "%s", s);       // ✗ s neukazuje na alokovanou paměť
```

## Dynamická paměť

Ve zkoušce se může objevit v zadání funkce, která pole vytváří nebo vrací (`<stdlib.h>`). Platí: co se alokuje, musí se uvolnit, a po uvolnění se ukazatel nepoužívá.

```c
int* a = malloc(n * sizeof(int));         // n prvků; paměť není vynulovaná
int* b = calloc(n, sizeof(int));          // n prvků vynulovaných
if (a == NULL) return NULL;               // vždy zkontrolovat
a = realloc(a, 2 * n * sizeof(int));      // zvětšení (správně přes pomocný ukazatel)
free(a);                                  // uvolnění

int* c = malloc(n);                       // ✗ chybí * sizeof(int): alokuje n bajtů
int* d = malloc(sizeof(d));               // ✗ velikost ukazatele, ne prvku
free(a); a[0] = 1;                        // ✗ použití po uvolnění
```

U struktur s ukazatelem (`Obrazec`) alokuje člen pole zvlášť: `o.body = malloc(o.pocet * sizeof(Bod));`. Pak jej zvlášť uvolníš.

## Psaní funkce od nuly: šablona a vzorové algoritmy

**Hlavička:** `návratový_typ jméno(typ parametr, typ parametr)`. Jména a pořadí parametrů přesně podle zadání, návratový typ podle toho, co se vrací.

| Co zadání říká | Návratový typ | Parametry |
| --- | --- | --- |
| „pravdivostní hodnota“, „ověří, zda“ | `bool` (C23: bez `#include <stdbool.h>`) |  |
| „počet“, „index“ | `int` (nebo `size_t`) |  |
| „desetinné číslo“, „průměr“ | `double` |  |
| „pole čísel“ + délka |  | `double arr[]` nebo `double *arr`, `int len` |
| matice |  | `int r, int c, int m[r][c]` |
| řetězec |  | `const char *s` (konec je `'\0'`, délku netřeba) |

Postup: (1) ošetři krajní případ z textu zadání (prázdné pole, `len < 1`), (2) vyber vzor níže, (3) ověř na vzorových hodnotách ze zadání, (4) zkontroluj hranice cyklů a to, že `return` je na všech cestách.

**Vzor „pro všechny platí“** (seřazeno, všechny kladné, všechny různé): předpokládej `true`, při prvním porušení hned `return false`, `return true` je **až za cyklem**.

```c
bool jeVzestupne(const int a[], int len)
{
    for (int i = 1; i < len; i++)
        if (a[i] < a[i - 1])
            return false;
    return true;
}
```

**Vzor „existuje“** (obsahuje hodnotu): opačně, při prvním nálezu `return true`, `return false` až za cyklem.

**Vzor „počítání, součet, extrém“:** proměnná před cyklem, aktualizace uvnitř, `return` až po cyklu. Průměr: `(double)soucet / len`.

**Vzor „všechny dvojice“:** vnořené cykly s `j = i + 1`, aby se prvek neporovnával sám se sebou a dvojice se neopakovaly. Rozdíl dvou `double` se měří přes `fabs(a - b)` (`<math.h>`). Alternativa bez dvou cyklů: spočítat minimum a maximum a porovnat jejich rozdíl.

**Vzor „matice“:** `for i` přes řádky, uvnitř `for j` přes sloupce; diagonála `m[i][i]`, vedlejší `m[i][c - 1 - i]`; transpozice `m[j][i]`.

**Vzor „řetězec“:** `for (int i = 0; s[i] != '\0'; i++)`; znaky se porovnávají s apostrofy (`s[i] == 'a'`); `isalpha`, `isdigit`, `toupper` z `<ctype.h>`.

```c
// ✗ chyby při psaní funkce
bool f(double arr, int len)                  // chybí [] nebo *, není to pole
for (int i = 0; i < len; i++);               // středník za for
for (int i = 0; i <= len; i++)               // čte arr[len], mimo pole
if (abs(arr[i] - arr[j]) > 1.0)              // abs je pro int, použij fabs
for (...) { if (...) return true; else return false; }   // vyhodnotí jen první prvek
if (x > 1.0)  vs  if (x >= 1.0)              // „o více než“ je >, „alespoň“ je >=
```

## Kontrolní seznam před odevzdáním

- Středníky: ano za `do { } while (…)` a za příkazy; ne za `for (…)`, `while (…)`, `if (…)`.
- `scanf`/`fscanf` mají v argumentech adresy (`&x`, u řetězce bez `&`), `printf`/`fprintf` hodnoty.
- Specifikátor sedí s typem: `int` `%d`, `double` `%lf` (u `scanf`), `char` `%c`, řetězec `%s`.
- Indexy: `0` až `len - 1`; poslední prvek je `a[len - 1]`.
- Ukazatel → `->`, struktura → `.`; adresa → `&`, hodnota z adresy → `*`.
- Každý `fopen` kontroluj proti `NULL`, každý otevřený soubor zavři, `FILE*` je první argument `fscanf`/`fprintf`.
- `argc` zahrnuje název programu; `argv[i]` jsou řetězce.
- Počáteční hodnoty: součet `0`, součin `1`, extrém z prvního prvku nebo z krajní hodnoty (`±DBL_MAX`, `INT_MIN`/`INT_MAX`).
- Funkce s návratovým typem vrací hodnotu na **všech** cestách; `return` uvnitř cyklu ukončí celou funkci.
- `int / int` je celočíselné; `abs` je jen pro `int`.
- Dvě řešení z jedné úlohy nejsou potřeba: napiš to jednodušší, které zvládneš ověřit na příkladech ze zadání.
