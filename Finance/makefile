OCB_FLAGS = -use-ocamlfind -tag thread
OCB = ocamlbuild
SRC = icapm icapm_allocation
ML_FILES = $(SRC:=.ml)
MLI_FILES = $(SRC:=.mli)

test.native: test.ml $(ML_FILES) $(MLI_FILES)
	@echo $(ML_FILES)
	$(OCB) $(OCB_FLAGS) $@

clean:
	$(OCB) -clean

.PHONY: clean
