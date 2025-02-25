
all: CONTROLLERS.pdf wiring_inner_city_1.pdf wiring_inner_city_2.pdf wiring_iller.pdf

%.pdf: %.md
	pandoc -o $@ $<

%.pdf: %.tex
	pdflatex $<
