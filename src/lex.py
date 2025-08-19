import enum

valid_ident = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' #Valid variable names in Tiny BASIC (A-Z)

class Lexer:
    def __init__(self, input):
        self.source = input + '\n'
        self.currentPos = -1
        self.currentChar = ''
        self.nextChar()

    def nextChar(self):
        self.currentPos += 1 #Moves currentPos to the next character
        if self.currentPos >= len(self.source) :
            self.currentChar = '\0' #end of file character
        else:
            self.currentChar = self.source[self.currentPos]

    def peek(self):
        if self.currentPos + 1 >= len(self.source):
            return '\0'
        else:
            return self.source[self.currentPos + 1] # Returns the character after currentPos

    def abort(self, message):
        print(f"Sintax Error: {message}")

    def skipComments(self):
        if self.currentChar == '#':
            while self.currentChar != '\n':
                self.nextChar()

    def skipWhitespace(self):
        while self.currentChar == ' ':
            self.nextChar()

    def getToken(self):
        self.skipWhitespace()
        self.skipComments()
        token = None

        if self.currentChar == '+':
            token = Token(TokenType.PLUS, self.currentChar)
        elif self.currentChar == '-':
            token = Token(TokenType.MINUS, self.currentChar)
        elif self.currentChar == '*':
            token = Token(TokenType.ASTERISK, self.currentChar)
        elif self.currentChar == '/':
            token = Token(TokenType.SLASH, self.currentChar)
        elif self.currentChar == '\n':
            token = Token(TokenType.NEWLINE, self.currentChar)
        elif self.currentChar == '\0':
            token = Token(TokenType.EOF, self.currentChar)
            return token
        elif self.currentChar == '\"':
            startPos = self.currentPos
            self.nextChar() #So it can enter the while loop
            while self.currentChar != '\"':
                if self.currentPos < len(self.source):
                    self.nextChar()
                else:
                    abortMessage = "Unterminated string literal"
                    self.abort(abortMessage)
                    return None
            token = Token(TokenType.STRING, self.source[startPos : self.currentPos + 1])

        elif self.currentChar == '=':
            if self.peek() == '=':
                self.nextChar()
                token = Token(TokenType.EQEQ, "==")
            else:
                token = Token(TokenType.EQ, self.currentChar)

        elif self.currentChar == '<':
            if self.peek() == '=':
                self.nextChar()
                token = Token(TokenType.LTEQ, "<=")
            else:
                token = Token(TokenType.LT, self.currentChar)

        elif self.currentChar == '>':
            if self.peek() == '=':
                self.nextChar()
                token = Token(TokenType.GTEQ, ">=")
            else:
                token = Token(TokenType.GT, self.currentChar)

        elif self.currentChar == '!':
            if self.peek() == '=':
                self.nextChar()
                token = Token(TokenType.NOTEQ, "!=")
            else:
                abortMessage = f"Invalid character next to !: {self.currentChar} .Expected ="
                self.abort(abortMessage)

        elif self.currentChar.isdigit():
            startPos = self.currentPos
            while self.peek().isdigit():
                self.nextChar()
            token = Token(TokenType.NUMBER,self.source[startPos : self.currentPos + 1])
        elif self.currentChar.isalpha():
            startPos = self.currentPos
            while self.peek().isalpha():
                self.nextChar()
            if startPos == self.currentPos and self.currentChar in valid_ident:
                token = Token(TokenType.IDENT, self.currentChar)
            else:
                matchedToken = Token.checkKeyword(self.source[startPos : self.currentPos + 1])
                if matchedToken:
                    token = Token(matchedToken, self.source[startPos : self.currentPos + 1])
                else:
                    abortMessage = f"Keyword not found: {self.source[startPos : self.currentPos + 1]}"
                    self.abort(abortMessage)

        self.nextChar()
        return token





class Token:

    def __init__(self, kind , text):
        self.kind = kind 
        self.value = text 

    @staticmethod
    def checkKeyword(name):
        for token in TokenType:
            if token.name == name and (token.value > 100 and token.value < 201):
                return token
        return None

class TokenType(enum.Enum):
    # DEFINE THE TOKEN TYPES
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3

    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    GOSUB = 108
    RETURN = 109
    END = 110

    # Operators.
    EQ = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211

