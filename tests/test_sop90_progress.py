"""Regression for the milestone's false-pass paths, independent of modeling output."""
import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from sop90_progress import progress,BASELINE_IDS
class MilestoneTests(unittest.TestCase):
 def fixture(self,n):
  audit={'items':[{'id':s,'status':'MATCHED' if i<n else 'MISMATCH'} for i,s in enumerate(BASELINE_IDS)]}
  result={'unproven_matches':[],'checks':{'asset_hashes_current':True,'ten_recent_distinct_photos':True,'three_independent_sources':True,'zero_unresolved_differences':n==21},'accuracy_gate':'PASS' if n==21 else 'NOT_ACCEPTED'}
  return audit,result
 def test_19_is_milestone_but_not_full_release(self):
  a,r=self.fixture(19);p=progress(a,r);self.assertTrue(p['milestone_90_pass']);self.assertEqual(p['percent'],90.48);self.assertEqual(p['full_release_accuracy_gate'],'NOT_ACCEPTED')
 def test_18_cannot_round_up(self):
  a,r=self.fixture(18);self.assertFalse(progress(a,r)['milestone_90_pass'])
 def test_deleting_failures_does_not_raise_score(self):
  a,r=self.fixture(18);a['items']=a['items'][:18];p=progress(a,r);self.assertEqual(p['denominator'],21);self.assertFalse(p['milestone_90_pass'])
 def test_unproven_match_does_not_count(self):
  a,r=self.fixture(19);r['unproven_matches']=[{'id':'G01'}];self.assertEqual(progress(a,r)['numerator'],18)
 def test_stale_assets_reset_proven_count(self):
  a,r=self.fixture(21);r['checks']['asset_hashes_current']=False;self.assertEqual(progress(a,r)['numerator'],0)
 def test_photos_remain_prerequisite(self):
  a,r=self.fixture(21);r['checks']['ten_recent_distinct_photos']=False;self.assertFalse(progress(a,r)['milestone_90_pass'])
 def test_new_defect_expands_denominator(self):
  a,r=self.fixture(19);a['items'].append({'id':'S02','status':'MISMATCH'});p=progress(a,r);self.assertEqual(p['required_matches'],20);self.assertFalse(p['milestone_90_pass'])
 def test_duplicate_ids_cannot_pass(self):
  a,r=self.fixture(21);a['items'].append(copy.deepcopy(a['items'][0]));self.assertFalse(progress(a,r)['milestone_90_pass'])
if __name__=='__main__':unittest.main()
