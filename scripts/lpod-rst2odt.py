#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2009 Ars Aperta, Itaapy, Pierlis, Talend.
#
# Authors: David Versmisse <david.versmisse@itaapy.com>
#
# This file is part of Lpod (see: http://lpod-project.org).
# Lpod is free software; you can redistribute it and/or modify it under
# the terms of either:
#
# a) the GNU General Public License as published by the Free Software
#    Foundation, either version 3 of the License, or (at your option)
#    any later version.
#    Lpod is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with Lpod.  If not, see <http://www.gnu.org/licenses/>.
#
# b) the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#

# Import from the Standard Library
from optparse import OptionParser
from sys import exit

# Import from lpod
from lpod import __version__
from lpod.document import odf_get_document
from lpod.rst2odt import rst2odt
from lpod.scriptutils import add_option_output, StdoutWriter



if  __name__ == "__main__":
    # Options initialisation
    usage = "%prog [-o output] <filename>"
    description = "Convert a rst file into an odt file"
    parser = OptionParser(usage, version=__version__,
            description=description)

    # --styles
    help = "import the styles from the given file"
    parser.add_option("-s", "--styles", dest="styles_from", metavar="FILE",
            help=help)
    # --output
    add_option_output(parser)

    # Parse !
    options, args = parser.parse_args()

    # Source
    if len(args) != 1:
        parser.print_help()
        exit(1)
    source = args[0]

    # Template
    template = None
    if options.styles_from:
        template = odf_get_document(options.styles_from)

    # Convert
    document = rst2odt(open(source).read(), template=template)

    # Save
    target = options.output
    if target is None:
        target = StdoutWriter()
    document.save(target=target)
