## makefile for the fake rate framework


ROOTCFLAGS = $(shell root-config --cflags)
ROOTLIBS   = $(shell root-config --libs) -lRooFitCore -lRooFit
ROOTGLIBS  = $(shell root-config --glibs)
#ROOTINCDIR = $(shell root-config --incdir)

LIBS       = $(ROOTLIBS)
INCLUDES   = -I. $(ROOTCFLAGS)
# this is a roofit version somewhere: -I/swshare/cms/slc5_amd64_gcc462/lcg/roofit/5.32.03-cms16/include/

CXX        = g++ -g -fPIC -fno-var-tracking -Wno-deprecated -D_GNU_SOURCE -O2
CXXFLAGS   =  $(INCLUDES)


SRCSA      = src/FWBaseClass.C src/Fakerates.cc
OBJSA      = $(patsubst %.C,%.o,$(SRCSA:.cc=.o))

includes = $(wildcard include/*.h)

## SRCSB      = src/FWBaseClass.C src/Estimation.cc
## OBJSB      = $(patsubst %.C,%.o,$(SRCSB:.cc=.o))
## 
SRCSC      = src/FWBaseClass.C src/Fakerates.cc src/FakeRatios.cc src/Closure.cc
OBJSC      = $(patsubst %.C,%.o,$(SRCSC:.cc=.o))

SRCSD      = src/FWBaseClass.C src/dps.cc
OBJSD      = $(patsubst %.C,%.o,$(SRCSD:.cc=.o))

.SUFFIXES: .cc,.C,.hh,.h
.PHONY : clean purge all depend


# Rules ====================================
all: Fakerates dps Closure depend

Fakerates: exe/Fakerates.C $(OBJSA)
	$(CXX) $(INCLUDES) $(LIBS) -ldl -o $@ $^

## Estimation: exe/Estimation.C $(OBJSB)
## 	$(CXX) $(INCLUDES) $(LIBS) -ldl -o $@ $^
## 
Closure: exe/Closure.C $(OBJSC)
	$(CXX) $(INCLUDES) $(LIBS) -ldl -o $@ $^

dps: exe/dps.C $(OBJSD)
	$(CXX) $(INCLUDES) $(LIBS) -ldl -o $@ $^

## old .depend: $(SRCSA) $(SRCSB) $(SRCSC)
## old 	rm -f ./.depend
## old 	$(foreach SRC,$(SRCA),$(SRCB),$(SRCC),$(CXX) -I. -I$(shell root-config --incdir) -MG -MM -MT $(patsubst %.C,%.o,$(SRC:.cc=.o)) $(SRC) >> ./.depend;)
depend: 
	rm -f ./.depend
	$(foreach SRC,$(SRCSA) $(SRCSC) $(SRCSD),$(CXX) -I. -I$(shell root-config --incdir) -MG -MM -MT $(patsubst %.C,%.o,$(SRC:.cc=.o)) $(SRC) >> ./.depend;)

	### $(foreach SRC,$(SRCSA) $(SRCSB) $(SRCSC) $(SRCSD),$(CXX) -I. -I$(shell root-config --incdir) -MG -MM -MT $(patsubst %.C,%.o,$(SRC:.cc=.o)) $(SRC) >> ./.depend;)

clean:
	find src -name '*.o' -exec $(RM) -v {} ';' 
	$(RM) .depend
	$(RM) Fakerates
	$(RM) Closure
	$(RM) dps

## 	$(RM) Estimation
## 	$(RM) Closure

-include .depend
