# BioNanoAnalyst
BioNanoAnalyst is a tool providing  GUI to assess the genome assembly quality using BioNano data.

# Introduction

Before using this tool, please make sure your platform satisfies the requirements below:

1. There are at least 2 CPUs in your machine
  
2. For Linux or macOS operating system, a Python (version:2.7.xx) and corresponding packages are required (see details below)

#Python Installation

1. Please download python from https://www.python.org/downloads/

2. Unpack the downloaded file, for exmaple using 
  
  $ tar -zxvf Python-2.7.xx.tar.gz in your terminal

3. Then enter into the created directory:
  
  $ cd Python-2.7

4. Start the build process by configuring everthing to your system:
  
  $ ./configure (you can specify a particular loaction using --prefix after ./configure)

5. Build all of the files with: 

  $ make

6. Install everything: 
  
  $ make install 

If there were no errors and eveything worked correctly, you should be able to type python at a command prompt and enter into the python interpreter:

  $ python 
  
  Python 2.7.x (...)
  
  ...
  
  Type "help", "copyright", "credits" or "license" for more information.
  >>>

#Install python packages

Using pip 

  Download get-pip.py from https://bootstrap.pypa.io/get-pip.py

  install pip: $ python get-pip.py
  
Or using the package source code as suggested 

#Required python packages:

numpy ($pip install numpy or http://www.numpy.org/)

pandas (pip install pandas or http://pandas.pydata.org/)

matplotlib ($ pip install matplotlib or http://matplotlib.org/)

Biopython ($pip install biopython or http://biopython.org/)

Image ($pip  install Image)

PyQt4 or PySide (https://www.riverbankcomputing.com/software/pyqt/download or $pip install PySide. If you have problem in installing this package, please refer [Issue #1](https://github.com/AppliedBioinformatics/BioNanoAnalyst/issues/1) 

# Run BioNanoAnalyst 

#For the Windows version:

  1. Please go to www.7-zip.org and download 7-zip

  2. Unzip the "Windows_version.7z" file downloaded from the "releases panel" 
  
  3. Find the App.exe and directly run it

#For the Linux or Mac version: 

  1. Please download the source code 

  2. After install python and all required python packages, please run the application using $ python App.py.
  


BioNanoAnalyst uses hashtables to store information, which is efficient in memeroy use. In the design of BioNanoAnalyst, most of the running time, it will use one CPU, while at some stage, it will use all CPUs -1.

In the test of E.coli (5Mb), clover (500Mb), canola (1000Mb) and human (3Gb) data, the peak memory consumptions were: ~100Mb, ~1G, ~1.5Gb and ~3.6 Gb respectively. The running time varies depending on the computational resource users have. On a local Windows 7 64-bit platform with an Intel i7-4790@3.60GHz processor (8 cores), the running time for the four datasets were: ~10s, ~2mins, ~20mins and ~4.64 hrs. Users can base on those to estimate their own running time and computational resource requirement.


A [tutorial](https://github.com/AppliedBioinformatics/BioNanoAnalyst/wiki/How-to-run-BioNanoAnalyst) is also given in the Wiki page to show how to run BioNanoAnalyst: 

#Note: 

When running BioNanAnalyst, the application may get stuck, please leave it alone until the job finished. 
