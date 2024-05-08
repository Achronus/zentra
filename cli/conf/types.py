from typing import Callable


# (library_name, filename)
LibraryNamePairs = list[tuple[str, str]]

# Used exclusively in 'printables.py'
# (list[items_to_add], list[items_to_remove])
GenerateDataTuple = tuple[list[str], list[str]]

MappingDict = dict[str, Callable]
