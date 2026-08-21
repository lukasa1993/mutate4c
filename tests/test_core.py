from mutate4c.core import sites
def test_sites():
 s=sites("int f(){ return 1 == 2 && true; }","a.c");ops=[(x[0].original,x[0].replacement) for x in s];assert ("==","!=") in ops and ("&&","||") in ops and ("true","false") in ops
def test_comment_skip(): assert all(x[0].line!=1 for x in sites("// a == b\nint f(){return 1 != 2;}","a.c"))
