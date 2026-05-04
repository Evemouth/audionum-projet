#!/bin/bash
pdflatex rapport.tex
pdflatex rapport.tex
rm rapport.aux
rm rapport.toc
rm rapport.log
rm rapport.out
evince rapport.pdf