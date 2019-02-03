#!/usr/bin/env python
# -*- coding: utf8 -*-
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from datetime import date

from PyQt4.QtCore import Qt, QSize
from PyQt4.QtGui import (QMainWindow, QLabel, QIcon, QLineEdit, QPalette,
                         QDateTimeEdit, QFont, QWidget, QTabBar, QToolButton,
                         QTextEdit, QColor, QIntValidator, QDoubleValidator,
                         QCommandLinkButton, QRadialGradient, QPainter, QBrush,
                         QPainterPath, QPen, QPushButton,
                         QCompleter, QComboBox, QSortFilterProxyModel,
                         QPixmap, QFrame)
# from PyQt4.QtWebKit import QWebView


class FMainWindow(QMainWindow):

    def __init__(self, parent=0, *args, **kwargs):
        QMainWindow.__init__(self)
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # self.setWindowIcon(QIcon.fromTheme(
        #     'logo', QIcon(u"{}logo.png".format(Config.img_media))))

        self.wc = self.width()
        self.hc = self.height()
        self.resize(self.wc, self.hc)

    def set_window_title(self, page_name):
        self.setWindowTitle(" ")

    def resizeEvent(self, event):
        """lancé à chaque redimensionnement de la fenêtre"""
        # trouve les dimensions du container
        self.wc = self.width()
        self.hc = self.height()
        # print(self.wc)
        # print(self.hc)

    def change_context(self, context_widget, *args, **kwargs):

        # instanciate context
        # print("change_context Window")
        self.view_widget = context_widget(parent=self, *args, **kwargs)
        # attach context to window
        self.setCentralWidget(self.view_widget)

    def open_dialog(self, dialog, modal=False, opacity=0.90, *args, **kwargs):
        d = dialog(parent=self, *args, **kwargs)
        d.setModal(modal)
        # d.setWindowFlags(Qt.FramelessWindowHint)
        d.setWindowOpacity(opacity)
        d.exec_()


class FWidget(QWidget):

    def __init__(self, parent=0, *args, **kwargs):

        QWidget.__init__(self, parent=parent, *args, **kwargs)
        self.pp = parent

        # self.setStyleSheet("font-family:Garamond")
        # self.setStyleSheet("font-family:Trebuchet MS;")
        self.setStyleSheet("font-family:Times New Roman;")

    def refresh(self):
        pass

    def change_main_context(self, context_widget, *args, **kwargs):
        # print("change_main_context")
        return self.parentWidget().change_context(context_widget, *args, **kwargs)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        return self.parentWidget().open_dialog(dialog, modal=modal, *args, **kwargs)


# class FWebView(QWebView):

#     def __init__(self, parent=0, *args, **kwargs):
#         QWebView.__init__(self, parent=parent, *args, **kwargs)
#         self.pp = parent

#     def change_main_context(self, context_widget, *args, **kwargs):
# return self.parentWidget().change_context(context_widget, *args,
# **kwargs)


class PyTextViewer(QTextEdit):

    # Initialise the instance.
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)

        self.setReadOnly(True)


class TabPane(QTabBar):

    def __init__(self, parent=None):
        super(TabPane, self).__init__(parent)

        css = """
        TabPane{
            border: 1px solid gray;
            border-radius: 7px;
            background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4984C7, stop: 1 #4C7);
        }
        """
        # self.setStyleSheet(css)

    def addBox(self, box):
        self.setLayout(box)


class Fhelper(QLabel):

    def __init__(self, *args, **kwargs):
        super(Fhelper, self).__init__(*args, **kwargs)
        css = """color: gry;font-size:20px"""
        self.setStyleSheet(css)


class FLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super(FLabel, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)


class FRLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super(FRLabel, self).__init__(*args, **kwargs)
        # self.setFont(QFont("Times New Roman", 50))
        css = """
                color: gry;
              """
        # self.setStyleSheet(css)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        # self.setFont(font)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignRight)


class FHeader(FLabel):

    def __init__(self, text, css=None, parent=None):
        FLabel.__init__(self, text, parent)
        self.setStyleSheet(css)


class FPageTitle(FLabel):

    def __init__(self, *args, **kwargs):
        super(FPageTitle, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)

        css = """font-weight: bold;font-size: 30px;color: green;"""
        self.setStyleSheet(css)


class FBoxTitle(FLabel):

    def __init__(self, *args, **kwargs):
        super(FBoxTitle, self).__init__(*args, **kwargs)
        self.setFont(QFont("Times New Roman", 12, QFont.Bold, True))
        self.setAlignment(Qt.AlignLeft)


class ErrorLabel(FLabel):

    def __init__(self, text, css=None, parent=None):
        FLabel.__init__(self, text, parent)
        font = QFont()
        self.setFont(font)
        red = QColor(Qt.red)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, red)
        self.setPalette(palette)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class FormLabel(FLabel):

    def __init__(self, text, parent=None):
        FLabel.__init__(self, text, parent)
        font = QFont()
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class QBadgeButton (QPushButton):

    def __init__(self, icon=None, text=None, parent=None):
        if icon:
            QPushButton.__init__(self, icon, text, parent)
        elif text:
            QPushButton.__init__(self, text, parent)
        else:
            QPushButton.__init__(self, parent)

        self.badge_counter = 0
        self.badge_size = 25

        self.redGradient = QRadialGradient(
            0.0, 0.0, 17.0, self.badge_size - 3, self.badge_size - 3)
        self.redGradient.setColorAt(0.0, QColor(0xe0, 0x84, 0x9b))
        self.redGradient.setColorAt(0.5, QColor(0xe9, 0x34, 0x43))
        self.redGradient.setColorAt(1.0, QColor(0xdc, 0x0c, 0x00))

    def setSize(self, size):
        self.badge_size = size

    def setCounter(self, counter):
        self.badge_counter = counter
        self.update()

    def paintEvent(self, event):
        QPushButton.paintEvent(self, event)
        p = QPainter(self)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.setRenderHint(QPainter.Antialiasing)

        if self.badge_counter > 0:
            point = self.rect().topRight()
            self.drawBadge(p, point.x() - self.badge_size - 1, point.y() + 1,
                           self.badge_size, str(self.badge_counter), QBrush(self.redGradient))

    def fillEllipse(self, painter, x, y, size, brush):
        path = QPainterPath()
        path.addEllipse(x, y, size, size)
        painter.fillPath(path, brush)

    def drawBadge(self, painter, x, y, size, text, brush):
        painter.setFont(QFont(painter.font().family(), 11, QFont.Bold))

        while ((size - painter.fontMetrics().width(text)) < 10):
            pointSize = painter.font().pointSize() - 1
            weight = QFont.Normal if (pointSize < 8) else QFont.Bold
            painter.setFont(
                QFont(painter.font().family(), painter.font().pointSize() - 1, weight))

        shadowColor = QColor(0, 0, 0, size)
        self.fillEllipse(painter, x + 1, y, size, shadowColor)
        self.fillEllipse(painter, x - 1, y, size, shadowColor)
        self.fillEllipse(painter, x, y + 1, size, shadowColor)
        self.fillEllipse(painter, x, y - 1, size, shadowColor)

        painter.setPen(QPen(Qt.white, 2))
        self.fillEllipse(painter, x, y, size - 3, brush)
        painter.drawEllipse(x, y, size - 3, size - 3)

        painter.setPen(QPen(Qt.white, 1))
        painter.drawText(x, y, size - 2, size - 2, Qt.AlignCenter, text)


class QToolBadgeButton (QToolButton):

    def __init__(self, parent=None):
        QToolButton.__init__(self, parent)

        self.badge_counter = 0
        self.badge_size = 5

        self.redGradient = QRadialGradient(
            0.0, 0.0, 17.0, self.badge_size - 3, self.badge_size - 3)
        self.redGradient.setColorAt(0.0, QColor(0xe0, 0x84, 0x9b))
        self.redGradient.setColorAt(0.5, QColor(0xe9, 0x34, 0x43))
        self.redGradient.setColorAt(1.0, QColor(0xdc, 0x0c, 0x00))

    def setSize(self, size):
        self.badge_size = size

    def setCounter(self, counter):
        self.badge_counter = counter

    def paintEvent(self, event):
        QToolButton.paintEvent(self, event)
        p = QPainter(self)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.setRenderHint(QPainter.Antialiasing)
        if self.badge_counter > 0:
            point = self.rect().topRight()
            self.drawBadge(p, point.x() - self.badge_size, point.y(),
                           self.badge_size, str(self.badge_counter), QBrush(self.redGradient))

    def fillEllipse(self, painter, x, y, size, brush):
        path = QPainterPath()
        path.addEllipse(x, y, size, size)
        painter.fillPath(path, brush)

    def drawBadge(self, painter, x, y, size, text, brush):
        painter.setFont(QFont(painter.font().family(), 11, QFont.Bold))

        while ((size - painter.fontMetrics().width(text)) < 10):
            pointSize = painter.font().pointSize() - 1
            weight = QFont.Normal if (pointSize < 8) else QFont.Bold
            painter.setFont(
                QFont(painter.font().family(), painter.font().pointSize() - 1, weight))

        shadowColor = QColor(0, 0, 0, size)
        self.fillEllipse(painter, x + 1, y, size, shadowColor)
        self.fillEllipse(painter, x - 1, y, size, shadowColor)
        self.fillEllipse(painter, x, y + 1, size, shadowColor)
        self.fillEllipse(painter, x, y - 1, size, shadowColor)

        painter.setPen(QPen(Qt.white, 2))
        self.fillEllipse(painter, x, y, size - 3, brush)
        painter.drawEllipse(x, y, size - 2, size - 2)

        painter.setPen(QPen(Qt.white, 1))
        painter.drawText(x, y, size - 2, size - 2, Qt.AlignCenter, text)


class Button(QCommandLinkButton):

    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.setAutoDefault(True)
        self.setIcon(QIcon.fromTheme('', QIcon('')))
        self.setCursor(Qt.PointingHandCursor)
        # self.setCursor(Qt.ForbiddenCursor)
        # self.setFixedSize(100, 40)


class BttRond(Button):

    def __init__(self, *args, **kwargs):
        super(BttRond, self).__init__(*args, **kwargs)
        self.setIcon(QIcon.fromTheme('', QIcon('')))
        css = """
                border-radius:9px;
                border:1px solid #4b8f29;
                color:#ffffff;
                font-family:arial;
                font-size:13px;
                font-weight:bold;
                padding:6px 12px;

        """
        # self.setStyleSheet(css)


class Deleted_btt(Button):

    def __init__(self, *args, **kwargs):
        super(Deleted_btt, self).__init__(*args, **kwargs)
        self.setIcon(QIcon.fromTheme('edit-delete', QIcon('')))
        css = """
                background-color:#fc8d83;
                border-radius:6px;
                border:1px solid #d83526;
                color:#ffffff;
                font-family:arial;
                font-size:15px;
                font-weight:bold;
                padding:6px 24px;
                text-decoration:none;
                """
        self.setStyleSheet(css)


class Warning_btt(Button):

    def __init__(self, *args, **kwargs):
        super(Warning_btt, self).__init__(*args, **kwargs)
        self.setIcon(QIcon.fromTheme('save', QIcon(
            u"{img_media}{img}".format(img_media=Config.img_media,
                                       img='warning.png'))))
        css = """
                    background-color:#ffec64;
                    border-radius:6px;
                    border:1px solid #ffaa22;
                    color:#333333;
                    font-family:arial;
                    font-size:15px;
                    font-weight:bold;
                    padding:6px 24px;
                """
        self.setStyleSheet(css)


class BttSmall(Button):

    def __init__(self, *args, **kwargs):
        super(BttSmall, self).__init__(*args, **kwargs)
        chart_count = len(self.text())
        # print(chart_count)
        self.setFixedWidth(chart_count + 45)
        # self.setFixedHeight(30)


class BttExportPDF(Button):

    def __init__(self, arg):
        super(BttExportPDF, self).__init__("pdf")


class LineEdit(QLineEdit):

    """Accepter que des nombre positive """

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        # self.setMaximumHeight(20)
        # self.setDisplayText("kkkkkk")
        # self.setMaximumWidth(200)


class IntLineEdit(LineEdit):

    """Accepter que des nombre positive """

    def __init__(self, parent=None):
        LineEdit.__init__(self, parent)
        self.setValidator(QIntValidator(self))
        self.setAlignment(Qt.AlignRight)
        self.setText(self.text().replace(" ", ""))


class FloatLineEdit(LineEdit):

    """Accepter que des nombre positive """

    def __init__(self, parent=None):
        LineEdit.__init__(self, parent)
        self.setAlignment(Qt.AlignRight)
        self.setValidator(QDoubleValidator(0.1, 0.1, 100, self))


class FormatDate(QDateTimeEdit):

    def __init__(self, *args, **kwargs):
        super(FormatDate, self).__init__(*args, **kwargs)
        self.setDisplayFormat(u"dd/MM/yyyy")
        self.setCalendarPopup(True)


class FPeriodTabBar(TabPane):

    def __init__(self, parent, main_date, *args, **kwargs):

        super(FPeriodTabBar, self).__init__(*args, **kwargs)

        for i in range(0, 3):
            self.addTab(u"{}".format(i))
        self.set_data_from(main_date)
        self.build_tab_list()

        self.currentChanged.connect(self.changed_period)

    def set_data_from(self, period):

        self.main_period = Period(
            period.year, period.duration, period.duration_number)
        self.periods = [self.main_period.previous,
                        self.main_period.current, self.main_period.next]

    def build_tab_list(self):
        for index, period in enumerate(self.periods):
            self.setTabText(index, str(period.display_name()))
            self.setTabToolTip(index, str(period))
        self.setTabTextColor(1, QColor('SeaGreen'))
        self.setCurrentIndex(1)

    def changed_period(self, index):
        if index == -1 or index == 1:
            return False
        else:
            np = self.periods[index]
            self.set_data_from(np)
            self.build_tab_list()
            self.parentWidget().main_date = np
            self.parentWidget().change_period(np)


class EnterDoesTab(QWidget):

    def keyReleaseEvent(self, event):
        super(EnterDoesTab, self).keyReleaseEvent(event)
        if event.key() == Qt.Key_Return:
            self.focusNextChild()


class EnterTabbedLineEdit(LineEdit, EnterDoesTab):
    pass

from PyQt4.QtGui import QCompleter, QComboBox, QSortFilterProxyModel

try:
    unicode
except:
    unicode = str


class ExtendedComboBox(QComboBox):

    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)
        # connect signals
        self.lineEdit().textEdited[unicode].connect(
            self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)
    # on selection of an item from the completer, select the corresponding
    # item from combobox

    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)

    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    # on model column change, update the model column of the filter and
    # completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)


class WigglyWidget(QWidget):

    def __init__(self, test, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setBackgroundRole(QtGui.QPalette.Midlight)
        # print(test)
        newFont = self.font()
        newFont.setPointSize(newFont.pointSize() + 20)
        self.setFont(newFont)

        self.timer = QtCore.QBasicTimer()
        self.text = QtCore.QString(test)

        self.step = 0
        self.timer.start(60, self)

    def paintEvent(self, event):
        sineTable = [0, 38, 71, 92, 100, 92, 71, 38,
                     0, -38, -71, -92, -100, -92, -71, -38]

        metrics = QtGui.QFontMetrics(self.font())
        x = (self.width() - metrics.width(self.text)) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2
        color = QtGui.QColor()

        painter = QtGui.QPainter(self)

        for i in xrange(self.text.size()):
            index = (self.step + i) % 16
            color.setHsv((15 - index) * 16, 255, 191)
            painter.setPen(color)
            painter.drawText(
                x, y - ((sineTable[index] * metrics.height()) / 400), QtCore.QString(self.text[i]))
            x += metrics.width(self.text[i])

    def setText(self, newText):
        self.text = QtCore.QString(newText)

    def timerEvent(self, event):
        if (event.timerId() == self.timer.timerId()):
            self.step = self.step + 1
            self.update()
        else:
            QtGui.QWidget.timerEvent(event)
