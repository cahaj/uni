#!/bin/sh
# Self-check for CRLF line endings; first crlf_probe=LF<LF> then single-line with if-statement checking it
crlf_probe=LF
if [ "$crlf_probe" != LF ]; then printf '%s\n' "POZOR: Skript $0 ma ukonceni radku CRLF (pravdepodobne prevzato z Windows)." "Nejprve prekonvertujte skript: dos2unix $0" "Potom ho opet spustte: sh $0" >&2; exit 1; fi # single line on purpose

# Test script for IZP 2026/27 proj1 (t9search).
# Date: 2026-09-30
# Run: sh test.sh
export POSIXLY_CORRECT=y
export LC_ALL=C

cd -- "$(dirname -- "$0")" || exit 1

die()
{
    echo "$@" >&2
    exit 1
}

# Check if software under test exists.
if ! [ -f t9search.c ]; then
    die "File t9search.c not found. Place it in the same directory as $0."
fi

# Check required tools and compile SUT.
for tool in gcc timeout diff sort tr sed tail od mktemp; do
    command -v "$tool" >/dev/null 2>&1 || die "Required tool not found: $tool"
done
gcc -std=c23 -Wall -Wextra -Werror -pedantic -o t9search t9search.c || die "Compilation failed."

# Keep files of failed tests for manual inspection and repeated execution.
# A separate directory prevents overwriting files from a previous run.
TESTDIR=$(mktemp -d ./test-results-XXXXXX) || die "Cannot create test directory."
passed=0
failed=0

# $1 file to be redirected to stdin
# $2 file with expected stdout, or !error for an expected input error
# $3-... SUT arguments
# Result: 0=test passed, 1=test failed. Sets status for diagnostics.
run_test()
{
    local stdinred="$1"
    local stdoutref="$2"
    shift 2

    (ulimit -f 128; exec timeout -k 1s 3s ./t9search "$@") \
        <"$stdinred" >"$TESTDIR/test-stdout.tmp" 2>"$TESTDIR/test-stderr.tmp"
    status=$?

    if [ "$stdoutref" = '!error' ]; then
        # Reject timeout, execution failures and signals. Do not compare stdout.
        [ "$status" -gt 0 ] && [ "$status" -lt 124 ] || return 1
        [ -s "$TESTDIR/test-stderr.tmp" ] || return 1
        local message
        local nonascii
        message=$(tr -d '[:space:]' <"$TESTDIR/test-stderr.tmp")
        nonascii=$(tr -d '\11\12\15\40-\176' <"$TESTDIR/test-stderr.tmp")
        [ -n "$message" ] && [ -z "$nonascii" ]
        return $?
    fi

    [ "$status" -eq 0 ] && [ ! -s "$TESTDIR/test-stderr.tmp" ] || return 1

    # sort would add a missing final LF, so check the last byte separately.
    local lastbyte
    lastbyte=$(tail -c 1 "$TESTDIR/test-stdout.tmp" | od -An -tu1 | tr -d '[:space:]')
    [ "$lastbyte" = 10 ] || return 1

    # Ignore ASCII letter case and line order, but preserve spaces and duplicates.
    tr 'A-Z' 'a-z' <"$stdoutref" | sort >"$TESTDIR/test-expected-sorted.tmp"
    tr 'A-Z' 'a-z' <"$TESTDIR/test-stdout.tmp" | sort >"$TESTDIR/test-stdout-sorted.tmp"
    diff "$TESTDIR/test-expected-sorted.tmp" "$TESTDIR/test-stdout-sorted.tmp" >/dev/null
}

# Colored terminal output.
GREEN=
RED=
RESET=
if [ -t 1 ]; then
    GREEN="\033[1;32m"
    RED="\033[1;31m"
    RESET="\033[0m"
fi

# $1 test id
# $2 test description
# $3 input content (with \n for line breaks)
# $4 expected output (with \n), or !error for an expected input error
# $5-... SUT arguments
# Result: 0=test passed, 1=test failed.
test_case()
{
    local id="$1"
    local desc="$2"
    local inputfile="$TESTDIR/test-input-${id}.tmp"
    local inputcontent="$3"
    local expectedfile="$TESTDIR/test-expected-${id}.tmp"
    local expectedcontent="$4"
    shift 4
    printf '%b' "$inputcontent" >"$inputfile"

    if [ "$expectedcontent" = '!error' ]; then
        run_test "$inputfile" '!error' "$@"
    else
        printf '%b' "$expectedcontent" >"$expectedfile"
        run_test "$inputfile" "$expectedfile" "$@"
    fi
    local result=$?

    if [ "$result" -eq 0 ]; then
        printf '%b✔%b %s\n' "$GREEN" "$RESET" "$desc"
        rm -f "$inputfile" "$expectedfile"
        passed=$((passed + 1))
    else
        printf '%b✘%b %s\n' "$RED" "$RESET" "$desc"
        echo "    Input: $inputfile"
        sed 's/^/        /' <"$inputfile"
        printf '\n    Execution:\n        ./t9search'
        for arg do printf " '%s'" "$arg"; done
        printf ' <"%s"\n' "$inputfile"
        echo "    Expected:"
        if [ "$expectedcontent" = '!error' ]; then
            echo "        Nonzero exit status and an ASCII error message on stderr."
        else
            sed 's/^/        /' <"$expectedfile"
            echo "        Exit status 0; empty stderr; each line ends with LF."
        fi
        echo "    Actual stdout:"
        sed 's/^/        /' <"$TESTDIR/test-stdout.tmp"
        printf '\n    Actual stderr:\n'
        sed 's/^/        /' <"$TESTDIR/test-stderr.tmp"
        printf '\n    Exit status: %s\n' "$status"
        mv "$TESTDIR/test-stdout.tmp" "$TESTDIR/test-stdout-${id}.tmp"
        mv "$TESTDIR/test-stderr.tmp" "$TESTDIR/test-stderr-${id}.tmp"
        failed=$((failed + 1))
    fi
    rm -f "$TESTDIR/test-stdout.tmp" "$TESTDIR/test-stderr.tmp" \
        "$TESTDIR/test-expected-sorted.tmp" "$TESTDIR/test-stdout-sorted.tmp"
    return "$result"
}

# -----------------------------
# Example test cases (not exhaustive). Add your own cases below.
# -----------------------------

# Basic cases.
test_case 1 "bez argumentu" \
"Petr Dvorak\n603123456\nJana Novotna\n777987654\nBedrich Smetana ml.\n541141120\n" \
"Petr Dvorak, 603123456\nJana Novotna, 777987654\nBedrich Smetana ml., 541141120\n"

test_case 2 "cele telefonni cislo" \
"Petr Dvorak\n603123456\n" \
"Petr Dvorak, 603123456\n" \
"603123456"

test_case 3 "jednoduche hledani jmena" \
"Jana\n777987654\n" \
"Jana, 777987654\n" \
"5262"

test_case 4 "nenalezeno" \
"Jana\n777987654\n" \
"Not found\n" \
"111"

# Combined cases: several contacts and more than one matching condition.
test_case 5 "rozliseni podobnych jmen" \
"AD\n111\nxAdx\n111\nA D\n111\nA-D\n111\nA.D\n111\nAxD\n111\nDA\n111\n" \
"AD, 111\nxAdx, 111\n" \
"23"

test_case 6 "ruzna pole kontaktu" \
"Ad\n111\nX\n1234\nA\n311\nAAB\n222\n" \
"Ad, 111\nX, 1234\n" \
"23"

test_case 7 "vice shod v jednom kontaktu" \
"Ad\n111\nX\n1234\nA\n311\nAAB\n222\n" \
"AAB, 222\n" \
"22"

test_case 8 "nula a plus v cisle" \
"Plus\n+420123\nNula\n0420123\nBez\n420123\n" \
"Plus, +420123\nNula, 0420123\n" \
"0420"

# Examples of invalid input.
test_case 9 "necislicovy argument" \
"Eva\n123\n" \
"!error" \
"2a"

test_case 10 "neuplny kontakt" \
"Eva\n" \
"!error" \
"382"

# Length boundaries: line endings are not counted.
test_case 11 "jmeno, cislo a filtr delky 100" \
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111\n" \
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA, 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111\n" \
"2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222"

test_case 12 "radek delky 101 je chyba" \
"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n123\n" \
"!error" \
"2"

# Return failure if any test failed, not only the last one.
printf '\nPassed: %s, failed: %s\n' "$passed" "$failed"
if [ "$failed" -eq 0 ]; then
    rmdir "$TESTDIR"
    exit 0
fi
printf 'Files of failed tests: %s\n' "$TESTDIR"
exit 1
