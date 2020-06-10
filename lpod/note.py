# -*- coding: UTF-8 -*-
#
# Copyright (c) 2009-2010 Ars Aperta, Itaapy, Pierlis, Talend.
#
# Authors: Hervé Cauwelier <herve@itaapy.com>
#          Romain Gauthier <romain@itaapy.com>
#          Jerome Dumonteil <jerome.dumonteil@itaapy.com>
#
# This file is part of Lpod (see: http://lpod-project.net).
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
from datetime import datetime
from types import FunctionType

# Import from lpod
from .element import odf_create_element, odf_element, register_element_class


def odf_create_note(note_class='footnote', note_id=None, citation=None,
                    body=None):
    """Create either a footnote or a endnote element with the given text,
    optionally referencing it using the given note_id.

    Arguments:

        note_class -- 'footnote' or 'endnote'

        note_id -- str

        citation -- unicode

        body -- unicode or odf_element

    Return: odf_element
    """
    data = ('<text:note>'
              '<text:note-citation/>'
              '<text:note-body/>'
            '</text:note>')
    element = odf_create_element(data)
    element.set_class(note_class)
    if note_id is not None:
        element.set_id(note_id)
    if citation is not None:
        element.set_citation(citation)
    if body is not None:
        element.set_body(body)
    return element



def get_unique_office_name(element=None):
    """Provide an autogenerated unique <office:name> for the document.
    """
    if element is not None:
        body = element.get_document_body()
    else:
        body = None
    if body:
        used = body.get_office_names()
    else:
        used = []
    # unplugged current paragraph:
    if element is not None:
        used.extend(element.get_office_names())
    i = 1
    while True:
        name = '__Fieldmark__lpod_%s' % i
        if name in used:
            i += 1
            continue
        break
    return name



def odf_create_annotation(text_or_element=None, creator=None, date=None,
                          name=None, parent=None):
    """Create an annotation element credited to the given creator with the
    given text, optionally dated (current date by default).
    If name not provided and some parent is provided, the name is autogenerated.

    Arguments:

        text -- unicode or odf_element

        creator -- unicode

        date -- datetime

        name -- unicode

        parent -- odf_element

    Return: odf_element
    """
    # fixme : use offset
    # TODO allow paragraph and text styles
    element = odf_create_element('office:annotation')
    element.set_body(text_or_element)
    if creator:
        element.set_dc_creator(creator)
    if date is None:
        date = datetime.now()
    element.set_dc_date(date)
    if not name:
        name = get_unique_office_name(parent)
        element.set_name(name)
    return element



def odf_create_annotation_end(annotation=None, name=None):
    """Create an annotation-end element. Either annotation or name must be
    provided to have proper reference for the annotation-end.

    Arguments:

        annotation -- odf_annotation element

        name -- unicode

    Return: odf_element
    """
    # fixme : use offset
    element = odf_create_element('office:annotation-end')
    if annotation:
        name = annotation.get_name()
    if not name:
        raise ValueError("Annotation-end must have a name")
    element.set_name(name)
    return element



class odf_note(odf_element):

    def get_class(self):
        return self.get_attribute('text:note-class')


    def set_class(self, note_class):
        return self.set_attribute('text:note-class', note_class)


    def get_id(self):
        return self.get_attribute('text:id')


    def set_id(self, note_id, *args, **kw):
        if type(note_id) is FunctionType:
            note_id = note_id(*args, **kw)
        return self.set_attribute('text:id', note_id)


    def get_citation(self):
        note_citation = self.get_element('text:note-citation')
        return note_citation.get_text()


    def set_citation(self, text):
        note_citation = self.get_element('text:note-citation')
        note_citation.set_text(text)


    def get_body(self):
        # XXX conflict with element.get_body
        note_body = self.get_element('text:note-body')
        return note_body.get_text_content()


    def set_body(self, text_or_element):
        note_body = self.get_element('text:note-body')
        if type(text_or_element) is str:
            note_body.set_text_content(text_or_element)
        elif isinstance(text_or_element, odf_element):
            note_body.clear()
            note_body.append(text_or_element)
        else:
            raise ValueError('Unexpected type for body: "%s"' % type(
                    text_or_element))


    def check_validity(self):
        if not self.get_class():
            raise ValueError('note class must be "footnote" or "endnote"')
        if not self.get_id():
            raise ValueError("notes must have an id")
        if not self.get_citation():
            raise ValueError("notes must have a citation")
        if not self.get_body():
            # XXX error?
            pass



class odf_annotation(odf_element):

    def get_body(self):
        return self.get_text_content()


    def set_body(self, text_or_element):
        if type(text_or_element) is str:
            self.set_text_content(text_or_element)
        elif isinstance(text_or_element, odf_element):
            self.clear()
            self.append(text_or_element)
        else:
            raise TypeError('expected unicode or odf_element')


    def get_name(self):
        return self.get_attribute('office:name')


    def set_name(self, name):
        return self.set_attribute('office:name', name)


    def get_start(self):
        """Return self.
        """
        return self


    def get_end(self):
        """Return the corresponding annotation-end tag or None.
        """
        name = self.get_name()
        parent = self.get_parent()
        if parent is None:
            raise ValueError("Can not find end tag: no parent available.")
        body = self.get_document_body()
        if not body:
            body = parent
        return body.get_annotation_end(name=name)


    def get_annotated(self, as_text=False, no_header=True, clean=True):
        """Returns the annotated content from an annotation.

        If no content exists (single position annotation or annotation-end not
        found), returns [] (or u'' if text flag is True).
        If as_text is True: returns the text content.
        If clean is True: suppress unwanted tags (deletions marks, ...)
        If no_header is True: existing text:h are changed in text:p
        By default: returns a list of odf_element, cleaned and without headers.

        Arguments:

            as_text -- boolean

            clean -- boolean

            no_header -- boolean

        Return: list or odf_element or text
        """
        end = self.get_end()
        if end is None:
            if as_text:
                return ''
            return None
        body = self.get_document_body()
        if not body:
            body = self.get_root()
        return body.get_between(self, end, as_text=as_text,
                                no_header=no_header, clean=clean)


    def delete(self, child=None):
        """Delete the given element from the XML tree. If no element is given,
        "self" is deleted. The XML library may allow to continue to use an
        element now "orphan" as long as you have a reference to it.

        For odf_annotation : delete the annotation-end tag if exists.

        Arguments:

            child -- odf_element
        """
        if child is not None:  # act like normal delete
            return super(odf_annotation, self).delete(child)
        end = self.get_end()
        if end:
            end.delete()
        # act like normal delete
        return super(odf_annotation, self).delete()


    #
    # Shortcuts expected to be reusable over several elements
    #

    def check_validity(self):
        if not self.get_body():
            raise ValueError("annotation must have a body")
        if not self.get_dc_creator():
            raise ValueError("annotation must have a creator")
        if not self.get_dc_date():
            self.set_dc_date(datetime.now())



class odf_annotation_end(odf_element):
    """The <office:annotation-end> element may be used to define the end of a
    text range of document content that spans element boundaries. In that case,
    an <office:annotation> element shall precede the <office:annotation-end>
    element. Both elements shall have the same value for their office:name
    attribute. The <office:annotation-end> element shall be preceded by an
    <office:annotation> element that has the same value for its office:name
    attribute as the <office:annotation-end> element. An <office:annotation-end>
    element without a preceding <office:annotation> element that has the same
    name assigned is ignored.
    """
    def get_name(self):
        return self.get_attribute('office:name')


    def set_name(self, name):
        return self.set_attribute('office:name', name)


    def get_start(self):
        """Return the corresponding annotation starting tag or None.
        """
        name = self.get_name()
        if parent is None:
            raise ValueError("Can not find start tag: no parent available.")
        body = self.get_document_body()
        if not body:
            body = parent
        return body.get_annotation(name=name)


    def get_end(self):
        """Return self.
        """
        return self



register_element_class('text:note', odf_note)
register_element_class('office:annotation', odf_annotation)
register_element_class('office:annotation-end', odf_annotation_end)
