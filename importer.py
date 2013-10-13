#!/usr/bin/env python
import xmltodict
from dateutil.parser import *
from collections import OrderedDict

USERS = {}
CATEGORIES = {}
POSTS = {}

def main():
    with open('backup.xml','r') as f:
        content = f.read()
        xml = xmltodict.parse(content)
        for item in xml['rss']['channel']['wp:author']:
            USERS[item['wp:author_id']] = {'display_name': item['wp:author_display_name'],
                                            'nickname': item['wp:author_login'],
                                            'email': item['wp:author_email']
                                            }
        for item in xml['rss']['channel']['wp:category']:
            CATEGORIES[item['wp:term_id']] = {'category_nicename': item['wp:category_nicename'],
                                              'category_name': item['wp:cat_name'],
                                              'parent': item['wp:category_parent']}

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
                        'categories': find_category_by_nicename(item['category']),
                        'date': parse(item['wp:post_date']),
                        'comments': None
                    }
                    try:
                        POSTS[item['wp:post_id']]['comments'] = parse_comments(item['wp:comment'])
                    except KeyError:
                        POSTS[item['wp:post_id']]['comments'] = []
            except Exception:
                pass
        for post in POSTS:
            write_post_file(POSTS[post])

def find_user_by_name(creator_name):
    for author in USERS:
        if USERS[author]['nickname'] == creator_name:
            return USERS[author]
    return None

def find_category_by_nicename(categories):
    category_dicts = []
    for category in [categories] if isinstance(categories, OrderedDict) else categories:
        for term_id in CATEGORIES:
            if CATEGORIES[term_id]['category_nicename'] == category['@nicename']:
                category_dicts.append(CATEGORIES[term_id])
    return category_dicts

def parse_comments(comments):
    all_comments = []
    for comment in [comments] if isinstance(comments, OrderedDict) else comments:
        c = {'id': comment['wp:comment_id'],
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
    with open('pages/posts/' + post['post_name'].replace('%c2%b7','') + '.html','wb') as f:
        f.write(bytes('title: ' + post['title'] + '\n', 'utf-8'))
        f.write(bytes('author: ' + post['creator']['display_name'] + '\n', 'utf-8'))
        f.write(bytes('date: ' + post['date'].strftime('%d-%m-%Y') + '\n\n\n', 'utf-8'))
        f.write(bytes('{% extends "post.html" %}\n{% block body %}\n', 'utf-8'))
        f.write(bytes(post['content'] + '\n', 'utf-8'))
        f.write(bytes('\n<hr>\n', 'utf-8'))
        categories = [category['category_name'] for category in post['categories']]
        f.write(bytes('Categories: ' + ', '.join(categories) if len(categories) > 1 else categories[0] , 'utf-8'))
        f.write(bytes('\n<hr>\n', 'utf-8'))
        for post in post['comments']:
            f.write(bytes('\n' + post['comment'] + '\n', 'utf-8'))
            f.write(bytes('--\n', 'utf-8'))
            if post['author_extra'] is None:
                f.write(bytes('by ' + post['author'] if post['author'] is not None else 'Anónim', 'utf-8'))
            else:
                f.write(bytes('by ' + post['author_extra']['display_name'], 'utf-8'))
            f.write(bytes(' on ' + post['date'] + '<br>', 'utf-8'))
        f.write(bytes('{% endblock %}', 'utf-8'))
        f.close()


if __name__ == '__main__':
    main()