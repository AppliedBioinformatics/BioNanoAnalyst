# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Manual.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Manual(object):
    def setupUi(self, Manual):
        Manual.setObjectName(_fromUtf8("Manual"))
        Manual.resize(740, 450)
        Manual.setMinimumSize(QtCore.QSize(740, 450))
        Manual.setMaximumSize(QtCore.QSize(740, 450))
        self.textBrowser = QtGui.QTextBrowser(Manual)
        self.textBrowser.setGeometry(QtCore.QRect(10, 40, 721, 371))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.label = QtGui.QLabel(Manual)
        self.label.setGeometry(QtCore.QRect(10, 10, 271, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.manual_bn = QtGui.QPushButton(Manual)
        self.manual_bn.setGeometry(QtCore.QRect(650, 420, 75, 23))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        self.manual_bn.setFont(font)
        self.manual_bn.setObjectName(_fromUtf8("manual_bn"))

        self.retranslateUi(Manual)
        QtCore.QMetaObject.connectSlotsByName(Manual)

    def retranslateUi(self, Manual):
        Manual.setWindowTitle(_translate("Manual", "Manual", None))
        self.textBrowser.setHtml(_translate("Manual", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:600;\">How to use BioNanoAnalyst:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\">1. Select a reference genome in fasta format (required). </span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\">2. Option 1 is not available in Windows system. If using raw BioNano reads (Option 1), please make sure &quot;scripts&quot; folder, &quot;Assember&quot; and &quot; RefAligner&quot;  are avaiable in your computer (see below for more detailed instructions). </span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\">For this option, a raw BioNano bnx file obatained from BioNano Irys platfrom is required. After importing the bnx file and setting the parameters, the assembly and alignment will be started. </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:600; color:#000000;\">Note:</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\"> this step can take a while based on your input files and the chosen settings.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\">3. If using aligned BioNano data (Option 2), an xmap file and the corresponding reference cmap and query cmap files are needed.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\">4. Before beginning the analysis, a confidence score should be specified (≥0).</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\">5. To start the analysis, click the &quot;Analyse&quot; button, BioNanoAnalyst will run and the &quot;Job status&quot; panel will immediately show the job status as &quot;Running&quot; in blue colour or &quot;Finished&quot; in green colour. </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:600; color:#000000;\">Note:</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\"> When BioNanoAnalyst is running, it may temporarily stop responding due to the heavy computing load. If this occurs, please let BioNanoAnalyst run and do not perform any action within the program.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\">6. After the &quot;Job status&quot; indicates &quot;Finished&quot;, the tabs in the top right panel show the results of mapping for each stop of the workflow, as a table of summary statistics and as a pie chart. A plot of the mapping results across all sites analysed is avaible via the bottom panel.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\">7. To view the summary mapping plot for a contig of interest, select a contig from the drop-down menu in the &quot;Mapping Plot&quot; panel. A copy of the plot shown can be saved to a specified directory; alternativly all contig plots can be saved using the &quot;Save all plots&quot; button.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:600; color:#000000;\">Setting up an analysis using raw BioNano data:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\">1. BioNanoAnalyst provides two options for analysing BioNano data in Linux/Unix system and macOS system. If you want to use raw BioNano data (Option 1), please download the BioNano tools &quot;Assembler&quot;, &quot;RefAligner&quot; and the &quot;scripts&quot; folder from BioNano Genomics:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#0000ff;\">http://bionanogenomics.com/support/software-updates/</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\">2. Install or decompress &quot;Assembler&quot; and &quot;RefAligner&quot; on your local computer and move them into a single folder, making sure the applications are not renamed and are executable. The folder containing these applications will need to be indicated under Option 1 -&gt; Settings -&gt; Tools for the analysis to run.</span></p></body></html>", None))
        self.label.setText(_translate("Manual", "Manual for using BioNanoAnalyst", None))
        self.manual_bn.setText(_translate("Manual", "OK", None))
