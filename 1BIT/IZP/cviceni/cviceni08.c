//== knihovny ==
#include <stdio.h>  //knihovna pro vstup a vystup
#include <stdlib.h> //knihovna pro praci s pameti

//== nove datove typy ==
typedef struct Svektor // deklarujeme datovy typ pro strukturu
{                      // jmenem "Svektor" se dvema polozkami
    int delka;         // pocet polozek
    int *pole;         // dynamicky alokovane pole
} vektor;              // jmeno tohoto typu je "vektor"

//== deklarace funkci ==
void vypisVektor(vektor *A);
void pridejPosledni(vektor *A, int cislo);
void odeberPosledni(vektor *A);
void odeberVsechny(vektor *A);
void pridejPrvni(vektor *A, int cislo);
void odeberIndex(vektor *A, int index);

//== definice funkci ==

// vypise vsechny prvky vektoru
void vypisVektor(vektor *A)
{
    printf("Vektor: ");                // Vypisujeme retezec "Vektor: "
    for (int i = 0; i < A->delka; i++) // pro vsechny prvky pole
    {
        printf("%i ", A->pole[i]); // vypisujeme hodnotu jednotlivych prvku
    }
    printf("\n"); // vypisujeme konec radku
}

// realokuje pole a na jeho konec prida novy prvek
void pridejPosledni(vektor *A, int cislo)
{
    int delka = (*A).delka;

    int *x = realloc((*A).pole, sizeof(int) * (delka + 1));
    if (x != NULL) {
        x[delka] = cislo; // delka +1 -1
        (*A).pole = x;
        (*A).delka = delka + 1;
    }
}

// overi jestli je pole prazdne, a pokud ne, tak z nej realokaci odebere posledni prvek
void odeberPosledni(vektor *A)
{
    int delka = (*A).delka;

    if (delka > 1) {
        int *x = realloc((*A).pole, sizeof(int) * (delka - 1));
        if (x != NULL) {
            (*A).pole = x;
            (*A).delka = delka - 1;
        } else {
            free((*A).pole);
            (*A).pole = NULL;
        }
    } else if (delka == 1) {
        free((*A).pole);
        (*A).pole = NULL;
        (*A).delka = 0;
    }
}

// uvolni pole (a odebere tak vsechny prvky)
void odeberVsechny(vektor *A)
{
    (*A).delka = 0;
    free((*A).pole);
    (*A).pole = NULL;
}

// realokuje pole a na jeho zacatek prida novy prvek
void pridejPrvni(vektor *A, int cislo)
{
    int delka = (*A).delka;

    int *x = realloc((*A).pole, sizeof(int) * (delka + 1));
    if (x != NULL) {
        for (int i = delka; i > 0; i--) { // delka +1 -1
            x[i] = x[i - 1];
        }
        x[0] = cislo;
        (*A).pole = x;
        (*A).delka = delka + 1;
    }
}

// overi zda prvek se zadanym indexem existuje, a pokud ano, tak ho smaze a provede realokaci
void odeberIndex(vektor *A, int index)
{
    int delka = (*A).delka;

    if (index < delka && index >= 0 && delka > 0) {
        for (int i = index; i < delka - 1; i++) {
            (*A).pole[i] = (*A).pole[i + 1]; // posun prvky za indexem o jedno doleva
        }
        odeberPosledni(A);
    }
}

int main(void) // zacatek programu
{
    vektor A = {0, NULL};
    vypisVektor(&A); // vytvarime vektor
                     //"A" je automaticky alokovana struktura
                     // obsahujici dynamicky alokovane pole
    pridejPosledni(&A, 10);
    vypisVektor(&A); // pridavame posledni prvek
    pridejPosledni(&A, 20);
    vypisVektor(&A); // pridavame posledni prvek
    pridejPosledni(&A, 30);
    vypisVektor(&A); // pridavame posledni prvek
    odeberPosledni(&A);
    vypisVektor(&A); // odebirame posledni prvek
    odeberVsechny(&A);
    vypisVektor(&A); // odebirame vsechny prvky
    odeberPosledni(&A);
    vypisVektor(&A); // odebirame neexistujici prvek
    pridejPrvni(&A, 40);
    vypisVektor(&A); // pridavame prvni prvek
    pridejPrvni(&A, 50);
    vypisVektor(&A); // pridavame prvni prvek
    pridejPrvni(&A, 60);
    vypisVektor(&A); // pridavame prvni prvek
    odeberIndex(&A, -1);
    vypisVektor(&A); // odebirame neexistujici prvek
    odeberIndex(&A, 3);
    vypisVektor(&A); // odebirame neexistujici prvek
    odeberIndex(&A, 1);
    vypisVektor(&A); // odebirame konkretni prvek
    odeberVsechny(&A);
    vypisVektor(&A); // odebirame vsechny prvky
    return 0;        // konec programu
}