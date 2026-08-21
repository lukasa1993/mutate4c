import argparse,json
from pathlib import Path
from dataclasses import asdict
from .core import *
EXTS=('.c', '.h'); VERSION="0.1.0"
def main():
 p=argparse.ArgumentParser(prog="mutate4c");p.add_argument("filters",nargs="*");p.add_argument("--root",default=".");p.add_argument("--test-command",required=True);p.add_argument("--max-mutants",type=int);p.add_argument("--timeout",type=int,default=120);p.add_argument("--json",action="store_true");p.add_argument("--version",action="version",version="%(prog)s "+VERSION);a=p.parse_args();r=Path(a.root).resolve();fs=discover(r,EXTS)
 if a.filters: fs=[f for f in fs if any(x in f.relative_to(r).as_posix() for x in a.filters)]
 rs=run(r,fs,a.test_command,a.max_mutants,a.timeout)
 if a.json: print(json.dumps([asdict(m) for m in rs],indent=2))
 else: [print(f"{m.file}:{m.line} {m.original}->{m.replacement} {m.status}") for m in rs]
 return 2 if any(m.status=="survived" for m in rs) else 0
