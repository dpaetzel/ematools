# Script to create an SVG graph of parts of your emanote Zettelkasten.
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

# TODO Consider using https://click.palletsprojects.com/en/8.1.x/setuptools/
import re

import urllib
import click
import networkx as nx
import toolz
from tqdm import tqdm

from ematools import fetch_zettels


@click.command()
@click.option(
    "--path", "-p", default="", help="Only Zettels with this prefix are included"
)
@click.option(
    "--exclude",
    "-e",
    default=None,
    help="Regular expression, Zettels matching this are excluded",
)
@click.option("--engine", default="fdp", help="Graphviz layout engine to use")
@click.option(
    "--include-edge-zettels/--exclude-edge-zettels",
    default=False,
    help=(
        "Whether to include excluded Zettels that are linked by included "
        "Zettels (if this is on, they are marked in blue)"
    ),
)
def cli(path, exclude, engine, include_edge_zettels):
    if exclude is None:
        exclude = f"^{r'.*/' * (path.count('/') + 1 + (not path.endswith('/')))}.*$"
    print(f"Using exclusion rule {exclude} …")

    print("Fetching Zettels …")
    zettels = fetch_zettels()

    pred = (
        lambda key: key.startswith(path)
        and not re.match(exclude, key)
        and
        # Always throw away archive.
        not re.match("/?Archive/", key)
    )

    zettels_filtered = {key: zettels[key] for key in zettels if pred(key)}

    graph = nx.DiGraph()

    for zettel in tqdm(zettels_filtered, desc="Building graph"):
        graph.add_node(zettel, label=zettels[zettel]["title"])
        for link in zettels[zettel]["links"]:
            try:
                zettel2 = (
                    link["resolvedRelTarget"]["contents"].removesuffix(".html") + ".md"
                )
                # Since resolvedRelTargets are URL encoded, we have to decode
                # them (e.g. spaces are %20).
                zettel2 = urllib.parse.unquote(zettel2)
            except KeyError:
                pass
            # If `zettel2` is also not a discarded Zettel, always add an edge.
            if zettel2 in zettels_filtered:
                graph.add_edge(zettel, zettel2)
            # … otherwise, only add an edge if we opetd to include edges to filtered Zettels.
            elif include_edge_zettels:
                graph.add_node(zettel2, color="blue", label=zettels[zettel2]["title"])
                graph.add_edge(zettel, zettel2)

    print("Marking unreachable notes …")
    degs = dict(graph.in_degree())
    unreachable_zettels = toolz.valfilter(lambda deg: deg == 0, degs).keys()
    graph.add_nodes_from(unreachable_zettels, color="red")

    print("Generating SVG …")
    agraph = nx.nx_agraph.to_agraph(graph)
    if engine == "all":
        for engine in ["dot", "neato", "fdp", "sfdp", "circo", "twopi", "nop", "osage"]:
            # These are the best ones for this purpose I think.
            # for engine in ["fdp", "sfdp", "circo"]:
            agraph.draw(f"graph-{engine}.svg", prog=engine)
    else:
        agraph.draw(f"graph-{engine}.svg", prog=engine)


if __name__ == "__main__":
    cli()
