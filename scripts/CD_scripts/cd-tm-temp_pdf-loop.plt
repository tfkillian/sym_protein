if(exist("n")==0 || n<0) n = n0;

filename = word(list, n);
set title filename;
plot f(x) lc rgb 'grey' lw 1 ,\
filename with line lc rgb 'black' lw 3;

n = n + dn;
if ( n < n1 ) reread;
undefine n;