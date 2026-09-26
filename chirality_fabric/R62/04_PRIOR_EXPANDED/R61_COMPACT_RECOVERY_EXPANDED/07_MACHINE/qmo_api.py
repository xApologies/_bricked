#!/usr/bin/env python3
"""Read-only mini API/CLI for the R61 Genesis Chirality recovery QMO."""
from __future__ import annotations

import argparse
import json
import sqlite3
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

DB = Path(__file__).resolve().parent / "genesis_chirality_recovery.sqlite"
TABLES = {
    "metadata", "qmos", "objects", "equations", "claims", "relations",
    "chronology", "open_debt", "sources", "supersessions", "aliases",
    "analogies", "recovery_rules"
}
ADDRESS_TABLES = ("qmos", "objects", "equations", "claims", "open_debt", "sources", "analogies", "recovery_rules")

def connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def rows(cur: sqlite3.Cursor) -> list[dict[str, Any]]:
    return [dict(r) for r in cur.fetchall()]

def info() -> dict[str, Any]:
    with connect() as con:
        meta = {r["key"]: r["value"] for r in con.execute("SELECT key,value FROM metadata")}
        counts = {}
        for table in sorted(TABLES - {"metadata"}):
            counts[table] = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        integrity = con.execute("PRAGMA integrity_check").fetchone()[0]
    return {"metadata": meta, "counts": counts, "sqlite_integrity": integrity}

def lookup_address(address: str) -> dict[str, Any]:
    out: dict[str, Any] = {"address": address, "records": {}}
    with connect() as con:
        alias = con.execute("SELECT * FROM aliases WHERE alias=?", (address,)).fetchone()
        if alias:
            out["alias"] = dict(alias)
            address = alias["canonical_address"]
            out["resolved_address"] = address
        for table in ADDRESS_TABLES:
            row = con.execute(f"SELECT * FROM {table} WHERE address=?", (address,)).fetchone()
            if row:
                out["records"][table] = dict(row)
        out["outgoing"] = rows(con.execute("SELECT * FROM relations WHERE source_address=? ORDER BY relation,target_address", (address,)))
        out["incoming"] = rows(con.execute("SELECT * FROM relations WHERE target_address=? ORDER BY relation,source_address", (address,)))
    out["found"] = bool(out["records"] or out["outgoing"] or out["incoming"] or out.get("alias"))
    return out

def neighbors(address: str, direction: str = "both") -> dict[str, Any]:
    with connect() as con:
        outgoing = rows(con.execute("SELECT * FROM relations WHERE source_address=? ORDER BY relation,target_address", (address,))) if direction in ("out", "both") else []
        incoming = rows(con.execute("SELECT * FROM relations WHERE target_address=? ORDER BY relation,source_address", (address,))) if direction in ("in", "both") else []
    return {"address": address, "direction": direction, "outgoing": outgoing, "incoming": incoming}

def search(term: str, limit: int = 100) -> dict[str, Any]:
    like = f"%{term}%"
    results: dict[str, list[dict[str, Any]]] = {}
    specs = {
        "qmos": ("address", "name", "definition", "notes"),
        "objects": ("address", "name", "definition", "notes"),
        "equations": ("address", "name", "expression", "interpretation", "notes"),
        "claims": ("address", "statement", "notes"),
        "open_debt": ("address", "title", "description", "notes"),
        "sources": ("address", "filename", "role", "notes"),
    }
    with connect() as con:
        for table, cols in specs.items():
            clause = " OR ".join(f"{c} LIKE ?" for c in cols)
            q = f"SELECT * FROM {table} WHERE {clause} LIMIT ?"
            vals = [like] * len(cols) + [limit]
            hit = rows(con.execute(q, vals))
            if hit:
                results[table] = hit
    return {"query": term, "results": results}

def list_table(table: str, limit: int = 500) -> list[dict[str, Any]]:
    if table not in TABLES:
        raise ValueError(f"Unknown table: {table}")
    order = "address" if table in ADDRESS_TABLES else ("seq" if table == "chronology" else "rowid")
    with connect() as con:
        return rows(con.execute(f"SELECT * FROM {table} ORDER BY {order} LIMIT ?", (limit,)))

class Handler(BaseHTTPRequestHandler):
    def send_json(self, payload: Any, code: int = 200) -> None:
        data = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        try:
            if path == "/":
                return self.send_json({
                    "name": "Genesis Chirality Fabric R61 Recovery QMO API",
                    "routes": ["/info", "/address/<address>", "/neighbors/<address>?direction=both", "/search?q=term", "/list/<table>"]
                })
            if path == "/info":
                return self.send_json(info())
            if path.startswith("/address/"):
                return self.send_json(lookup_address(urllib.parse.unquote(path[len("/address/"):])) )
            if path.startswith("/neighbors/"):
                addr = urllib.parse.unquote(path[len("/neighbors/"):])
                direction = query.get("direction", ["both"])[0]
                return self.send_json(neighbors(addr, direction))
            if path == "/search":
                return self.send_json(search(query.get("q", [""])[0]))
            if path.startswith("/list/"):
                return self.send_json(list_table(path[len("/list/"):]))
            return self.send_json({"error": "not found"}, 404)
        except Exception as exc:
            return self.send_json({"error": str(exc)}, 400)

def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("info")
    p = sub.add_parser("address"); p.add_argument("address")
    p = sub.add_parser("neighbors"); p.add_argument("address"); p.add_argument("--direction", choices=("out","in","both"), default="both")
    p = sub.add_parser("search"); p.add_argument("term"); p.add_argument("--limit", type=int, default=100)
    p = sub.add_parser("list"); p.add_argument("table", choices=sorted(TABLES)); p.add_argument("--limit", type=int, default=500)
    p = sub.add_parser("serve"); p.add_argument("--host", default="127.0.0.1"); p.add_argument("--port", type=int, default=8797)
    args = parser.parse_args()
    if args.cmd == "info": result = info()
    elif args.cmd == "address": result = lookup_address(args.address)
    elif args.cmd == "neighbors": result = neighbors(args.address, args.direction)
    elif args.cmd == "search": result = search(args.term, args.limit)
    elif args.cmd == "list": result = list_table(args.table, args.limit)
    elif args.cmd == "serve":
        print(f"Serving {DB} on http://{args.host}:{args.port}")
        ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
        return
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
