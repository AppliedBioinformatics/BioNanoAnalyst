# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'About.ui'
#
# Created by: PySide UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt4 import QtGui,QtCore
except ImportError:
    from PySide import QtGui,QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName(_fromUtf8("About"))
        About.resize(378, 342)
        About.setMinimumSize(QtCore.QSize(378, 342))
        About.setMaximumSize(QtCore.QSize(378, 342))
        self.label = QtGui.QLabel(About)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(About)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 181, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(About)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 211, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(8)
        font.setItalic(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(About)
        self.label_4.setGeometry(QtCore.QRect(10, 60, 261, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(8)
        font.setItalic(False)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.textBrowser = QtGui.QTextBrowser(About)
        self.textBrowser.setGeometry(QtCore.QRect(10, 90, 361, 211))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.about_bn = QtGui.QPushButton(About)
        self.about_bn.setGeometry(QtCore.QRect(290, 310, 75, 23))
        self.about_bn.setObjectName(_fromUtf8("about_bn"))

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        About.setWindowTitle(_translate("About", "About BioNanoAnalyst", None))
        self.label.setText(_translate("About", "Application: BioNanoAnalyst", None))
        self.label_2.setText(_translate("About", "Version:      1.0", None))
        self.label_3.setText(_translate("About", "Copyright by Applied Bioinformatics Group", None))
        self.label_4.setText(_translate("About", "University of western Australia, Perth, WA, Australia", None))
        self.textBrowser.setHtml(_translate("About", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:8pt;\">BioNanoAnalyst, an open-source software package to facilitate the quality assessment of BioNano optical mapping and reference sequence assembly.  </span><span style=\" font-size:8pt;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:8pt;\">Written in Python and converted into system specific applications, BioNanoAnalyst can easily run on multiple platforms with minimal dependencies. </span><span style=\" font-size:8pt;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:8pt;\">Integrating with several command lines in the interface, BioNanoAnalyst offers a Graphical User Interface (GUI) to visualize the statistics of the BioNano optical mapping process.  </span><span style=\" font-size:8pt;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:8pt;\">Graphs and corresponding tables are provided to assess the quality of reference sequence assembly. Based on this report, misassembly correction can be carried out by users to enhance the quality of genome assemblies.</span><span style=\" font-size:8pt;\"> </span></p></body></html>", None))
        self.about_bn.setText(_translate("About", "OK", None))
