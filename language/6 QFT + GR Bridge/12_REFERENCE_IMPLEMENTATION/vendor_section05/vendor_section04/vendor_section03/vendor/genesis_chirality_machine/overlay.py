from dataclasses import dataclass, field
import hashlib, json, time
from .cell import ChiralityCell

@dataclass
class FabricOverlay:
    committed: dict = field(default_factory=dict)
    staged: dict = field(default_factory=dict)
    receipts: list = field(default_factory=list)

    def stage(self, address, cell: ChiralityCell):
        self.staged[address.as_int()] = cell

    def read(self, address, base_reader):
        k=address.as_int()
        if k in self.staged: return self.staged[k]
        if k in self.committed: return self.committed[k]
        return base_reader(address)

    def commit(self, reason='overlay_commit'):
        items=[]
        for k,v in sorted(self.staged.items()):
            self.committed[k]=v
            items.append((k, v.pack().hex()))
        payload=json.dumps(items, separators=(',',':')).encode()
        digest=hashlib.sha256(payload).hexdigest()
        receipt={'kind':reason,'count':len(items),'digest':digest,'timestamp_ns':time.time_ns()}
        self.receipts.append(receipt)
        self.staged.clear()
        return receipt

    def root_hash(self):
        h=hashlib.sha256()
        for k,v in sorted(self.committed.items()):
            h.update(k.to_bytes(16,'big')); h.update(v.pack())
        return h.hexdigest()
