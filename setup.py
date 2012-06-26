from distutils.core import setup

setup(name='lookit',
      version='1.2.0',
      description='Quick Screenshot Uploader',
      author='Zach Tibbitts',
      author_email='zachtib@gmail.com',
      url='http://zachtib.github.com/lookit',
      license='GPLv3',
      packages=['lookit'],
      package_dir={'lookit': 'src'},
      package_data={'lookit': ['data/*.xml', 'poster/*.py']},
      scripts=['src/lookit'],
      data_files=[
          ('share/applications', ['lookit.desktop']),
          ('share/pixmaps', ['lookit.svg']),
          ('share/icons/ubuntu-mono-light/apps/24',
              ['icons/ubuntu-mono-light/apps/24/lookit-panel.svg']),
          ('share/icons/ubuntu-mono-light/apps/22',
              ['icons/ubuntu-mono-light/apps/22/lookit-panel.svg']),
          ('share/icons/ubuntu-mono-dark/apps/24',
              ['icons/ubuntu-mono-dark/apps/24/lookit-panel.svg']),
          ('share/icons/ubuntu-mono-dark/apps/22',
              ['icons/ubuntu-mono-dark/apps/22/lookit-panel.svg']),
          ('share/icons/hicolor/scalable/apps', ['lookit-panel.svg']),
          ('share/gnome-shell/extensions/lookit@extensions.zachtib.com', [
              'src/gnome-shell/extensions/lookit@extensions.zachtib.com/extension.js',
              'src/gnome-shell/extensions/lookit@extensions.zachtib.com/metadata.json',
              'src/gnome-shell/extensions/lookit@extensions.zachtib.com/stylesheet.css'])
      ],
     )
