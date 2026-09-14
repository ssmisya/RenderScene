"""Regression tests for the false acceptance paths; fixtures are not real references."""
import copy, datetime, hashlib, importlib.util, json, sys, tempfile, unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from validate_references import inspect, sha
from release_gate import check_release

class GateTests(unittest.TestCase):
    def setUp(self):
        tmp=ROOT/'.tools/test_reference_gate';tmp.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=tmp);self.root=Path(self.tmp.name)
        self.now=datetime.date.today();self.photos=[]
        (self.root/'scene.blend').write_bytes(b'SYNTHETIC TEST FIXTURE')
        self.assets={'scene.blend':sha(self.root/'scene.blend')}
        (self.root/'date.txt').write_text('Synthetic dated test caption')
        for i in range(10):
            p=self.root/f'p{i}.png';Image.new('RGB',(200,100),(i*20,4,5)).save(p)
            self.photos.append({'id':str(i),'file':p.name,'sha256':sha(p),'dimensions':[200,100],
                'source_url':'https://test.invalid/original','image_url':'https://test.invalid/image',
                'author':'test','source_group':'group'+str(i%3),'capture_date':str(self.now),
                'date_evidence':{'kind':'capture_caption','detail':'Synthetic test evidence',**self.ref('date.txt')},
                'download_date':str(self.now),'position_orientation':'test front','coverage':['front'],
                'observations':'Synthetic fixture only','license':'test','reviewed':True,'usable_for_architecture':True,
                'original_photo_id':str(i),'dedup_review':'DISTINCT'})
        (self.root/'camera.json').write_text(json.dumps({'assets':self.assets,'position':[0,0,0],
            'rotation':[0,0,0],'lens_mm':35,'resolution':[200,100]}))
        Image.new('RGB',(200,100),'white').save(self.root/'render.png')
        Image.new('RGB',(400,100),'gray').save(self.root/'compare.png')
        pts=[[.1,.1],[.5,.1],[.9,.1],[.1,.9],[.5,.9],[.9,.9]]
        items=[]
        for i in range(10):
            comp={'photo_id':str(i),'visual_result':'MATCHED','visible_features':['test topology'],
                  'render':self.ref('render.png'),'camera':self.ref('camera.json'),'comparison':self.ref('compare.png'),
                  'landmarks':[{'feature':str(n),'photo':p,'render':p[:]} for n,p in enumerate(pts)]}
            items.append({'id':str(i),'status':'MATCHED','photo_ids':[str(i)],'comparisons':[comp]})
        self.audit={'schema_version':2,'review_date':str(self.now),'scope':'fixture','target_epoch':str(self.now),
                    'coverage':[{'id':'front','photo_ids':[str(i) for i in range(10)]}],
                    'coverage_complete':True,'current_epoch_verified':True,'time_conflicts':[],
                    'assets':self.assets,'items':items}
    def tearDown(self):self.tmp.cleanup()
    def ref(self,name):return {'file':name,'sha256':sha(self.root/name)}
    def result(self):return inspect(self.root,self.photos,self.audit,self.now)
    def test_complete_fixture_passes(self):self.assertEqual(self.result()['accuracy_gate'],'PASS')
    def test_missing_original_fails(self):
        (self.root/'p0.png').unlink();r=self.result();self.assertFalse(r['checks']['source_integrity']);self.assertEqual(r['accuracy_gate'],'NOT_ACCEPTED')
    def test_corrupt_original_fails(self):
        (self.root/'p0.png').write_bytes(b'broken');self.assertFalse(self.result()['checks']['source_integrity'])
    def test_publication_date_not_capture(self):
        self.photos[0]['capture_date']=None;self.photos[0]['publication_date']=str(self.now);self.assertFalse(self.result()['checks']['ten_recent_distinct_photos'])
    def test_editing_date_not_original_date(self):
        self.photos[0]['date_evidence']['kind']='photoshop_modified';self.assertFalse(self.result()['checks']['ten_recent_distinct_photos'])
    def test_crop_duplicate_not_counted(self):
        self.photos[1]['original_photo_id']=self.photos[0]['original_photo_id'];self.assertFalse(self.result()['checks']['ten_recent_distinct_photos'])
    def test_indoor_photo_not_counted(self):
        self.photos[0]['usable_for_architecture']=False;self.assertFalse(self.result()['checks']['ten_recent_distinct_photos'])
    def test_missing_comparison_fails(self):
        (self.root/'compare.png').unlink();self.assertFalse(self.result()['checks']['matches_have_evidence'])
    def test_missing_angle_not_hidden_by_count(self):
        self.audit['coverage'].append({'id':'rear','photo_ids':['0']});self.assertFalse(self.result()['checks']['coverage_complete'])
    def test_open_defect_not_hidden_by_count(self):
        self.audit['items'][0]['status']='MISMATCH';self.assertFalse(self.result()['checks']['zero_unresolved_differences'])
    def test_empty_detail_list_fails(self):
        self.audit['items']=[];self.assertFalse(self.result()['checks']['nonempty_detail_inventory'])
    def test_na_needs_reason(self):
        self.audit['items'][0]['status']='NOT_APPLICABLE';self.assertFalse(self.result()['checks']['matches_have_evidence'])
    def test_old_asset_render_fails(self):
        (self.root/'scene.blend').write_bytes(b'CHANGED SCENE');self.assertFalse(self.result()['checks']['asset_hashes_current'])
    def test_large_reprojection_error_fails(self):
        self.audit['items'][0]['comparisons'][0]['landmarks'][0]['render']=[.2,.1];self.assertFalse(self.result()['checks']['matches_have_evidence'])
    def test_every_photo_needs_comparison(self):
        self.audit['items'].pop();self.assertFalse(self.result()['checks']['every_eligible_photo_compared'])
    def test_degenerate_landmarks_fail(self):
        for p in self.audit['items'][0]['comparisons'][0]['landmarks']:
            p['photo']=[.5,.5];p['render']=[.5,.5]
        self.assertFalse(self.result()['checks']['matches_have_evidence'])
    def test_future_date_fails(self):
        self.photos[0]['capture_date']=str(self.now+datetime.timedelta(days=1));self.assertFalse(self.result()['checks']['ten_recent_distinct_photos'])
    def test_false_coverage_flag_fails(self):
        self.audit['coverage_complete']=False;self.assertFalse(self.result()['checks']['coverage_complete'])
    def test_time_conflict_blocks(self):
        self.audit['time_conflicts']=['unresolved'];self.assertFalse(self.result()['checks']['no_time_conflicts'])
    def test_developer_cannot_release_with_runtime_pass_only(self):
        f=self.root/'references/test';f.mkdir(parents=True)
        (f/'sources.json').write_text(json.dumps(self.photos));self.audit['items'][0]['status']='MISMATCH'
        for name in ['runtime','blender']:
            p=self.root/(name+'.json');p.write_text(json.dumps({'all_checks_pass':True,'exported_application':True,'assets':self.assets}));self.audit[name+'_report']=self.ref(p.name)
        (f/'audit.json').write_text(json.dumps(self.audit));(self.root/'ACTIVE_REVIEW.json').write_text(json.dumps({'batch':'test','status':'ACCEPTED','release_allowed':True}))
        self.assertIn('zero_unresolved_differences',check_release(self.root))

if __name__=='__main__':unittest.main()
