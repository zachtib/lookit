from distutils.core import setup

setup(name='lookit',
      version='0.5.0',
      description='Quick Screenshot Uploader',
      author='Zach Tibbitts',
      author_email='zachtib@gmail.com',
      url='http://zachtib.github.com/lookit',
      license='GPLv2',
      packages=['lookit'],
      package_dir={'lookit': 'src'},
      package_data={'lookit': ['data/*.xml']},
      scripts=['src/lookit'],
      data_files=[('share/applications', ['lookit.desktop']),
		  ('share/pixmaps', ['lookit.svg', 'lookit-dark.svg', 
						'lookit-light.svg'])],
     )
