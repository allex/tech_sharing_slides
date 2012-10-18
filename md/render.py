#!/usr/bin/env python
# encoding: utf-8
# vim: set sw=2 et:

import sys
import os
import codecs
import re
import jinja2
import markdown

# print "Usage: {0} mdfile".format(sys.argv[0])

def process_slides():
  argv = sys.argv
  if len(argv) < 2:
    md_file = 'slides.md'
  else :
    md_file = argv[1]

  dist_filename = os.path.basename(md_file).split('.')[0]
  with codecs.open('../' + dist_filename + '.html', 'w', encoding='utf8') as outfile:
    md = codecs.open(md_file, encoding='utf8').read()
    md_slides = md.split('\n---\n')
    print len(md_slides)

    slides = []
    # Process each slide separately.
    for md_slide in md_slides:
      slide = {}
      sections = md_slide.split('\n\n')
      # Extract metadata at the beginning of the slide (look for key: value)
      # pairs.
      metadata_section = sections[0]
      metadata = parse_metadata(metadata_section)
      slide.update(metadata)

      if not slide.has_key('content'):
          remainder_index = metadata and 1 or 0
          # Get the content from the rest of the slide.
          content_section = '\n\n'.join(sections[remainder_index:])
          html = markdown.markdown(content_section)
          slide['content'] = postprocess_html(html, markdown)

      slides.append(slide)

    template = jinja2.Template(open('base.html').read())
    outfile.write(template.render(locals()))

def parse_metadata(section):
  """Given the first part of a slide, returns metadata associated with it."""
  metadata = {}
  metadata_lines = section.split('\n')
  for line in metadata_lines:
    colon_index = line.find(':')
    if colon_index != -1:
      key = line[:colon_index].strip()
      val = line[colon_index + 1:].strip()
      metadata[key] = val

  return metadata

def postprocess_html(html, metadata):
  """Returns processed HTML to fit into the slide template format."""
  return html

def isNotNull(value):
    return value is not None and len(value) > 0

if __name__ == '__main__':
  process_slides()
