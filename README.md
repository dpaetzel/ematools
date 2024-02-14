# ematools


Python scripts that interface with [Emanote](https://github.com/srid/emanote).


For now, only `graphs.py` is provided which allows you to draw (ugly) link
graphs of parts of your Zettelkasten.


## Usage


Assuming you're running `emanote run -p 8000` in the provided example `Zettels`
directory (or in your own Emanote directory, see the [Emanote
docs](https://emanote.srid.ca/)) or. Note that an Emanote server URL of
`localhost:8000` is currently hard coded.


You can then run

```
PYTHONPATH=src:$PYTHONPATH python graph.py --path "" --engine fdp
```

which generates the graph of all Zettels in your top-level Zettel directory
which looks something like (see the generated SVG file)

![[Example.svg]]


Note that isolated Zettels that are not linked to by any other Zettel have a red
border.


You can also inspect a partial graph only (relevant if your Zettelkasten is
large) by restricting set of Zettels from which links are considered to
a subdirectory by setting the path to something different than `""`, e.g.

```
PYTHONPATH=src:$PYTHONPATH python graph.py --path "2" --engine fdp
```

which generates a graph from the top-level Zettel which looks something like
(see the generated SVG file)

![[Example2.svg]]



## Restrictions


Obsidian-style query results are (as of 2023) not included in the JSON export of
Emanote. This means only hard-coded links are included in the graph.
