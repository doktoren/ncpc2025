
Fix typing of segments in python/sprague_grundy.py:

```
def kayles_moves(segments: Hashable) -> Iterable[Hashable]:
    """
    Kayles (bowling pins):
    State: sorted tuple of segment lengths. A move removes 1 pin or 2 adjacent pins in one segment,
    thus splitting it into up to two new segments. Return new canonical (sorted) state.
    """
    assert isinstance(segments, tuple)
```

`class Point` in `python.convex_hull.py`: I think this could be simplified using a dataclass?