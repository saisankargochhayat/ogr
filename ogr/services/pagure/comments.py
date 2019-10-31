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

import datetime
from typing import Optional

from ogr.abstract import IssueComment, PRComment


# TODO: Keep reference to (ogr's) Issue/PR


class PagureCommentParser:
    def _from_raw_comment(self, raw_comment: dict) -> None:
        self.comment = raw_comment["comment"]
        self.author = raw_comment["user"]["name"]
        self.created = self.__datetime_from_timestamp(raw_comment["date_created"])
        self.edited = self.__datetime_from_timestamp(raw_comment["edited_on"])

    @staticmethod
    def __datetime_from_timestamp(
        timestamp: Optional[str],
    ) -> Optional[datetime.datetime]:
        return datetime.datetime.fromtimestamp(int(timestamp)) if timestamp else None


class PagureIssueComment(PagureCommentParser, IssueComment):
    def __str__(self) -> str:
        return "Pagure" + super().__str__()


class PagurePRComment(PagureCommentParser, PRComment):
    def __str__(self) -> str:
        return "Pagure" + super().__str__()
