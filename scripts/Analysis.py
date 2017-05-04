#!/usr/bin/env python

################################################
# Script: BioNano.py
# Author: Andy Yuan
# Email:  yuxuan.yuan@research.uwa.edu.au
# Last modified date: 05/07/2016
################################################

import pandas as pd
import numpy as np
from Bio import SeqIO
from Bio.Seq import Seq
import os
import sys
import re
import multiprocessing
from multiprocessing import Process, Queue
from time import sleep
import matplotlib.pyplot as plt

class BioNano(object):
    """
    The main aim of this script is to deal with BioNano analysis results.
    The functions in this script can deal with different problems. When calling them, please
    read the illustration first.
    """

    def __init__(self, xmap_file, r_cmap_file, q_cmap_file, confidence_score, reference):
        self.xmap = xmap_file
        self.rcmap = r_cmap_file
        self.qcmap = q_cmap_file
        self.confidence_score = confidence_score
        self.ref = reference
        self.name=xmap_file.rsplit('.',1)[0].split('/')[-1]
        self.XmapTable = None
        self.filtered_XmapTable = None
        self.RcmapTable = None
        self.QcmapTable = None
        self.ref_id = None
        self.ref_inf = None
        self.cmap = None
        self.unqualified = None
        self.qualified = None
        self.mapped = None
        self.unmapped = None
        self.BN = None
        self.detail = None
        self.no_data = None
        self.kicked = None

    def convert_tables(self):
        """
        Based on the confidence score, convert xmap file and two corresponding cmap files
        into "pandas table".
        """
        pd.set_option('display.width',200)
        with open ('%s.table' % self.name, 'a') as xmap_table:
            with open (self.xmap) as xmap:
                for line in xmap:
                    if line.startswith('#h'):
                        hearder = line[3:]
                        xmap_table.write(hearder)
                    if line[0]!='#':
                        xmap_table.write(line)
        with open ('%s.rtable' % self.name, 'a') as rcmap_table:
            with open (self.rcmap) as rcmap:
                for line in rcmap:
                    if line.startswith('#h'):
                        hearder = line[3:]
                        rcmap_table.write(hearder)
                    if line[0]!='#':
                        rcmap_table.write(line)
        with open ('%s.qtable' % self.name, 'a') as qcmap_table:
            with open (self.qcmap) as qcmap:
                for line in qcmap:
                    if line.startswith('#h'):
                        hearder = line[3:]
                        qcmap_table.write(hearder)
                    if line[0]!='#':
                        qcmap_table.write(line)
        self.XmapTable = pd.read_table('%s.table' % self.name)
        headers_x = ['RefContigID','RefStartPos','RefEndPos','QryContigID','QryStartPos',
        'QryEndPos','Orientation', 'Confidence','QryLen','RefLen', 'Alignment']
        self.filtered_XmapTable = self.XmapTable[self.XmapTable['Confidence']>=self.confidence_score][headers_x].reset_index(drop=True)
        headers_r = ['CMapId','ContigLength','NumSites','SiteID','Position']
        self.RcmapTable = pd.read_table('%s.rtable' % self.name)[headers_r]
        headers_q = ['CMapId','ContigLength','NumSites','SiteID','Position','Coverage']
        self.QcmapTable = pd.read_table('%s.qtable' % self.name)[headers_q]
        os.remove('%s.table' % self.name)
        os.remove('%s.rtable' % self.name)
        os.remove('%s.qtable' % self.name)

    def mapped_ctgs(self):
        """m
        Without specfic confidence score, get the mapped anchors.
        """
        return self.XmapTable['RefContigID'].unique()

    def Anchors(self):
        """
        Based on the confidence score, get the mapped anchors.
        """
        return self.filtered_XmapTable['RefContigID'].unique()

    def parse_fasta(self):
        self.ref_id=dict()
        self.ref_inf=dict()
        i=1
        N = 0
        ref_inf=np.empty(shape=[0,3])
        for seqs in SeqIO.parse(self.ref,'fasta'):
            seq_id = seqs.id
            self.ref_id[i] = seq_id
            seq = str(seqs.seq.upper())
            seq_len = len(seq)
            self.ref_inf[seq_id]=seq_len
            N+=seq.count('N')
            ref_inf = np.append(ref_inf,[[i,seq_id,seq_len]],axis=0)
            i+=1
        self.ref_detail = pd.DataFrame(ref_inf,columns=['Index','Contig','Length(bp)'])
        self.N = N


    def qualification_filter(self):
        """
        Providing information of those unqualified and qualified contigs from the orginal fasta file
        with the criterion: >20Kb & >=5 restriction sites inside.
        """
        unqualified = np.empty(shape=[0,3])
        qualified = np.empty(shape=[0,4])
        rm_dup = self.RcmapTable[['CMapId','ContigLength','NumSites']].drop_duplicates()
        for i in self.ref_id.keys():
            index = i
            name = self.ref_id[i]
            length = self.ref_inf[name]
            if i not in self.RcmapTable['CMapId'].unique():
                unqualified = np.append(unqualified,[[index,name, length]],axis=0)
            else:
                Id = rm_dup[rm_dup['CMapId']==i].index[0]
                sites = rm_dup['NumSites'][Id]
                qualified = np.append(qualified,[[index,name,length,sites]],axis=0)
        self.unqualified = pd.DataFrame(unqualified, columns=['index','contig','length(bp)'])
        self.qualified = pd.DataFrame(qualified, columns=['index','contig','length(bp)','numSites'])

    def BioNano_stats(self):
        """
        This script aims to give a whole statitics of the mapped BioNano data.
        """
        self.BN = self.QcmapTable[['CMapId','ContigLength','NumSites']].drop_duplicates().reset_index(drop=True)

    def mapping_filter(self):
        """
        Providing information of those mapped and unmapped contigs
        """
        unmapped = np.empty(shape=[0,4])
        mapped = np.empty(shape=[0,4])
        kicked = np.empty(shape=[0,4])
        no_data = np.empty(shape=[0,4])
        indexs = self.qualified.index
        for i in indexs:
            index = int(self.qualified['index'][i])
            name = self.qualified['contig'][i]
            length = self.qualified['length(bp)'][i]
            sites = self.qualified['numSites'][i]
            if index in self.Anchors():
                mapped = np.append(mapped,[[index,name,length,sites]],axis=0)
            else:
                unmapped = np.append(unmapped,[[index,name,length,sites]],axis=0)
                if (index in self.mapped_ctgs()) and (index not in self.Anchors()):
                    kicked = np.append(kicked,[[index,name,length,sites]],axis=0)
                if index not in self.mapped_ctgs():
                    no_data = np.append(no_data,[[index,name,length,sites]],axis=0)

        self.unmapped = pd.DataFrame(unmapped,columns=['index','contig','length(bp)','numSites'])
        self.mapped = pd.DataFrame(mapped,columns=['index','contig','length(bp)','numSites'])
        self.kicked = pd.DataFrame(kicked,columns=['index','contig','length(bp)','numSites'])
        self.no_data = pd.DataFrame(no_data,columns=['index','contig','length(bp)','numSites'])




    def getDetail(self):
        """
        Make the filtered_XmapTable in more detail.
        """
        q = Queue()
        procs = []
        tasks = multiprocessing.cpu_count()-1
        lines = len(self.filtered_XmapTable)
        pairwise=np.empty(shape=[0,18])
        if lines%tasks!=0:
            vol = lines//(tasks-1)
        else:
            vol = lines//tasks
        start= 0
        end = 0
        ntasks = range(tasks)
        chuncks = []
        for i in ntasks:
            if i == ntasks[-1]:
                chunck=range(vol*ntasks[-1],lines)
                chuncks.append(chunck)
            else:
                end = end+vol
                chunck=range(start,end)
                chuncks.append(chunck)
                start = end
        for i in ntasks:
            t = Process(target=self.alignedInf,args=(chuncks[i],i/1.0e3,q))
            procs.append(t)
            t.start()

        for i in ntasks:
            pairwise = np.concatenate((pairwise, q.get()),axis=0)

        for i in procs:
            i.join()

        names=['RefContigID','Contig','RefStartPos','RefEndPos','QryContigID','QryStartPos','QryEndPos',
               'Orientation','Confidence','RefSiteId','RefNumSites','QrySiteId','QryNumSites','RefSitePos',
               'QrySitePos','Coverage','RefLen','QryLen']
        pairwise=pd.DataFrame(pairwise,columns=names)
        tsf = ['RefContigID','RefStartPos','RefEndPos','QryContigID','QryStartPos','QryEndPos',
               'Confidence','RefSiteId','RefNumSites','QrySiteId','QryNumSites','RefSitePos',
               'QrySitePos','Coverage','RefLen','QryLen']
        pairwise[tsf]=pairwise[tsf].apply(pd.to_numeric)
        self.detail = pairwise.sort_values(['RefContigID','RefStartPos','RefSiteId'],
        ascending=[True, True, True]).reset_index(drop=True)

    def getPaired(self):
        """
        Make the filtered_XmapTable in more detail.
        """
        q = Queue()
        procs = []
        tasks = multiprocessing.cpu_count()-1
        nAnchor = len(self.Anchors())
        pairwise=np.empty(shape=[0,23])
        if nAnchor%tasks!=0:
            vol = nAnchor//(tasks-1)
        else:
            vol = nAnchor//tasks
        start= 0
        end = 0
        ntasks = range(tasks)
        chuncks = []
        for i in ntasks:
            if i == ntasks[-1]:
                chunck=[m for m in self.Anchors()[vol*ntasks[-1]:nAnchor]]
                chuncks.append(chunck)
            else:
                end = end+vol
                chunck=[j for j in self.Anchors()[start:end]]
                chuncks.append(chunck)
                start = end
        for i in ntasks:
            t = Process(target=self.pairwise,args=(chuncks[i],i/1.0e3,q))
            procs.append(t)
            t.start()

        for i in ntasks:
            pairwise = np.concatenate((pairwise, q.get()),axis=0)

        for i in procs:
            i.join()

        names=['RefContigID','Contig','RefLen','RefNumSites','QryContigID','QryLen','QryNumSites',
        'RefSiteId_1','RefSiteId_2','RefSiteDis','Ref_site1_pos','Ref_site2_pos','Ref_pos_dis',
        'QrySiteId_1','QrySiteId_2','QrySiteDis','Qry_site1_pos','Qry_site2_pos','Qry_pos_dis',
        'Qry_site1_cov','Qry_site2_cov','Orientation','Dis_diff']
        pairwise=pd.DataFrame(pairwise,columns=names)
        tsf = ['RefContigID','RefLen','RefNumSites','QryContigID','QryLen','QryNumSites',
        'RefSiteId_1','RefSiteId_2','RefSiteDis','Ref_site1_pos','Ref_site2_pos','Ref_pos_dis',
        'QrySiteId_1','QrySiteId_2','QrySiteDis','Qry_site1_pos','Qry_site2_pos','Qry_pos_dis',
        'Qry_site1_cov','Qry_site2_cov', 'Dis_diff']
        pairwise[tsf]=pairwise[tsf].apply(pd.to_numeric)
        self.paired = pairwise.sort_values(['RefContigID','RefSiteId_1','Ref_site1_pos'],
        ascending=[True, True, True]).reset_index(drop=True)

    def getMissing(self):
        no_data = np.empty(shape=[0,5])
        for i in self.Anchors():
            sub_rcmap = self.RcmapTable[self.RcmapTable['CMapId']==i]
            numSites=sub_rcmap['NumSites'].unique()[0]
            for j in range(1, numSites+1):
                sub_detail = self.detail[self.detail['RefContigID']==i].reset_index(drop=True)
                matched_site = [m for m in sub_detail['RefSiteId']]
                if j not in matched_site:
                    ctg = self.ref_id[i]
                    index = sub_rcmap[sub_rcmap['SiteID']==j].index[0]
                    position = sub_rcmap['Position'][index]
                    no_data = np.append(no_data,[[i,ctg,j,position,numSites]],axis=0)
        self.missing = pd.DataFrame(no_data, columns=['index','contig','siteID','position','numSites'])

    def pairwise(self,chunck,nsec,out_q):
        sleep(nsec)
        pairwise = np.empty(shape=[0,23])
        for i in chunck:
            sub_detail = self.detail[self.detail['RefContigID']==i].reset_index(drop=True)
            Qrys = sub_detail['QryContigID'].unique()
            for n in Qrys:
                sub = sub_detail[sub_detail['QryContigID']==n].reset_index(drop=True)
                p_1, p_2 = 1,2
                ctg = sub['Contig'][p_1-1]
                ctg_len = sub['RefLen'][p_1-1]
                numSites = sub['RefNumSites'][p_1-1]
                ori = sub['Orientation'][p_1-1]
                qry_ctg = sub['QryContigID'][p_1-1]
                qry_len = sub['QryLen'][p_1-1]
                qry_numSite = sub['QryNumSites'][p_1-1]
                while p_2<=len(sub):
                    ref_rs_1 = sub['RefSiteId'][p_1-1]
                    ref_rs_2 = sub['RefSiteId'][p_2-1]
                    ref_rs_dis = abs(ref_rs_2 -ref_rs_1)
                    ref_pos_1 = sub['RefSitePos'][p_1-1]
                    ref_pos_2 = sub['RefSitePos'][p_2-1]
                    ref_pos_dis = abs(ref_pos_2 -ref_pos_1)
                    qry_cov_1 = sub['Coverage'][p_1-1]
                    qry_cov_2 = sub['Coverage'][p_2-1]
                    qry_rs_1 = sub['QrySiteId'][p_1-1]
                    qry_rs_2 = sub['QrySiteId'][p_2-1]
                    qry_rs_dis = abs(qry_rs_2 - qry_rs_1)
                    qry_pos_1 = sub['QrySitePos'][p_1-1]
                    qry_pos_2 = sub['QrySitePos'][p_2-1]
                    qry_pos_dis = abs(qry_pos_2 -qry_pos_1)
                    dis_dif = float("%.1f"%(ref_pos_dis - qry_pos_dis))
                    pairwise = np.append(pairwise,[[i,ctg,ctg_len,numSites,qry_ctg,qry_len,qry_numSite,ref_rs_1,
                    ref_rs_2,ref_rs_dis,ref_pos_1,ref_pos_2,ref_pos_dis, qry_rs_1,qry_rs_2,qry_rs_dis,
                    qry_pos_1,qry_pos_2,qry_pos_dis,qry_cov_1,qry_cov_2,ori,dis_dif]],axis=0)
                    p_1+=1
                    p_2+=1

        out_q.put(pairwise)

    def alignedInf(self,chunck,nsec,out_q):
        """
        Clearly show the alignment information between assembly and BioNano maps.
        """
        sleep(nsec)
        pairwise=np.empty(shape=[0,18])

        for i in chunck:
            RefCtgId=self.filtered_XmapTable['RefContigID'][i]
            name = self.ref_id[RefCtgId]
            RefStartPos=self.filtered_XmapTable['RefStartPos'][i]
            RefEndPos=self.filtered_XmapTable['RefEndPos'][i]
            QryCtgId=self.filtered_XmapTable['QryContigID'][i]
            QryStartPos=self.filtered_XmapTable['QryStartPos'][i]
            QryEndPos=self.filtered_XmapTable['QryEndPos'][i]
            Orientation=self.filtered_XmapTable['Orientation'][i]
            Confidence=self.filtered_XmapTable['Confidence'][i]
            QryLen=self.filtered_XmapTable['QryLen'][i]
            RefLen=self.filtered_XmapTable['RefLen'][i]
            alignments=self.filtered_XmapTable['Alignment'][i]
            Alignments=[pair for pair in re.split('[()]',alignments) if len(pair)>0]
            for pair in Alignments:
                pair=pair.split(',')
                r_site=int(pair[0])
                q_site=int(pair[1])
                r_site_pos = self.RcmapTable[(self.RcmapTable['CMapId']==RefCtgId) &
                                           (self.RcmapTable['SiteID']==r_site)]['Position'].values[0]
                r_nsites = self.RcmapTable[(self.RcmapTable['CMapId']==RefCtgId) &
                                           (self.RcmapTable['SiteID']==r_site)]['NumSites'].values[0]
                q_site_pos = self.QcmapTable[(self.QcmapTable['CMapId']==QryCtgId) &
                                           (self.QcmapTable['SiteID']==q_site)]['Position'].values[0]
                q_nsites = self.QcmapTable[(self.QcmapTable['CMapId']==QryCtgId) &
                                           (self.QcmapTable['SiteID']==q_site)]['NumSites'].values[0]
                cov=self.QcmapTable[(self.QcmapTable['CMapId']==QryCtgId) &
                                    (self.QcmapTable['SiteID']==q_site)]['Coverage'].values[0]
                pairwise=np.append(pairwise,[[RefCtgId,name,RefStartPos,RefEndPos,QryCtgId,
                                              QryStartPos,QryEndPos,Orientation,Confidence,
                                              r_site,r_nsites,q_site,q_nsites,r_site_pos,q_site_pos,cov,
                                              RefLen,QryLen]],axis=0)
        out_q.put(pairwise)

    def checkStatus(self):
        Q_dis=np.empty(shape=[0,10])
        Q_rs=np.empty(shape=[0,12])
        pos_diff = []
        pos_coor={}
        a=0
        for ctg in self.Anchors():
            sub_paired = self.paired[self.paired['RefContigID']==ctg].reset_index(drop=True)
            qrys = sub_paired['QryContigID'].unique()
            for i in qrys:
                sub = sub_paired[sub_paired['QryContigID']==i].reset_index(drop=True)
                for j in range(len(sub)):
                    index=sub['RefContigID'][j]
                    name = sub['Contig'][j]
                    ref_site1 = sub['RefSiteId_1'][j]
                    ref_site2 = sub['RefSiteId_2'][j]
                    ref_pos1 = sub['Ref_site1_pos'][j]
                    ref_pos2 = sub['Ref_site2_pos'][j]
                    ref_site_dis = sub['RefSiteDis'][j]
                    ref_pos_dis = sub['Ref_pos_dis'][j]
                    qry_site1 = sub['QrySiteId_1'][j]
                    qry_site2 = sub['QrySiteId_2'][j]
                    qry_site_dis = sub['QrySiteDis'][j]
                    qry_pos_dis = sub['Qry_pos_dis'][j]
                    cov_1 = sub['Qry_site1_cov'][j]
                    cov_2 = sub['Qry_site2_cov'][j]
                    ori = sub['Orientation'][j]
                    dis_dif = float(ref_pos_dis - qry_pos_dis)
                    pos_diff.append(dis_dif)
                    pos_coor[a]=[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2]
                    a+=1
                    if ref_site_dis==0:
                        if qry_site_dis==1:
                            Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,'Collapsed','None']],axis=0)
                        if qry_site1+1<qry_site2:
                            qry_missed_sites=str(range(qry_site1+1,qry_site2))
                            Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,'Collapsed',qry_missed_sites]],axis=0)
                        if qry_site1-1>qry_site2:
                            qry_missed_sites=str(range(qry_site1-1,qry_site2,-1))
                            Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,'Collapsed',qry_missed_sites]],axis=0)
                    if ref_site_dis==1:
                        if ori=='+':
                            #if qry_site_dis==0:
                            #    Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,'None','Collapsed']],axis=0)
                            if qry_site1+1<qry_site2:
                                qry_missed_sites=str(range(qry_site1+1,qry_site2))
                                Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,'None',qry_missed_sites]],axis=0)
                            if qry_site1> qry_site2:
                                Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,'None','chimeric region']],axis=0)
                        if ori=='-':
                            #if qry_site_dis==0:
                            #   Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,'None','Collapsed']],axis=0)
                            if qry_site1-1>qry_site2:
                                qry_missed_sites=str(range(qry_site1-1,qry_site2,-1))
                                Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,'None',qry_missed_sites]],axis=0)
                            if qry_site1 < qry_site2:
                                Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,'None','chimeric region']],axis=0)
                    if ref_site_dis>1:
                        if ori=='+':
                            #if qry_site_dis==0:
                            #   ref_missed_sites=str(range(ref_site1+1,ref_site2))
                            #    Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,ref_missed_sites,'Collapsed']],axis=0)
                            if qry_site_dis==1:
                                ref_missed_sites=str(range(ref_site1+1,ref_site2))
                                Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,ref_missed_sites,'None']],axis=0)
                            if qry_site1+1<qry_site2:
                                ref_missed_sites=str(range(ref_site1+1,ref_site2))
                                qry_missed_sites=str(range(qry_site1+1,qry_site2))
                                Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,ref_missed_sites,qry_missed_sites]],axis=0)
                            if qry_site1>qry_site2:
                                ref_missed_sites=str(range(ref_site1+1,ref_site2))
                                Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,ref_missed_sites,'chimeric region']],axis=0)
                        if ori=='-':
                            #if qry_site_dis==0:
                            #    ref_missed_sites=str(range(ref_site1+1,ref_site2))
                            #    Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,ref_missed_sites,'Collapsed']],axis=0)
                            if qry_site_dis==1:
                                ref_missed_sites=str(range(ref_site1+1,ref_site2))
                                Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,ref_missed_sites,'None']],axis=0)
                            if qry_site1-1>qry_site2:
                               ref_missed_sites=str(range(ref_site1+1,ref_site2))
                               qry_missed_sites=str(range(qry_site1-1,qry_site2,-1))
                               Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,ref_missed_sites,qry_missed_sites]],axis=0)
                            if qry_site1<qry_site2:
                                ref_missed_sites=str(range(ref_site1+1,ref_site2))
                                Q_rs = np.append(Q_rs,[[index,name,ref_site1,ref_pos1,ref_site2,ref_pos2,qry_site1,qry_site2,cov_1,cov_2,ref_missed_sites,'chimeric region']],axis=0)

        dis = np.array(pos_diff)
        Q3 = np.percentile(dis,75)
        Q1 = np.percentile(dis,25)
        IQR = Q3-Q1
        lower = Q1-1.5*IQR
        upper = Q3+1.5*IQR
        #print 'Distance difference lower boundary is: %s' % lower
        #print 'Distance difference upper boundary is: %s' % upper
        b=0
        for m in pos_diff:
            if m>upper or m<lower:
                Q_dis = np.append(Q_dis,[pos_coor[b]],axis=0)
            b+=1
        self.Q_dis=pd.DataFrame(Q_dis,columns=['Index','Contig','RefSiteId_1','Ref_pos_1','RefSiteId_2','Ref_pos_2','QrySiteId_1','QrySiteId_2','Qry_cov1','Qry_cov2'])
        self.Q_rs=pd.DataFrame(Q_rs,columns=['Index','Contig','RefSiteId_1','Ref_pos_1','RefSiteId_2','Ref_pos_2','QrySiteId_1','QrySiteId_2','Qry_cov1','Qry_cov2','Ref_missed_sites','Qry_missed_sites'])

    def merge(self):
        good = np.empty(shape=[0,5])
        q_rs_a= np.empty(shape=[0,5])
        q_dis_a= np.empty(shape=[0,5])
        both = np.empty(shape=[0,5])
        overall = np.empty(shape=[0,8])
        for i in self.Anchors():
            name = self.ref_id[i]
            sub_detail=self.detail[self.detail['RefContigID']==i].reset_index(drop=True)
            mapping=[int(l) for l in sub_detail['RefSiteId']]
            sub_rcmap = self.RcmapTable[self.RcmapTable['CMapId']==i].reset_index(drop=True)
            i=str(i)
            numSites=sub_rcmap['NumSites'].unique()[0]
            sub_missing = self.missing[self.missing['index']==i].reset_index(drop=True)
            mis_sites=[int(a) for a in sub_missing['siteID']]
            sub_q_rs = self.Q_rs[self.Q_rs['Index']==i].reset_index(drop=True)
            sub_q_dis = self.Q_dis[self.Q_dis['Index']==i].reset_index(drop=True)
            q_rs=[]
            q_dis=[]
            for b in range(len(sub_q_rs)):
                rs1 = int(sub_q_rs['RefSiteId_1'][b])
                rs2 = int(sub_q_rs['RefSiteId_2'][b])
                if rs1<=rs2:
                    q_rs+=range(rs1,rs2+1)
                else:
                    q_rs+=range(rs1,rs2-1,-1)
            for c in range(len(sub_q_dis)):
                ds1 = int(sub_q_dis['RefSiteId_1'][c])
                ds2 = int(sub_q_dis['RefSiteId_2'][c])
                if ds1<=ds2:
                    q_dis+=range(ds1,ds2+1)
                else:
                    q_dis+=range(ds1,ds2-1,-1)
            Q_a= set(q_dis+q_rs+mis_sites)
            overlaps=set(q_rs).intersection(q_dis)
            Q_r = [r for r in q_rs if r not in q_dis]
            Q_d = [d for d in q_dis if d not in q_rs]
            
            Overlaps=list(overlaps)
            if len(Overlaps)>0:
                for e in Overlaps:
                    for check in range(len(sub_q_rs)):
                        c1=int(sub_q_rs['RefSiteId_1'][check])
                        c2=int(sub_q_rs['RefSiteId_2'][check])
                        if c1==e and c2 not in Overlaps:
                            Q_r.append(e)
                            overlaps.discard(e)
                        if c2 ==e and c1 not in Overlaps:
                            Q_r.append(e) 
                            overlaps.discard(e)
            Q_r=sorted(set(Q_r))

            if len(Overlaps)>0:
                for e in Overlaps:
                    for check in range(len(sub_q_dis)):
                        c1=int(sub_q_dis['RefSiteId_1'][check])
                        c2=int(sub_q_dis['RefSiteId_2'][check])
                        if c1 ==e and c2 not in Overlaps:
                            Q_d.append(e)
                            overlaps.discard(e)
                        if c2 ==e and c1 not in Overlaps:
                            Q_d.append(e)
                            overlaps.discard(e)
            Q_d=sorted(set(Q_d))

            for j in range(1, numSites+1):
                if j in mapping:
                    index=sub_detail[sub_detail['RefSiteId']==j].index[0]
                    cov=sub_detail['Coverage'][index]
                else:
                    cov=None
                if j not in Q_a :
                    pos = sub_rcmap['Position'][j-1]
                    numSites = sub_rcmap['NumSites'][j-1]
                    good = np.append(good,[[i,name,j,pos,numSites]],axis=0)
                    overall = np.append(overall,[[i,name,j,pos,numSites,cov,'Consistent',4]],axis=0)
                if j in Q_d :
                    pos = sub_rcmap['Position'][j-1]
                    numSites = sub_rcmap['NumSites'][j-1]
                    q_dis_a =np.append(q_dis_a,[[i,name,j,pos,numSites]],axis=0)
                    overall = np.append(overall,[[i,name,j,pos,numSites,cov,'Distance_discordant',2]],axis=0)
                if j in Q_r:
                    pos = sub_rcmap['Position'][j-1]
                    numSites = sub_rcmap['NumSites'][j-1]
                    q_rs_a =np.append(q_rs_a,[[i,name,j,pos,numSites]],axis=0)
                    overall = np.append(overall,[[i,name,j,pos,numSites,cov,'Number_discordant',3]],axis=0)
                if j in overlaps:
                    pos = sub_rcmap['Position'][j-1]
                    numSites = sub_rcmap['NumSites'][j-1]
                    both =np.append(both,[[i,name,j,pos,numSites]],axis=0)
                    overall = np.append(overall,[[i,name,j,pos,numSites,cov,'Num+dis_discordant',1]],axis=0)
                if j in mis_sites and j not in q_dis and j not in q_rs and j not in overlaps:
                    pos = sub_rcmap['Position'][j-1]
                    numSites = sub_rcmap['NumSites'][j-1]
                    overall = np.append(overall,[[i,name,j,pos,numSites,cov,'missing',0]],axis=0)

        self.overall = pd.DataFrame(overall,columns=['index','contig','siteID','position','numSites','coverage','mapping_status','score'])
        self.good = pd.DataFrame(good,columns=['index','contig','siteID','position','numSites'])
        self.q_rs_a = pd.DataFrame(q_rs_a,columns=['index','contig','siteID','position','numSites'])
        self.q_dis_a = pd.DataFrame(q_dis_a,columns=['index','contig','siteID','position','numSites'])
        self.both = pd.DataFrame(both,columns=['index','contig','siteID','position','numSites'])

def make_RefCmap(fasta_file, enz=None, min_len=20, min_nsite=5, path=None):
    name = fasta_file.rsplit('.',1)[0].split('/')[-1]
    index = 0
    enzymes = {'BspQI':'GCTCTTC',
                'BbvCI':'CCTCAGC',
                'Bsml':'GAATGC',
                'BsrDI':'GCAATG',
                'bseCI':'ATCGAT',
                'BssSI':'CACGAG'}
    try:
        cmap_file='%s/%s_%s.cmap'%(path,name,enz)
        forwards = enzymes[enz]
        reverse = str(Seq(forwards).reverse_complement())
        with open (cmap_file,'a') as ref_cmap:
            ref_cmap.write('# CMAP File Version:\t0.1\n')
            ref_cmap.write('# Label Channels:\t1\n')
            ref_cmap.write('# Nickase Recognition Site 1:\t%s\n'%forwards)
            ref_cmap.write('# Enzyme1:\tNt.%s\n'%enz)
            ref_cmap.write('# Number of Consensus Nanomaps:\tN/A\n')
            ref_cmap.write('#h CMapId\tContigLength\tNumSites\tSiteID\tLabelChannel\tPosition\tStdDev\tCoverage\tOccurrence\n')
            ref_cmap.write('#f int\tfloat\tint\tint\tint\tfloat\tfloat\tint\tint\n')
            for seqs in SeqIO.parse(fasta_file,'fasta'):
       	        seq = str(seqs.seq.upper())
       	        seq_len = len(seq)
       	        index+=1
       	        if seq_len >= min_len*1000:
                    nsites = len(re.findall('%s|%s'%(forwards,reverse),seq))
                    if nsites >=min_nsite:
                        j=1
                        for o in re.finditer('%s|%s'%(forwards,reverse),seq):
                            ref_cmap.write('%s\t%.1f\t%d\t%d\t1\t%.1f\t1.0\t1\t1\n'%(index,seq_len,nsites,j,o.start()+1))
                            j+=1
                        ref_cmap.write('%s\t%.1f\t%d\t%d\t0\t%.1f\t0.0\t1\t0\n'%(index,seq_len,nsites,j,seq_len))
    except:
        pass
