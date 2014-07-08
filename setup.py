import subprocess
from os.path import join
from distutils.core import setup
from distutils.log import warn, info
from distutils.command.install_data import install_data as _install_data

class InstallData(_install_data):
    """
    Run some GNOME integration tasks or reverse those, respectively.
    """

    def run(self):
        _install_data.run(self)
        self._update_icon_cache()

    def _update_icon_cache(self):
        """
        Warm icon caches since we update icon themes with new files
        """

        theme_dirs = [
            join(self.install_dir, 'share', 'icons', 'ubuntu-mono-light'),
            join(self.install_dir, 'share', 'icons', 'ubuntu-mono-dark'),
            join(self.install_dir, 'share', 'icons', 'hicolor')
        ]

        for theme_dir in theme_dirs:
            try:
                info('updating icons cache for: %s', theme_dir)
                subprocess.call(
                    ['gtk-update-icon-cache', '-q', '-f', '-t', theme_dir])
            except Exception, ex:
                warn('updating icon cache failed: %s', ex)

setup(name='lookit',
      version='1.2.0',
      description='Quick Screenshot Uploader',
      author='Zach Tibbitts',
      author_email='zachtib@gmail.com',
      url='http://zachtib.github.com/lookit',
      maintainer='Dirk Rother',
      maintainer_email='dirrot.dev@gmail.com',
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
      cmdclass={
          'install_data': InstallData }
     )
