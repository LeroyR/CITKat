import citkat as i

import os
from pathlib import Path
from os import environ, getcwd
from urllib.parse import urlparse

from flask_frozen import Freezer

from glob import glob

from flask import Blueprint, render_template, current_app
from lxml.etree import XPath, XMLParser, parse, XMLSyntaxError
from werkzeug.utils import safe_join
from flask import url_for

import citkat.modules.browse as mod_b

if 'CI_PAGES_URL' in environ:
	url = environ.get('CI_PAGES_URL')
	#i.citkat.config["SERVER_NAME"] = urlparse(url).hostname
	#print(f"SERVER_NAME: {urlparse(url).hostname}")
	i.citkat.config['FREEZER_BASE_URL'] = url
	print(f"FREEZER_BASE_URL: { url}")
	#i.citkat.config['APPLICATION_ROOT'] = urlparse(url).path
	#print(f"APPLICATION_ROOT: {urlparse(url).path}")

#with i.citkat.app_context():
#    print(url_for('static', filename="node_modules/bootstrap/dist/css/bootstrap.min.css"))

i.citkat.config["FREEZER_IGNORE_404_NOT_FOUND"] = False
i.citkat.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True
i.citkat.config["FREEZER_REMOVE_EXTRA_FILES"] = True

freezer = Freezer(i.citkat)

@freezer.register_generator
def browse():
	for entity in mod_b.titles:
		#yield 'browse.browse' , {'entity': entity}
		yield "/browse/" + entity + "/"

@freezer.register_generator
def static_page():
	for entity in mod_b.titles:
		for itm in glob(safe_join(current_app.config['catalog-directory'], entity, '*.xml')):
			filename = itm.split('/')[-1]
			yield "/"+ entity + "/" + filename

@freezer.register_generator
def versions():
	for entity in mod_b.titles:
		for itm in glob(safe_join(current_app.config['catalog-directory'], entity, '*.xml')):
			filename_no_suffix = Path(itm).stem
			yield "/api/versions/" + entity + "/" + filename_no_suffix

@freezer.register_generator
def backlinks():
	for entity in mod_b.titles:
		for itm in glob(safe_join(current_app.config['catalog-directory'], entity, '*.xml')):
			filename = os.path.basename(Path(itm))
			yield "/api/backlinks/" + entity + "/" + filename

def freeze():
	print(f"using catalog dir: {i.citkat.config['catalog-directory']}")
	i.citkat.config['FREEZER_DESTINATION'] = getcwd() + "/public"
	print(f"using destination: {i.citkat.config['FREEZER_DESTINATION']}")
	freezer.freeze()

def debug():
	print(f"using catalog dir: {i.citkat.config['catalog-directory']}")
	#i.citkat.config['FREEZER_RELATIVE_URLS'] = True
	#freezer.freeze()
	freezer.run(debug=True)

if __name__ == '__main__':
	debug()
