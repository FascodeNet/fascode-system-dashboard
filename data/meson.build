resource_data = files(
  'ui/about-dialog.ui',
  'ui/disk-speed.ui',
  'ui/net-speed.ui',
  'ui/swap-box.ui',
  'ui/window.ui'
)

resources = gnome.compile_resources(
  id,
  id + '.gresource.xml',
  c_name: 'resources',
  dependencies: resource_data
)
