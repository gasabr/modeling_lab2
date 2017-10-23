import unittest

from process import Buffer, Processor


class TestBuffer(unittest.TestCase):
    def test_full(self):
        b = Buffer(2)
        b.push(1, 1)
        b.push(10101, 2)
        self.assertEqual(b.is_full(), True)

    def test_not_full(self):
        b = Buffer(2)
        self.assertEqual(b.is_full(), False)

    def test_overflow(self):
        b = Buffer(3)
        b.push(12312, 123)
        b.push(890, 99)
        b.push(56, 0)
        self.assertRaises(IndexError, b.push, 123, 176)

    def test_pop_push(self):
        b = Buffer(2)
        b.push(123, 9)
        b.push(65432, 1)
        self.assertEqual(b.pop(), 1)
        self.assertEqual(b.pop(), 9)

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

    def test_queue_empting(self):
        p = Processor('test', 10, Buffer(1))
        work_time = p.add_process(14)
        p.add_process(789)
        self.assertEqual(1, p.get_queue_len())
        # the queue length should stay 1 after additinal push
        p.add_process(444)
        self.assertEqual(1, p.get_queue_len())

        # this is one more `work` than needed to finish process
        for i in range(work_time):
            p.process()
        
        # the process should take the next element from the buffer
        self.assertEqual(p.get_queue_len(), 0)
        # the process should take the next element from buffer
        # and continue working
        self.assertNotEqual(p.process(), 0)

    def test_is_busy_on_init(self):
        p = Processor('test', 10)
        self.assertEqual(p.is_busy(), False)

    def test_is_busy_after_proc_finish(self):
        p = Processor('test', 10)
        work_time = p.add_process(12313)
        for w in range(work_time-1):
            p.process()
            #  self.assertEqual(p.is_busy(), True)
        self.assertEqual(p.is_busy(), False)

if __name__ == '__main__':
    unittest.main()
