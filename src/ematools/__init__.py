# Simple Python library to interact with emanote.
#
# Copyright (C) 2024 David Pätzel <david.paetzel@posteo.de>
#
# This file is part of ematools.
#
# ematools is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# ematools is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# ematools. If not, see <https://www.gnu.org/licenses/>.

import requests


def fetch_zettels():
    url = "http://127.0.0.1:8000/-/export.json"
    resp = requests.get(url=url)
    zettels = resp.json()

    # Throw away Zettelkasten metadata.
    zettels = zettels["files"]

    return zettels
