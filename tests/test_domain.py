from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import compare_settlement as tool

FUTURES = b'contract,contract_month,price,quote_time,unit\nEC2404,2024-04,1200,2024-01-09T00:00:00Z,index_points\n'
INDEX = b'index_name,period_end,published_at,value\nSCFIS_EUROPE,2024-01-05T00:00:00Z,2024-01-08T00:00:00Z,1000\n'

class ECTests(unittest.TestCase):
    def run_ec(self, futures=FUTURES, index=INDEX):
        return tool.analyze(futures,index,'EC2404','2024-01-09T00:00:00Z','synthetic')

    def test_difference_is_not_final_settlement(self):
        result = self.run_ec()
        self.assertEqual(result['futures_minus_last_published_index'],200)
        self.assertAlmostEqual(result['difference_ratio'],.2)
        self.assertFalse(result['index_published_after_quote'])
        self.assertNotIn('final_settlement_price',result)

    def test_future_publication_not_period_end_controls_visibility(self):
        reports = [self.run_ec(index=INDEX+f'SCFIS_EUROPE,2024-01-08T00:00:00Z,2024-01-10T00:00:00Z,{v}\n'.encode()) for v in (200,9999)]
        for result in reports:
            self.assertEqual(result['last_published_index'],1000)
            self.assertEqual(result['excluded_future_publications'],1)
        self.assertEqual(reports[0]['difference_ratio'], reports[1]['difference_ratio'])

    def test_future_quote_is_excluded(self):
        result = self.run_ec(futures=FUTURES+b'EC2404,2024-04,9000,2024-01-10T00:00:00Z,index_points\n')
        self.assertEqual(result['futures_price'],1200)
        self.assertEqual(result['excluded_future_quotes'],1)

    def test_index_published_after_stale_quote_is_explicit(self):
        result = self.run_ec(futures=FUTURES.replace(b'2024-01-09',b'2024-01-07'))
        self.assertTrue(result['index_published_after_quote'])
        self.assertEqual(result['quote_age_seconds'],172800)

    def test_scfi_cannot_be_substituted(self):
        with self.assertRaises(ValueError):
            self.run_ec(index=INDEX.replace(b'SCFIS_EUROPE',b'SCFI_EUROPE'))

    def test_contract_month_and_unit_must_match(self):
        for old,new in [(b'2024-04',b'2024-06'),(b'index_points',b'USD_per_container')]:
            with self.subTest(new=new), self.assertRaises(ValueError):
                self.run_ec(futures=FUTURES.replace(old,new))

    def test_invalid_publication_order_duplicates_and_missing_visibility(self):
        for raw in [INDEX.replace(b'2024-01-05',b'2024-01-09'), INDEX+INDEX.splitlines()[1]+b'\n', INDEX.replace(b'2024-01-08',b'2024-01-10')]:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.run_ec(index=raw)

    def test_latest_available_quote_and_publication_are_selected(self):
        futures = FUTURES+b'EC2404,2024-04,1150,2024-01-08T00:00:00Z,index_points\n'
        index = INDEX+b'SCFIS_EUROPE,2024-01-04T00:00:00Z,2024-01-07T00:00:00Z,800\n'
        self.assertEqual(self.run_ec(futures,index)['futures_minus_last_published_index'],200)
