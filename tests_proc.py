import unittest

from process import Buffer, Processor


class TestBuffer(unittest.TestCase):
    def test_full(self):
        b = Buffer(2)
        b.push(1)
        b.push(10101)
        self.assertEqual(b.is_full(), True)

    def test_not_full(self):
        b = Buffer(2)
        self.assertEqual(b.is_full(), False)

    def test_overflow(self):
        b = Buffer(3)
        b.push(12312)
        b.push(890)
        b.push(56)
        self.assertRaises(IndexError, b.push, 123)


class TestProcessor(unittest.TestCase):

    def test_processing_flow(self):
        # create a process
        p = Processor('tt', 40)
        till_free = p.add_process(123)
        current_state = till_free

        # check if process reduces till free timer with each call 
        # to process method
        for i in range(till_free):
            self.assertEqual(p.process(), current_state - 1)
            current_state -= 1

        # check that in the end of process till free is set to 0
        self.assertEqual(0, p.process())

    def test_buffer_limit(self):
        ''' Adds more processes than process can handle till buffer overflow '''
        b = Buffer(2)
        p = Processor('rtt', 40, b)
        p.add_process(123)
        p.add_process(1231231)
        p.add_process(87)
        self.assertEqual(0, p.add_process(666))


if __name__ == '__main__':
    unittest.main()
