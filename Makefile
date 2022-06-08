P ?= script
NAME := Adv
LEXER := $(NAME)Lexer
PARSER := $(NAME)Parser

$(LEXER).class: $(LEXER).java
	javac -cp "/usr/share/java/antlr-4.10.1-complete.jar:$CLASSPATH" $<

$(PARSER).class: $(PARSER).java $(LEXER).java
	javac -cp "/usr/share/java/antlr-4.10.1-complete.jar:$CLASSPATH" $<

$(LEXER).java: $(LEXER).g4
	antlr4 $(LEXER).g4

$(PARSER).java: $(LEXER).g4
	antlr4 $(PARSER).g4

all: $(PARSER).class $(LEXER).class

test_all:
	bash test_all.sh

python: $(PARSER).g4 $(LEXER).g4
	antlr4 -Dlanguage=Python3 *.g4

run: $(LEXER).class $(PARSER).class
	grun $(NAME) $P -tree

run_gui: $(LEXER).class $(PARSER).class
	grun $(NAME) $P -gui

clean:
	rm -f *.class *.java *.tokens *.interp