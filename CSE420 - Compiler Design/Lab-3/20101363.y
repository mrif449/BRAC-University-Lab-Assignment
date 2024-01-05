%{
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fstream>
#include "symbol_info.h"
#include "TreeNode.h"
#define YYSTYPE symbol_info*

extern int yyparse(void);
extern int yylex(void);

extern FILE *yyin;

extern YYSTYPE yylval;

std::ofstream outlog;

int lines = 1;

TreeNode* rootNode = nullptr;

void yyerror(const char *s)
{
    outlog << "At line " << lines << " " << s << std::endl << std::endl;
}

%}

%token IF ELSE FOR WHILE DO BREAK INT CHAR FLOAT DOUBLE VOID RETURN SWITCH CASE DEFAULT CONTINUE PRINTF ADDOP MULOP INCOP DECOP RELOP ASSIGNOP LOGICOP NOT LPAREN RPAREN LCURL RCURL LTHIRD RTHIRD COMMA SEMICOLON CONST_INT CONST_FLOAT ID

%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%start program

%%

program : program unit
	{
		TreeNode* factorNode = TreeNode::createNonTerminalNode("program");
		factorNode->addChild($1->getNode());
		factorNode->addChild($2->getNode());
		$$ = new symbol_info("program", "non_terminal", factorNode);
		rootNode = factorNode;
	}
	| unit
	{
		TreeNode* factorNode = TreeNode::createNonTerminalNode("program");
		factorNode -> addChild($1->getNode());
		$$ = new symbol_info("program", "non_terminal", factorNode);
		rootNode = factorNode;                                
	}
	;

unit : var_declaration
	 {
		TreeNode* factorNode = TreeNode::createNonTerminalNode("unit");
		factorNode -> addChild($1->getNode());
		$$ = new symbol_info("unit", "non_terminal",factorNode);
		
	 }
     | func_definition
     {
		TreeNode* factorNode = TreeNode::createNonTerminalNode("unit");
		factorNode -> addChild($1->getNode());
		$$ = new symbol_info("unit", "non_terminal",factorNode);
		
	 }
     ;

func_definition : type_specifier id_name LPAREN parameter_list RPAREN compound_statement
		{	
			TreeNode* factorNode = TreeNode::createNonTerminalNode("func_definition"); /// WILL THERE
			factorNode -> addChild($1->getNode());
			factorNode -> addChild($2->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("LPAREN", "("));
			factorNode -> addChild($4->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("RPAREN", ")"));
			factorNode -> addChild($6->getNode());
			$$ = new symbol_info("func_definition", "non_terminal", factorNode); /// WILL THERE 
		}
		| type_specifier id_name LPAREN RPAREN compound_statement 
		{
			TreeNode* factorNode = TreeNode::createNonTerminalNode("func_definition");
			factorNode -> addChild($1->getNode());
			factorNode -> addChild($2->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("LPAREN", "("));
			factorNode -> addChild(TreeNode::createTerminalNode("RPAREN", ")"));
			factorNode -> addChild($5->getNode());
			$$ = new symbol_info("func_definition", "non_terminal", factorNode);
			
		}
 		;

parameter_list : parameter_list COMMA type_specifier ID
		{
			TreeNode* factorNode = TreeNode::createNonTerminalNode("parameter_list");
			factorNode -> addChild($1->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("COMMA", ","));
			factorNode -> addChild($3->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("ID", "id"));
			$$ = new symbol_info("parameter_list", "non_terminal", factorNode);
		}
		| parameter_list COMMA type_specifier
		{
			TreeNode* factorNode = TreeNode::createNonTerminalNode("parameter_list");
			factorNode -> addChild($1->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("COMMA", ","));
			factorNode -> addChild($3->getNode());
			$$ = new symbol_info("parameter_list", "non_terminal", factorNode);
		}
 		| type_specifier ID
 		{
			TreeNode* factorNode = TreeNode::createNonTerminalNode("parameter_list");
			factorNode -> addChild($1->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("ID", "id"));
			$$ = new symbol_info("parameter_list", "non_terminal", factorNode);
		}
		| type_specifier
		{
			TreeNode* factorNode = TreeNode::createNonTerminalNode("parameter_list");
			factorNode -> addChild($1->getNode());
			$$ = new symbol_info("parameter_list", "non_terminal", factorNode);
		}
 		;

compound_statement : LCURL statements RCURL
		{ 
 			TreeNode* factorNode = TreeNode::createNonTerminalNode("compound_statement");
			factorNode -> addChild(TreeNode::createTerminalNode("LCURL", $1->getname().c_str()));
			factorNode -> addChild($2->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("RCURL", $3->getname().c_str()));
			$$ = new symbol_info("compound_statement", "non_terminal", factorNode);
		}
		| LCURL RCURL
		{ 
 			TreeNode* factorNode = TreeNode::createNonTerminalNode("compound_statement");
			factorNode -> addChild(TreeNode::createTerminalNode("LCURL", $1->getname().c_str()));
			factorNode -> addChild(TreeNode::createTerminalNode("RCURL", $2->getname().c_str()));
			$$ = new symbol_info("compound_statement", "non_terminal", factorNode);
		}
		;
var_declaration : type_specifier declaration_list SEMICOLON
		{
			TreeNode* factorNode = TreeNode::createNonTerminalNode("var_declaration");
			factorNode -> addChild($1->getNode());
			factorNode -> addChild($2->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("SEMICOLON", ":"));
			$$ = new symbol_info("var_declaration", "non_terminal", factorNode);
		}
		;
type_specifier : INT
		{
			$$ = new symbol_info("type", "terminal", TreeNode::createTerminalNode("type", "int"));
		}
		| FLOAT
		{
			$$ = new symbol_info("type", "terminal", TreeNode::createTerminalNode("type", "float"));
		}
		| VOID
		{
			$$ = new symbol_info("type", "terminal", TreeNode::createTerminalNode("type", "void"));
		}
		;
declaration_list : declaration_list COMMA id_name
		{
			TreeNode* factorNode = TreeNode::createNonTerminalNode("declaration_list");
			factorNode -> addChild($1->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("COMMA", ","));
			factorNode -> addChild(TreeNode::createTerminalNode("id_name",   $3->getname().c_str()));
			$$ = new symbol_info("declaration_list", "non_terminal", factorNode);
		}
		| declaration_list COMMA id_name LTHIRD CONST_INT RTHIRD //array after some declaration
		{
			TreeNode* factorNode = TreeNode::createNonTerminalNode("declaration_list");
			factorNode ->addChild($1->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("COMMA", ","));
			factorNode -> addChild(TreeNode::createTerminalNode("id_name",   $3->getname().c_str()));
			factorNode -> addChild(TreeNode::createTerminalNode("LTHIRD", $4->getname().c_str()));
			factorNode -> addChild(TreeNode::createTerminalNode("id_name",   $5->getname().c_str()));
			factorNode -> addChild(TreeNode::createTerminalNode("RTHIRD", $6->getname().c_str()));
			$$ = new symbol_info("declaration_list", "non_terminal", factorNode);
		}
		| id_name
		{
			$$ = new symbol_info("declaration_list", "terminal", TreeNode::createTerminalNode("declaration_list",  $1->getname().c_str()));

		}
		| id_name LTHIRD CONST_INT RTHIRD //array
		{
			TreeNode* factorNode = TreeNode::createNonTerminalNode("declaration_list");
			factorNode -> addChild(TreeNode::createTerminalNode("id_name",   $1->getname().c_str()));
			factorNode -> addChild(TreeNode::createTerminalNode("LTHIRD",   $2->getname().c_str()));
			factorNode -> addChild(TreeNode::createTerminalNode("CONST_INT",   $3->getname().c_str()));
			factorNode -> addChild(TreeNode::createTerminalNode("RTHIRD",   $4->getname().c_str()));
			$$ = new symbol_info("declaration_list", "non_terminal", factorNode);

		}
		;
id_name : ID
		{
			$$ = new symbol_info("id", "terminal", TreeNode::createTerminalNode("id", $1->getname().c_str()));
		}
		;
statements : statement
		{
			TreeNode* factorNode = TreeNode::createNonTerminalNode("statements");
			factorNode -> addChild($1->getNode());
			$$ = new symbol_info("statements", "non_terminal", factorNode);
		}
		| statements statement
		{
			TreeNode* factorNode = TreeNode::createNonTerminalNode("statements");
			factorNode -> addChild($1->getNode());
			factorNode -> addChild($2->getNode());
			$$ = new symbol_info("statements", "non_terminal", factorNode);
		}
		;


statement : var_declaration
	  {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("statement");
			factorNode -> addChild($1->getNode());
			$$ = new symbol_info("statement", "non_terminal", factorNode);
	  }
	  | expression_statement
	  {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("statement");
			factorNode -> addChild($1->getNode());
			$$ = new symbol_info("statement", "non_terminal", factorNode);
	  }
	  | compound_statement
	  {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("statement");
			factorNode -> addChild($1->getNode());
			$$ = new symbol_info("statement", "non_terminal", factorNode);
	  }
	  | FOR LPAREN expression_statement expression RPAREN statement
	  {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("statement");
			factorNode -> addChild(TreeNode::createTerminalNode("FOR",   "FOR"));
			factorNode -> addChild(TreeNode::createTerminalNode("LPAREN",   "("));
			factorNode -> addChild($3->getNode());
			factorNode -> addChild($4->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("RPAREN",   ")"));
			factorNode -> addChild($6->getNode());
			$$ = new symbol_info("statement", "non_terminal", factorNode);
	  }
	  | IF LPAREN expression RPAREN statement %prec LOWER_THAN_ELSE
	  {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("statement");
			factorNode -> addChild(TreeNode::createTerminalNode("IF",   "FOR"));
			factorNode -> addChild(TreeNode::createTerminalNode("LPAREN",   "("));
			factorNode -> addChild($3->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("RPAREN",   ")"));
			factorNode -> addChild($5->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("LOWER_THAN_ELSE",   "ELSE"));
			$$ = new symbol_info("statement", "non_terminal", factorNode);
	  }
	  | IF LPAREN expression RPAREN statement ELSE statement
	  {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("statement");
			factorNode -> addChild(TreeNode::createTerminalNode("IF",   "IF"));
			factorNode -> addChild(TreeNode::createTerminalNode("LPAREN",   "("));
			factorNode -> addChild($3->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("RPAREN",   ")"));
			factorNode -> addChild($5->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("ELSE",   "ELSE"));
			factorNode -> addChild($7->getNode());
			$$ = new symbol_info("statement", "non_terminal", factorNode);
	  }
	  | WHILE LPAREN expression RPAREN statement
	  {
 	     	TreeNode* factorNode = TreeNode::createNonTerminalNode("statement");
			factorNode -> addChild(TreeNode::createTerminalNode("WHILE",   "WHILE"));
			factorNode -> addChild(TreeNode::createTerminalNode("LPAREN",   "("));
			factorNode -> addChild($3->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("RPAREN",   ")"));
			factorNode -> addChild($5->getNode());
 
	 		$$ = new symbol_info("statement", "non_terminal", factorNode);
	  }
	  | PRINTF LPAREN id_name RPAREN SEMICOLON
	  {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("statement");
			factorNode -> addChild(TreeNode::createTerminalNode("PRINTF",   "printf"));
			factorNode -> addChild(TreeNode::createTerminalNode("LPAREN",   "("));
			factorNode -> addChild(TreeNode::createTerminalNode("id_name",  $3->getname()));
			factorNode -> addChild(TreeNode::createTerminalNode("RPAREN",   ")"));
			factorNode -> addChild(TreeNode::createTerminalNode("SEMICOLON",   ":"));
			$$ = new symbol_info("statement", "non_terminal", factorNode);
	  }
	  | RETURN expression SEMICOLON
	  {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("statement");
			factorNode -> addChild(TreeNode::createTerminalNode("RETURN",   "return"));
			factorNode -> addChild($2->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("SEMICOLON",   ":"));
			$$ = new symbol_info("statement", "non_terminal", factorNode);
	  }
	  ;

expression_statement : SEMICOLON
			{
				 $$ = $1;
	        }			
			| expression SEMICOLON 
			{
				TreeNode* factorNode = TreeNode::createNonTerminalNode("expression_statement");
				factorNode->addChild(TreeNode::createTerminalNode("SEMICOLON",   ":"));
				$$ = new symbol_info("expression_statement", "non_terminal", factorNode);

	        }
			;

variable : id_name 	
     {
	    $$ = $1;
	 }	
	 | id_name LTHIRD expression RTHIRD 
	 {
	 	TreeNode* factorNode = TreeNode::createNonTerminalNode("variable");
		factorNode -> addChild(TreeNode::createTerminalNode("id_name",   $1->getname().c_str()));
		factorNode -> addChild(TreeNode::createTerminalNode("LTHIRD",   $2->getname().c_str()));
		factorNode -> addChild($3->getNode());
		factorNode -> addChild(TreeNode::createTerminalNode("RTHIRD",   $4->getname().c_str()));
		$$ = new symbol_info("variable", "non_terminal", factorNode);
	 }
	 ;

expression : logic_expression //expr can be void
	   {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("expression");
			factorNode->addChild($1->getNode());
			$$ = new symbol_info("expression", "non_terminal", factorNode);
	   }
	   | variable ASSIGNOP logic_expression 	
	   {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("expression");
			factorNode ->addChild($1->getNode());
			factorNode ->addChild(TreeNode::createTerminalNode("ASSIGNOP",   "="));
			factorNode ->addChild($3->getNode());
			$$ = new symbol_info("expression", "non_terminal", factorNode);
	   }
	   ;

logic_expression : rel_expression //lgc_expr can be void
	     {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("logic_expression");
			factorNode->addChild($1->getNode());
			$$ = new symbol_info("logic_expression", "non_terminal", factorNode);
	     }	
		 | rel_expression LOGICOP rel_expression 
		 {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("logic_expression");
			factorNode -> addChild($1->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("RTHIRD",   $2->getname().c_str()));
			factorNode -> addChild($3->getNode());
			$$ = new symbol_info("logic_expression", "non_terminal", factorNode);
	     }	
		 ;

rel_expression	: simple_expression //rel_expr can be void
		{
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("rel_expression");
			factorNode -> addChild($1->getNode());
			$$ = new symbol_info("rel_expression", "non_terminal", factorNode);
	    }
		| simple_expression RELOP simple_expression
		{
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("rel_expression");
			factorNode -> addChild($1->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("RELOP",   $2->getname().c_str()));
			factorNode -> addChild($3->getNode());
			$$ = new symbol_info("rel_expression", "non_terminal", factorNode);
	    }
		;

simple_expression : term //simp_expr can be void /// WILL THERE
          {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("simple_expression");
			factorNode->addChild($1->getNode());
			$$ = new symbol_info("simple_expression", "non_terminal", factorNode);
	      }
		  | simple_expression ADDOP term 
		  {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("simple_expression");
			factorNode -> addChild($1->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("ADDOP", $2->getname().c_str()));
			factorNode -> addChild($3->getNode());
			$$ = new symbol_info("simple_expression", "non_terminal", factorNode);
	      }
		  ;             ////////WILL THERE

term :	unary_expression //term can be void because of un_expr->factor
     {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("term");
			factorNode->addChild($1->getNode());
			$$ = new symbol_info("term", "non_terminal", factorNode);
	 }
     |  term MULOP unary_expression
     {
	    	TreeNode* factorNode = TreeNode::createNonTerminalNode("term");
			factorNode -> addChild($1->getNode());
			factorNode -> addChild(TreeNode::createTerminalNode("MULOP",$2->getname().c_str()));
			factorNode -> addChild($3->getNode());
			$$ = new symbol_info("term", "non_terminal", factorNode);
	 }
     ;

unary_expression : ADDOP unary_expression  // un_expr can be void because of factor
		 {
	    	TreeNode* expressionNode = TreeNode::createNonTerminalNode("unary_expression");
			expressionNode->addChild(TreeNode::createTerminalNode("ADDOP", $1->getname().c_str()));
			expressionNode->addChild($2->getNode());
			$$ = new symbol_info("unary_expression", "non_terminal", expressionNode);

	     }
		 | NOT unary_expression 
		 {
	    	TreeNode* expressionNode = TreeNode::createNonTerminalNode("unary_expression");
			expressionNode->addChild(TreeNode::createTerminalNode("NOT", $1->getname().c_str()));
			expressionNode->addChild($2->getNode());
			$$ = new symbol_info("unary_expression", "non_terminal", expressionNode);

	     }
		 | factor 
		 {
	    	$$ = $1;
	     }
		 ;


factor : variable  // factor can be void
    {
	    $$ = $1;
	}
	| id_name LPAREN argument_list RPAREN
	{
	   		TreeNode* factorNode = TreeNode::createNonTerminalNode("factor");
			factorNode->addChild(TreeNode::createTerminalNode("id_name", $1->getname().c_str()));
			factorNode->addChild(TreeNode::createTerminalNode("LPAREN", "("));
			factorNode->addChild($3->getNode());
			factorNode->addChild(TreeNode::createTerminalNode("RPAREN", ")"));
			$$ = new symbol_info("factor", "non_terminal", factorNode);

	}
	| LPAREN expression RPAREN
	{
	   		TreeNode* factorNode = TreeNode::createNonTerminalNode("factor");
			factorNode->addChild(TreeNode::createTerminalNode("LPAREN", "("));
			factorNode->addChild($2->getNode());
			factorNode->addChild(TreeNode::createTerminalNode("RPAREN", ")"));
			$$ = new symbol_info("factor", "non_terminal", factorNode);

	}
	| CONST_INT 
	{
	    $$ = new symbol_info("const_int", "terminal", TreeNode::createTerminalNode("const_int", $1->getname().c_str()));
	}
	| CONST_FLOAT
	{
	    $$ = new symbol_info("const_float", "terminal", TreeNode::createTerminalNode("const_float", $1->getname().c_str()));
	}
	| variable I+
	NCOP 
	{
	    TreeNode* factorNode = TreeNode::createNonTerminalNode("increment_expression");
		factorNode->addChild($1->getNode());
		factorNode->addChild(TreeNode::createTerminalNode("INCOP", "++"));
		$$ = new symbol_info("increment_expression", "non_terminal", factorNode);
	}
	| variable DECOP
	{
	    TreeNode* factorNode = TreeNode::createNonTerminalNode("decrement_expression");
		factorNode->addChild($1->getNode());
		factorNode->addChild(TreeNode::createTerminalNode("DECOP", "--"));
		$$ = new symbol_info("decrement_expression", "non_terminal", factorNode);
	}
	;

argument_list : arguments         /// WILL THERE
			  {
					$$ = $1;
			  }
			  |
			  {
			  }
			  ;/////// THERE

arguments : arguments COMMA logic_expression
		  {
				TreeNode* factorNode = TreeNode::createNonTerminalNode("argument_list");
				factorNode->addChild($1->getNode());
				factorNode->addChild(TreeNode::createTerminalNode("COMMA", ","));
				factorNode->addChild($3->getNode());
				$$ = new symbol_info("argument_list", "non_terminal", factorNode);
		  }
	      | logic_expression
	      {
				TreeNode* factorNode = TreeNode::createNonTerminalNode("argument_list");
				factorNode->addChild($1->getNode());
				$$ = new symbol_info("argument_list", "non_terminal", factorNode);
		  }
	      ;
%%

int main(int argc, char *argv[])
{
    if (argc != 2) 
    {
        std::cout << "Please input file name" << std::endl;
        return 0;
    }
    yyin = fopen(argv[1], "r");
    outlog.open("20101363_log.txt", std::ios::trunc);

    if (yyin == NULL)
    {
        std::cout << "Couldn't open file" << std::endl;
        return 0;
    }

    yyparse();

    if (rootNode) {
        rootNode->postOrderTraversal(outlog);
    }

    outlog.close();
    fclose(yyin);

    return 0;
}