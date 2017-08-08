from urllib import parse

from django.db import models
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.utils._os import safe_join, abspathu
from django.core.files import locks, File
import os
from django.core.files.move import file_move_safe
import errno
from django.conf import settings
from django.utils.encoding import filepath_to_uri


@deconstructible
class EEStorage(Storage):

    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.MEDIA_ROOT
        self.base_location = location
        self.location = abspathu(self.base_location)
        if base_url is None:
            base_url = settings.MEDIA_URL
        self.base_url = base_url

    def __eq__(self, other):
        return self == other

    def _open(self, name, mode='rb'):
       return File(open(self.path(name), mode))

    def path(self, name):
        try:
            path = safe_join(self.location, name)
        except ValueError:
            raise print("Attempted access to '%s' denied." % name)
        return os.path.normpath(path)

    def exists(self, name):
        return os.path.exists(self.path(name))

    def _save(self, name, content):
        full_path = self.path(name)
        directory = os.path.dirname(full_path)
        print(directory, full_path, '----------save_method')
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        if not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)

        while True:
            try:
                # This file has a file path that we can move.
                if hasattr(content, 'temporary_file_path'):
                    print(content.temporary_file_path(), full_path, '-----temp_method')
                    file_move_safe(content.temporary_file_path(), full_path)
                    content.close()

                else:
                    flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                             getattr(os, 'O_BINARY', 0))
                    fd = os.open(full_path, flags, 0o666)
                    try:
                        locks.lock(fd, locks.LOCK_EX)
                        _file = None
                        for chunk in content.chunks():
                            if _file is None:
                                mode = 'wb' if isinstance(chunk, bytes) else 'wt'
                                _file = os.fdopen(fd, mode)
                            _file.write(chunk)
                    finally:
                        locks.unlock(fd)
                        if _file is not None:
                            _file.close()
                        else:
                            os.close(fd)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    # Ooops, the file exists. We need a new file name.
                    name = self.get_available_name(name)
                    full_path = self.path(name)
                else:
                    raise
            else:
                break

        if settings.FILE_UPLOAD_PERMISSIONS is not None:
            os.chmod(full_path, settings.FILE_UPLOAD_PERMISSIONS)

        return name

    def delete(self, name):
        name = self.path(name)
        if os.path.exists(name):
            try:
                os.remove(name)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return parse.urljoin(self.base_url, filepath_to_uri(name))






class CustomFile(models.Model):
    file = models.FileField('custom', upload_to='user_media', storage=EEStorage())

    def __str__(self):
        return self.file.name


class Second(models.Model):
    file = models.FileField('new', upload_to='new_dict')


class StandardFile(models.Model):
    file = models.FileField('standard')
