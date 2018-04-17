import json
import os
import subprocess
import sys

import uuid
from IPython.core.display import HTML
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
        'codemirror_mode': {"name": "text/x-lua"},
        'pygments_lexer': 'lua',
        'file_extension': '.lua',
        'version': '5.3',
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
    zenroom_modules = ['octet', 'ecdh', 'data', 'math', 'string', 'table']

    def get_usage(self):
        return 'This is the Zenroom kernel implementation look at zenroom.dyne.org for more information'

    def do_execute_direct(self, code, silent=False):
        if silent:
            return
        cmd = [self._find_best_executable()]
        p = subprocess.run(cmd,
                           input=code,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding='utf-8', universal_newlines=True)
        stderr = p.stderr.split('\n')[:-3]
        self.Display(self._clean_errors())

        if stderr:
            error = [__ for __ in stderr if '[!]' in __]
            if not error:
                return self._display_json(p.stdout)
            self.Error(error[0])
            line = int(error[0].split(":")[1]) - 1
            self.Display(self._highlight_errorline(line))

    def get_kernel_help_on(self, info, level=0, none_on_fail=False):
        expr = info["full_obj"]
        self.last_info = info
        url = None
        if expr in self.zenroom_modules:
            url = "https://zenroom.dyne.org/api/modules/%s.html" % expr

        if url:
            try:
                import html2text
                import urllib
                try:
                    html = str(urllib.request.urlopen(url).read(), encoding="utf-8")
                except:
                    html = str(urllib.urlopen(url).read())
            except:
                return url
            visible_text = html2text.html2text(html)
            return visible_text
        elif none_on_fail:
            return None
        else:
            return "Sorry, no available help for '%s'" % expr

    def get_completions(self, info):
        token = info["full_obj"]
        self.last_info = info
        return [command for command in set(self.zenroom_modules) if command.startswith(token)]

    @staticmethod
    def _find_best_executable():
        executable = os.environ.get('ZENROOM_BIN', None)
        if not executable or not which(executable):
            if which('zenroom-shared'):
                executable = 'zenroom-shared'
            elif which('zenroom-static'):
                executable = 'zenroom-static'
            else:
                msg = ('Zenroom executable not found, please add it to path or set'
                       ' "ZENROOM_BIN" environment variable')
                raise OSError(msg)
            executable = executable.replace(os.path.sep, '/')
        return executable

    def _display_json(self, output):
        _uuid = str(uuid.uuid4())
        try:
            json_output = json.dumps(json.loads(output))
            self.Display(HTML('''
                <div id="%s" style="width:100%%;"></div>
                <script>
                require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
                   document.getElementById('%s').appendChild(renderjson(%s))
                });
                </script>
            ''' % (_uuid, _uuid, json_output)))
        except:
            return output if output else None

    @staticmethod
    def _clean_errors():
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

    @staticmethod
    def _highlight_errorline(line):
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
