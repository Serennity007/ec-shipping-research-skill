import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
NAME=ROOT.name

class DomainCLITests(unittest.TestCase):
    def command(self,output):
        common=['--as-of','2024-01-09T15:00:00+08:00','--data-kind','synthetic','--out',str(output)]
        if NAME=='crude-oil-research-skill':
            files=[ROOT/'examples/curve.csv']
            args=['analyze_curve.py','--csv',str(files[0])]
        elif NAME=='ec-shipping-research-skill':
            files=[ROOT/'examples/futures.csv',ROOT/'examples/settlement-index.csv']
            args=['compare_settlement.py','--futures',str(files[0]),'--index',str(files[1]),'--contract','EC2404']
        else:
            files=[ROOT/'examples/breadth.csv']
            args=['analyze_breadth.py','--csv',str(files[0]),'--universe','DEMO','--expected-count','10']
        return [sys.executable,str(ROOT/'scripts'/args[0]),*args[1:],*common],files

    def test_domain_cli_runs_from_an_unrelated_directory_and_preserves_files(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'output with spaces.json'
            args,files=self.command(output)
            originals=[p.read_bytes() for p in files]
            run=subprocess.run(args,cwd=temp,capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            result=json.loads(output.read_text(encoding='utf-8'))
            self.assertEqual(result['data_kind'],'synthetic')
            self.assertIn('generated_at_utc',result)
            stored=output.read_bytes()
            self.assertNotEqual(subprocess.run(args,cwd=temp,capture_output=True).returncode,0)
            self.assertEqual(output.read_bytes(),stored)
            for file,raw in zip(files,originals):
                args[-1]=str(file)
                self.assertNotEqual(subprocess.run(args,cwd=temp,capture_output=True).returncode,0)
                self.assertEqual(file.read_bytes(),raw)

    def test_committed_outputs_match_input_byte_hashes(self):
        structure=json.loads((ROOT/'examples/structure-output.json').read_text(encoding='utf-8'))
        self.assertEqual(structure['source_sha256'],hashlib.sha256((ROOT/'examples/bars.csv').read_bytes()).hexdigest())
        _,files=self.command(Path('unused.json'))
        domain=json.loads((ROOT/'examples/domain-output.json').read_text(encoding='utf-8'))
        hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in files]
        if len(hashes)==1:
            self.assertEqual(domain['source_sha256'],hashes[0])
        else:
            self.assertEqual(domain['source_sha256'],dict(zip(['futures','index'],hashes)))
