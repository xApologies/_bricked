import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
let failures = 0;
function check(ok, label) {
 console.log((ok ? 'PASS ' : 'FAIL ') + label);
 if (!ok) failures++;
}
const read = p => readFileSync(resolve(root,p),'utf8');
const stages = ["00_RELEASE","01_DESIGN","02_CYBERSECURITY","03_GENESIS_MODEL","04_STATE_MODEL","05_ALGORITHMS","06_PSEUDOCODE","07_VISUALIZATION","08_INTERACTION","09_FLAGS_AND_KEYS","10_TESTING","11_DIAGRAMS","12_MACHINE_READABLE","13_IMPLEMENTATION_HANDOFF","14_PROVENANCE"];
const modules = [["M01_GENESIS",44,"L000 FIRST LIGHT + L001–L043 ROOT."],["M02_CODE",11,""],["M03_NETWORK",21,""],["M04_VIRTUALIZE",21,""],["M05_VIRTUAL_BOXING",21,"Strictly one Red VM versus one Blue VM."],["M06_RAID",21,"One-versus-many Virtual Boxing plus memory/storage resilience."],["M07_FLEET",21,"Controller/worker orchestration and many-versus-many."],["M08_SOVEREIGN",11,"Final synthesis/certification."]];
const paths = ["docs/architecture","docs/design","docs/cybersecurity","docs/visual_language","docs/glossary","docs/diagrams","game/genesis","game/sandbox","game/gameplay","game/levels","game/networking","game/security","game/persistence","game/platform","game/rendering","content/art","content/audio","content/vfx","content/ui","content/shaders","content/blender","data/levels","data/objects","data/states","data/algorithms","data/tests","tools/validators","tools/exporters","tools/generators","tools/dev","tests/unit","tests/integration","tests/regression","tests/adversarial","tests/performance","platform/ios","platform/android","platform/desktop","provenance/decisions","provenance/checkpoints","provenance/sources","provenance/audits","development/checkpoints","development/systems/BOOT_NAVIGATION","development/systems/SHARED_SYSTEMS","development/constitution/LEVEL_XX/00_RELEASE","development/constitution/LEVEL_XX/01_DESIGN","development/constitution/LEVEL_XX/02_CYBERSECURITY","development/constitution/LEVEL_XX/03_GENESIS_MODEL","development/constitution/LEVEL_XX/04_STATE_MODEL","development/constitution/LEVEL_XX/05_ALGORITHMS","development/constitution/LEVEL_XX/06_PSEUDOCODE","development/constitution/LEVEL_XX/07_VISUALIZATION","development/constitution/LEVEL_XX/08_INTERACTION","development/constitution/LEVEL_XX/09_FLAGS_AND_KEYS","development/constitution/LEVEL_XX/10_TESTING","development/constitution/LEVEL_XX/11_DIAGRAMS","development/constitution/LEVEL_XX/12_MACHINE_READABLE","development/constitution/LEVEL_XX/13_IMPLEMENTATION_HANDOFF","development/constitution/LEVEL_XX/14_PROVENANCE","development/modules","development/modules/M01_GENESIS","development/modules/M02_CODE","development/modules/M03_NETWORK","development/modules/M04_VIRTUALIZE","development/modules/M05_VIRTUAL_BOXING","development/modules/M06_RAID","development/modules/M07_FLEET","development/modules/M08_SOVEREIGN","docs/genesis"];
check(paths.every(p=>existsSync(resolve(root,p))), 'Requested repository directories exist');
check(stages.every(s=>existsSync(resolve(root,'development/constitution/LEVEL_XX',s))), 'All 15 invariant stages exist');
check(modules.every(([m])=>existsSync(resolve(root,'development/modules',m))), 'All eight module directories exist');
const canon = read('development/modules/README.md');
const rows = [...canon.matchAll(/^\| \[(M\d{2}_[A-Z_]+)\]\([^\n]+?\) \| (\d+) \|/gm)];
check(rows.length===8 && modules.every(([m,n])=>rows.some(r=>r[1]===m && Number(r[2])===n)) && rows.reduce((s,r)=>s+Number(r[2]),0)===171 && canon.includes('| **TOTAL** | **171** |'), 'Documented scenario counts total 171');
const genesis = ["11D_ARCHITECTURE","GENESIS_FIELD","CHIRALITY_FABRIC","CHIRALITY_BYTE","RESOLUTION","BANDWIDTH","RAINBOW_ROAD","PSSP","GHOSTING","DECS","GUARDIAN_CDN","CHIRALITY_CYCLES","GENESIS_LANGUAGE"];
check(genesis.every(g=>read('docs/genesis/'+g+'.md').includes('Status: **OPEN')), 'All 13 shared Genesis specifications remain OPEN');
function walk(p) {
 return readdirSync(resolve(root,p),{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(p+'/'+e.name):[p+'/'+e.name]);
}
check(['game','content','data','platform','tests'].every(p=>walk(p).every(f=>f.endsWith('/.gitkeep'))), 'Runtime, content, data, platform and test boundaries contain placeholders only');
console.log('SCOPE: these structural checks do not certify level acceptance or Gold status.');
const manifest = JSON.parse(read('provenance/sources/dev-import.json'));
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
check(sha(readFileSync(resolve(root,manifest.source))) === manifest.sha256, 'Original ZIP SHA-256 matches recorded source');
const templateFiles = walk(manifest.destination).map(p=>p.slice(manifest.destination.length+1)).sort();
const expectedFiles = manifest.files.map(f=>f.path).sort();
check(manifest.file_count === 87 && manifest.files.length === 87 && JSON.stringify(templateFiles) === JSON.stringify(expectedFiles), 'All 87 imported template files preserved with exact relative paths');
check(manifest.files.every(f=>{
 const p=resolve(root,manifest.destination,f.path);
 if (!existsSync(p)) return false;
 const bytes=readFileSync(p);
 return bytes.length===f.bytes && sha(bytes)===f.sha256;
}), 'Every imported file matches its ZIP-entry length and SHA-256');
process.exitCode = failures ? 1 : 0;
