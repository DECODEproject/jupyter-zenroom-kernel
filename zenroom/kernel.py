import json
import os
import subprocess
import sys

import uuid
from IPython.core.display import HTML, JSON
from metakernel import MetaKernel
from pexpect import which



class ZenroomKernel(MetaKernel):
    implementation = 'zenroom'
    implementation_version = '0.5.0'
    language = 'lua'
    language_version = '5.3'
    banner = 'Zenroom a Small, secure and portable virtual machine for crypto language processing, part DECODE project'
    language_info = {
        'mimetype': 'text/x-lua',
        'name': 'lua',
        'codemirror_mode': { "name": "text/x-lua" },
        'pygments_lexer': 'lua',
        'file_extension': '.lua',
    }
    kernel_json = dict(
        argv=[sys.executable,
              '-m', 'zenroom',
              '-f', '{connection_file}'],
        display_name='Zenroom',
        language='zenroom',
        codemirror_mode='lua',
        name='zenroom'
    )

    def get_usage(self):
        return 'This is the Zenroom kernel implementation look at zenroom.dyne.org for more information'

    def do_execute_direct(self, code, silent=False):
        if silent:
            return

        cmd = [self._find_best_executable()]
        p = subprocess.run(cmd, input=code, capture_output=True, encoding='utf-8')
        stderr = p.stderr.split('\n')[:-3]
        self.Display(self._clean_errors())

        if stderr:
            error = [__ for __ in stderr if '[!]' in __]
            if not error:
                return self._display_json(p.stdout)
            self.Error(error[0])
            line = int(error[0].split(":")[1]) - 1
            self.Display(self._highlight_errorline(line))

    def get_help_on(self, expr, level=0, none_on_fail=False, cursor_pos=-1):
        self.log(expr)

    @staticmethod
    def _find_best_executable():
        executable = os.environ.get('ZENROOM_BIN', None)
        if not executable or not which(executable):
            if which('zenroom-shared'):
                executable = 'zenroom-shared'
            elif which('zenroom-static'):
                executable = 'zenroom-static'
            else:
                msg = ('zenroom executable not found, please add to path or set'
                       '"ZENROOM_BIN" environment variable')
                raise OSError(msg)
            executable = executable.replace(os.path.sep, '/')
        return executable

    def _display_json(self, output):
        _uuid = str(uuid.uuid4())
        try:
            json_output = json.dumps(json.loads(output))
            self.log.warn(json_output)
            self.log.warn(_uuid)
            self.Display(HTML('''
                <div id="%s" style="width:100%%;"></div>
                <script>
                require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
                   document.getElementById('%s').appendChild(renderjson(%s))
                });
                </script>
            ''' % (_uuid, _uuid, json_output)))
        except Exception as e:
            self.log.error(e)
            return output

    def _clean_errors(self):
        return HTML("""
            <script>
                Jupyter.notebook.select_prev();
                var cell = Jupyter.notebook.get_selected_cell();
                cell.code_mirror.eachLine(function(line) {
                    cell.code_mirror.removeLineClass(line, 'background')
                })
                Jupyter.notebook.select_next();
            </script>
        """)

    def _highlight_errorline(self, line):
        return HTML("""
            <style type="text/css">.line-error{background-color:#ff7;}</style>
            <script>
                Jupyter.notebook.select_prev()
                var cell = Jupyter.notebook.get_selected_cell();
                cell.code_mirror.addLineClass(%s, 'background', 'line-error');
                cell.show_line_numbers(1)
                Jupyter.notebook.select_next()
            </script>
            """ % line)