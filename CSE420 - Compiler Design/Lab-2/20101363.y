%{

#include "symbol_info.h"

#define YYSTYPE symbol_info*

extern YYSTYPE yylval;
extern ofstream outlog;

int lines = 1;  // Initialize lines

%}

%token IF ELSE FOR WHILE DO BREAK CONTINUE RETURN INT FLOAT CHAR VOID DOUBLE SWITCH CASE DEFAULT PRINTLN

%%

start : program
    {
        outlog << "Total lines: " << lines << endl;
    }
    ;

program : program unit
    {
        outlog << "At line no: " << lines << " program : program unit " << endl << endl;
        outlog << $1->getname() + "\n" + $2->getname() << endl << endl;
 
        $$ = new symbol_info($1->getname() + "\n" + $2->getname(), "program");
    }
    | unit
    {

    }
    ;

unit : func_definition
    {

    }
    ;

func_definition : type_specifier ID LPAREN parameter_list RPAREN compound_statement
        {   
            outlog << "At line no: " << lines << " func_definition : type_specifier ID LPAREN parameter_list RPAREN compound_statement " << endl << endl;
            outlog << $1->getname() + " " + $2->getname() + "(" + $4->getname() + ")\n" + $6->getname() << endl << endl;
 
            $$ = new symbol_info($1->getname() + " " + $2->getname() + "(" + $4->getname() + ")\n" + $6->getname(), "func_def"); 
        }
        | type_specifier ID LPAREN RPAREN compound_statement
        {
 
            outlog << "At line no: " << lines << " func_definition : type_specifier ID LPAREN RPAREN compound_statement " << endl << endl;
            outlog << $1->getname() + " " + $2->getname() + "()\n" + $5->getname() << endl << endl;
 
            $$ = new symbol_info($1->getname() + " " + $2->getname() + "()\n" + $5->getname(), "func_def"); 
        }
        ;

type_specifier : INT
    {
        outlog << "At line no: " << lines << " type_specifier : INT " << endl << endl;
        outlog << "int" << endl << endl;
 
        $$ = new symbol_info("int", "type_specifier");
    }
    ;

parameter_list : type_specifier ID
    {
        outlog << "At line no: " << lines << " parameter_list : type_specifier ID " << endl << endl;
        outlog << $1->getname() + " " + $2->getname() << endl << endl;
 
        $$ = new symbol_info($1->getname() + " " + $2->getname(), "parameter_list");
    }
    ;

compound_statement : LCURL statements RCURL
    {
        outlog << "{" + $2->getname() + "}" << endl;
 
        $$ = new symbol_info("{" + $2->getname() + "}", "compound_statement");
    }
    ;

statements : statement
    {
        outlog << $1->getname() << endl;
 
        $$ = new symbol_info($1->getname(), "statements");
    }
    | statements statement
    {
        outlog << $1->getname() << $2->getname() << endl;
 
        $$ = new symbol_info($1->getname() + $2->getname(), "statements");
    }
    ;

statement : PRINTLN LPAREN ID RPAREN SEMICOLON
    {
        outlog << "printf(" + $3->getname() + ");" << endl;
 
        $$ = new symbol_info("printf(" + $3->getname() + ");", "statement");
    }
    ;

%%

void yyerror(const char* s) {
    cout << "Error: " << s << endl;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        cout << "Usage: " << argv[0] << " <input_file>" << endl;
        return 1;
    }

    yyin = fopen(argv[1], "r");
    outlog.open("my_log.txt", ios::trunc);

    if (yyin == NULL) {
        cout << "Couldn't open file" << endl;
        return 1;
    }

    yyparse();

    outlog.close();

    fclose(yyin);

    return 0;
}
