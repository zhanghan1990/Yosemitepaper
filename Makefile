BIB = allstorage.bib Tian.bib ref_Tian3.bib Tian_rest.bib cache.bib Vaneet_cloud.bib ref_tian2.bib

icdcs.pdf: icdcs.tex $(BIB)
	pdflatex icdcs
	bibtex icdcs
	pdflatex icdcs
