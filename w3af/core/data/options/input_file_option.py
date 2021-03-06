"""
file_option.py

Copyright 2008 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import os

from w3af import ROOT_PATH
from w3af.core.controllers.exceptions import BaseFrameworkException
from w3af.core.data.options.baseoption import BaseOption
from w3af.core.data.options.option_types import INPUT_FILE

ROOT_PATH_VAR = '%ROOT_PATH%'


class InputFileOption(BaseOption):

    _type = INPUT_FILE

    def set_value(self, value):
        """
        :param value: The value parameter is set by the user interface, which
        for example sends "w3af/plugins/audit/ssl_certificate/ca.pem" or
        "%ROOT_PATH%/plugins/audit/ssl_certificate/ca.pem".

        If required we replace the %ROOT_PATH% with the right value for this
        platform.
        """
        if value == '':
            self._value = value
            return

        validated_value = self.validate(value)

        # I want to make the paths shorter, so we're going to make them
        # relative, at least in the case where they are inside the cwd
        current_dir = os.path.abspath(os.curdir)
        configured_value_dir = os.path.abspath(os.path.dirname(value))
        if configured_value_dir.startswith(current_dir):
            self._value = os.path.relpath(validated_value)
        else:
            self._value = validated_value

    def get_value_for_profile(self):
        """
        This method is called before saving the option value to the profile file

        Added when fixing:
            https://github.com/andresriancho/w3af/issues/402

        :return: A string representation of the path, with the ROOT_PATH
                 replaced with %ROOT_PATH%. Then when we load a value in
                 set_value we're going to replace the %ROOT_PATH% with ROOT_PATH
        """
        abs_path = os.path.abspath(self._value)
        replaced_value = abs_path.replace(ROOT_PATH, ROOT_PATH_VAR)
        return replaced_value

    def validate(self, value):

        value = value.replace(ROOT_PATH_VAR, ROOT_PATH)

        directory = os.path.abspath(os.path.dirname(value))
        if not os.path.isdir(directory):
            msg = 'Invalid input file option value "%s", the directory does'\
                  ' not exist.'
            raise BaseFrameworkException(msg % value)

        if not os.access(directory, os.R_OK):
            msg = 'Invalid input file option value "%s", the user doesn\'t have' \
                  ' enough permissions to read from the specified directory.'
            raise BaseFrameworkException(msg % value)

        if not os.path.exists(value):
            msg = 'Invalid input file option value "%s", the specified file' \
                  ' does not exist.'
            raise BaseFrameworkException(msg % value)

        if not os.access(value, os.R_OK):
            msg = 'Invalid input file option value "%s", the user doesn\'t have' \
                  ' enough permissions to read the specified file.'
            raise BaseFrameworkException(msg % value)

        if not os.path.isfile(value):
            msg = 'Invalid input file option value "%s", the path doesn\'t' \
                  ' point to a file.'
            raise BaseFrameworkException(msg % value)

        return value
