import os
from typing import Dict

from ....core.component import ProcessorComponent
from ....core.domain import Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import ProcessState, RequiresNoFinalisation
from wai.common.cli.options import TypedOption, FlagOption

from ....core.util.path import PathKey, path_to_str

PH_NAME = "{name}"
PH_EXT = "{ext}"
PH_OCCURRENCES = "{occurrences}"
PH_COUNT = "{count}"
PH_PDIR = "{[p]+dir}"
PH_PDIR_SUFFIX = "{pdir}"

PH_LIST = [
    PH_NAME,
    PH_EXT,
    PH_OCCURRENCES,
    PH_COUNT,
    PH_PDIR,
]

PH_HELP = {
    PH_NAME: "the name of the file, without path or extension.",
    PH_EXT: "the extension of the file (incl dot).",
    PH_OCCURRENCES: "the number of times this name (excl extension) has been encountered.",
    PH_COUNT: "the number of files encountered so far.",
    PH_PDIR: "the parent directory of the file: 'p': immediate parent, the more the p's the higher up in the hierarchy.",
}

PH_SAME = PH_NAME + PH_EXT


def _format_help() -> str:
    """
    Generates the help for the name format.

    :return: the generated help
    """
    result = "Available placeholders:\n"
    for ph in PH_LIST:
        result += "- %s: %s\n" % (ph, PH_HELP[ph])

    return result


class Rename(
    RequiresNoFinalisation,
    ProcessorComponent[Instance, Instance]
):
    """
    ISP that renames files using a user-supplied format.
    """

    name_format: str = TypedOption(
        "-f", "--name-format",
        type=str,
        default=PH_SAME,
        help="the format for the new name.\n%s" % _format_help()
    )

    verbose: bool = FlagOption(
        "--verbose",
        help="outputs information about generated names"
    )

    _count: int = ProcessState(lambda self: 0)

    _occurrences: Dict[str, int] = ProcessState(lambda self: {})

    def _parent_dir(self, path: str, pattern: str) -> str:
        """
        Returns the parent directory that corresponds to the pdir pattern.

        :param path: the directory path of the file
        :param pattern: the pdir pattern (without curly brackets)
        :return: the parent dir, empty string if failed to determine or too high
        """
        pattern = pattern.replace("dir", "")
        num = pattern.count("p")
        if num == 0:
            return ""
        orig_num = num
        orig_path = path
        pdir = os.path.basename(path)
        while (num > 1) and (len(path) > 0):
            path = os.path.dirname(path)
            pdir = os.path.basename(path)
            num -= 1
        if pdir == "":
            self.logger.warning("Number of parents (%d) is too high for path (%s) to generate a name!" % (orig_num, orig_path))
        return pdir

    def process_element(
            self,
            element: Instance,
            then: ThenFunction[Instance],
            done: DoneFunction
    ):
        # nothing to do?
        if self.name_format == PH_SAME:
            then(element)
            return

        path, name = os.path.split(path_to_str(element.key))
        name, ext = os.path.splitext(name)

        # increment counter
        self._count += 1

        # occurrences
        if name not in self._occurrences:
            self._occurrences[name] = 1
        else:
            self._occurrences[name] += 1

        # generate new name
        new_name = self.name_format
        new_name = new_name.replace(PH_NAME, name)
        new_name = new_name.replace(PH_EXT, ext)
        new_name = new_name.replace(PH_COUNT, str(self._count))
        new_name = new_name.replace(PH_OCCURRENCES, str(self._occurrences[name]))
        while PH_PDIR_SUFFIX in new_name:
            index = new_name.index(PH_PDIR_SUFFIX)
            start = new_name.rfind("{", 0, index)
            if start == -1:
                self.logger.error("Found '%s' without starting '{' in name format!" % PH_PDIR_SUFFIX)
                break
            pattern = new_name[start+1:index+4]
            pdir = self._parent_dir(path, pattern)
            if self.verbose:
                self.logger.info("Parent dir: %s -> %s" % (pattern, pdir))
            new_name = new_name.replace("{%s}" % pattern, pdir)

        if self.verbose:
            self.logger.info("Result: %s -> %s" % (name, new_name))

        new_element = type(element).from_parts(
            PathKey(os.path.join(path, new_name)),
            element.data,
            element.annotation
        )
        then(new_element)
