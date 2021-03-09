sources = [
  'circle.vala',
  'cpu.vala',
  'dashboard.vala',
  'dialog.vala',
  'disk.vala',
  'header.vala',
  'mem.vala',
  'net.vala',
  'swap.vala',
  'util.vala',
  'window.vala'
]

c_args = [
  '-DVERSION="@0@"'.format(meson.project_version()),
  '-DGETTEXT_PACKAGE="@0@"'.format(meson.project_name()),
  '-DGNOMELOCALEDIR="@0@"'.format(join_paths(get_option('prefix'), get_option('localedir'))),
  '-DAPPLICATION_ID="@0@"'.format(id)
]

executable(
  meson.project_name(),
  sources + resources,
  dependencies: deps,
  c_args: c_args,
  vala_args: vapi_dirs,
  install: true
)
