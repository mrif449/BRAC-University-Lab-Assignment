%option noyywrap

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

FILE* yyoutlog;
int lines = 1;

char* intToString(int num) {
    char* str = (char*)malloc(12);  // Sufficient for 32-bit integers
    snprintf(str, 12, "%d", num);
    return str;
}
%}

%%

[ \t]        {/* Ignore whitespace and tabs */ }

\n           {
                lines++;
              }

"if"          { fprintf(yyoutlog, "Line No. %s: Token <IF> Lexeme if found\n", intToString(lines)); }
"else"        { fprintf(yyoutlog, "Line No. %s: Token <ELSE> Lexeme else found\n", intToString(lines)); }

[a-zA-Z_][a-zA-Z0-9_]* {
                fprintf(yyoutlog, "Line No. %s: Token <ID> Lexeme %s found\n", intToString(lines), yytext);
              }

[0-9]+        {
                fprintf(yyoutlog, "Line No. %s: Token <CONST_INT> Lexeme %s found\n", intToString(lines), yytext);
              }

[0-9]+"."[0-9]+ {
                fprintf(yyoutlog, "Line No. %s: Token <CONST_FLOAT> Lexeme %s found\n", intToString(lines), yytext);
              }

[+\-]         {
                fprintf(yyoutlog, "Line No. %s: Token <ADDOP> Lexeme %s found\n", intToString(lines), yytext);
              }

"("          { fprintf(yyoutlog, "Line No. %s: Token <LPAREN> Lexeme ( found\n", intToString(lines)); }
")"          { fprintf(yyoutlog, "Line No. %s: Token <RPAREN> Lexeme ) found\n", intToString(lines)); }
"{"          { fprintf(yyoutlog, "Line No. %s: Token <LCURL> Lexeme { found\n", intToString(lines)); }
"}"          { fprintf(yyoutlog, "Line No. %s: Token <RCURL> Lexeme } found\n", intToString(lines)); }
"="          { fprintf(yyoutlog, "Line No. %s: Token <ASSIGNOP> Lexeme = found\n", intToString(lines)); }
":"          { fprintf(yyoutlog, "Line No. %s: Token <COLON> Lexeme : found\n", intToString(lines)); }
","          { fprintf(yyoutlog, "Line No. %s: Token <COMMA> Lexeme , found\n", intToString(lines)); }

.            { /* Ignore any other characters */ }

%%

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Please input file name\n");
        return 0;
    }

    yyin = fopen(argv[1], "r");

    if (yyin == NULL) {
        printf("File does not exist\n");
        return 0;
    }

    yyoutlog = fopen("20101363_log.txt", "w");

    yylex();

    fprintf(yyoutlog, "Total lines: %d\n", lines);

    fclose(yyoutlog);
    fclose(yyin);

    return 0;
}