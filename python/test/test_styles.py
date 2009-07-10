# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Itaapy, ArsAperta, Pierlis, Talend

# Import from the Standard Library
from unittest import TestCase, main

# Import from lpod
from lpod.document import odf_get_document, odf_create_style
from lpod.document import odf_create_style_text_properties
from lpod.styles import hex2rgb, rgb2hex
from lpod.xmlpart import LAST_CHILD


class Hex2RgbTestCase(TestCase):

    def test_color_low(self):
        color = '#012345'
        expected = (1, 35, 69)
        self.assertEqual(hex2rgb(color), expected)


    def test_color_high(self):
        color = '#ABCDEF'
        expected = (171, 205, 239)
        self.assertEqual(hex2rgb(color), expected)


    def test_color_lowercase(self):
        color = '#abcdef'
        expected = (171, 205, 239)
        self.assertEqual(hex2rgb(color), expected)


    def test_color_bad_size(self):
        color = '#fff'
        self.assertRaises(ValueError, hex2rgb, color)


    def test_color_bad_format(self):
        color = '978EAE'
        self.assertRaises(ValueError, hex2rgb, color)


    def test_color_bad_hex(self):
        color = '#978EAZ'
        self.assertRaises(ValueError, hex2rgb, color)



class Rgb2HexTestCase(TestCase):

    def test_color_name(self):
        color = 'violet'
        expected = '#EE82EE'
        self.assertEqual(rgb2hex(color), expected)


    def test_color_tuple(self):
        color = (171, 205, 239)
        expected = '#ABCDEF'
        self.assertEqual(rgb2hex(color), expected)


    def test_color_bad_name(self):
        color = 'dark white'
        self.assertRaises(KeyError, rgb2hex, color)


    def test_color_bad_tuple(self):
        # For alpha channel? ;-)
        color = (171, 205, 238, 128)
        self.assertRaises(ValueError, rgb2hex, color)


    def test_color_bad_low_channel(self):
        color = (171, 205, -1)
        self.assertRaises(ValueError, rgb2hex, color)


    def test_color_bad_high_channel(self):
        color = (171, 205, 256)
        self.assertRaises(ValueError, rgb2hex, color)


    def test_color_bad_value(self):
        color = {}
        self.assertRaises(TypeError, rgb2hex, color)



class TestStyle(TestCase):

    def setUp(self):
        self.document = document = odf_get_document('samples/example.odt')
        self.styles = document.get_xmlpart('styles')


    def tearDown(self):
        del self.styles
        del self.document


    def test_create_style(self):
        style = odf_create_style('style1', 'paragraph')
        expected = ('<style:style style:name="style1" '
                      'style:family="paragraph"/>')
        self.assertEqual(style.serialize(), expected)


    def test_create_properties(self):
        properties = odf_create_style_text_properties()
        properties.set_attribute('fo:color', '#0000ff')
        properties.set_attribute('fo:background-color', '#ff0000')
        expected = ('<style:text-properties fo:color="#0000ff" '
                      'fo:background-color="#ff0000"/>')
        self.assertEqual(properties.serialize(), expected)


    def test_get_style_list(self):
        styles = self.styles
        style_list = styles.get_style_list()
        # XXX default style, outline style, page layout and master page are
        # not counted
        self.assertEqual(len(style_list), 9)


    def test_get_style_list_family(self):
        styles = self.styles
        style_list = styles.get_style_list(family='paragraph')
        # XXX default style is not counted
        self.assertEqual(len(style_list), 9)


    def test_get_style_automatic(self):
        styles = self.styles
        style = styles.get_style('Mpm1', 'page-layout')
        # XXX page layout is not found
        self.assertNotEqual(style, None)


    def test_get_style_named(self):
        styles = self.styles
        style = styles.get_style('Heading_20_1', 'paragraph')
        self.assertNotEqual(style, None)


    def test_insert_style(self):
        styles = self.styles
        clone = styles.clone()
        style = odf_create_style('style1', 'paragraph')
        properties = odf_create_style_text_properties()
        properties.set_attribute('fo:color', '#0000ff')
        properties.set_attribute('fo:background-color', '#ff0000')
        style.insert_element(properties, LAST_CHILD)
        context = clone.get_category_context('named')
        context.insert_element(style, LAST_CHILD)

        expected = ('<style:style style:name="style1" '
                                 'style:family="paragraph">'
                      '<style:text-properties fo:color="#0000ff" '
                                             'fo:background-color="#ff0000"/>'
                    '</style:style>')
        get1 = clone.get_style('style1', 'paragraph')
        self.assertEqual(get1.serialize(), expected)



if __name__ == '__main__':
    main()