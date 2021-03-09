project(
    'dashboard',
    ['vala', 'c'],
    version: 'v0.0.1',
    license: 'MIT'
)

id = 'org.fascode.dashboard'

cc = meson.get_compiler('c')

gnome = import('gnome')
#i18n = import('i18n')

deps = [
    dependency('cairo'),
    dependency('glib-2.0'),
    dependency('gobject-2.0'),
    dependency('gio-2.0'),
    dependency('gtk+-3.0'),
    dependency('libgtop-2.0'),
    cc.find_library('m')
]

vapi_dir = join_paths(meson.source_root (), 'vapi')
vapi_dirs = [ '--vapidir=@0@'.format(vapi_dir) ]

subdir('data')
subdir('src')
