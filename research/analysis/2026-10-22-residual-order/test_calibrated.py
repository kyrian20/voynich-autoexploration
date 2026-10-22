import unittest
from residual_order_calibrated import Calibrated,GRID
class Calibration(unittest.TestCase):
 def test_normalized_and_development_monotonic_selection(self):
  train=[{'group':'train','tokens':['ax','by']*20+['cz','ax']}]
  dev=[{'group':'dev','tokens':['ax','by']*5}]
  model=Calibrated(train,dev)
  for a in ('ax','unseen'):
   probabilities=[model.probabilities(a,w) for w in model.events]
   for i in range(4):self.assertAlmostEqual(sum(p[i] for p in probabilities),1.0,places=12)
  for layer,scores in enumerate(model.calibration):
   chosen=next(s['development_bits'] for s in scores if s['weight']==model.weights[layer])
   self.assertLessEqual(chosen,scores[0]['development_bits'])
 def test_disjoint_development_required(self):
  row={'group':'same','tokens':['a','b']}
  with self.assertRaises(ValueError):Calibrated([row],[row])
 def test_no_test_input_to_calibration_interface(self):
  import inspect
  self.assertEqual(list(inspect.signature(Calibrated).parameters),['train','development','cap'])
if __name__=='__main__':unittest.main()
