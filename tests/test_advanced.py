from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import analyze_route_scenarios as tool

HEADER='scenario,known_at,base_cycle_days,extra_cycle_days,affected_share,demand_change_fraction\n'
def case(base=60,extra=20,share=.5,demand=0):
    return (HEADER+f'DEMO,2024-01-09T00:00:00Z,{base},{extra},{share},{demand}\n').encode()

class AdvancedTests(unittest.TestCase):
    def check(self,raw):
        return tool.analyze(raw,'2024-01-09T00:00:00Z','synthetic')

    def test_fixed_fleet_capacity_uses_baseline_weighted_shares(self):
        result=self.check(case())['scenarios'][0]
        self.assertEqual(result['effective_capacity_fraction'],.875)
        self.assertEqual(result['capacity_loss_fraction'],.125)
        self.assertAlmostEqual(result['demand_per_capacity_relative'],1/.875)
        self.assertEqual(self.check(case(share=1))['scenarios'][0]['effective_capacity_fraction'],.75)
        self.assertEqual(self.check(case(share=0))['scenarios'][0]['effective_capacity_fraction'],1)

    def test_demand_decline_can_offset_detour_pressure(self):
        result=self.check(case(demand=-.2))['scenarios'][0]
        self.assertEqual(result['pressure_vs_baseline'],'lower')
        self.assertNotIn('ec_return',result)
        self.assertEqual(self.check(case(extra=0,demand=0))['scenarios'][0]['pressure_vs_baseline'],'unchanged')

    def test_invalid_parameters_and_duplicates_are_rejected(self):
        for raw in [case(base=0),case(extra=-1),case(share=1.1),case(demand=-1),case()+case().splitlines()[1]+b'\n']:
            with self.subTest(raw=raw),self.assertRaises(ValueError):
                self.check(raw)

    def test_future_assumptions_are_not_available_at_cutoff(self):
        raw=case()+b'FUTURE,2024-01-10T00:00:00Z,60,99999,1,1\n'
        result=self.check(raw)
        self.assertEqual(len(result['scenarios']),1)
        self.assertEqual(result['excluded_future_scenarios'],1)
