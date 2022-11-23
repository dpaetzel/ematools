import re

import urllib
import click
import networkx as nx
import toolz
from tqdm import tqdm

from ematools import fetch_zettels


@click.command()
@click.option("--path", "-p", default="")
@click.option("--exclude", "-e", default=None)
@click.option("--engine", default="fdp")
def cli(path, exclude, engine):
    if exclude is None:
        exclude = f"^{r'.*/' * (path.count('/') + 1 + (not path.endswith('/')))}.*$"
    print(f"Using exclusion rule {exclude} …")

    print("Fetching Zettels …")
    zettels = fetch_zettels()

    pred = (
        lambda key: key.startswith(path) and not re.match(exclude, key) and
        # Always throw away archive.
        not re.match("/?Archive/", key))

    zettels = {key: zettels[key] for key in zettels if pred(key)}

    graph = nx.DiGraph()

    for zettel in tqdm(zettels, desc="Building graph"):
        graph.add_node(zettel, label=zettels[zettel]["title"])
        for link in zettels[zettel]["links"]:
            try:
                zettel2 = link["resolvedRelTarget"]["contents"].removesuffix(
                    ".html") + ".md"
                # Since resolvedRelTargets are URL encoded, we have to decode
                # them (e.g. spaces are %20).
                zettel2 = urllib.parse.unquote(zettel2)
            except KeyError:
                pass
            if pred(zettel2):
                graph.add_edge(zettel, zettel2)

    print("Marking unreachable notes …")
    degs = dict(graph.in_degree())
    unreachable_zettels = toolz.valfilter(lambda deg: deg == 0, degs).keys()
    graph.add_nodes_from(unreachable_zettels, color="red")

    print("Generating SVG …")
    agraph = nx.nx_agraph.to_agraph(graph)
    if engine == "all":
        for engine in [
                "dot", "neato", "fdp", "sfdp", "circo", "twopi", "nop", "osage"
        ]:
            # These are the best ones for this purpose I think.
            # for engine in ["fdp", "sfdp", "circo"]:
            agraph.draw(f"graph-{engine}.svg", prog=engine)
    else:
        agraph.draw(f"graph-{engine}.svg", prog=engine)


if __name__ == "__main__":
    cli()
