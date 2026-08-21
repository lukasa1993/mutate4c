from pathlib import Path
EXCLUDED={".git","build","dist","target","vendor",".venv","venv","node_modules"}
def discover(root, exts):
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts and not any(x in EXCLUDED for x in p.parts))

from dataclasses import dataclass,asdict
import re,subprocess
@dataclass
class Mutant:
    file:str; line:int; original:str; replacement:str; status:str="not-run"
OPS=[("==","!="),("!=","=="),(">=","<"),("<=",">"),("&&","||"),("||","&&"),("+","-"),("-","+"),("*","/"),("true","false"),("false","true")]
def sites(text,rel):
    out=[]
    for a,b in OPS:
        for m in re.finditer(re.escape(a),text):
            ls=text.rfind("\n",0,m.start())+1
            if "//" in text[ls:m.start()]:continue
            out.append((Mutant(rel,text.count("\n",0,m.start())+1,a,b),m.start(),m.end()))
    return sorted(out,key=lambda x:x[1])
def run(root,files,cmd,max_mutants=None,timeout=120):
    if subprocess.run(cmd,cwd=root,shell=True,timeout=timeout).returncode:raise RuntimeError("baseline test command failed")
    results=[]
    for p in files:
        original=p.read_text(errors="ignore"); rel=p.relative_to(root).as_posix()
        for mu,a,b in sites(original,rel):
            if max_mutants is not None and len(results)>=max_mutants:return results
            try:
                p.write_text(original[:a]+mu.replacement+original[b:])
                mu.status="survived" if subprocess.run(cmd,cwd=root,shell=True,timeout=timeout).returncode==0 else "killed"
            except subprocess.TimeoutExpired:mu.status="killed"
            finally:p.write_text(original)
            results.append(mu)
    return results
