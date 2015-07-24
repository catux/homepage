#!/usr/bin/env python
import os
import re
import codecs
import simplejson as json

template = u"""
{{% extends 'post_list_template.html' %}}

{{% block links %}}
 {0}
{{% endblock %}}
"""

LINKS = []

HOST = json.loads(open('app/src/templates/context/_all.json').read()).get('homepage')

for root, _, files in os.walk('app/src/templates/posts/'):
    for name in files:
        filename = os.path.join(root, name)
        with codecs.open(filename, 'r', 'utf-8') as f:
            content = f.read()
            title = re.findall(r'title %\}([^}]+)\{', content)[0][6:-1]
            post_date = re.findall(r'post_date %\}([^}]+)\{', content)[0][6:-1]
            author = re.findall(r'author %\}([^}]+)\{', content)[0][6:-1]

            rel_path = os.path.relpath(filename, 'app/src/templates/')
            LINKS.append((
                post_date,
                '<li class="list-group-item"><a class="blog-post" href="%s%s">%s <div class="pull-right hidden-xs"><span class="badge blog-date">%s</span>&nbsp;<span class="badge blog-date">%s</span></div></a></li>'
                % (HOST, rel_path, title, author, post_date)
                )
            )


with open('app/src/templates/post_list.html', 'wb') as f:
    ordered_links = sorted(LINKS, key=lambda x: x[0], reverse=True)
    content = template.format(''.join([x[1] for x in ordered_links]))
    f.write(content.encode('utf-8'))
