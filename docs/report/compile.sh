#!/bin/sh

pdflatex main.tex;
bibtex main;
pdflatex main.tex;
pdflatex main.tex;
rm main-blx.bib
rm *.aux
rm *.bbl
rm *.blg
rm *.log
rm *.run.xml
rm *.toc
