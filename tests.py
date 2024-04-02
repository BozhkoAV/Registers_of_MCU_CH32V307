import unittest
from unittest.mock import patch
import registers
import io


class Test(unittest.TestCase):
    # FS 2.1
    def test_fun_info(self):
        with open('expected_results/fun_info_res.txt', 'r') as file:
            expected_output = file.read().strip()

        with io.StringIO() as output:
            with patch('sys.stdout', output):
                registers.fun_info()
            actual_output = output.getvalue().strip()

        self.assertEqual(actual_output, expected_output)

    # FS 2.2
    def test_fun_tree(self):
        with open('expected_results/fun_tree_res.txt', 'r', encoding='utf-8') as file:
            expected_output = file.read().strip()

        with io.StringIO() as output:
            with patch('sys.stdout', output):
                registers.fun_tree()
            actual_output = output.getvalue().strip()

        self.assertEqual(actual_output, expected_output)

    # FS 3.1
    def test_fun_group(self):
        with open('expected_results/fun_group_res.txt', 'r') as file:
            expected_output = file.read().strip()

        with io.StringIO() as output:
            with patch('sys.stdout', output):
                registers.fun_group(['ADC1'])
            actual_output = output.getvalue().strip()

        self.assertEqual(actual_output, expected_output)

    # FS 4.1
    def test_fun_register(self):
        with open('expected_results/fun_register_res.txt', 'r') as file:
            expected_output = file.read().strip()

        with io.StringIO() as output:
            with patch('sys.stdout', output):
                registers.fun_register(['ADC1', 'STATR'])
            actual_output = output.getvalue().strip()

        self.assertEqual(actual_output, expected_output)

    # FS 5.1
    def test_fun_bit(self):
        with open('expected_results/fun_bit_res.txt', 'r') as file:
            expected_output = file.read().strip()

        with io.StringIO() as output:
            with patch('sys.stdout', output):
                registers.fun_bit(['ADC1', 'STATR', 'AWD'])
            actual_output = output.getvalue().strip()

        self.assertEqual(actual_output, expected_output)

    # FS 6.1
    def test_fun_hex(self):
        with open('expected_results/fun_hex_res.txt', 'r') as file:
            expected_output = file.read().strip()

        with io.StringIO() as output:
            with patch('sys.stdout', output):
                registers.fun_hex(['ADC1', 'CTLR1', 'AWDCH', '11'])
            actual_output = output.getvalue().strip()

        self.assertEqual(actual_output, expected_output)

    # FS 7.1
    def test_fun_bin(self):
        with open('expected_results/fun_bin_res.txt', 'r') as file:
            expected_output = file.read().strip()

        with io.StringIO() as output:
            with patch('sys.stdout', output):
                registers.fun_bin(['ADC1', 'CTLR1', 'AWDCH', '11'])
            actual_output = output.getvalue().strip()

        self.assertEqual(actual_output, expected_output)

    # FS 8.1
    def test_fun_regh(self):
        with open('expected_results/fun_regh_res.txt', 'r') as file:
            expected_output = file.read().strip()

        with io.StringIO() as output:
            with patch('sys.stdout', output):
                registers.fun_regh(['ADC1', 'STATR', '11'])
            actual_output = output.getvalue().strip()

        self.assertEqual(actual_output, expected_output)

    # FS 9.1
    def test_fun_regb(self):
        with open('expected_results/fun_regb_res.txt', 'r') as file:
            expected_output = file.read().strip()

        with io.StringIO() as output:
            with patch('sys.stdout', output):
                registers.fun_regb(['ADC1', 'STATR', '11'])
            actual_output = output.getvalue().strip()

        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest.main()
