#!/usr/bin/env python3
"""Local editorial operations, never an unauthenticated web admin."""
import argparse,json,sqlite3
from pathlib import Path
from atlas import Atlas,ROOT,REVIEWABLE
p=argparse.ArgumentParser(); p.add_argument('--db',type=Path,default=ROOT/'.local/atlas.sqlite')
s=p.add_subparsers(dest='cmd',required=True)
s.add_parser('init'); i=s.add_parser('import'); i.add_argument('file',type=Path)
s.add_parser('check'); s.add_parser('queue')
r=s.add_parser('review'); r.add_argument('table',choices=REVIEWABLE);r.add_argument('id');r.add_argument('status',choices=['approved','pending','disputed','retired']);r.add_argument('--reviewer',required=True);r.add_argument('--evidence',required=True)
b=s.add_parser('backup');b.add_argument('destination',type=Path)
a=p.parse_args(); atlas=Atlas(a.db)
if a.cmd=='init':out={'database':str(a.db),'schema':1}
elif a.cmd=='import':out=atlas.import_file(a.file)
elif a.cmd=='check':out=atlas.validate()
elif a.cmd=='queue':out={t:atlas.rows(t) for t in REVIEWABLE}
elif a.cmd=='review':out=atlas.review(a.table,a.id,a.status,a.reviewer,a.evidence)
else:
 if a.destination.exists():raise SystemExit('备份目标已存在；请选择新文件，避免覆盖。')
 with atlas.connect() as source, sqlite3.connect(a.destination) as target:source.backup(target)
 out={'backup':str(a.destination)}
print(json.dumps(out,ensure_ascii=False,indent=2))
