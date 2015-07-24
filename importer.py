#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmltodict
from datetime import datetime
from collections import OrderedDict

USERS = {}
CATEGORIES = {}
POSTS = {}


def main():
    with open('backup.xml', 'r') as f:
        content = f.read()
        xml = xmltodict.parse(content)
        for item in xml['rss']['channel']['wp:author']:
            USERS[item['wp:author_id']] = {
                'display_name': item['wp:author_display_name'],
                'nickname': item['wp:author_login'],
                'email': item['wp:author_email']
            }

        print 'Found %s users!' % len(USERS.keys())

        for item in xml['rss']['channel']['wp:category']:
            CATEGORIES[item['wp:term_id']] = {
                'category_nicename': item['wp:category_nicename'],
                'category_name': item['wp:cat_name'],
                'parent': item['wp:category_parent']
            }

        print 'Found %s categories!' % len(CATEGORIES.keys())

        for item in xml['rss']['channel']['item']:
            try:
                if item['wp:post_type'] == 'post':
                    POSTS[item['wp:post_id']] = {
                        'title': item['title'],
                        'post_name': item['wp:post_name'],
                        'link': item['link'], 
                        'creator': find_user_by_name(item['dc:creator']),
                        'status': item['wp:status'],
                        'content': item['content:encoded'],
                        'categories': find_cat_by_nicename(item['category']),
                        'date': datetime.strptime(
                            item['wp:post_date'], '%Y-%m-%d %H:%M:%S'),
                        'comments': None
                    }
                    try:
                        POSTS[item['wp:post_id']]['comments'] = parse_comments(item['wp:comment'])
                    except KeyError:
                        POSTS[item['wp:post_id']]['comments'] = []
            except Exception as e:
                # TODO investigate why!
                print 'Could not read one of the posts: %s' % e

        print 'Found %s posts to write' % len(POSTS.keys())

        for post in POSTS:
            write_post_file(POSTS[post])


def find_user_by_name(creator_name):
    for author in USERS:
        if USERS[author]['nickname'] == creator_name:
            return USERS[author]
    return None


def find_cat_by_nicename(categories):
    category_dicts = []
    for category in [categories] if isinstance(categories, OrderedDict) else categories:
        for term_id in CATEGORIES:
            if CATEGORIES[term_id]['category_nicename'] == category['@nicename']:
                category_dicts.append(CATEGORIES[term_id])
    return category_dicts


def parse_comments(comments):
    all_comments = []
    for comment in [comments] if isinstance(comments, OrderedDict) else comments:
        c = {
            'id': comment['wp:comment_id'],
            'author': comment['wp:comment_author'],
            'date': comment['wp:comment_date'],
            'comment': comment['wp:comment_content']
        }
        try:
            c['author_extra'] = USERS[comment['wp:comment_user_id']]
        except KeyError:
            c['author_extra'] = None

        all_comments.append(c)
    return all_comments


def write_post_file(post):
    post_name = post['post_name'].replace('%c2%b7','')
    print 'Writing post [%s]' % post_name

    post_content = u"""
    {{% extends 'post_template.html' %}}

    {{% block title %}}
        {0}
    {{% endblock %}}

    {{% block author %}}
        {1}
    {{% endblock %}}

    {{% block post_date %}}
        {2}
    {{% endblock %}}

    {{% block categories %}}
        {3}
    {{% endblock %}}

    {{% block post %}}
        {4}
    {{% endblock %}}

    {{% block comments %}}
        {5}
    {{% endblock %}}

    """
    with open('app/src/templates/posts/' + post_name + '.html','wb') as f:
        comment_template = u'<p class="comment">{0}<hr>Escrit per {1} el {2}</p>'
        comments = []
        for comment in post['comments']:
            d = comment['date']
            c = comment['comment']
            if comment['author_extra']:
                a = comment['author_extra']['display_name']
            else:
                a = comment.get('author', 'Anónim')

            comments.append(comment_template.format(c, a, d))

        content = post_content.format(
            post['title'],
            post['creator']['display_name'],
            post['date'],
            ', '.join(category['category_name'] for category in post['categories']),
            post['content'],
            ''.join(comments)
        )
        f.write(content.encode('utf-8'))


if __name__ == '__main__':
    main()