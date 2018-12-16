if(exist("n")==0 || n<0) n = n0

filename = word(list, n);
set title filename;
plot filename pointtype 2 pointsize 0.5 lc rgb 'blue';

n = n + dn;
if ( n < n1 ) reread;
undefine n;