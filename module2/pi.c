#include <stdio.h>
#include <stdlib.h>

int calc_pi(int N, double * out){
    int i;
    double sgn = 1;
    *out = 0;
    for(i=0; i<N; i++){
        *out += sgn/(2*i+1);
        sgn = -sgn;
        }
    }
