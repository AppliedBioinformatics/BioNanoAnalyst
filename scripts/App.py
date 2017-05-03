#!/usr/bin/env python

################################################################
## Application:               BioNanoAnalyst
## Author:                    Yuxuan Yuan
## Email:                     yuxuan.yuan@research.uwa.edu.au
## Last modification Date:    02/12/2016
## Copyright: Copyright (c) 2016 Applied Bioinformatics Group
## UWA, Perth WA, Australia
################################################################

#======================== libraries ==========================
import os
import re
import sys
import codecs
from time import time
from time import sleep
if sys.platform == 'win32':
    import codecs
import webbrowser
import subprocess
import multiprocessing
try:
    from PyQt4 import QtGui,QtCore
    from PyQt4.QtGui import*
except ImportError:
    from PySide import QtGui,QtCore
    from PySide.QtGui import*
from datetime import datetime
from Frameworks import Ui_BioNanoAnalyst
from About import Ui_About
from Manual import Ui_Manual
from Settings import Ui_Settings
from Analysis import*
import pandas as pd
import numpy as np
import FileDialog
from matplotlib.pyplot import figure, show
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import  NavigationToolbar2QT as NavigationToolbar
#=======================================================================================

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_BioNanoAnalyst()
        self.ui.setupUi(self)
        self.ref = None
        self.enz = None
        self.bnx = None
        self.xmap = None
        self.rcmap = None
        self.qcmap = None
        self.cs = None
        self.about_window = None
        self.manual_window = None
        self.parameters_window = None
        self.running = None
        self.output_path = None
        self.format = None
        self.ctg_figure = None
        self.axes = None
        self.canvas = None
        self.canvas_ctg = None
        self.ref_table = QtGui.QTableWidget()
        self.unqualified_table = QtGui.QTableWidget()
        self.qualified_table = QtGui.QTableWidget()
        self.BN_table = QtGui.QTableWidget()
        self.unmapped_table = QtGui.QTableWidget()
        self.mapped_table = QtGui.QTableWidget()
        self.filtered_table = QtGui.QTableWidget()
        self.no_data_table = QtGui.QTableWidget()
        self.missing_table = QtGui.QTableWidget()
        self.good_table = QtGui.QTableWidget()
        self.site_p_table = QtGui.QTableWidget()
        self.pos_p_table = QtGui.QTableWidget()
        self.both_table = QtGui.QTableWidget()
        #==================== menubar ====================
        self.ui.actionNew.setShortcut('Ctrl+N')
        self.ui.actionClose.setShortcut('Ctrl+Q')
        self.ui.actionAbout.setShortcut('Ctrl+A')
        self.ui.actionManual.setShortcut('Ctrl+M')
        self.ui.actionFeedbacks.setShortcut('Ctrl+F')
        self.ui.actionNew.triggered.connect(self.new)
        self.ui.actionClose.triggered.connect(self.quit)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionManual.triggered.connect(self.manual)
        self.ui.actionFeedbacks.triggered.connect(self.feedbacks)
        #=================== reference panel ==================
        self.ui.ref_select_bn.clicked.connect(self.select_ref)
        self.ui.ref_clear_bn.clicked.connect(self.clear_ref)
        #================== raw data panel ====================
        self.ui.raw_frame.setEnabled(False)
        self.ui.raw_checkBox.stateChanged.connect(self.enable_raw)
        self.ui.enzyme_combox.addItems(['BspQI','BbvCI','BsmI','BsrDI','bseCI'])
        self.ui.enzyme_combox.activated[str].connect(self.enzyme)
        self.ui.raw_select_bn.clicked.connect(self.select_bnx)
        self.ui.raw_clear_bn.clicked.connect(self.clear_bnx)
        self.ui.raw_settings_bn.clicked.connect(self.raw_settings)
        self.ui.raw_start_bn.clicked.connect(self.raw_start)
        #================= aligned data panel =================
        self.ui.aligned_frame.setEnabled(False)
        self.ui.aligned_checkBox.stateChanged.connect(self.enable_aligned)
        self.ui.xmap_select_bn.clicked.connect(self.select_xmap)
        self.ui.xmap_clear_bn.clicked.connect(self.clear_xmap)
        self.ui.rcmap_select_bn.clicked.connect(self.select_rcmap)
        self.ui.rcmap_clear_bn.clicked.connect(self.clear_rcmap)
        self.ui.qcmap_select_bn.clicked.connect(self.select_qcmap)
        self.ui.qcmap_clear_bn.clicked.connect(self.clear_qcmap)
        #================= analysis panel ===================
        self.ui.analyse_bn.clicked.connect(self.analyse)
        #=================== Stats panel ========================
        self.ui.show_ref_bn.clicked.connect(self.show_ref)
        self.ui.show_unqualified_bn.clicked.connect(self.show_unqualified)
        self.ui.show_qualified_bn.clicked.connect(self.show_qualified)
        self.ui.show_mapped_bn.clicked.connect(self.show_mapped)
        self.ui.show_unmapped_bn.clicked.connect(self.show_unmapped)
        self.ui.show_BN_bn.clicked.connect(self.show_BN)
        self.ui.show_no_mapping_bn.clicked.connect(self.show_no_data)
        self.ui.show_filtered_bn.clicked.connect(self.show_kicked)
        self.ui.show_missing_bn.clicked.connect(self.show_missing)
        self.ui.show_good_bn.clicked.connect(self.show_good)
        self.ui.show_rsp_bn.clicked.connect(self.show_site_p)
        self.ui.show_pp_bn.clicked.connect(self.show_pos_p)
        self.ui.show_both_bn.clicked.connect(self.show_both)
        self.clip = QtGui.QApplication.clipboard()
        #==================== mapping status panel ===================
        self.ui.save_select_bn.clicked.connect(self.save_select)
        self.ui.save_clear_bn.clicked.connect(self.save_clear)
        fig_format =['pdf','png','jpg','jpeg','eps', 'tif','ps', 'svg', 'svgz']
        self.ui.fig_format_combox.addItems(fig_format)
        self.ui.fig_format_combox.activated[str].connect(self.fig_format)
        self.ui.fig_save_bn.clicked.connect(self.save_fig)
        self.ui.save_all_bn.clicked.connect(self.save_all_figurs)
        self.ui.save_qlt_bn.clicked.connect(self.save_qlt)
    #======================================= Functions ==========================================
    def new(self):
        window = Main(self)
        window.show()

    def quit(self):
        response=QtGui.QMessageBox.question(self, 'Warning !', 'Do you want to close the appliction?',
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if response == QtGui.QMessageBox.Yes:
            sys.exit()

    def about(self):
        self.about_window = about()
        self.about_window.show()

    def manual(self):
        self.manual_window = manual()
        self.manual_window.show()

    def feedbacks(self):
        webbrowser.open("https://github.com/AppliedBioinformatics/BioNanoAnalyst/issues")

    def select_ref(self):
        if sys.platform == 'win32':
            ref = QFileDialog.getOpenFileName(self, 'Select reference sequences', '','sequences (*fasta *fa *fna)')
            self.ref=codecs.decode(str(ref)[1:-1].split(',')[0][2:-1],'unicode_escape')
            self.ui.ref_input.setText(self.ref)
        else:
            self.ref = unicode(QFileDialog.getOpenFileName(self, 'Select reference sequences', '','sequences (*fasta *fa *fna)'))
            self.ui.ref_input.setText(self.ref)

    def clear_ref(self):
        self.ui.ref_input.clear()
        self.ref = None

    def enable_raw(self):
        if self.ui.raw_checkBox.isChecked():
            if sys.platform =='win32':
                self.ui.raw_frame.setEnabled(False)
                self.ui.aligned_checkBox.setEnabled(False)
                QtGui.QMessageBox.question(self, 'Warning !', 'Currently Option 1 is only available in Linux and MacOS system !',
                    QtGui.QMessageBox.Ok)
            else:
                self.ui.raw_frame.setEnabled(True)
                self.ui.aligned_checkBox.setEnabled(False)
        else:
            self.ui.raw_frame.setEnabled(False)
            self.ui.aligned_checkBox.setEnabled(True)

    def enzyme(self):
        self.enz = self.ui.enzyme_combox.currentText()

    def select_bnx(self):
        if sys.platform == 'win32':
            bnx = QFileDialog.getOpenFileName(self,'Select bnx file','','bnx file (*.bnx)')
            self.bnx = codecs.decode(str(bnx)[1:-1].split(',')[0][2:-1],'unicode_escape')
            self.ui.raw_input.setText(self.bnx)
        else:
            self.bnx = unicode(QFileDialog.getOpenFileName(self,'Select bnx file','','bnx file (*.bnx)'))
            self.ui.raw_input.setText(self.bnx)

    def clear_bnx(self):
        self.ui.raw_input.clear()
        self.bnx = None

    def raw_settings(self):
        self.parameters_window = Settings()
        self.parameters_window.show()

    def raw_start(self):
        if QtGui.QMessageBox.Ok not in [self.handle_ref_error(), self.handle_bnx_error(), self.handle_settings_error()]:
            try:
                self.ui.raw_status_label.setStyleSheet('color: blue')
                self.ui.raw_status_label.setText('Running...')
                qApp.processEvents()
                self.ui.raw_status_label.repaint()
                self.run_assembler()
                self.run_refAligner()
                self.ui.raw_status_label.setStyleSheet('color: green')
                self.ui.raw_status_label.setText('Finished !')
            except:
                self.ui.raw_status_label.setStyleSheet('color: red')
                self.ui.raw_status_label.setText('Crashed !')
                self.ui.raw_status_label.repaint()
                qApp.processEvents()
                QtGui.QMessageBox.question(self, 'Error !', 'Something is wrong, please check the error messages!',QtGui.QMessageBox.Ok)


    def enable_aligned(self):
        if self.ui.aligned_checkBox.isChecked():
            self.ui.aligned_frame.setEnabled(True)
            self.ui.raw_checkBox.setEnabled(False)
        else:
            self.ui.aligned_frame.setEnabled(False)
            self.ui.raw_checkBox.setEnabled(True)

    def select_xmap(self):
        if sys.platform == 'win32':
            xmap = QFileDialog.getOpenFileName(self,'Select xmap file','','xmap file (*.xmap)')
            self.xmap = codecs.decode(str(xmap)[1:-1].split(',')[0][2:-1],'unicode_escape')
            self.ui.xmap_input.setText(self.xmap)
        else:
            self.xmap = unicode(QFileDialog.getOpenFileName(self,'Select xmap file','','xmap file (*.xmap)'))
            self.ui.xmap_input.setText(self.xmap)

    def clear_xmap(self):
        self.ui.xmap_input.clear()
        self.xmap = None

    def select_rcmap(self):
        if sys.platform == 'win32':
            rcmap = QFileDialog.getOpenFileName(self,'Select ref cmap file','','cmap file (*_r.cmap)')
            self.rcmap = codecs.decode(str(rcmap)[1:-1].split(',')[0][2:-1],'unicode_escape')
            self.ui.rcmap_input.setText(self.rcmap)
        else:
            self.rcmap = unicode(QFileDialog.getOpenFileName(self,'Select ref cmap file','','cmap file (*_r.cmap)'))
            self.ui.rcmap_input.setText(self.rcmap)

    def clear_rcmap(self):
        self.ui.rcmap_input.clear()
        self.rcmap = None

    def select_qcmap(self):
        if sys.platform == 'win32':
            qcmap = QFileDialog.getOpenFileName(self,'Select qry cmap file','','cmap file (*_q.cmap)')
            self.qcmap = codecs.decode(str(qcmap)[1:-1].split(',')[0][2:-1],'unicode_escape')
            self.ui.qcmap_input.setText(self.qcmap)
        else:
            self.qcmap = unicode(QFileDialog.getOpenFileName(self,'Select qry cmap file','','cmap file (*_q.cmap)'))
            self.ui.qcmap_input.setText(self.qcmap)

    def clear_qcmap(self):
        self.ui.qcmap_input.clear()
        self.qcmap = None

    def ctgs(self):
        ctg =self.ui.ctg_check_combox.currentText()
        sub = self.running.overall[self.running.overall['contig']==ctg].reset_index(drop=True)
        tsf=['siteID','position','coverage','score']
        sub[tsf]=sub[tsf].apply(pd.to_numeric)
        x=sub['siteID']
        y1=sub['coverage']
        y2=sub['score']
        pos=sub['position']
        D=dict()
        for t in range(len(x)):
            D[x[t]]=(pos[t],y2[t])
        x_scale =[x.min()-2,x.max()+2]
        #y1_scale=[y1.min()-2,y2.max()+2]
        y2_scale=[-1,8]
        try:
            for items in reversed(range(self.ui.gridLayout_7.count())):
                self.ui.gridLayout_7.itemAt(items).widget().deleteLater()
        except:
            pass
        self.ctg_figure = Figure(facecolor='w')
        self.axes =self.ctg_figure.add_axes([0.05, 0.14, 0.9, 0.8])
        #self.axes.hold(False)
        self.canvas_ctg = FigureCanvas(self.ctg_figure)
        #self.toolbar= NavigationToolbar(self.canvas_ctg, self)
        #self.ui.gridLayout_7.addWidget(self.toolbar,0, 0, 1, 1)
        self.ui.gridLayout_7.addWidget(self.canvas_ctg, 1, 0, 1, 1)
        ax2 = self.axes.twinx()
        self.axes.plot(x, y1, 'bo-')
        for j in range(len(y2)):
            if y2[j]==0:
                ax2.plot(x[j], y2[j], 'x',c='black')
            if y2[j]==1:
                ax2.plot(x[j], y2[j], 'd',c='red')
            if y2[j]==2:
                ax2.plot(x[j], y2[j], '<',c='purple')
            if y2[j]==3:
                ax2.plot(x[j], y2[j], '>',c='pink')
            if y2[j]==4:
                ax2.plot(x[j], y2[j], 'p',c='green')
        lines = [
            ('Consistent', {'color': 'green', 'linestyle': ':', 'marker': 'p'}),
            ('Number discordant', {'color': 'pink', 'linestyle': ':', 'marker': '>'}),
            ('Distance discordant', {'color': 'purple', 'linestyle': ':', 'marker': '<'}),
            ('Num+dis discordant', {'color': 'red', 'linestyle': ':', 'marker': 'd'}),
            ( 'No data', {'color': 'black', 'linestyle': ':', 'marker': 'x'})
        ]
        ax2.legend(
        [create_dummy_line(**l[1]) for l in lines],
        [l[0] for l in lines],
        loc='upper center',bbox_to_anchor=(0.5, 1.06),
        ncol=5, fancybox=True, shadow=True
        )
        ax2.plot(x,y2,'y-')
        self.axes.set_xlabel('SiteID')
        self.axes.set_xlim(x_scale)
        self.axes.set_ylabel('Coverage',color='b')
        #self.axes.set_ylim(y1_scale)
        ax2.set_ylabel('score')
        ax2.set_ylim(y2_scale)
        scale=1.1
        zp=ZoomPan()
        figZoom1=zp.zoom_factory(self.axes, base_scale=scale)
        figPan1=zp.pan_factory(self.axes)
        figZoom2=zp.zoom_factory(ax2, base_scale=scale)
        figPan2=zp.pan_factory(ax2.axes)
        self.canvas_ctg.mpl_connect('pick_event', DataCursor(ax2,D))
        ax2.set_picker(1)
        self.canvas_ctg.show()

    def save_select(self):
        self.output_path = unicode(QFileDialog.getExistingDirectory())
        self.ui.save_input.setText(self.output_path)
    def save_clear(self):
        self.ui.save_input.clear()
        self.output_path = None

    def fig_format(self):
        self.format = self.ui.fig_format_combox.currentText()

    def save_fig(self):
        ctg = self.ui.ctg_check_combox.currentText()
        format = self.ui.fig_format_combox.currentText()
        try:
            fig_name=r'%s/%s_mapping_status.%s'%(self.output_path,ctg,format)
            if sys.platform =='win32':
                fig_name = fig_name.replace('\\','/')
            self.ctg_figure.savefig(fig_name)
        except AttributeError:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please select a contig !',QtGui.QMessageBox.Ok)
        except IOError:
            QtGui.QMessageBox.question(self, 'Error !', 'Please select an output path !',QtGui.QMessageBox.Ok)

    def save_all_figurs(self):
        try:
            format = self.ui.fig_format_combox.currentText()
            for ctg in self.running.overall['contig'].unique():
                sub = self.running.overall[self.running.overall['contig']==ctg].reset_index(drop=True)
                tsf=['siteID','coverage','score']
                sub[tsf]=sub[tsf].apply(pd.to_numeric)
                x=sub['siteID']
                y1=sub['coverage']
                y2=sub['score']
                x_scale =[x.min()-2,x.max()+2]
                y2_scale=[-1,8]
                fig = plt.figure(figsize=(16.9,4),facecolor='w')
                ax1 = fig.add_axes([0.05, 0.14, 0.9, 0.8])
                ax2 = ax1.twinx()
                ax1.plot(x, y1, 'bo-')
                for j in range(len(y2)):
                    if y2[j]==0:
                        ax2.plot(x[j], y2[j], 'x',c='black')
                    if y2[j]==1:
                        ax2.plot(x[j], y2[j], 'd',c='red')
                    if y2[j]==2:
                        ax2.plot(x[j], y2[j], '<',c='purple')
                    if y2[j]==3:
                        ax2.plot(x[j], y2[j], '>',c='pink')
                    if y2[j]==4:
                        ax2.plot(x[j], y2[j], 'p',c='green')
                lines = [
                    ('Consistent', {'color': 'green', 'linestyle': ':', 'marker': 'p'}),
                    ('Number discordant', {'color': 'pink', 'linestyle': ':', 'marker': '>'}),
                    ('Distance discordant', {'color': 'purple', 'linestyle': ':', 'marker': '<'}),
                    ('Num+dis discordant', {'color': 'red', 'linestyle': ':', 'marker': 'd'}),
                    ( 'No data', {'color': 'black', 'linestyle': ':', 'marker': 'x'})]
                ax2.legend(
                [create_dummy_line(**l[1]) for l in lines],
                [l[0] for l in lines],
                loc='upper center',bbox_to_anchor=(0.5, 1.06),
                ncol=5, fancybox=True, shadow=True)
                ax2.plot(x,y2,'y-')
                ax1.set_xlabel('SiteID')
                ax1.set_xlim(x_scale)
                ax1.set_ylabel('Coverage',color='b')
                ax2.set_ylabel('score')
                ax2.set_ylim(y2_scale)
                fig_name=r'%s/%s_mapping_status.%s'%(self.output_path,ctg,format)
                if sys.platform =='win32':
                    fig_name = fig_name.replace('\\','/')
                fig.savefig(fig_name,format=format)
                fig.clf()
                plt.close()
        except IOError:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please select an output loaction !',QtGui.QMessageBox.Ok)
        except AttributeError:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please check the contig(s) !',QtGui.QMessageBox.Ok)

    def save_qlt(self):
        try:
            curr_time=datetime.now().strftime('%Y%m%d_%H-%M-%S')
            if sys.platform=='win32':
                path=r'%s'% self.output_path
            else:
                path=self.output_path
            name='BioNanoAnalyst_report_cs%s_%s.gff3'% (self.cs,curr_time)
            name_all='BioNanoAnalyst_report_overall_pairs_cs%s_%s.txt'% (self.cs, curr_time)
	    test=len(self.running.overall)
            fd=open(os.path.join(path,name),'w')
            for j in self.running.overall['contig'].unique():
                sub=self.running.overall[self.running.overall['contig']==j].reset_index(drop=True)
                startp=sub['position'][0]
                i=1
                ctg=sub['contig'][0]
                while i < len(sub):
                    score1=sub['score'][i-1]
                    score2=sub['score'][i]
                    status1=sub['mapping_status'][i-1]
                    status2=sub['mapping_status'][i-1]
                    if score1==score2 and i!=len(sub)-1:
                        next
                    if score1==score2 and i==len(sub)-1:
                        fd.write('%s\tBioNanoAnalyst\tOptical_mapping\t%s\t%s\t.\t.\t.\tName=%s\n'% (ctg,startp, sub['position'][i], sub['mapping_status'][i]))
                    if score1>score2 and i!=len(sub)-1:
                        endp=sub['position'][i]
                        fd.write('%s\tBioNanoAnalyst\tOptical_mapping\t%s\t%s\t.\t.\t.\tName=%s\n'% (ctg,startp, endp, sub['mapping_status'][i-1]))
                        startp=endp
                    if score1>score2 and i==len(sub)-1:
                        fd.write('%s\tBioNanoAnalyst\tOptical_mapping\t%s\t%s\t.\t.\t.\tName=%s\n'% (ctg,startp, sub['position'][i], sub['mapping_status'][i]))
                    if score1<score2 and i!=len(sub)-1:
                        endp=sub['position'][i-1]
                        fd.write('%s\tBioNanoAnalyst\tOptical_mapping\t%s\t%s\t.\t.\t.\tName=%s\n'% (ctg,startp, endp, sub['mapping_status'][i-1]))
                        startp=endp
                    if score1<score2 and i==len(sub)-1:
                        fd.write('%s\tBioNanoAnalyst\tOptical_mapping\t%s\t%s\t.\t.\t.\tName=%s\n'% (ctg,startp, sub['position'][i], sub['mapping_status'][i]))
                    i+=1
            self.running.paired.to_csv(os.path.join(path,name_all),sep='\t', index=False)
        except IOError:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please select an output loaction !',QtGui.QMessageBox.Ok)
        except AttributeError:
            return QtGui.QMessageBox.question(self, 'Error !', 'No report can be saved !',QtGui.QMessageBox.Ok)

    def handle_ref_error(self):
        try:
            if os.stat(self.ref).st_size>0:
                with open(self.ref) as f:
                    for i in range(2):
                        line=f.next().strip()
                        if i == 0 and line[0]!='>':
                            return QtGui.QMessageBox.question(self, 'Error !', 'Please check your input reference !',
                            QtGui.QMessageBox.Ok)
                        if i == 1 and len(re.findall("[^ATGCN]", line.upper()))>0:
                            return QtGui.QMessageBox.question(self, 'Error !', 'Please check your input reference !',
                            QtGui.QMessageBox.Ok)
            else:
                return QtGui.QMessageBox.question(self, 'Warning !', 'The selected reference file is empty, please check !',
                QtGui.QMessageBox.Ok)
        except:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please input a reference file !',
            QtGui.QMessageBox.Ok)

    def handle_bnx_error(self):
        try:
            if os.stat(self.bnx).st_size == 0:
                return QtGui.QMessageBox.question(self, 'Warning !', 'The selected bnx file is empty, please check !',
                QtGui.QMessageBox.Ok)
        except:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please input a .bnx file !', QtGui.QMessageBox.Ok)

    def handle_settings_error(self):
        try:
            self.settings = self.parameters_window.parameters
        except:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please check your settings !',
            QtGui.QMessageBox.Ok)

    def handle_xmap_error(self):
        try:
            if os.stat(self.xmap).st_size == 0:
                return QtGui.QMessageBox.question(self, 'Warning !', 'The selected xmap file is empty, please check !',
                QtGui.QMessageBox.Ok)
        except:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please input a .xmap file !', QtGui.QMessageBox.Ok)

    def handle_rcmap_error(self):
        try:
            if os.stat(self.rcmap).st_size == 0:
                return QtGui.QMessageBox.question(self, 'Warning !', 'The selected _r.cmap file is empty, please check !',
                QtGui.QMessageBox.Ok)
        except:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please input a _r.cmap file !', QtGui.QMessageBox.Ok)

    def handle_qcmap_error(self):
        try:
            if os.stat(self.qcmap).st_size == 0:
                return QtGui.QMessageBox.question(self, 'Warning !', 'The selected _q.cmap file is empty, please check !',
                QtGui.QMessageBox.Ok)
        except:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please input a _q.cmap file !', QtGui.QMessageBox.Ok)

    def corresponding_check(self):
        if QtGui.QMessageBox.Ok not in [self.handle_xmap_error(), self.handle_rcmap_error(), self.handle_qcmap_error()]:
            self.files = dict()
            self.files['xmap'] = self.xmap
            with open (self.xmap) as xmap:
                for i in range(20): # the value here can be changed
                    try:
                        line = r'%s' % xmap.next().strip()
                        line = line.replace('\\','/')
                    except StopIteration:
                        pass
                    if line.startswith('# Reference Maps From:'):
                        try:
                            line = line.split()[-1].rsplit('/',1)[-1]
                            rcmap = self.rcmap.rsplit('/',1)[-1]
                            if line != rcmap:
                                return QtGui.QMessageBox.question(self, 'Error !', 'Rcmap file name in Xmap file is not the one you select !',
                                QtGui.QMessageBox.Ok)
                            else:
                                self.files['rcmap'] = self.rcmap
                        except:
                            return QtGui.QMessageBox.question(self, 'Error !', 'Please check your xmap file !', QtGui.QMessageBox.Ok)
                    if line.startswith('# Query Maps From:'):
                        try:
                            line = line.split()[-1]
                            line = line.rsplit('/',1)[-1]
                            qcmap = self.qcmap.rsplit('/',1)[-1]
                            if line != qcmap:
                                return QtGui.QMessageBox.question(self, 'Error !', 'Qcmap file name in Xmap file is not the one you select !',
                                 QtGui.QMessageBox.Ok)
                            else:
                                self.files['qcmap'] = self.qcmap
                        except:
                            return QtGui.QMessageBox.question(self, 'Error !', 'Please check your xmap file !', QtGui.QMessageBox.Ok)

    def handle_cs_error(self):
        cs = self.ui.cs_input.text()
        try:
            self.cs = float(cs)
            if self.cs < 0:
                return QtGui.QMessageBox.question(self, 'Error !', 'Please input a confidence score >=0',
                 QtGui.QMessageBox.Ok)
        except ValueError:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please input a confidence score >=0',
            QtGui.QMessageBox.Ok)

    def handle_O1(self):
        if QtGui.QMessageBox.Ok in [self.handle_bnx_error(), self.handle_settings_error()]:
            return False
        else:
            return True

    def handle_O2(self):
        if QtGui.QMessageBox.Ok in [self.handle_xmap_error(), self.handle_rcmap_error(), self.handle_qcmap_error()]:
            return False
        else:
            return True

    def analyse(self):
        if QtGui.QMessageBox.Ok not in [self.handle_ref_error()]:
            pass
        else:
            return
        if QtGui.QMessageBox.Ok not in [self.handle_cs_error()]:
            pass
        else:
            return
        if self.ui.raw_checkBox.isChecked():
            if sys.platform == 'win32':
                return QtGui.QMessageBox.question(self, 'Error !', 'Currently Option 1 is not available in Windows !',
                QtGui.QMessageBox.Ok)
            if self.handle_O1()== True:
                try:
                    if os.path.exists(self.xmap) and os.path.exists(self.rcmap) and os.path.exists(self.qcmap):
                        t1=time()
                        try:
                            self.ui.ctg_check_combox.clear()
                            self.ui.textBrowser.clear()
                            self.ui.verticalLayout_3.takeAt(0).widget().setParent(None)
                            self.canvas_ctg.close()
                        except:
                            pass
                        try:
                            for items in reversed(range(self.ui.gridLayout_7.count())):
                                self.ui.gridLayout_7.itemAt(items).widget().deleteLater()
                        except:
                                pass
                        mapping_status_view=QtGui.QGraphicsView(self.ui.mapping_status_frame)
                        self.ui.gridLayout_7.addWidget(mapping_status_view, 0, 0, 1, 1)
                        try:
                            ## Start analysis
                            self.running = BioNano(self.xmap, self.rcmap, self.qcmap, self.cs, self.ref)
                            self.running.convert_tables()
                            ## Emit the running signal
                            self.ui.analyse_status_label.setStyleSheet('color: blue')
                            self.ui.analyse_status_label.setText('Running...')
                            qApp.processEvents()
                            self.ui.analyse_status_label.repaint()
                            self.running.BioNano_stats()
                            self.running.parse_fasta()
                            self.running.qualification_filter()
                            self.running.mapping_filter()
                            self.running.getDetail()
                            self.running.getMissing()
                            self.running.getPaired()
                            self.running.checkStatus()
                            self.running.merge()
                            self.stats()
                            self.ui.ctg_check_combox.addItems([i for i in self.running.mapped['contig']])
                            self.ui.ctg_check_combox.activated[str].connect(self.ctgs)
                            ## Make graphs
                            self.figure = plt.figure(facecolor='w')
                            self.figure.hold(False)
                            self.canvas = FigureCanvas(self.figure)
                            self.canvas.setMaximumSize(720,420)
                            self.ui.verticalLayout_3.addWidget(self.canvas)
                            ax=plt.subplot()
                            labels = np.char.array(['unqualified', 'no mapping','filtered', 'mapped'])
                            sizes = np.array([self.unqualified_len, self.no_mapping_len, self.filtered_len, self.mapped_len])
                            colors = ['lightcoral', 'gold', 'lightskyblue', 'yellowgreen']
                            explode = (0, 0, 0, 0.1)
                            porcent = 100.*sizes/sizes.sum()
                            patches, texts= plt.pie (sizes, colors=colors, startangle=140, shadow=True,explode=explode)
                            Labels=['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, porcent)]
                            plt.legend(patches, Labels, loc='upper left', bbox_to_anchor=(-0.1, 1.),fontsize=8)
                            plt.text(0.5,1.08,'Proportion of sublength to total reference length',horizontalalignment='center',fontsize=18,transform = ax.transAxes)
                            #plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
                            #plt.title('Proportion of sublength to total reference length')
                            plt.axis('equal')
                            self.canvas.draw()
                            ## Emit the 'finished' signal
                            self.ui.analyse_status_label.setStyleSheet('color: green')
                            self.ui.analyse_status_label.setText('Finished !')
                            t2=time()
                            print 'The running time is %.2f seconds'%(t2-t1)
                        except AttributeError:
                            return
                except:
                    QtGui.QMessageBox.question(self, 'Error !', 'BioNano optical mapping from option 1 is incomplete, please check !',
                    QtGui.QMessageBox.Ok)

        if self.ui.aligned_checkBox.isChecked():
            if self.handle_O2()== True:
                t1=time()
                try:
                    self.ui.ctg_check_combox.clear()
                    self.ui.textBrowser.clear()
                    self.ui.verticalLayout_3.takeAt(0).widget().setParent(None)
                    self.canvas_ctg.close()
                except:
                    pass
                try:
                    for items in reversed(range(self.ui.gridLayout_7.count())):
                        #self.ui.gridLayout_7.itemAt(items).widget().deleteLater()
                        self.ui.gridLayout_7.itemAt(items).widget().setParent(None)
                except:
                    pass
                mapping_status_view=QtGui.QGraphicsView(self.ui.mapping_status_frame)
                self.ui.gridLayout_7.addWidget(mapping_status_view, 0, 0, 1, 1)
                try:
                    ## Start analysis
                    self.running = BioNano(self.xmap, self.rcmap, self.qcmap, self.cs, self.ref)
                    self.running.convert_tables()
                    ## Emit the running signal
                    self.ui.analyse_status_label.setStyleSheet('color: blue')
                    self.ui.analyse_status_label.setText('Running...')
                    qApp.processEvents()
                    self.ui.analyse_status_label.repaint()
                    self.running.BioNano_stats()
                    self.running.parse_fasta()
                    self.running.qualification_filter()
                    self.running.mapping_filter()
                    self.running.getDetail()
                    self.running.getMissing()
                    self.running.getPaired()
                    self.running.checkStatus()
                    self.running.merge()
                    self.stats()
                    self.ui.ctg_check_combox.addItems([i for i in self.running.mapped['contig']])
                    self.ui.ctg_check_combox.activated[str].connect(self.ctgs)
                    ## Make graphs
                    self.figure = plt.figure(facecolor='w')
                    self.figure.hold(False)
                    self.canvas = FigureCanvas(self.figure)
                    self.canvas.setMaximumSize(720,420)
                    self.ui.verticalLayout_3.addWidget(self.canvas)
                    ax=plt.subplot()
                    labels = np.char.array(['unqualified', 'no mapping','filtered', 'mapped'])
                    sizes = np.array([self.unqualified_len, self.no_mapping_len, self.filtered_len, self.mapped_len])
                    colors = ['lightcoral', 'gold', 'lightskyblue', 'yellowgreen']
                    explode = (0, 0, 0, 0.1)
                    porcent = 100.*sizes/sizes.sum()
                    patches, texts= plt.pie (sizes, colors=colors, startangle=140, shadow=True,explode=explode)
                    Labels=['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, porcent)]
                    plt.legend(patches, Labels, loc='upper left', bbox_to_anchor=(-0.1, 1.),fontsize=8)
                    plt.text(0.5,1.08,'Proportion of sublength to total reference length',horizontalalignment='center',fontsize=18,transform = ax.transAxes)
                    #plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
                    #plt.title('Proportion of sublength to total reference length')
                    plt.axis('equal')
                    self.canvas.draw()
                    ## Emit the 'finished' signal
                    self.ui.analyse_status_label.setStyleSheet('color: green')
                    self.ui.analyse_status_label.setText('Finished !')
                    t2=time()
                    print 'The running time is %.2f seconds' % (t2-t1)
                except AttributeError:
                    return
        if not self.ui.raw_checkBox.isChecked() and not self.ui.aligned_checkBox.isChecked():
            return QtGui.QMessageBox.question(self, 'Error !', 'Please select Option 1 or Option 2 and fill it !',
            QtGui.QMessageBox.Ok)

    def show_ref(self):
        try:
            self.ref_table.setWindowTitle('Information for reference')
            self.ref_table.setColumnCount(len(self.running.ref_detail.columns))
            self.ref_table.setRowCount(len(self.running.ref_detail.index))
            for i in range(len(self.running.ref_detail.index)):
                for j in range(len(self.running.ref_detail.columns)):
                    self.ref_table.setItem(i,j,QTableWidgetItem(str(self.running.ref_detail.iat[i, j])))
            self.ref_table.setHorizontalHeaderLabels(['Index','Contig','Length(bp)','Splitted_ctg',
            'Start','End','Id_in_all'])
            self.ref_table.setMinimumSize(380,560)
            self.ref_table.show()
        except:
            pass
    def show_unqualified(self):
        try:
            self.unqualified_table.setWindowTitle('Information for unqualified contigs')
            self.unqualified_table.setColumnCount(len(self.running.unqualified.columns))
            self.unqualified_table.setRowCount(len(self.running.unqualified.index))
            for i in range(len(self.running.unqualified.index)):
                for j in range(len(self.running.unqualified.columns)):
                    self.unqualified_table.setItem(i,j,QTableWidgetItem(str(self.running.unqualified.iat[i, j])))
            self.unqualified_table.setHorizontalHeaderLabels(['index','contig','length(bp)'])
            self.unqualified_table.setMinimumSize(380,560)
            self.unqualified_table.show()
        except:
            pass

    def show_qualified(self):
        try:
            self.qualified_table.setWindowTitle('Information for qualified contigs')
            self.qualified_table.setColumnCount(len(self.running.qualified.columns))
            self.qualified_table.setRowCount(len(self.running.qualified.index))
            for i in range(len(self.running.qualified.index)):
                for j in range(len(self.running.qualified.columns)):
                    self.qualified_table.setItem(i,j,QTableWidgetItem(str(self.running.qualified.iat[i, j])))
            self.qualified_table.setHorizontalHeaderLabels(['index','contig','length(bp)','numSites'])
            self.qualified_table.setMinimumSize(450,560)
            self.qualified_table.show()
        except:
            pass

    def show_BN(self):
        try:
            self.BN_table.setWindowTitle('Information for matched BioNano data')
            self.BN_table.setColumnCount(len(self.running.BN.columns))
            self.BN_table.setRowCount(len(self.running.BN.index))
            for i in range(len(self.running.BN.index)):
                for j in range(len(self.running.BN.columns)):
                    self.BN_table.setItem(i,j,QTableWidgetItem(str(self.running.BN.iat[i, j])))
            self.BN_table.setHorizontalHeaderLabels(['CMapId','ContigLength','NumSites'])
            self.BN_table.setMinimumSize(380,560)
            self.BN_table.show()
        except:
            pass

    def show_unmapped(self):
        try:
            self.unmapped_table.setWindowTitle('Information for unmapped contigs')
            self.unmapped_table.setColumnCount(len(self.running.unmapped.columns))
            self.unmapped_table.setRowCount(len(self.running.unmapped.index))
            for i in range(len(self.running.unmapped.index)):
                for j in range(len(self.running.unmapped.columns)):
                    self.unmapped_table.setItem(i,j,QTableWidgetItem(str(self.running.unmapped.iat[i, j])))
            self.unmapped_table.setHorizontalHeaderLabels(['index','contig','length(bp)','numSites'])
            self.unmapped_table.setMinimumSize(450,560)
            self.unmapped_table.show()
        except:
            pass

    def show_mapped(self):
        try:
            self.mapped_table.setWindowTitle('Information for mapped contigs')
            self.mapped_table.setColumnCount(len(self.running.mapped.columns))
            self.mapped_table.setRowCount(len(self.running.mapped.index))
            for i in range(len(self.running.mapped.index)):
                for j in range(len(self.running.mapped.columns)):
                    self.mapped_table.setItem(i,j,QTableWidgetItem(str(self.running.mapped.iat[i, j])))
            self.mapped_table.setHorizontalHeaderLabels(['index','contig','length(bp)','numSites'])
            self.mapped_table.setMinimumSize(450,560)
            self.mapped_table.show()
        except:
            pass

    def show_kicked(self):
        try:
            self.filtered_table.setWindowTitle('Information for filtered contigs')
            self.filtered_table.setColumnCount(len(self.running.kicked.columns))
            self.filtered_table.setRowCount(len(self.running.kicked.index))
            for i in range(len(self.running.kicked.index)):
                for j in range(len(self.running.kicked.columns)):
                    self.filtered_table.setItem(i,j,QTableWidgetItem(str(self.running.kicked.iat[i, j])))
            self.filtered_table.setHorizontalHeaderLabels(['index','contig','length(bp)','numSites'])
            self.filtered_table.setMinimumSize(450,560)
            self.filtered_table.show()
        except:
            pass

    def show_no_data(self):
        try:
            self.no_data_table.setWindowTitle('Information for contigs with no BioNano data matched')
            self.no_data_table.setColumnCount(len(self.running.no_data.columns))
            self.no_data_table.setRowCount(len(self.running.no_data.index))
            for i in range(len(self.running.no_data.index)):
                for j in range(len(self.running.no_data.columns)):
                    self.no_data_table.setItem(i,j,QTableWidgetItem(str(self.running.no_data.iat[i, j])))
            self.no_data_table.setHorizontalHeaderLabels(['index','contig','length(bp)','numSites'])
            self.no_data_table.setMinimumSize(450,560)
            self.no_data_table.show()
        except:
            pass

    def show_missing(self):
        try:
            self.missing_table.setWindowTitle('Information for ref restriction site missing mapping')
            self.missing_table.setColumnCount(len(self.running.missing.columns))
            self.missing_table.setRowCount(len(self.running.missing.index))
            for i in range(len(self.running.missing.index)):
                for j in range(len(self.running.missing.columns)):
                    self.missing_table.setItem(i,j,QTableWidgetItem(str(self.running.missing.iat[i, j])))
            self.missing_table.setHorizontalHeaderLabels(['index','contig','siteID','position','numSites'])
            self.missing_table.setMinimumSize(500,560)
            self.missing_table.show()
        except:
            pass


    def show_good(self):
        try:
            self.good_table.setWindowTitle('Information for well matched ref restriction site')
            self.good_table.setColumnCount(len(self.running.good.columns))
            self.good_table.setRowCount(len(self.running.good.index))
            for i in range(len(self.running.good.index)):
                for j in range(len(self.running.good.columns)):
                    self.good_table.setItem(i,j,QTableWidgetItem(str(self.running.good.iat[i,j])))
            self.good_table.setHorizontalHeaderLabels(['index','contig','siteID','position','numSites'])
            self.good_table.setMinimumSize(500,560)
            self.good_table.show()
        except:
            pass
    def show_site_p(self):
        try:
            self.site_p_table.setWindowTitle('Information for ref restriction site having number of site matching problem')
            self.site_p_table.setColumnCount(len(self.running.q_rs_a.columns))
            self.site_p_table.setRowCount(len(self.running.q_rs_a.index))
            for i in range(len(self.running.q_rs_a.index)):
                for j in range(len(self.running.q_rs_a.columns)):
                    self.site_p_table.setItem(i,j,QTableWidgetItem(str(self.running.q_rs_a.iat[i,j])))
            self.site_p_table.setHorizontalHeaderLabels(['index','contig','siteID','position','numSites'])
            self.site_p_table.setMinimumSize(500,560)
            self.site_p_table.show()
        except:
            pass
    def show_pos_p(self):
        try:
            self.pos_p_table.setWindowTitle('Information for ref restriction site having postion matching problem')
            self.pos_p_table.setColumnCount(len(self.running.q_dis_a.columns))
            self.pos_p_table.setRowCount(len(self.running.q_dis_a.index))
            for i in range(len(self.running.q_dis_a.index)):
                for j in range(len(self.running.q_dis_a.columns)):
                    self.pos_p_table.setItem(i,j,QTableWidgetItem(str(self.running.q_dis_a.iat[i,j])))
            self.pos_p_table.setHorizontalHeaderLabels(['index','contig','siteID','position','numSites'])
            self.pos_p_table.setMinimumSize(500,560)
            self.pos_p_table.show()
        except:
            pass
    def show_both(self):
        try:
            self.both_table.setWindowTitle('Information for ref restriction site having both problems')
            self.both_table.setColumnCount(len(self.running.both.columns))
            self.both_table.setRowCount(len(self.running.both.index))
            for i in range(len(self.running.both.index)):
                for j in range(len(self.running.both.columns)):
                    self.both_table.setItem(i,j,QTableWidgetItem(str(self.running.both.iat[i,j])))
            self.both_table.setHorizontalHeaderLabels(['index','contig','siteID','position','numSites'])
            self.both_table.setMinimumSize(500,560)
            self.both_table.show()
        except:
            pass
    def stats(self):
        unqualified = None
        unqualified_len = None
        unmapped = None
        unmapped_len = None
        no_mapping = None
        no_mapping_len = None
        filtered =None
        filtered_len =None
        ref_ctgs=len(self.running.ref_id)
        ref_len = sum([i for i in self.running.ref_inf.values()])/1.0e6
        ref_N = self.running.N/1.0e6
        mapped = len(self.running.mapped.index)
        mapped_len = sum([int(i) for i in self.running.mapped['length(bp)']])
        BN = len(self.running.BN.index)
        BN_len = sum([int(i) for i in self.running.BN['ContigLength']])/1.0e6
        qualified = len(self.running.qualified.index)
        qualified_len = sum([int(i) for i in self.running.qualified['length(bp)']])/1.0e6
        try:
            unqualified = len(self.running.unqualified.index)
            unqualified_len = sum([int(i) for i in self.running.unqualified['length(bp)']])
        except:
            pass
        try:
            unmapped = len(self.running.unmapped.index)
            unmapped_len = sum([int(i) for i in self.running.unmapped['length(bp)']])/1.0e6
        except:
            pass
        try:
            no_mapping = len(self.running.no_data.index)
            no_mapping_len = sum([int(i) for i in self.running.no_data['length(bp)']])
        except:
            pass
        try:
            filtered = len(self.running.kicked.index)
            filtered_len = sum([int(i) for i in self.running.kicked['length(bp)']])
        except:
            pass
        self.ui.textBrowser.append('\n')
        self.ui.textBrowser.append('When confidence score = %s, the statistics are listed as below:\n'%self.cs)
        self.ui.textBrowser.append('Subject\tNumContig\tTotalLength(Mb)\tLen2Ref (%)\t\tNum2Ref (%)')
        self.ui.textBrowser.append('Reference\t%s\t%.2f\t\t100.00\t\t100.00'%(ref_ctgs,ref_len))
        self.ui.textBrowser.append('Qualified\t%s\t%.2f\t\t%.2f\t\t%.2f'%(qualified,qualified_len,qualified_len/ref_len*100,float(qualified)/ref_ctgs*100))
        try:
            self.ui.textBrowser.append('Unqualified\t%s\t%.2f\t\t%.2f\t\t%.2f'%(unqualified,unqualified_len/1.0e6,unqualified_len/1.0e4/ref_len,float(unqualified)/ref_ctgs*100))
        except:
            pass
        try:
            self.ui.textBrowser.append('Unmapped\t%s\t%.2f\t\t%.2f\t\t%.2f'%(unmapped,unmapped_len,unmapped_len/ref_len*100,float(unmapped)/ref_ctgs*100))
        except:
            pass
        try:
            self.ui.textBrowser.append('No mapping\t%s\t%.2f\t\t%.2f\t\t%.2f'%(no_mapping,no_mapping_len/1.0e6,no_mapping_len/1.0e4/ref_len,float(no_mapping)/ref_ctgs*100))
        except:
            pass
        try:
            self.ui.textBrowser.append('filtered\t%s\t%.2f\t\t%.2f\t\t%.2f'%(filtered,filtered_len/1.0e6,filtered_len/1.0e4/ref_len,float(filtered)/ref_ctgs*100))
        except:
            pass
        self.ui.textBrowser.append('Mapped\t%s\t%.2f\t\t%.2f\t\t%.2f'%(mapped,mapped_len/1.0e6,mapped_len/1.0e4/ref_len,float(mapped)/ref_ctgs*100))
        self.ui.textBrowser.append('BioNano\t%s\t%.2f\t\tNA\t\tNA\n'%(BN,BN_len))
        self.ui.textBrowser.append('Note: The totoal length of Ns in the reference is %s Mb.\n'%ref_N)
        self.unqualified_len = unqualified_len
        self.mapped_len = mapped_len
        self.no_mapping_len = no_mapping_len
        self.filtered_len = filtered_len

    def run_assembler(self):
        pgm = 'python'
        script = self.settings['script_path']+'/pipelineCL.py'
        thread = '-T %s'% self.settings['threads']
        jobs = '-j %s'% self.settings['jobs']
        iter = '-i %s'% self.settings['iteration']
        tools = '-t %s'% self.settings['tools_path']
        if self.settings['gs']>=500:
            xml = '-a ' + self.settings['script_path']+'/optArguments_human.xml'
        elif self.settings['gs']<500 and self.settings['gs']>100:
            xml = '-a '+ self.settings['script_path']+'/optArguments_medium.xml'
        else:
            xml = '-a '+ self.settings['script_path']+'/optArguments_small.xml'
        name = self.ref.rsplit('/',1)[-1].rsplit('.',1)[0]
        self.raw_output = '-l '+self.settings['output_path']+'/'+name
        bnx = self.bnx.replace(' ','\ ')
        bnx = '-b '+bnx
        cmd = '%s %s -w -d -U %s %s %s %s %s %s %s'%(pgm, script, thread, jobs, iter, tools, xml, self.raw_output, bnx)
        os.system(cmd)
    def run_refAligner(self):
        name = self.ref.rsplit('/',1)[-1].rsplit('.',1)[0]
        self.enzyme()
        make_RefCmap(self.ref, enz=str(self.enz), min_len=20, min_nsite=5, path=self.settings['output_path'])
        rcmap = self.settings['output_path']+'/'+name+'_'+self.enz+'.cmap'
        pgm = self.settings['tools_path']+'/RefAligner'
        ref = '-ref %s'% rcmap
        qcmap = '-i '+self.settings['output_path']+'/'+name+'/contigs/exp_refineFinal1/EXP_REFINEFINAL1.cmap'
        outprefix = '-o %s'% (self.settings['output_path']+'/'+name)
        cmd = '%s -f %s %s %s -maxthreads 32 -res 2.9 -FP 0.6 -FN 0.06 -sf 0.20 -sd 0.0 -sr 0.01 -extend 1 -outlier 0.0001 -endoutlier 0.001 -PVendoutlier -deltaX 12 -deltaY 12 -xmapchim 12 -hashgen 5 7 2.4 1.5 0.05 5.0 1 1 1 -hash -hashdelta 50 -mres 1e-3 -hashMultiMatch 100 -insertThreads 4 -nosplit 2 -biaswt 0 -T 1e-12 -S -1000 -indel -PVres 2 -rres 0.9 -MaxSE 0.5 -HSDrange 1.0 -outlierBC -xmapUnique 12 -AlignRes 2. -outlierExtend 12 24 -Kmax 12 -f -maxmem 128 -BestRef 1 -stdout -stderr' % (pgm, ref, qcmap, outprefix)
        os.system(cmd)
        self.xmap = outprefix+'.xmap'
        self.rcmap = outprefix+'_r.cmap'
        self.qcmap = outprefix+'_q.cmap'

def create_dummy_line(**kwds):
    return Line2D([], [], **kwds)



class Settings(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.tools_path = None
        self.scripts_path = None
        self.gs = None
        self.output_path = None
        self.threads = 4
        self.jobs = 2
        self. iteration = 5
        self.ui.tools_location_selecet_bn.clicked.connect(self.select_tools_path)
        self.ui.tools_location_clear_bn.clicked.connect(self.clear_tools_path)
        self.ui.scripts_location_selecet_bn.clicked.connect(self.select_scripts_path)
        self.ui.scripts_location_clear_bn.clicked.connect(self.clear_scripts_path)
        self.ui.threads_spinBox.setValue(self.threads)
        self.ui.threads_spinBox.setMinimum(1)
        self.ui.jobs_spinBox.setValue(self.jobs)
        self.ui.jobs_spinBox.setMinimum(1)
        self.ui.iteration_spinBox.setValue(self. iteration)
        self.ui.iteration_spinBox.setMinimum(1)
        self.ui.output_select_bn.clicked.connect(self.select_output_path)
        self.ui.output_clear_bn.clicked.connect(self.clear_output_path)
        self.ui.setting_confirm_frame.accepted.connect(self.confirm)
        self.ui.setting_confirm_frame.rejected.connect(self.cancel)

    def select_tools_path(self):
        self.tools_path = unicode(QFileDialog.getExistingDirectory())
        self.ui.tools_location_input.setText(self.tools_path)

    def clear_tools_path(self):
        self.ui.tools_location_input.clear()
        self.tools_path = None

    def select_scripts_path(self):
        self.scripts_path = unicode(QFileDialog.getExistingDirectory())
        self.ui.scripts_location_input.setText(self.scripts_path)

    def clear_scripts_path(self):
        self.ui.scripts_location_input.clear()
        self.scripts_path = None


    def select_output_path(self):
        self.output_path = str (QFileDialog.getExistingDirectory())
        self.ui.output_input.setText(self.output_path)

    def clear_output_path(self):
        self.ui.output_input.clear()
        self.output_path = None

    def confirm_tool_path(self):
        try:
            if sys.platform == 'win32':
                assembler = (self.tools_path + '\WindowsAssembler.exe').replace('\\','/')
                refaligner = (self.tools_path + '\WindowsRefAligner.exe').replace('\\','/')
                if not (os.path.exists(assembler) and os.path.exists(refaligner)):
                    return QtGui.QMessageBox.question(self, 'Error !', 'Please check the tool path or tools inside !',
                    QtGui.QMessageBox.Ok)
                else:
                    if os.access(assembler, os.X_OK) == False:
                        return QtGui.QMessageBox.question(self, 'Warning!', 'WindowsAssembler.exe is not executable, please check !',
                        QtGui.QMessageBox.Ok)
                    if os.access(refaligner, os.X_OK) == False:
                        return QtGui.QMessageBox.question(self, 'Warning!', 'WindowsRefAligner.exe is not executable, please check !',
                        QtGui.QMessageBox.Ok)
            else:
                assembler = self.tools_path + '/Assembler'
                refaligner = self.tools_path + '/RefAligner'
                if not (os.path.exists(assembler) and os.path.exists(refaligner)):
                    return QtGui.QMessageBox.question(self, 'Error !', 'Please check the tool path or tools inside !',
                    QtGui.QMessageBox.Ok)
                else:
                    if os.access(assembler, os.X_OK) == False:
                        return QtGui.QMessageBox.question(self, 'Warning!', 'Assembler is not executable, please check !',
                        QtGui.QMessageBox.Ok)
                    if  os.access(refaligner, os.X_OK) == False:
                        return QtGui.QMessageBox.question(self, 'Warning!', 'RefAligner is not executable, please check !',
                        QtGui.QMessageBox.Ok)
        except:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please check the tool path or tools inside !', QtGui.QMessageBox.Ok)

    def confirm_scripts_path(self):
        try:
            script1=self.scripts_path+'/pipelineCL.py'
            script2=self.scripts_path+'/Pipeline.py'
            if not (os.path.exists(script1) and os.path.exists(script2)):
                return QtGui.QMessageBox.question(self, 'Error !', 'Please check the scripts path or scripts inside !',
                    QtGui.QMessageBox.Ok)
        except:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please check the scripts path or scripts inside !',
                    QtGui.QMessageBox.Ok)

    def confirm_output_path(self):
        try:
            len(self.output_path)
        except:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please select a output path !', QtGui.QMessageBox.Ok)

    def confirm_gs(self):
        self.gs= self.ui.gs_input.text()
        try:
            self.gs = float(self.gs)
            if self.gs<=0:
                return QtGui.QMessageBox.question(self, 'Error !', 'Please input a genome size bigger than 0 !', QtGui.QMessageBox.Ok)
        except ValueError:
            return QtGui.QMessageBox.question(self, 'Error !', 'Please check your input genome size !', QtGui.QMessageBox.Ok)



    def confirm(self):
        if QtGui.QMessageBox.Ok not in [self.confirm_tool_path(),self.confirm_scripts_path(),self.confirm_gs(),self.confirm_output_path()]:
            self.parameters = dict()
            self.parameters['tools_path'] = self.tools_path
            self.parameters['script_path'] = self.scripts_path
            self.parameters['threads'] = self.ui.threads_spinBox.value()
            self.parameters['jobs'] = self.ui.jobs_spinBox.value()
            self.parameters['iteration'] = self.ui.iteration_spinBox.value()
            self.parameters['gs'] = self.gs
            self.parameters['output_path'] = self.output_path
            self.close()

    def cancel(self):
        self.close()

class about(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_About()
        self.ui.setupUi(self)
        self.ui.about_bn.clicked.connect(self.confirm)
    def confirm(self):
        self.close()

class manual(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_Manual()
        self.ui.setupUi(self)
        self.ui.manual_bn.clicked.connect(self.confirm)
    def confirm(self):
        self.close()

class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.xzoom = True
        self.yzoom = True
        self.cidBP = None
        self.cidBR = None
        self.cidBM = None
        self.cidKeyP = None
        self.cidKeyR = None
        self.cidScroll = None

    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location
            if(xdata is None):
                return()
            if(ydata is None):
                return()

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print(event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            if(self.xzoom):
                ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            if(self.yzoom):
                ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()
            ax.figure.canvas.flush_events()

        def onKeyPress(event):
            if event.key == 'x':
                self.xzoom = True
                self.yzoom = False
            if event.key == 'y':
                self.xzoom = False
                self.yzoom = True

        def onKeyRelease(event):
            self.xzoom = True
            self.yzoom = True

        fig = ax.get_figure() # get the figure of interest

        self.cidScroll = fig.canvas.mpl_connect('scroll_event', zoom)
        self.cidKeyP = fig.canvas.mpl_connect('key_press_event',onKeyPress)
        self.cidKeyR = fig.canvas.mpl_connect('key_release_event',onKeyRelease)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press


        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()
            ax.figure.canvas.flush_events()

        fig = ax.get_figure() # get the figure of interest

        self.cidBP = fig.canvas.mpl_connect('button_press_event',onPress)
        self.cidBR = fig.canvas.mpl_connect('button_release_event',onRelease)
        self.cidBM = fig.canvas.mpl_connect('motion_notify_event',onMotion)
        # attach the call back

        #return the function
        return onMotion

class DataCursor(object):
    text_template = 'siteID: %d\nLocation: %s'
    x, y = 0.0, 0.0
    xoffset, yoffset = -20, 20
    text_template = 'siteID: %d\nLocation: %s'


    def __init__(self, ax, pos):
        self.ax = ax
        self.pos= pos
        self.annotation = ax.annotate(self.text_template,
                xy=(self.x, self.y), xytext=(self.xoffset, self.yoffset),
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                )
        self.annotation.set_visible(False)

    def __call__(self, event):
        self.event = event
        self.x, self.y = event.mouseevent.xdata, event.mouseevent.ydata
        try:
            if self.x >= self.pos.keys()[0] and self.x<=self.pos.keys()[-1]:
                self.annotation.xy = self.x, self.y
                hz=self.x-int(round(self.x))
                sz=self.y-self.pos[int(round(self.x))][1]
                if int(round(self.x)) in self.pos.keys() and (hz)**2<0.02 and (sz)**2<0.02:
                        self.annotation.set_text(self.text_template % (int(round(self.x-0.4)), self.pos[int(round(self.x-0.4))][0]))
                        self.annotation.set_visible(True)
                        event.canvas.draw()
                else:
                    self.annotation.set_visible(False)
        except:
            pass

if __name__=="__main__":
    multiprocessing.freeze_support()
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
