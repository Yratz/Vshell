import zipfile
from abc import ABC, abstractmethod
from typing import List
import stat


class Command(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(
            self, archive: zipfile.ZipFile, path: zipfile.Path
    ) -> zipfile.Path:
        pass


class PWDCommand(Command):
    def __init__(self):
        super().__init__()

    def run(
            self, archive: zipfile.ZipFile, path: zipfile.Path
    ) -> zipfile.Path:
        print(path.at)
        return path


class LSCommand(Command):
    def __init__(self):
        super().__init__()

    def _get_file_representation(
            self, path: zipfile.Path, info: zipfile.ZipInfo
    ) -> List[str]:
        line = []

        # print modifiers
        hi = info.external_attr >> 16
        line.append('%r' % stat.filemode(hi))

        # print size
        line.append(f"{info.file_size}")

        # print datetime
        line.append(
            f"{info.date_time[0]}-{info.date_time[1]}-{info.date_time[2]}T"
            f"{info.date_time[3]}::{info.date_time[4]}"
        )

        # print name
        line.append(path.name)

        return line

    def run(
            self, archive: zipfile.ZipFile, path: zipfile.Path
    ) -> zipfile.Path:
        files_info = {info.filename: info for info in archive.infolist()}
        representations = []
        for file in path.iterdir():
            info = files_info[file.at]
            representations.append(
                self._get_file_representation(file, info)
            )

        if len(representations) > 0:
            representation_size = len(representations[0])
            lengths = [
                max([len(x[i]) for x in representations])
                for i in range(representation_size)
            ]

            aligned_representations = [
                [f"{x[i]:<{length}}" for i, length in enumerate(lengths)]
                for x in representations
            ]

            for align_representation in aligned_representations:
                print(' '.join(align_representation))

        return path


class CDCommand(Command):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    def run(
            self, archive: zipfile.ZipFile, path: zipfile.Path
    ) -> zipfile.Path:
        if self.filename == ".":
            return path
        elif self.filename == "..":
            return path.parent
        else:
            new_path = path.joinpath(self.filename)
            if new_path.exists() and new_path.is_dir():
                return new_path
            else:
                print(f"This path doesn't exist "
                      f"or is not a folder: {self.filename}")

                return path


class CATCommand(Command):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    def run(
            self, archive: zipfile.ZipFile, path: zipfile.Path
    ) -> zipfile.Path:
        file = path.joinpath(self.filename)
        if file.exists() and file.is_file():
            try:
                print(file.read_text())
            except UnicodeError:
                print(f"This is a byte-file and can't "
                      f"be read as a text: {self.filename}")
        else:
            print(f"This path does not exist "
                  f"or it is not a file: {self.filename}")

        return path
