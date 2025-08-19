from lex import Lexer,  TokenType 

def main():
    code = "10 IF A == 20 GOTO 100 \n 20 PRINT \"Hola\" # nice code :D"
    lexer = Lexer(code)
    token = lexer.getToken()
    while (token and (token.kind != TokenType.EOF)):
        print(token.kind)
        token = lexer.getToken()

    return


if __name__ == "__main__":
    main()

