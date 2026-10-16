import itertools
import random
import unittest
from src.prioritizers import prioritize,STRATEGIES
from src.metrics import evaluate
from src.cases import generate,passes
from src import subject


class MethodTests(unittest.TestCase):
    def test_known_metrics(self):
        records={"a":{"cost_ns":2,"coverage":{1}},"b":{"cost_ns":3,"coverage":{2}},
                 "c":{"cost_ns":5,"coverage":{3}}}
        m=evaluate(list(records),records,{"a":{"F1"},"b":set(),"c":{"F2"}},7)
        self.assertAlmostEqual(m["apfd"],.5)
        self.assertAlmostEqual(m["apfdc"],.575)
        self.assertAlmostEqual(m["auc_completion"],.4)
        self.assertEqual(m["first_fault_with_overhead_ns"],9)

    def test_permutations_and_coverage_stagnation(self):
        records={"a":{"cost_ns":3,"coverage":{1}},"b":{"cost_ns":1,"coverage":{1}},
                 "c":{"cost_ns":2,"coverage":{2}},"d":{"cost_ns":1,"coverage":set()}}
        for strategy in STRATEGIES:
            out,_=prioritize(records,strategy)
            self.assertEqual(sorted(out),sorted(records))
        self.assertEqual(prioritize(records,"cost_aware")[0][0],"b")

    def test_zero_gain_terminates(self):
        data={str(i):{"cost_ns":1,"coverage":set()} for i in range(10)}
        for s in STRATEGIES:
            self.assertEqual(len(prioritize(data,s)[0]),10)

    def test_metric_permutations_match_integral(self):
        data={str(i):{"cost_ns":i+1,"coverage":{i}} for i in range(4)}
        kills={"0":{"x"},"1":{"y"},"2":{"x","z"},"3":set()}
        for order in itertools.permutations(data):
            seen=set();time=0;area=0
            for i in order:
                area+=len(seen)*data[i]["cost_ns"]
                time+=data[i]["cost_ns"];seen|=kills[i]
            self.assertAlmostEqual(evaluate(order,data,kills)["auc_completion"],area/(3*time))

    def test_specification_anchors(self):
        self.assertEqual(subject.discount(10000,False,"PROMO10"),9000)
        self.assertEqual(subject.discount(10000,True,"PROMO10"),9500)
        self.assertEqual(subject.freight(20000,"local",3,False),0)
        self.assertEqual(subject.freight(20000,"local",3,True),2500)
        self.assertEqual(subject.checkout([[1000,2,10,200]]),(2800,2000,0,800,8))

    def test_all_generated_cases(self):
        for case in generate():
            self.assertTrue(passes(subject,case),case["id"])


if __name__=="__main__": unittest.main()
