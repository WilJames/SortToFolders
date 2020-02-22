# -*- coding: utf-8 -*-

from PySide2.QtCore import (Signal, QThread, QTimer)
from sys import argv, path, platform
import re
import time
import json
import os

from pathlib import Path, PurePath
import shutil
import stat

_WINDOWS = os.name == 'nt'
posix = nt = None
if os.name == 'posix':
    import posix
elif _WINDOWS:
    import nt

COPY_BUFSIZE = 1024 * 1024 if _WINDOWS else 64 * 1024
_USE_CP_SENDFILE = hasattr(os, "sendfile") and platform.startswith("linux")
_HAS_FCOPYFILE = posix and hasattr(posix, "_fcopyfile")  # macOS


class Error(OSError):
    pass


class SameFileError(Error):
    """Raised when source and destination are the same file."""


class SpecialFileError(OSError):
    """Raised when trying to do a kind of operation (e.g. copying) which is
    not supported on a special file (e.g. a named pipe)"""


class _GiveupOnFastCopy(Exception):
    """Raised as a signal to fallback on using raw read()/write()
    file copy when fast-copy functions fail to do so.
    """


class MovingThread(QThread):
    setName = Signal(list)
    progress = Signal(dict)
    showWindowProgress = Signal()

    def __init__(self, parent=None):
        super(MovingThread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def st(self, dataTarget, data):
        if not self.isRunning():
            self.statusWork = True

            self.dataTarget = dataTarget
            self.data = data

            self.totalFiles = 0
            self.totalSize = 0

            self.count = 0
            self.totalCopied = 0

            self.start(QThread.NormalPriority)

    def run(self):
        targetFiles = [path for item in self.dataTarget for path in self.scandir(
            os.path.normpath(item['path']))]
        listFiles = self.listMoving(targetFiles, self.data)

        # print(listFiles)

        if (totalFiles:= len(listFiles)):
            self.totalFiles = totalFiles
            self.showWindowProgress.emit()
            self.moving(listFiles)

    def listMoving(self, targetFiles: list, listData: list) -> list:
        tempList = []
        toMovingList = []

        for item in listData:
            path = os.path.normpath(item['path'])
            ext = item['extension']
            if not ext:
                continue

            filesNames = [PurePath(x).name for x in self.scandir(path)]

            for itemTarget in targetFiles:
                nameTarget = PurePath(itemTarget).stem
                extTarget = PurePath(itemTarget).suffix
                fullName = PurePath(itemTarget).name

                if extTarget.lower() in ext:
                    size = os.path.getsize(itemTarget)
                    self.totalSize += size

                    if fullName in filesNames or fullName in tempList:
                        if not shutil._samefile(itemTarget, os.path.join(path, fullName)):
                            fullName = self.rename_files(
                                fullName, filesNames, tempList)

                    tempList.append(fullName)
                    toMovingList.append((itemTarget,
                                         os.path.join(path, fullName),
                                         PurePath(itemTarget).name, size)
                                        )

        return sorted(toMovingList, key=lambda x: x[3])

    def scandir(self, target: str) -> list:
        '''Возвращает список файлов без ярлыков, папок и файлов с точкой на UNIX
        '''
        with os.scandir(target) as it:
            if _WINDOWS:
                files = [os.fsdecode(entry.path) for entry in it if entry.is_file(
                ) and not entry.name.endswith('.lnk')]
            else:
                files = [os.fsdecode(entry.path) for entry in it if not entry.name.startswith(
                    '.') and entry.is_file() and not entry.is_symlink()]
        return files

    def rename_files(self, name_file: str, list_move_to_path: list, temp_list: list) -> str:
        '''Переименование файла
        '''
        count = 0
        filename, extension = os.path.splitext(name_file)
        delete = re.compile(fr"\s*\(\d+\){extension}$")

        while name_file in list_move_to_path or name_file in temp_list:
            if delete.search(name_file):
                count += 1
                name_file = delete.sub(f' ({count}){extension}', name_file)
            else:
                name_file = f'{filename} (1){extension}'

        return name_file

    def moving(self, list_to_moving: list):
        self.start_time = time.monotonic()
        time.sleep(0.1)
        for src, dst, name, file_size in list_to_moving:
            if self.statusWork:
                self.setName.emit([name, src, dst])
                # self.current_file_size = size

                real_dst = self.move(os.path.normcase(src), os.path.normcase(
                    dst), callback=self.copy_progress, total=file_size)
                if real_dst:
                    self.count += 1
            else:
                break

    # def humansize(self, nbytes):
    #     ''' Перевод байт в кб, мб и т.д.'''
    #     suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    #     i = 0
    #     while nbytes >= 1024 and i < len(suffixes) - 1:
    #         nbytes /= 1024.
    #         i += 1
    #     f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    #     return '%s %s' % (f, suffixes[i])

    def copy_progress(self, copied, current, total):
        self.totalCopied += current

        end_time = time.monotonic()
        time_elapsed = end_time - self.start_time

        speed = self.totalCopied / time_elapsed
        bytes_remain = self.totalSize - self.totalCopied
        time_remain = int(bytes_remain / speed)

        less_files = self.totalFiles - self.count
        less_size = self.totalSize - self.totalCopied

        # self.time_less_sec.emit(time_remain)

        self.progress.emit({'time_remain': time_remain,
                            'speed': speed,
                            'percent': int(100 * self.totalCopied / self.totalSize),
                            'less_files': less_files,
                            'less_size': less_size})

        # self.timeandspeed.emit([time_remain, f'{self.humansize(speed)}/s'])
        # self.progress.emit(int(100*self.totalCopied/self.totalSize))

        # print('\r' + f"{time_remain}, {self.humansize(speed)}/s, {int(100*self.totalCopied/self.totalSize)}", end='')

    def move(self, src, dst, callback, total):
        real_dst = dst
        try:
            os.rename(src, real_dst)
            callback(total, total, total=total)
        except OSError:
            self.copy2(src, real_dst)
            if not self.statusWork:
                src = real_dst
            try:
                os.unlink(src)
            except PermissionError:
                time.sleep(0.5)
                os.unlink(src)
        return real_dst

    def copy2(self, src, dst, *, follow_symlinks=True):
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        self.copyfile(src, dst, follow_symlinks=follow_symlinks)
        shutil.copystat(src, dst, follow_symlinks=follow_symlinks)
        return dst

    def copyfile(self, src, dst, *, follow_symlinks=True):
        if self._samefile(src, dst):
            raise SameFileError(
                "{!r} and {!r} are the same file".format(src, dst))

        file_size = 0
        for i, fn in enumerate([src, dst]):
            try:
                st = self._stat(fn)
            except OSError:
                pass
            else:
                if stat.S_ISFIFO(st.st_mode):
                    fn = fn.path if isinstance(fn, os.DirEntry) else fn
                    raise SpecialFileError("`%s` is a named pipe" % fn)
                if _WINDOWS and i == 0:
                    file_size = st.st_size

        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            if _HAS_FCOPYFILE:
                try:
                    shutil._fastcopy_fcopyfile(
                        fsrc, fdst, posix._COPYFILE_DATA)
                    return dst
                except _GiveupOnFastCopy:
                    pass
            # to do for Linux
            elif _USE_CP_SENDFILE:
                try:
                    # shutil._fastcopy_sendfile(fsrc, fdst)
                    self._fastcopy_sendfile(fsrc, fdst, callback=self.copy_progress, total=file_size)
                    return dst
                except _GiveupOnFastCopy:
                    pass
            elif _WINDOWS and file_size > 0:
                self._copyfileobj_readinto(fsrc, fdst, callback=self.copy_progress, total=file_size, length=min(
                    file_size, shutil.COPY_BUFSIZE))
                return dst

            self.copyfileobj(
                fsrc, fdst, callback=self.copy_progress, total=file_size)

        return dst

    def _fastcopy_sendfile(self, fsrc, fdst, callback, total):
        global _USE_CP_SENDFILE
        try:
            infd = fsrc.fileno()
            outfd = fdst.fileno()
        except Exception as err:
            raise _GiveupOnFastCopy(err)  # not a regular file
        try:
            blocksize = max(os.fstat(infd).st_size, 2 ** 23)  # min 8MiB
        except OSError:
            blocksize = 2 ** 27  # 128MiB
        if sys.maxsize < 2 ** 32:
            blocksize = min(blocksize, 2 ** 30)

        offset = 0
        while True:
            try:
                sent = os.sendfile(outfd, infd, offset, blocksize)
            except OSError as err:
                err.filename = fsrc.name
                err.filename2 = fdst.name

                if err.errno == errno.ENOTSOCK:
                    _USE_CP_SENDFILE = False
                    raise _GiveupOnFastCopy(err)

                if err.errno == errno.ENOSPC:  # filesystem is full
                    raise err from None

                if offset == 0 and os.lseek(outfd, 0, os.SEEK_CUR) == 0:
                    raise _GiveupOnFastCopy(err)

                raise err
            else:
                if sent == 0 or not self.statusWork:
                    break  # EOF
                offset += sent
                callback(offset, sent, total=total)

    def _copyfileobj_readinto(self, fsrc, fdst, callback, total, length=shutil.COPY_BUFSIZE):
        fsrc_readinto = fsrc.readinto
        fdst_write = fdst.write
        with memoryview(bytearray(length)) as mv:
            copied = 0
            while True:
                n = fsrc_readinto(mv)
                if not n or not self.statusWork:
                    break
                elif n < length:
                    with mv[:n] as smv:
                        fdst.write(smv)
                        copied += len(smv)
                        callback(copied, len(smv), total=total)
                else:
                    fdst_write(mv)
                    copied += len(mv)
                    callback(copied, len(mv), total=total)

    def copyfileobj(self, fsrc, fdst, callback, total, length=0):
        if not length:
            length = shutil.COPY_BUFSIZE
        fsrc_read = fsrc.read
        fdst_write = fdst.write
        copied = 0
        while True:
            buf = fsrc_read(length)
            if not buf or not self.statusWork:
                break
            fdst_write(buf)
            copied += len(buf)
            callback(copied, len(buf), total=total)

    def _samefile(self, src, dst):
        # Macintosh, Unix.
        if isinstance(src, os.DirEntry) and hasattr(os.path, 'samestat'):
            try:
                return os.path.samestat(src.stat(), os.stat(dst))
            except OSError:
                return False

        if hasattr(os.path, 'samefile'):
            try:
                return os.path.samefile(src, dst)
            except OSError:
                return False

        # All other platforms: check for same pathname.
        return (os.path.normcase(os.path.abspath(src)) ==
                os.path.normcase(os.path.abspath(dst)))

    def _stat(self, fn):
        return fn.stat() if isinstance(fn, os.DirEntry) else os.stat(fn)
