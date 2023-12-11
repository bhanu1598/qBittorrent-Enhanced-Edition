#VERSION: 1.23

# Author:
#  Christophe DUMEZ (chris@qbittorrent.org)

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the author nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import glob
import importlib
import os
import pathlib
import sys

# qbt tend to run this script in 'isolate mode' so append the current path manually
current_path = str(pathlib.Path(__file__).parent.resolve())
if current_path not in sys.path:
    sys.path.append(current_path)

from helpers import download_file

supported_engines = dict()

engines = glob.glob(os.path.join(os.path.dirname(__file__), 'engines', '*.py'))
for engine in engines:
    e = engine.split(os.sep)[-1][:-3]
    if len(e.strip()) == 0:
        continue
    if e.startswith('_'):
        continue
    try:
        module = importlib.import_module("engines." + e)
        engine_class = getattr(module, e)
        globals()[e] = engine_class
        engine_url = getattr(engine_class, 'url')
        supported_engines[engine_url] = e
    except Exception:
        pass

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SystemExit('./nova2dl.py engine_url download_parameter')
    engine_url = sys.argv[1].strip()
    download_param = sys.argv[2].strip()
    if engine_url not in supported_engines.keys():
        raise SystemExit('./nova2dl.py: this engine_url was not recognized')
    engine = globals()[supported_engines[engine_url]]()
    if hasattr(engine, 'download_torrent'):
        engine.download_torrent(download_param)
    else:
        print(download_file(download_param))
    sys.exit(0)
