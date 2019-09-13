from PyQt5.QtWidgets import *
from MainWindow import Ui_MainWindow
from GoogleFreeTrans import Translator
import lexer
try:
    from googletrans import Translator
    GOOGLE_TRANSLATE_AVAILABLE = True

except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.destTextEdit.setReadOnly(True)

        if GOOGLE_TRANSLATE_AVAILABLE:
            self.srcLanguage.currentTextChanged[str].connect(self.update_src_language)
        else:
            self.srcLanguage.hide()

        self.translateButton.pressed.connect(self.translate)

        self.show()


    def translate(self):
        translator = Translator.translator('fa', 'en')
        key_word = {"اگر": "if", "وگر": "elif", "وگرنه": "else", "واردکن": "import", "کلاس": "class",
                    "تعریف": "def", "تازمانیکه": "while", "برای": "for", "در": "in", "نه": "not",
                    "و": "and", "یا": "or", "برگردان": "return", "چاپ": "print", "ادامه": "continue", "توقف": "break"}
        sybols = [":", "<", "<", "=", "==", "+", "_", "*", "**", "(", ")", "[", "]", "{", "}", "\\", "\"", "\'", "\n",
                  "<=",
                  "<>", ">=", "#", ""]

        codeTextPersian = self.srcTextEdit.toPlainText()
        codeWordsPersian = codeTextPersian.replace(" ", " s ").replace("\n", " n ").replace("\t", " t ").split(" ")
        englishCode = ""
        word_dict = {}
        for word in codeWordsPersian:
            if word in key_word.keys():
                word_dict[key_word[word]] = word
                englishCode += key_word[word]
            elif word in sybols:
                word_dict[word] = word
                englishCode += word
            elif word == "s":
                englishCode += " "
            elif word == "n":
                englishCode += "\n"
            elif word == "t":
                englishCode += "\t"
            else:

                newWord = 'ـ'.join(translator.translate(word).split(" "))
                word_dict[newWord] = word
                englishCode += newWord
        print(word_dict)
        lex = lexer.lexer(englishCode)
        lex = lex.split("\n")
        finalCode = ""
        for line in lex:
            l = line.split(" |")
            if l[0] in word_dict.keys():
                if len(l) > 1:

                    finalCode += str(word_dict[l[0]]) + " |" + l[1] + "\n"
        self.destTextEdit.setPlainText(finalCode)
        finalFile = open("englishCode.txt", "w")
        finalFile.write(englishCode)




if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    app.exec_()