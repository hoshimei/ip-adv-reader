parser grammar AdvParser;

options {
	tokenVocab = AdvLexer;
}

script: line*;

line: item | title_item;

item: L_SQBR IDENTIFIER key_value* R_SQBR;

title_item: L_SQBR TITLE TITLE EQUAL IDENTIFIER+ R_SQBR;

key_value: IDENTIFIER EQUAL value;

value: IDENTIFIER | item | json;

json: j_value;

j_obj:
	ESCA_L_BRACE j_pair (COMMA j_pair)* ESCA_R_BRACE
	| ESCA_L_BRACE ESCA_R_BRACE;

j_pair: J_STRING COLON j_value;

j_arr: L_SQBR j_value (COMMA j_value)* R_SQBR | L_SQBR R_SQBR;

j_value:
	J_STRING
	| J_NUMBER
	| j_obj
	| j_arr
	| J_TRUE
	| J_FALSE
	| J_NULL;
