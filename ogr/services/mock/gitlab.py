# MIT License
#
# Copyright (c) 2018-2019 Red Hat, Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import gitlab

from ogr.persistent_storage import use_persistent_storage_without_overwriting
from ogr.utils import RequestResponse


@use_persistent_storage_without_overwriting
class BetterGitlab(gitlab.Gitlab):
    def http_request(self, *args, **kwargs):
        keys_internal = list(args) + [kwargs.items()]
        if self.persistent_storage.is_write_mode:
            raw_response = super().http_request(*args, **kwargs)

            try:
                json_output = raw_response.json()
            except ValueError:
                json_output = None

            output = RequestResponse(
                status_code=raw_response.status_code,
                ok=raw_response.ok,
                content=raw_response.content,
                json=json_output,
                reason=raw_response.reason,
                headers=raw_response.headers,
                links=raw_response.links,
            )
            self.persistent_storage.store(
                keys=keys_internal, values=output.to_json_format()
            )
        else:
            output_dict = self.persistent_storage.read(keys=keys_internal)
            output = RequestResponse(**output_dict)
        return output
