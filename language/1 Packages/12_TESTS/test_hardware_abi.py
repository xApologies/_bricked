import hashlib, os, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1]/'09_EMULATOR'))
from genesis_chirality_machine.address import FabricAddress
from genesis_chirality_machine.cell import ChiralityCell, RIGHT_PATTERN, LEFT_PATTERN, q16, uq16
from genesis_chirality_machine.codec import CalibratedLevelCodec
from genesis_chirality_machine.image import FabricImageBuilder, FabricImage
from genesis_chirality_machine.fixture import deterministic_cells
from genesis_chirality_machine.machine import GenesisChiralityMachine

class HardwareABITests(unittest.TestCase):
    def setUp(self):
        self.td=tempfile.TemporaryDirectory(); self.path=Path(self.td.name)/'f.gcf'
        FabricImageBuilder.build(self.path, deterministic_cells(512))
        self.base_sha=hashlib.sha256(self.path.read_bytes()).hexdigest()
        self.fabric=FabricImage(self.path); self.m=GenesisChiralityMachine(self.fabric)
    def tearDown(self): self.fabric.close(); self.td.cleanup()

    def test_address_roundtrip(self):
        a=FabricAddress(self.fabric.fabric_tag,1,7,3,2); self.assertEqual(FabricAddress.unpack(a.pack()),a)
    def test_cell_32_bytes(self): self.assertEqual(len(ChiralityCell.right().pack()),32)
    def test_right_left_witnesses(self):
        self.assertEqual(RIGHT_PATTERN,0x69); self.assertEqual(LEFT_PATTERN,0x96)
        self.assertEqual(ChiralityCell.right().mirror().occupancy_pattern, LEFT_PATTERN)
    def test_mirror_involution(self):
        c=ChiralityCell.right(state_class=3,sigma=123); self.assertEqual(c.mirror().mirror(),c)
    def test_q16(self): self.assertAlmostEqual(uq16(q16(.5)),.5,places=4)
    def test_codec_roundtrip(self):
        c=CalibratedLevelCodec()
        for i in range(8): self.assertEqual(c.decode(c.encode(i)),i)
    def test_mount_identity(self): self.assertEqual(self.m.mount_receipt()['cell_count'],512)
    def test_read_cell(self):
        a=self.fabric.address_for_index(3); self.assertIn(self.m.read(a).handedness,(-1,1))
    def test_overlay_precedence(self):
        a=self.fabric.address_for_index(2); old=self.m.read(a)
        new=ChiralityCell.left(state_class=7,identity_tag=999)
        self.m.stage(a,new); self.assertEqual(self.m.read(a),new); self.assertNotEqual(old,new)
    def test_commit_receipt(self):
        a=self.fabric.address_for_index(4); self.m.stage(a,ChiralityCell.right(state_class=5)); r=self.m.commit(); self.assertEqual(r['count'],1)
    def test_base_immutable_after_overlay(self):
        a=self.fabric.address_for_index(5); self.m.stage(a,ChiralityCell.left(state_class=6)); self.m.commit()
        self.assertEqual(hashlib.sha256(self.path.read_bytes()).hexdigest(), self.base_sha)
    def test_fabric_address_wrong_tag_rejected(self):
        a=FabricAddress(self.fabric.fabric_tag^1,0,0)
        with self.assertRaises(Exception): self.fabric.read(a)
    def test_geometric_region(self): self.assertEqual(self.m.geometric_region(10,20)['count'],20)
    def test_occupancy_3d_shape(self):
        o=ChiralityCell.right().occupancy_3d; self.assertEqual(len(o),2); self.assertEqual(len(o[0]),2); self.assertEqual(len(o[0][0]),2)

if __name__=='__main__': unittest.main()
