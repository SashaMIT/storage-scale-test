import importlib.util
import unittest
from pathlib import Path


def _load():
    path = Path(__file__).resolve().parents[1] / "utils" / "slurm" / "group_into_bins.py"
    spec = importlib.util.spec_from_file_location("group_into_bins", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GroupIntoBinsTest(unittest.TestCase):
    def test_remainder_keeps_full_groups_at_the_requested_size(self):
        mod = _load()
        nodes = [(f"n{i:02d}", 10) for i in range(60)]
        bins = mod.partition(nodes, 25)
        self.assertEqual([len(b) for b in bins], [25, 25, 10])
        self.assertEqual(mod.compute_target(nodes, 25), 250)

    def test_exact_multiple_stays_one_group_per_bin(self):
        mod = _load()
        nodes = [(f"n{i:02d}", 10) for i in range(50)]
        bins = mod.partition(nodes, 25)
        self.assertEqual([len(b) for b in bins], [25, 25])
        self.assertEqual(mod.compute_target(nodes, 25), 250)


if __name__ == "__main__":
    unittest.main()
