#!/usr/bin/env python
import os
import re
import codecs

template = u"""
{{% extends 'base.html' %}}

{{% block content %}}
<h1> Arxiu del blog </h1>
 {0}
{{% endblock %}}
"""

LINKS = []

for root, _, files in os.walk('app/src/templates/posts/'):
    for name in files:
        filename = os.path.join(root, name)
        with codecs.open(filename, 'r', 'utf-8') as f:
            content = f.read()
            title = re.findall(r'title %\}([^}]+)\{', content)[0][6:-1]
            post_date = re.findall(r'post_date %\}([^}]+)\{', content)[0][6:-1]

            rel_path = os.path.relpath(filename, 'app/src/templates/')
            LINKS.append((
                post_date,
                '<a href="http://localhost:9000/%s">%s ( %s )</a>'
                % (rel_path, title, post_date)
                )
            )  # TODO localhost should be picked from general config


with open('app/src/templates/post_list.html', 'wb') as f:
    ordered_links = sorted(LINKS, key=lambda x: x[0], reverse=True)
    content = template.format('<br>'.join([x[1] for x in ordered_links]))
    f.write(content.encode('utf-8'))
