# Sets the variables LDRC, LDFLAGS
include MakeMacros
include MakeImplicit
include ObsList
# This is for linking the BasicStructs and Interpolation 
# shared objects. Sets variables 
# CTXLIBBS, CTXLIBINTERP
include MakeCTX

EXE = epic

# MKLLIBS are linked statically. Dynamic linking did not work.
# Guide: https://software.intel.com/en-us/articles/intel-mkl-link-line-advisor/
# Also, see doc/Suggested static link line from Intel Math Kernel Library Link Line Advisor.pdf
# -lifcore -lifcoremt -lstdc++ are added to make Fotran, C and C++ correctly compile together
MKLLIBS = ${MKLROOT}/lib/intel64/libmkl_scalapack_ilp64.a -Wl,--start-group ${MKLROOT}/lib/intel64/libmkl_intel_ilp64.a ${MKLROOT}/lib/intel64/libmkl_intel_thread.a ${MKLROOT}/lib/intel64/libmkl_core.a ${MKLROOT}/lib/intel64/libmkl_blacs_intelmpi_ilp64.a -Wl,--end-group -liomp5 -lpthread -lifcore -lifcoremt -lstdc++ -lm -ldl

LIBS = -lfftw3f $(CTXLIBBS) $(CTXLIBINTERP) $(MKLLIBS) -lm

# OBS contains all the .h files
$(EXE): $(OBS) *.h
	$(LDRC) -DMKL_ILP64 -I${MKLROOT}/include -qopenmp $(LDFLAGS) $(OBS) -o $@ $(LIBS)

copy_to_bin: $(EXE)
	cp $(EXE) bin/

clean:
	rm -f *.o *~ $(EXE)

