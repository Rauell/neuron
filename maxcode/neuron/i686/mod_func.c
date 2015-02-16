#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," IM.mod");
    fprintf(stderr," IT.mod");
    fprintf(stderr," SinClamp.mod");
    fprintf(stderr," cadecay.mod");
    fprintf(stderr," gap.mod");
    fprintf(stderr," gapc.mod");
    fprintf(stderr," gapc1.mod");
    fprintf(stderr," hh2.mod");
    fprintf(stderr," izap.mod");
    fprintf(stderr, "\n");
  }
  _IM_reg();
  _IT_reg();
  _SinClamp_reg();
  _cadecay_reg();
  _gap_reg();
  _gapc_reg();
  _gapc1_reg();
  _hh2_reg();
  _izap_reg();
}
