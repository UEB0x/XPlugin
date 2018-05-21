#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 2018.05.21

import os, sys
import getopt
import shutil
import glob
import subprocess
import re
import traceback
import types

def rename(src, dst):
    if os.path.exists(dst):
        run('rm -fr {dst}'.format(dst=dst))
    os.rename(src, dst)

def myreplace(root, src, dst):
    """
    replace file content in @root directory: @src -> dst
    """

    if not os.path.exists(root):
        print '# {folder} is not exists'.format(folder=root)
        return

    for i in os.listdir(root):
        if i in ['.', '..', '.git', 'rename.py', 'README.md']: continue

        path = os.path.join(root,i)
        if os.path.isfile(path) and not os.path.isdir(path):
            f = open(path, 'rb')
            content = f.read()
            f.close()
            if src in content:
                f = open(path, 'wb')
                f.write(content.replace(src, dst))
                f.close()
        if os.path.isdir(path): myreplace(path, src, dst)

def myrename(root, src, dst):
    """
    rename file in @root directory: @src -> @dst
    """

    if not os.path.exists(root):
        print '# {folder} is not exists'.format(folder=root)
        return

    for i in os.listdir(root):
        if i in ['.', '..', '.git']: continue

        path = os.path.join(root,i)
        if os.path.isdir(path):
            myrename(path, src, dst)

        if (os.path.isfile(path) or os.path.isdir(path)) and src in i:
            f = os.path.join(root,i)
            t = os.path.join(root,i.replace(src, dst))
            # print '# {f} -> {t}'.format(f=f,t=t)
            rename(f, t)

def run(cmd, quiet=False):
    from subprocess import call
    if quiet:
        ret = call(cmd, shell=True, stdout=subprocess.PIPE)
    else:
        ret = call(cmd, shell=True)
    if ret != 0:
        print '==> Command failed: ' + cmd
        print '==> Stopping build.'
        sys.exit(1)

def get_curr_path():
    return os.path.dirname(os.path.realpath(__file__))

def main(name):

    plugin_name_src = 'XPlugin'
    plugin_name_dst = name

    curr_plugin_path = get_curr_path()
    new_plugin_path = os.path.join(curr_plugin_path, '..', plugin_name_dst)

    myrename(curr_plugin_path, plugin_name_src, plugin_name_dst)

    myreplace(curr_plugin_path, plugin_name_src, plugin_name_dst)
    myreplace(curr_plugin_path, plugin_name_src.upper(), plugin_name_dst.upper())

    rename(curr_plugin_path, new_plugin_path)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
