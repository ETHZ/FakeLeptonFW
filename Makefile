## makefile for the fake rate framework


ROOTCFLAGS = $(shell root-config --cflags)
ROOTLIBS   = $(shell root-config --libs)
ROOTGLIBS  = $(shell root-config --glibs)

LIBS       = $(ROOTLIBS)
INCLUDES   = -I. $(ROOTCFLAGS)

CXX        = g++ -g -fPIC -fno-var-tracking -Wno-deprecated -D_GNU_SOURCE -O2
CXXFLAGS   = $(ROOTCFLAGS) $(INCLUDES)


##SRCSA      = src/TreeClass.C src/Fakerates.cc
SRCSA      = src/FWBaseClass.C src/Fakerates.cc
OBJSA      = $(patsubst %.C,%.o,$(SRCSA:.cc=.o))

includes = $(wildcard include/*.h)

SRCSB      = src/TreeClass.C src/Estimation.cc
OBJSB      = $(patsubst %.C,%.o,$(SRCSB:.cc=.o))

SRCSC      = src/TreeClass.C src/Closure.cc
OBJSC      = $(patsubst %.C,%.o,$(SRCSC:.cc=.o))

.SUFFIXES: .cc,.C,.hh,.h
.PHONY : clean purge all depend


# Rules ====================================
all: Fakerates Estimation Closure

Fakerates: exe/Fakerates.C $(OBJSA)
	$(CXX) $(INCLUDES) $(LIBS) -ldl -o $@ $^

Estimation: exe/Estimation.C $(OBJSB)
	$(CXX) $(INCLUDES) $(LIBS) -ldl -o $@ $^

Closure: exe/Closure.C $(OBJSC)
	$(CXX) $(INCLUDES) $(LIBS) -ldl -o $@ $^

depend: .depend

## old .depend: $(SRCSA) $(SRCSB) $(SRCSC)
## old 	rm -f ./.depend
## old 	$(foreach SRC,$(SRCA),$(SRCB),$(SRCC),$(CXX) -I. -I$(shell root-config --incdir) -MG -MM -MT $(patsubst %.C,%.o,$(SRC:.cc=.o)) $(SRC) >> ./.depend;)
depend: 
	rm -f ./.depend
	$(foreach SRC,$(SRCSA) $(SRCSB) $(SRCSC),$(CXX) -I. -I$(shell root-config --incdir) -MG -MM -MT $(patsubst %.C,%.o,$(SRC:.cc=.o)) $(SRC) >> ./.depend;)


clean:
	find src -name '*.o' -exec $(RM) -v {} ';' 
	$(RM) .depend
	$(RM) Fakerates
	$(RM) Estimation
	$(RM) Closure

-include .depend
