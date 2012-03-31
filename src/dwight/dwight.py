#!/usr/bin/env python
# encoding: utf-8
"""

dwight.py: assistant to the django manage.py command.

Run Django management commands against arbitrary settings.

Dwight License Agreement (MIT License)
------------------------------------------

Copyright (c) 2012 Alexander Bohn

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Created by FI$H 2000 on 2012-03-31.
Copyright (c) 2012 Objects In Space And Time, LLC. All rights reserved.

"""
from __future__ import with_statement

__version__ = '0.8.0'
__license__ = __doc__

import sys, os, re, imp, argparse
from argh import arg, alias, ArghParser
from userconfig import UserConfig

ERRORS = {
    'nofile': "Error: Can't find a settings file at %s. You may have to run django-admin.py, passing it your settings module.\n(If it does indeed exist, attempting to load your settings file throws an ImportError.)\n",
}

DEFAULT_SETTINGS = [
    
    ('__meta__', {
        'our_default':  "",
        'last':         "",
        'last_file':    ""}),
    
    ('__filepath__', {
        '/dev/null':    "devnull"})

    ]

class DwightConfig(UserConfig):
    default_section_name = '__meta__'


CFG = DwightConfig('dwight', defaults=DEFAULT_SETTINGS)

pathfillet = lambda pth: os.path.split(pth)[0]

class BloodAloneMovesTheWheelsOfHistory(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        if option_string is None:
            option_string = ''
        out = []
        out.extend(values)
        out.extend(option_string.split())
        setattr(args, self.dest, out)

def load_with_label(LABEL, attr='filepath'):
    return CFG.get(LABEL, attr)

def load_settings_file(pth):
    mod_name = os.path.splitext(os.path.basename(os.path.abspath(pth)))[0]
    if mod_name == '__init__':
        mod_name = os.path.splitext(os.path.basename(os.path.dirname(os.path.abspath(pth))))[0]
    mod_name = LABEL = CFG.get('__filepath__', pth.lower(), mod_name)
    CFG.set('__meta__', 'last', LABEL)
    CFG.set('__meta__', 'last_file', pth)
    re_qualified = re.compile(
        r'%(nm)s%(sep)s(\S+?)(?:%(sep)s__init__)?(?:\.py)|(?:%(sep)s)' % dict(
            nm=mod_name, sep=os.path.sep),
        re.IGNORECASE).findall(pth)
    mod_qualified = re_qualified.pop().replace(os.path.sep, '.')
    
    #print "******************"
    #print mod_qualified
    #print re_qualified
    #print LABEL
    #print mod_name
    #print pth
    #print "******************"
    
    whacks = mod_qualified.count('.') + 2
    whackedpth = str(pth)
    for i in xrange(0, whacks):
        whackedpth = pathfillet(whackedpth)
    
    sys.path.append(whackedpth)
    os.environ['DJANGO_SETTINGS_MODULE'] = mod_qualified
    os.environ['PYTHONPATH'] = ":".join([pyth for pyth in sys.path if not pyth.endswith('.egg')])
    
    return imp.load_source(mod_qualified, pth)

def store_settings_file(LABEL, pth):
    CFG.set_default(LABEL, 'filepath', pth)
    CFG.set('__meta__', 'last', LABEL)
    CFG.set('__meta__', 'last_file', pth)
    CFG.set('__filepath__', pth, LABEL)
    CFG.set(LABEL, 'filepath', pth)


@arg('--settings-file', nargs="?", default="None",
    help="Path to your Django settings file (n'\xc3\xa9'e 'settings.py')")
@arg('MGMT_CMD', nargs=1,
    help="Management command to execute")
@arg('MGMT_ARGS', nargs=argparse.REMAINDER, action=BloodAloneMovesTheWheelsOfHistory,
    help="Management command arguments")
@alias('manage-with')
def assist_the_regional_manager(args):
    if not os.path.exists(args.settings_file):
        sys.stderr.write(ERRORS['nofile'] % args.settings_file)
        sys.exit(1)
    from django.core.management import execute_manager
    settings = load_settings_file(args.settings_file)
    mgmt_argv = [str(__file__),] + args.MGMT_CMD + args.MGMT_ARGS
    execute_manager(settings, argv=mgmt_argv)

@arg('LABEL', nargs="?",
    help="Name under which to store this setting")
@arg('SETTINGS_FILE', nargs="?",
    help="Path to your Django settings file (n'\xc3\xa9'e 'settings.py')")
@alias('alias')
def keep_careful_notes(args):
    if not os.path.exists(args.SETTINGS_FILE):
        sys.stderr.write(ERRORS['nofile'] % args.SETTINGS_FILE)
        sys.exit(1)
    store_settings_file(args.LABEL, args.SETTINGS_FILE)

@arg('LABEL', nargs="?",
    help="Name under which to store this setting")
@arg('MGMT_CMD', nargs=1,
    help="Management command to execute")
@arg('MGMT_ARGS', nargs=argparse.REMAINDER, action=BloodAloneMovesTheWheelsOfHistory,
    help="Management command arguments")
@alias('mgmt')
def rule_with_an_iron_fist(args):
    settings_file = load_with_label(args.LABEL)
    if not os.path.exists(settings_file):
        sys.stderr.write(ERRORS['nofile'] % settings_file)
        sys.exit(1)
    settings = load_settings_file(settings_file)
    from django.core.management import execute_manager
    mgmt_argv = [str(__file__),] + args.MGMT_CMD + args.MGMT_ARGS
    execute_manager(settings, argv=mgmt_argv)

p = ArghParser()
p.add_commands([assist_the_regional_manager, keep_careful_notes, rule_with_an_iron_fist])

def yodogg():
    #argvee = [str(__file__), 'manage', '--settings-file=/Users/fish/Dropbox/imagekit/django-imagekit-f2k/imagekit/schmettings.py', 'diffsettings', '--verbosity=2']
    #argvee = [str(__file__), 'manage-with', '--settings-file=/Users/fish/Dropbox/ost2/ost2/settings/base.py', 'migrate', '--list', '--verbosity=2']
    
    #sys.argv = [str(__file__), 'diffsettings']
    #sys.argv = [str(__file__), 'help']
    
    argvee = [str(__file__), 'manage-with', '--settings-file=/Users/fish/Dropbox/ost2/ost2/settings/base.py', 'migrate', '--list', '--verbosity=2']
    p.dispatch(argv=argvee[1:])
    argvee = [str(__file__), 'alias', 'ost2-base', '/Users/fish/Dropbox/ost2/ost2/settings/base.py']
    p.dispatch(argv=argvee[1:])
    argvee = [str(__file__), 'alias', 'ost2', '/Users/fish/Dropbox/ost2/ost2/settings/__init__.py']
    p.dispatch(argv=argvee[1:])
    argvee = [str(__file__), 'alias', 'ost2-superlocal', '/Users/fish/Dropbox/ost2/ost2/settings/superlocal.py']
    p.dispatch(argv=argvee[1:])
    argvee = [str(__file__), 'alias', 'imagekit', '/Users/fish/Dropbox/imagekit/django-imagekit-f2k/imagekit/schmettings.py']
    p.dispatch(argv=argvee[1:])
    argvee = [str(__file__), 'alias', 'signalqueue', '/Users/fish/Dropbox/django-signalqueue/signalqueue/settings/__init__.py']
    p.dispatch(argv=argvee[1:])
    argvee = [str(__file__), 'alias', 'delegate', '/Users/fish/Dropbox/django-delegate/delegate/settings.py']
    p.dispatch(argv=argvee[1:])
    
    argvee = [str(__file__), 'manage', 'signalqueue', 'diffsettings']
    p.dispatch(argv=argvee[1:])

def main():
    p.dispatch(argv=sys.argv[1:])

if __name__ == '__main__':
    main()

