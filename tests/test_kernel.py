import unittest
from unittest import SkipTest

import jupyter_kernel_test


class TestZenroomKernel(jupyter_kernel_test.KernelTests):
    kernel_name = "zenroom"
    language_name = "lua"
    code_hello_world = "print('hello, world')"
    code_page_something = "?ecdh"
    code_generate_error = "print(3+baddasdasdasdcbcbc)"
    code_execute_result = [
        {'code': "octet = require'octet'", 'result': '<IPython.core.display.HTML object>', 'mime': 'text/plain'}
    ]
    code_display_data = code_execute_result
    code_stderr = code_generate_error
    completion_samples = [{'text': 'oct', 'complete_reply': 'octet'}]

    def test_execute_stdout(self):
        if not self.code_hello_world:
            raise SkipTest

        self.flush_channels()
        reply, output_msgs = self.execute_helper(code=self.code_hello_world)
        self.assertEqual(reply['content']['status'], 'ok')
        self.assertGreaterEqual(len(output_msgs), 1)
        for msg in output_msgs:
            if (msg['msg_type'] == 'execute_result'):
                self.assertIn('hello, world', str(msg['content']['data']['text/plain']))
                break
        else:
            self.assertTrue(False, "Expected one output message of type 'execute_result' and 'content.name'='stdout'")


    def test_execute_result(self):
        if not self.code_execute_result:
            raise SkipTest

        for sample in self.code_execute_result:
            with self.subTest(code=sample['code']):
                self.flush_channels()
                reply, output_msgs = self.execute_helper(sample['code'])
                self.assertEqual(reply['content']['status'], 'ok')
                self.assertEqual(len(output_msgs), 1)
                self.assertEqual(output_msgs[0]['msg_type'], 'display_data')
                self.assertIn('text/plain', output_msgs[0]['content']['data'])
                self.assertEqual(output_msgs[0]['content']['data'][sample['mime']], sample['result'])

    def test_error(self):
        if not self.code_generate_error:
            raise SkipTest

        self.flush_channels()
        reply, output_msgs = self.execute_helper(self.code_generate_error)
        self.assertEqual('stderr', output_msgs[1]['content']['name'])
        self.assertGreaterEqual(len(output_msgs), 2)
        self.assertIn("[!]", output_msgs[1]['content']['text'])