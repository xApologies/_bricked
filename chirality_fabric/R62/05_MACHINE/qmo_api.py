#!/usr/bin/env python3
import argparse, json, sqlite3, sys
from pathlib import Path

DB = Path(__file__).with_name('genesis_chirality_full_checkpoint.sqlite')
TABLES = {
    'qmos','objects','equations','claims','relations','chronology','open_debt','sources',
    'supersessions','aliases','analogies','recovery_rules','artifacts','thread_segments',
    'checkpoint_components','file_aliases','metadata'
}
ADDRESS_TABLES = ['qmos','objects','equations','claims','open_debt','sources','aliases','analogies','recovery_rules','artifacts','thread_segments']

def connect():
    con=sqlite3.connect(DB)
    con.row_factory=sqlite3.Row
    return con

def emit(x):
    print(json.dumps(x,indent=2,ensure_ascii=False))

def info(con):
    md={r['key']:r['value'] for r in con.execute('select key,value from metadata order by key')}
    counts={t:con.execute(f'select count(*) from {t}').fetchone()[0] for t in sorted(TABLES) if t!='metadata'}
    emit({'metadata':md,'counts':counts,'integrity':con.execute('pragma integrity_check').fetchone()[0]})

def address(con, key):
    out=[]
    for t in ADDRESS_TABLES:
        cols=[r[1] for r in con.execute(f'pragma table_info({t})')]
        col='address' if 'address' in cols else ('alias' if 'alias' in cols else None)
        if col:
            rows=con.execute(f'select * from {t} where {col}=?',(key,)).fetchall()
            out += [{'table':t, **dict(r)} for r in rows]
    emit(out)

def search(con, term):
    q=f'%{term}%'; out=[]
    for t in ['qmos','objects','equations','claims','open_debt','sources','artifacts','thread_segments']:
        cols=[r[1] for r in con.execute(f'pragma table_info({t})')]
        textcols=[c for c in cols if c not in {'id','size_bytes','priority','embedded','seq'}]
        where=' OR '.join([f'CAST({c} AS TEXT) LIKE ?' for c in textcols])
        rows=con.execute(f'select * from {t} where {where}',(q,)*len(textcols)).fetchall()
        out += [{'table':t, **dict(r)} for r in rows]
    emit(out)

def neighbors(con, key, direction):
    out=[]
    if direction in ('out','both'):
        out += [dict(r) for r in con.execute('select * from relations where source_address=?',(key,))]
    if direction in ('in','both'):
        out += [dict(r) for r in con.execute('select * from relations where target_address=?',(key,))]
    emit(out)

def list_table(con, table, limit):
    if table not in TABLES: raise SystemExit(f'Unknown table: {table}')
    emit([dict(r) for r in con.execute(f'select * from {table} limit ?',(limit,))])

def resume(con):
    emit({
      'primary_resume_address':'@open/native_multiscale_update_law',
      'record': [dict(r) for r in con.execute("select * from open_debt where address='@open/native_multiscale_update_law'")],
      'neighbors':[dict(r) for r in con.execute("select * from relations where source_address='@eq/domain_generator_map' or target_address='@eq/domain_generator_map' or source_address='@eq/local_update_generator' or target_address='@eq/local_update_generator'")]
    })

def main():
    ap=argparse.ArgumentParser(description='Queryable API for GENESIS Chirality Fabric Full Checkpoint R62')
    sp=ap.add_subparsers(dest='cmd',required=True)
    sp.add_parser('info')
    a=sp.add_parser('address'); a.add_argument('key')
    s=sp.add_parser('search'); s.add_argument('term')
    n=sp.add_parser('neighbors'); n.add_argument('key'); n.add_argument('--direction',choices=['in','out','both'],default='both')
    l=sp.add_parser('list'); l.add_argument('table'); l.add_argument('--limit',type=int,default=100)
    sp.add_parser('resume')
    args=ap.parse_args(); con=connect()
    try:
        {'info':lambda:info(con),'address':lambda:address(con,args.key),'search':lambda:search(con,args.term),'neighbors':lambda:neighbors(con,args.key,args.direction),'list':lambda:list_table(con,args.table,args.limit),'resume':lambda:resume(con)}[args.cmd]()
    finally: con.close()
if __name__=='__main__': main()
