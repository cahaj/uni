#include <ctype.h>
#include <stdio.h>
#include <string.h>

#define MAX_LEN 100
#define MAX_LEN_W_RESERVE (MAX_LEN + 16) // rezerva pro newlines, EOF, porovnavani velikosti

// statusove konstanty pro lepsi citelnost kodu
#define LINE_EOF 0
#define LINE_TOO_LONG -1

// prelozi charakter vstupu do cisla, nebo do separacniho charakteru #
char translate(char c)
{
    // pokud je cislo, vrat cislo
    if (c >= '0' && c <= '9') {
        return c;
    }

    if (c == '+') {
        return '0';
    }

    if (c >= 'A' && c <= 'Z') {
        c = tolower(c);
    }

    if (c >= 'a' && c <= 'c') {
        return '2';
    }
    if (c >= 'd' && c <= 'f') {
        return '3';
    }
    if (c >= 'g' && c <= 'i') {
        return '4';
    }
    if (c >= 'j' && c <= 'l') {
        return '5';
    }
    if (c >= 'm' && c <= 'o') {
        return '6';
    }
    if (c >= 'p' && c <= 's') {
        return '7';
    }
    if (c >= 't' && c <= 'v') {
        return '8';
    }
    if (c >= 'w' && c <= 'z') {
        return '9';
    }

    // jiny znak = #
    return '#';
}

void translate_input(const char input[], char output[])
{
    int length = strlen(input);
    for (int i = 0; i < length; i++) {
        char translated = translate(input[i]);
        output[i] = translated;
    }
    output[length] = '\0';
}

int is_valid_filter(const char arg[])
{
    int length = strlen(arg);

    if (length < 1 || length > MAX_LEN) {
        return 0;
    }

    for (int i = 0; i < length; i++) {
        if (arg[i] < '0' || arg[i] > '9') {
            return 0;
        }
    }

    return 1;
}

int is_valid_name(const char name[])
{
    int length = strlen(name);

    if (length < 1) {
        return 0;
    }

    for (int i = 0; i < length; i++) {
        if (name[i] < ' ' || name[i] > '~') { // tisknutelne ASCII
            return 0;
        }
    }

    return 1;
}

int is_valid_phone(const char phone[])
{
    int length = strlen(phone);
    int start = 0; // prvni charakter telcisla musi byt cislo

    // plusko je povoleno, posune start cisla o 1 pozici
    if (phone[0] == '+') {
        start = 1;
    }

    // aspon jedno cislo, kryje i kdyby bylo jen +
    if (start >= length) {
        return 0;
    }

    for (int i = start; i < length; i++) {
        if (phone[i] < '0' || phone[i] > '9') {
            return 0;
        }
    }

    return 1;
}

int read_line(char line[])
{
    // fgets prepise line radkem z stdin a prida \0, konci bud EOF, newline nebo specifikovanym limitem
    // pokud fgets precte na radku jenom EOF, neprepise line a vraci pouze NULL
    // s kazdou iteraci se fgets posune dal, dokud zase nenarazi na nejaky terminacni prvek
    if (fgets(line, MAX_LEN_W_RESERVE, stdin) == NULL) {
        return LINE_EOF;
    }

    int length = strlen(line);

    if (length > 0 && line[length - 1] == '\n') {
        line[length - 1] = '\0'; // prepise newline za terminacni charakter retezce
        length--; // pokud obsahuje newline, tak newline neni zapocitana do limitu vstupu
    }
    if (length > MAX_LEN) {
        return LINE_TOO_LONG;
    }

    // pokud je delka vpodarku a neni newline, tak je to posledni radek souboru
    return 1;
}

int main(int argc, char *argv[])
{
    const char *filter = ""; // ukazatel filter ukazuje na \0 v ROM

    if (argc > 2) {
        fprintf(stderr, "Error: moc argumentu. Maximalni pocet je 2.\n");
        return 1;
    }

    if (argc == 2) {
        if (!is_valid_filter(argv[1])) {
            fprintf(stderr, "Error: argument musi byt od 1 to %d cislic (0-9) dlouhy.\n", MAX_LEN);
            return 1;
        }

        filter = argv[1]; // filter ted ukazuje na argv[1]
    }


    char name[MAX_LEN_W_RESERVE];
    char phone[MAX_LEN_W_RESERVE];
    char name_translated[MAX_LEN_W_RESERVE];
    char phone_translated[MAX_LEN_W_RESERVE];
    int found = 0;

    while (1) {
        int status = read_line(name); // read_line prepise name a vrati status

        if (status == LINE_EOF) {
            break; //na konci souboru vzdy
        }
        if (status == LINE_TOO_LONG) {
            fprintf(stderr, "Error: radek je delsi nez %d znaku.\n", MAX_LEN);
            return 1;
        }

  
        status = read_line(phone);

        if (status == LINE_EOF) {
            fprintf(stderr, "Error: posledni kontakt nema cislo.\n"); 
            return 1;
        }
        if (status == LINE_TOO_LONG) {
            fprintf(stderr, "Error: radek je delsi nez %d znaku.\n", MAX_LEN);
            return 1;
        }


        if (!is_valid_name(name)) {
            fprintf(stderr, "Error: spatny format jmena.\n");
            return 1;
        }
        if (!is_valid_phone(phone)) {
            fprintf(stderr, "Error: spatny format telefonniho cisla.\n");
            return 1;
        }


        translate_input(name, name_translated);
        translate_input(phone, phone_translated);

        // strstr vraci pointer na misto, kde je podretezec (needle) obsazen v retezci (haystack), nebo NULL pokud needle neni v haystacku
        // pokud filter porad ukazuje na \0, tak strstr nebude NULL a vypise vsechna jmena a telcisla
        if (strstr(name_translated, filter) != NULL || strstr(phone_translated, filter) != NULL) {
            printf("%s, %s\n", name, phone);
            found++;
        }
    }

    if (found == 0) {
        printf("Not found\n");
    }

    return 0;
}
