from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1]/'09_EMULATOR'))
from genesis_chirality_machine.boot import boot
from genesis_chirality_machine.cell import ChiralityCell

machine, receipt = boot('reference_fabric.gcf')
address = machine.fabric.address_for_index(0)
base = machine.read(address)
machine.stage(address, ChiralityCell.left(state_class=3, identity_tag=0xA57A))
commit = machine.commit('example_dynamic_geometric')
print(receipt)
print(base)
print(machine.read(address))
print(commit)
