//== knihovny ==
#include <math.h>  //knihovna matematickych funkci
#include <stdio.h> //knihovna pro vstup a vystup

//(pri prekladu bude potreba pridat parametr -lm, viz cviceni 2 slide 5)
// https://www.fit.vut.cz/person/husa/public/IZP-cv02.pdf#view=fit&page=5

//== nove datove typy ==
typedef struct Sbod // definujeme strukturu jmenem "Sbod"
{                   // se dvema polozkami
    float x;        // polozka typu "float" jmenem "x"
    float y;        // polozka typu "float" jmenem "y"
} bod;              // deklarujeme jeji datovy typ "bod"

//== deklarace funkci ==
void vypisMnozinu(int delka, bod pole[]);
float vzdalenost(bod A, bod B);
float prumernaVzdalenost(int delka, bod pole[]);
void stredMnoziny(int delka, bod pole[], bod *S);
bod *nejblizsiBod(int delka, bod pole[], bod S);

//== definice funkci ==
// vypise vsechny body mnoziny (pole)
void vypisMnozinu(int delka, bod pole[])
{
    for (int i = 0; i < delka; i++) {                                 // pro vsechny polozky pole
        printf("pole[%i] = (%.3f, %.3f)\n", i, pole[i].x, pole[i].y); // vypis souradnice
    }
}

// spocita vzajemnou vzdalenost dvou bodu (dle Pythagorovy vety)
float vzdalenost(bod A, bod B)
{
    float dx = A.x - B.x;           // pocitame rozdil na ose X
    float dy = A.y - B.y;           // pocitame rozdil na ose Y
    return sqrt(dx * dx + dy * dy); // pocitame Pythagorovu vetu
}

// spocita prumer vzajemnych vzdalenosti vsech bodu mnoziny
// napriklad: (AB + AC + AD + BC + BD + CD) / 6
// pri implementaci doporucuji pouzit funkci vzdalenost
float prumernaVzdalenost(int delka, bod pole[])
{
    int prumer;
    float soucet;

    int c = 0;
    for (int i = 0; i < delka; i++) {
        for (int j = i + 1; j < delka; j++) {
            soucet += vzdalenost(pole[i], pole[j]);
        }
    }

    float delka_f = delka;
    return soucet / (delka_f * (delka_f - 1) / 2);
}

// spocita souradnice stredu mnoziny a ulozi je do bodu S
//(souradnice stredu jsou aritmeticky prumer souradnic vsech bodu mnoziny)
void stredMnoziny(int delka, bod pole[], bod *S)
{
    float soucet_x = 0;
    float soucet_y = 0;

    for (int i = 0; i < delka; i++) {
        soucet_x += pole[i].x;
        soucet_y += pole[i].y;
    }

    (*S).x = soucet_x / delka;
    (*S).y = soucet_y / delka;
}

// vrati ukazatel na ten z bodu mnoziny (pole), ktery je nejblize k jejimu stredu (S)
// pri implementaci doporucuji pouzit funkci vzdalenost
bod *nejblizsiBod(int delka, bod pole[], bod S)
{
    bod *nejblizsi = &pole[0];
    float nejblizsi_vzdalenost = vzdalenost(pole[0], S);
    for (int i = 1; i < delka; i++) {
        float vzd = vzdalenost(pole[i], S);
        if (vzd < nejblizsi_vzdalenost) {
            nejblizsi_vzdalenost = vzd;
            nejblizsi = &pole[i];
        }
    }
    return nejblizsi;
}

int main(void) // zacatek programu
{
#define VELIKOST_A 4 // pocet prvku mnoziny A
#define VELIKOST_B 4 // pocet prvku mnoziny B

    bod MA[VELIKOST_A] = {{0.0, 0.0}, {1.0, 1.0}, {2.0, 2.0}, {2.0, 0.0}}; // prvni mnozina
    bod MB[VELIKOST_B] = {{0.0, 0.0}, {1.0, 3.0}, {3.0, 2.0}, {3.0, 0.0}}; // druha mnozina
    float d;                                                               // prumerna vzdalenost
    bod S;                                                                 // stred mnoziny
    bod *N;                                                                // ukazatel na nejblizsi bod

    printf("Mnozina A:\n");
    vypisMnozinu(VELIKOST_A, MA);                            // vypisujeme vsechny body mnoziny A
    d = prumernaVzdalenost(VELIKOST_A, MA);                  // pocitame prumernou vzdalenost
    printf("Prumerna vzdalenost je %f\n", d);                // vypis
    stredMnoziny(VELIKOST_A, MA, &S);                        // pocitame souradnice stredu
    printf("Souradnice stredu  (%.2f, %.2f)\n", S.x, S.y);   // vypis
    N = nejblizsiBod(VELIKOST_A, MA, S);                     // zjistujeme nejblizsi bod
    printf("Nejblizsi prvek je (%.2f, %.2f)\n", N->x, N->y); // vypis

    printf("\n");

    printf("Mnozina B:\n");
    vypisMnozinu(VELIKOST_B, MB);                            // vypisujeme vsechny body mnoziny B
    d = prumernaVzdalenost(VELIKOST_B, MB);                  // pocitame prumernou vzdalenost
    printf("Prumerna vzdalenost je %f\n", d);                // vypis
    stredMnoziny(VELIKOST_B, MB, &S);                        // pocitame souradnice stredu
    printf("Souradnice stredu  (%.2f, %.2f)\n", S.x, S.y);   // vypis
    N = nejblizsiBod(VELIKOST_B, MB, S);                     // zjistujeme nejblizsi bod
    printf("Nejblizsi prvek je (%.2f, %.2f)\n", N->x, N->y); // vypis

    return 0; // konec programu
}