lexer grammar AdvLexer;

L_SQBR: '[';
R_SQBR: ']';
EQUAL: '=';
ESCA_L_BRACE: '\\{';

TITLE: 'title';

fragment ASCII_CHAR: [a-z#A-Z0-9_{}\-];
/*
 fragment JAPANESE: [\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}]; fragment CHINESE:
 '\u4E00' ..'\u9FA5'; fragment SPECIAL_CHARS: [　、ー…―え？！。（）～♪{}];
 */
fragment SPECIAL_CHARS: [　];
fragment NON_ASCII: ~('\u0000' .. '\u00ff');
fragment LINE_BREAK: '\\n';
WS: [ \t\r\n]+ -> skip;

// ---------- in json ----------
COMMA: ',';
DOT: '.';
COLON: ':';
ESCA_R_BRACE: '\\}';

J_STRING: '"' (J_ESC | J_SAFECODEPOINT)* '"';

fragment J_ESC: '\\' (["\\/bfnrt] | J_UNICODE);
fragment J_UNICODE: 'u' J_HEX J_HEX J_HEX J_HEX;
fragment J_HEX: [0-9a-fA-F];
fragment J_SAFECODEPOINT: ~ ["\\\u0000-\u001F];

J_NUMBER: '-'? J_INT ('.' [0-9]+)? J_EXP?;

fragment J_INT: '0' | [1-9] [0-9]*;

// no leading zeros

fragment J_EXP: [Ee] [+\-]? J_INT;

J_TRUE: 'true';
J_FALSE: 'false';
J_NULL: 'null';

// ------ default rules ------
CHAR: ASCII_CHAR | SPECIAL_CHARS | NON_ASCII | LINE_BREAK;

// TODO: split IDENTIFIER and TEXT
IDENTIFIER: CHAR+;