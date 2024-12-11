import dataclasses
import sys
import time
import unittest


@dataclasses.dataclass
class Timings:
    timings = []

    def start(self, name:str):
        self.timings.append([name, 1000 * time.time()])

    def stop(self):
        self.timings[-1].append(1000 * time.time())

    def __repr__(self) -> str:
        pad = max(len(t[0]) for t in self.timings)
        return '\n'.join(
            [f'{t[0]:{pad}} {(t[2] - t[1]):8.3f} ms' for t in sorted(self.timings)])


class TimedTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.timings = Timings()

    def setUp(self):
        self.__class__.timings.start(self._testMethodName[5:])

    def tearDown(self):
        self.__class__.timings.stop()

    @classmethod
    def tearDownClass(cls):
        print(cls.timings, file=sys.stderr)
