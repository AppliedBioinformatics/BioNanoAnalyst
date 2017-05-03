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
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">BioNanoAnalyst provides an user friendly GUI and users can easily following. </span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Before using it, users need to make sure the followings: </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">1. BioNaoAnalyst provides two options in using the BioNano data. If users want to using option 1, please download the BioNano tools (&quot;Assembler&quot; and &quot;RefAligner&quot;) from http://www.bnxinstall.com/RefAlignerAssembler and &quot;scripts&quot; from http://www.bnxinstall.com/Scripts. </span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">2. For the BioNano tools, if users use Linux or MacOS system, </span><span style=\" font-family:\'-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol\'; font-size:10pt; color:#24292e; background-color:#ffffff;\">please use the command &quot;grep avx /proc/cpuinfo&quot; or &quot;grep sse2 /proc/cpuinfo&quot; and search for the word ‘avx’ or ‘sse2’. If both types exist, use AVX as it is faster than SSE2.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">3. Install or unzip &quot;Assembler&quot; and &quot;RefAligner&quot;into your local computer and put them in one folder.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">4. Make sure the tools are executable and do not rename them.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">5. If users don\'t want to use option 1, please leave this option.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">How to use BioNanoAnalyst:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Steps:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">1. Select a reference genome in fasta/fa/fna format (required). </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">2. If using raw BioNano maps (Option 1), please ensure &quot;scripts&quot;, &quot;Assembler&quot; and &quot; RefAligner&quot; from BioNano Genomics are available in your system (see below for more detailed instructions). </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">For this option, a raw BioNano bnx file obtained from BioNano Genomics platform, such as Irys platform is required. After selecting a proper enzyme, importing the bnx file and setting the parameters under \'Settings\', the assembly and alignment can be started by clicking the \'Start\' button. Note: Option 1 is currently not available in Windows system. When running this step, it can take a while depended on the input files and the settings. We recommend to run this step on a cluster if you have a big dataset (&gt;100Mb). For your convenience, we have also provided a script to help run jobs on a cluster: https://github.com/AppliedBioinformatics/runBNG.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">3. If using aligned BioNano data (Option 2), an xmap file and the corresponding ref and query cmap files are needed. Note: the aligned files are generated by comparing a ref and qry maps, such as EXP_REFINAL1.cmap from the /exp_refineFinal1 folder as the query map and _in silico_ digested NGS sequences as a ref map.They are not the _de novo_ assembled sub-files.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">4. In the analysis step, a confidence score should be specified (≥0) before starting. Bioinformatician from BioNano Genomics suggests using 15 as a good start. Usually, we recommend a confidence score between 10-20, however, users can adjust this number depending on their own mapping quality. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Below is a table interpreting a confidence score and its association with the quality of nucleotide mappings from the comparison between human NGS assembly data: </span><a href=\"http://hgdownload.soe.ucsc.edu/goldenPath/hg19/chromosomes/chr1.fa.gz\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">hg19_chr1</span></a><span style=\" font-size:10pt;\"> and all </span><a href=\"http://hgdownload.cse.ucsc.edu/goldenPath/hg24may2000/bigZips/contigFa.zip\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">contigs</span></a><span style=\" font-size:10pt;\"> from 24/05/2000 assembly which were used to build chr1. The method was to digest hg19_chr1 and all contigs _in silico_ using _BspQI_ to get cmap files and then use hg19_chr1.cmap as a ref cmap and ctgs.cmap as a query map to map them using RefAligner. After getting an xmap file, we used blastn to align each mapped contig with chr1 in their mapped regions reported in the xmap file under a corresponding confidence score. In blastn result, we only selected the top hit with an identity rate&gt;=99%, Evalue ~0. Note: The table below provides a tested result for users to check the mapping stats with a corresponding confidence score. To decided which confidence score should be used, users may visually check the mapping quality or check the xmap file. The tricky thing is if using a large confidence score, information below this selected confidence score will be hidden, which means users may lose many mappings. A proper confidence score is really depended on the research purpose that users want to achieve.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Overall:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Mapping: ctgs_chr1_to_hg19_chr1</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Min_confidence_score: 12.25</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Max_confidence_score: 544.78</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Total_number_of_mapping: 109</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Total_refer_mapped_length: 95146336 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">confidence_score average_mapping_size*    confidence_score     map_left(%)    total_ref_mapped_len </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">[10, 15)    66393 bp             &gt;=10         100.00     95146336 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">[15,20)     70402 bp             &gt;=15        90.83     93835874 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">[20,25)     102637 bp             &gt;=20         77.98     91670481 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">[25,30)     111613 bp             &gt;=25         69.72     90008858 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">[30,35)     194000 bp             &gt;=30         57.80     86644558 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">[35,40)     197171 bp             &gt;=35         50.46    84090226 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">[40,45)     167396 bp             &gt;=40         45.87     82112264 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">[45,50)     202646 bp             &gt;=45         41.28     79622104 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">[50,55)     240851 bp             &gt;=50         38.53     78516942 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">[55,60)     188613 bp             &gt;=55         33.94     75394112 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">&gt;=60     235605 bp             &gt;=60        32.11    74036462 bp</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">*Result from BLASTN best/top hit</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">5. After specifying a confidence score, click the &quot;Analyse&quot; button, BioNanoAnalyst will run and the &quot;Job status&quot; panel will immediately show the job status as &quot;Running&quot; in blue colour or &quot;Finished&quot; in green colour. Note: When BioNanoAnalyst is running, it may temporarily stop responding due to the heavy computing load. If this occurs, please let BioNanoAnalyst run and do not perform any action within the program.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">6. After the &quot;Job status&quot; indicates &quot;Finished&quot;, the tabs in the top right panel show the results of mapping for each stop of the workflow, as a table of summary statistics and as a pie chart. Plots of the mapping results across all sites analysed is available via the bottom panel.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">7. To view the summary mapping plot for a contig of interest, select a contig from the drop-down menu in the &quot;Mapping Plot&quot; panel. Users can zoom the plot and click specific site to check its site ID and position on the reference. A copy of the plot shown can be saved to a specified directory; alternatively all contig plots can be saved using the &quot;Save all plots&quot; button. Users may also save a gff3 file into a selected directory, which contains all information reported by BioNanoAnalyst by clicking the &quot;save quality report&quot; button.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Setting up an analysis using raw BioNano data:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">1. BioNanoAnalyst provides two options for analysing BioNano data in Linux/Unix system and macOS system. If users want to use raw BioNano data (Option 1), please set BioNano tools ( &quot;Assembler&quot; and &quot;RefAligner&quot;) and the &quot;scripts&quot; properly in the system. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">2. Install or decompress &quot;Assembler&quot; and &quot;RefAligner&quot; on your local computer and move them into a single folder, making sure the applications are not renamed and are executable. The folder containing these applications will need to be indicated under Option 1 -&gt; Settings -&gt; Tools for the analysis to run.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"><br /></span></p></body></html>", None))
        self.label.setText(_translate("Manual", "Manual for using BioNanoAnalyst", None))
        self.manual_bn.setText(_translate("Manual", "OK", None))
