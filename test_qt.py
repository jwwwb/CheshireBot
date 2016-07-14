# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, uic
import test_cl


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('ui_design.ui', self)
        self.perft = test_cl.PerfTester()
        self.field_selected = False
        self.showing_moves = False
        self.legal_fields = []
        for row in range(20, 100, 10):
            for field in range(1, 9):
                self.legal_fields.append(row+field)
        self.set_up_ui()
        self.pushButtonUndo.clicked.connect(self.undo)
        self.pushButtonPrintMoves.clicked.connect(self.print_moves)
        self.pushButtonShowMoves.clicked.connect(self.show_moves)
        self.pushButtonPerft.clicked.connect(self.test_perft)
        self.pushButtonSplitPerft.clicked.connect(self.split_perft)
        self.pushButtonLoad.clicked.connect(self.load_fen)
        self.pushButtonState.clicked.connect(self.print_state)

    # beginning of auto-generated code #
    def set_up_ui(self):
        self.F21.clicked.connect(self.clicked21)
        self.F21.setStyleSheet("background-color: grey")
        self.F22.clicked.connect(self.clicked22)
        self.F22.setStyleSheet("background-color: white")
        self.F23.clicked.connect(self.clicked23)
        self.F23.setStyleSheet("background-color: grey")
        self.F24.clicked.connect(self.clicked24)
        self.F24.setStyleSheet("background-color: white")
        self.F25.clicked.connect(self.clicked25)
        self.F25.setStyleSheet("background-color: grey")
        self.F26.clicked.connect(self.clicked26)
        self.F26.setStyleSheet("background-color: white")
        self.F27.clicked.connect(self.clicked27)
        self.F27.setStyleSheet("background-color: grey")
        self.F28.clicked.connect(self.clicked28)
        self.F28.setStyleSheet("background-color: white")
        self.F31.clicked.connect(self.clicked31)
        self.F31.setStyleSheet("background-color: white")
        self.F32.clicked.connect(self.clicked32)
        self.F32.setStyleSheet("background-color: grey")
        self.F33.clicked.connect(self.clicked33)
        self.F33.setStyleSheet("background-color: white")
        self.F34.clicked.connect(self.clicked34)
        self.F34.setStyleSheet("background-color: grey")
        self.F35.clicked.connect(self.clicked35)
        self.F35.setStyleSheet("background-color: white")
        self.F36.clicked.connect(self.clicked36)
        self.F36.setStyleSheet("background-color: grey")
        self.F37.clicked.connect(self.clicked37)
        self.F37.setStyleSheet("background-color: white")
        self.F38.clicked.connect(self.clicked38)
        self.F38.setStyleSheet("background-color: grey")
        self.F41.clicked.connect(self.clicked41)
        self.F41.setStyleSheet("background-color: grey")
        self.F42.clicked.connect(self.clicked42)
        self.F42.setStyleSheet("background-color: white")
        self.F43.clicked.connect(self.clicked43)
        self.F43.setStyleSheet("background-color: grey")
        self.F44.clicked.connect(self.clicked44)
        self.F44.setStyleSheet("background-color: white")
        self.F45.clicked.connect(self.clicked45)
        self.F45.setStyleSheet("background-color: grey")
        self.F46.clicked.connect(self.clicked46)
        self.F46.setStyleSheet("background-color: white")
        self.F47.clicked.connect(self.clicked47)
        self.F47.setStyleSheet("background-color: grey")
        self.F48.clicked.connect(self.clicked48)
        self.F48.setStyleSheet("background-color: white")
        self.F51.clicked.connect(self.clicked51)
        self.F51.setStyleSheet("background-color: white")
        self.F52.clicked.connect(self.clicked52)
        self.F52.setStyleSheet("background-color: grey")
        self.F53.clicked.connect(self.clicked53)
        self.F53.setStyleSheet("background-color: white")
        self.F54.clicked.connect(self.clicked54)
        self.F54.setStyleSheet("background-color: grey")
        self.F55.clicked.connect(self.clicked55)
        self.F55.setStyleSheet("background-color: white")
        self.F56.clicked.connect(self.clicked56)
        self.F56.setStyleSheet("background-color: grey")
        self.F57.clicked.connect(self.clicked57)
        self.F57.setStyleSheet("background-color: white")
        self.F58.clicked.connect(self.clicked58)
        self.F58.setStyleSheet("background-color: grey")
        self.F61.clicked.connect(self.clicked61)
        self.F61.setStyleSheet("background-color: grey")
        self.F62.clicked.connect(self.clicked62)
        self.F62.setStyleSheet("background-color: white")
        self.F63.clicked.connect(self.clicked63)
        self.F63.setStyleSheet("background-color: grey")
        self.F64.clicked.connect(self.clicked64)
        self.F64.setStyleSheet("background-color: white")
        self.F65.clicked.connect(self.clicked65)
        self.F65.setStyleSheet("background-color: grey")
        self.F66.clicked.connect(self.clicked66)
        self.F66.setStyleSheet("background-color: white")
        self.F67.clicked.connect(self.clicked67)
        self.F67.setStyleSheet("background-color: grey")
        self.F68.clicked.connect(self.clicked68)
        self.F68.setStyleSheet("background-color: white")
        self.F71.clicked.connect(self.clicked71)
        self.F71.setStyleSheet("background-color: white")
        self.F72.clicked.connect(self.clicked72)
        self.F72.setStyleSheet("background-color: grey")
        self.F73.clicked.connect(self.clicked73)
        self.F73.setStyleSheet("background-color: white")
        self.F74.clicked.connect(self.clicked74)
        self.F74.setStyleSheet("background-color: grey")
        self.F75.clicked.connect(self.clicked75)
        self.F75.setStyleSheet("background-color: white")
        self.F76.clicked.connect(self.clicked76)
        self.F76.setStyleSheet("background-color: grey")
        self.F77.clicked.connect(self.clicked77)
        self.F77.setStyleSheet("background-color: white")
        self.F78.clicked.connect(self.clicked78)
        self.F78.setStyleSheet("background-color: grey")
        self.F81.clicked.connect(self.clicked81)
        self.F81.setStyleSheet("background-color: grey")
        self.F82.clicked.connect(self.clicked82)
        self.F82.setStyleSheet("background-color: white")
        self.F83.clicked.connect(self.clicked83)
        self.F83.setStyleSheet("background-color: grey")
        self.F84.clicked.connect(self.clicked84)
        self.F84.setStyleSheet("background-color: white")
        self.F85.clicked.connect(self.clicked85)
        self.F85.setStyleSheet("background-color: grey")
        self.F86.clicked.connect(self.clicked86)
        self.F86.setStyleSheet("background-color: white")
        self.F87.clicked.connect(self.clicked87)
        self.F87.setStyleSheet("background-color: grey")
        self.F88.clicked.connect(self.clicked88)
        self.F88.setStyleSheet("background-color: white")
        self.F91.clicked.connect(self.clicked91)
        self.F91.setStyleSheet("background-color: white")
        self.F92.clicked.connect(self.clicked92)
        self.F92.setStyleSheet("background-color: grey")
        self.F93.clicked.connect(self.clicked93)
        self.F93.setStyleSheet("background-color: white")
        self.F94.clicked.connect(self.clicked94)
        self.F94.setStyleSheet("background-color: grey")
        self.F95.clicked.connect(self.clicked95)
        self.F95.setStyleSheet("background-color: white")
        self.F96.clicked.connect(self.clicked96)
        self.F96.setStyleSheet("background-color: grey")
        self.F97.clicked.connect(self.clicked97)
        self.F97.setStyleSheet("background-color: white")
        self.F98.clicked.connect(self.clicked98)
        self.F98.setStyleSheet("background-color: grey")

    def clicked21(self):
        self.clicked(21)

    def clicked22(self):
        self.clicked(22)

    def clicked23(self):
        self.clicked(23)

    def clicked24(self):
        self.clicked(24)

    def clicked25(self):
        self.clicked(25)

    def clicked26(self):
        self.clicked(26)

    def clicked27(self):
        self.clicked(27)

    def clicked28(self):
        self.clicked(28)

    def clicked31(self):
        self.clicked(31)

    def clicked32(self):
        self.clicked(32)

    def clicked33(self):
        self.clicked(33)

    def clicked34(self):
        self.clicked(34)

    def clicked35(self):
        self.clicked(35)

    def clicked36(self):
        self.clicked(36)

    def clicked37(self):
        self.clicked(37)

    def clicked38(self):
        self.clicked(38)

    def clicked41(self):
        self.clicked(41)

    def clicked42(self):
        self.clicked(42)

    def clicked43(self):
        self.clicked(43)

    def clicked44(self):
        self.clicked(44)

    def clicked45(self):
        self.clicked(45)

    def clicked46(self):
        self.clicked(46)

    def clicked47(self):
        self.clicked(47)

    def clicked48(self):
        self.clicked(48)

    def clicked51(self):
        self.clicked(51)

    def clicked52(self):
        self.clicked(52)

    def clicked53(self):
        self.clicked(53)

    def clicked54(self):
        self.clicked(54)

    def clicked55(self):
        self.clicked(55)

    def clicked56(self):
        self.clicked(56)

    def clicked57(self):
        self.clicked(57)

    def clicked58(self):
        self.clicked(58)

    def clicked61(self):
        self.clicked(61)

    def clicked62(self):
        self.clicked(62)

    def clicked63(self):
        self.clicked(63)

    def clicked64(self):
        self.clicked(64)

    def clicked65(self):
        self.clicked(65)

    def clicked66(self):
        self.clicked(66)

    def clicked67(self):
        self.clicked(67)

    def clicked68(self):
        self.clicked(68)

    def clicked71(self):
        self.clicked(71)

    def clicked72(self):
        self.clicked(72)

    def clicked73(self):
        self.clicked(73)

    def clicked74(self):
        self.clicked(74)

    def clicked75(self):
        self.clicked(75)

    def clicked76(self):
        self.clicked(76)

    def clicked77(self):
        self.clicked(77)

    def clicked78(self):
        self.clicked(78)

    def clicked81(self):
        self.clicked(81)

    def clicked82(self):
        self.clicked(82)

    def clicked83(self):
        self.clicked(83)

    def clicked84(self):
        self.clicked(84)

    def clicked85(self):
        self.clicked(85)

    def clicked86(self):
        self.clicked(86)

    def clicked87(self):
        self.clicked(87)

    def clicked88(self):
        self.clicked(88)

    def clicked91(self):
        self.clicked(91)

    def clicked92(self):
        self.clicked(92)

    def clicked93(self):
        self.clicked(93)

    def clicked94(self):
        self.clicked(94)

    def clicked95(self):
        self.clicked(95)

    def clicked96(self):
        self.clicked(96)

    def clicked97(self):
        self.clicked(97)

    def clicked98(self):
        self.clicked(98)
    # end of auto-generated code #

    def show_moves(self):
        if self.field_selected:
            all_moves = self.perft.get_legal_moves()
            all_starts, all_goals = test_cl.MoveArray(all_moves).convert2()
            if self.field_selected in all_starts:
                goals = all_goals[all_starts == self.field_selected]
                for goal in goals:
                    self.color_field(goal, 'goal')
            self.showing_moves = True

    def print_moves(self):
        all_moves = self.perft.get_legal_moves()
        test_cl.output_moves(all_moves[all_moves != 0])

    def print_state(self):
        print(self.perft.game.state)

    def undo(self):
        if self.field_selected:
            num = self.field_selected
            self.color_field(num, 'blank')
            self.field_selected = False
        if self.showing_moves:
            for num in self.legal_fields:
                self.color_field(num, 'blank')
            self.showing_moves = False

    def color_field(self, num, style):
        if num in self.legal_fields:
            if style == 'blank':
                color = 'grey' if (num//10 + num % 10) % 2 else 'white'
            elif style == 'start':
                color = 'darkCyan' if (num//10 + num % 10) % 2 else 'cyan'
            elif style == 'goal':
                color = 'darkMagenta' if (num//10 + num % 10) % 2 else 'magenta'
            else:
                color = 'grey' if (num//10 + num % 10) % 2 else 'white'
            eval('self.F{}.setStyleSheet("background-color: {}")'.format(num, color))

    def clicked(self, num):
        print 'user clicked {}'.format(num)
        if not self.field_selected:
            self.field_selected = num
            self.color_field(num, 'start')
        if self.field_selected:
            goals = []
            all_moves = self.perft.get_legal_moves()
            all_starts, all_goals = test_cl.MoveArray(all_moves).convert2()
            if self.field_selected in all_starts:
                goals = all_goals[all_starts == self.field_selected]
            if num in goals:
                self.perft.apply_move(self.field_selected*128+num)
                self.showing_moves = True
                self.undo()
                self.update_board()

    def update_board(self):
        symcon = u' x♙♘♗♖♕♔;:♚♛♜♝♞♟x'
        for i in range(test_cl.BOARD_SIZE):
            if i in self.legal_fields:
                eval('self.F{}.setText(symcon[self.perft.game.state[i]])'.format(i))

    def test_perft(self):
        i = self.spinBoxPerft.value()
        if i <= 5:
            print('Perft for depth={} is: {}'.format(i, self.perft.perft(i)))
        else:
            print('(Deep) perft for depth={} is: {}'.format(i, self.perft.deep_perft(i-5, 5)))

    def split_perft(self):
        i = self.spinBoxSplitPerft.value()
        if i <= 6:
            self.perft.split_perft(i)
        else:
            self.perft.deep_split_perft(i)

    def load_fen(self):
        fen = str(self.lineEditFEN.text())
        self.perft.game.set_fen_state(fen)
        self.update_board()
        # print(self.perft.game.state)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())