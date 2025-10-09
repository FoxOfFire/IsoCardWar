import rtree

class BBRTree:
    rt_index = rtree.index.Index

    def __init__(self) -> None:
        rt_props = rtree.index.Property(
            dimension=2,
            storage=rtree.index.RT_Memory,
        )
        self.__index = rtree.index.Index(properties=props, interleaved=False)
 


