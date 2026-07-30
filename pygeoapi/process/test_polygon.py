# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#          Francesco Martinelli <francesco.martinelli@ingv.it>
#
# Copyright (c) 2026 Tom Kralidis
# Copyright (c) 2024 Francesco Martinelli
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import json
import logging

from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError


LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.1.0',
    'id': 'test-polygon',
    'title': {
        'en': 'Get Test Polygon',
    },
    'description': {
        'en': 'An example process that takes a string as input, and returns a file as output. '
        'Intended to demonstrate a simple data i/o  process.',
    },
    'jobControlOptions': ['sync-execute', 'async-execute'],
    'inputs': {
        'dataset': {
            'title': 'Dataset',
            'description': 'Polygon you wish to get back as output. Must be one of:'
            'erie; baykal; world.',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
        },
        'fileform': {
            'title': 'File Format',
            'description': 'Optionally, specify the file format; must be one of: geojson, shp, gpkg. If not specified,'
            'process will return erie as geojson; baykal as gpkg; or world as shapefile. ',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'keywords': ['file format']
        },
        'as_bytes': {
            'title': 'As bytes',
            'description': 'Whether to force return as bytes',
            'schema': {
                'type': 'boolean',
                'default': False
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'keywords': ['as_bytes']
        },
        'media_type': {
            'title': 'Media type', # TODO must this be adjusted to file format?
            'description': 'Force a specific media type',
            'schema': {
                'type': 'string',
                'default': 'application/json'
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'keywords': ['media_type']
        }
    },
    'outputs': {
        'testpolygon': {
            'title': 'Test Polygon',
            'description': 'Test polygon file',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json' # TODO must this be adjusted to file format?
            }
        }
    },
}


class TestPolygonProcessor(BaseProcessor):
    """Test Polygon Processor"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.get_polytest.TestPolygonProcessor
        """

        super().__init__(processor_def, PROCESS_METADATA)
        self.supports_outputs = True

    def execute(self, data, outputs=None):
        mimetype = data.get('media_type', 'application/json') # TODO adjust data type here?
        dataset = data.get('dataset')

        if dataset is None:
            raise ProcessorExecuteError('Cannot process without a dataset name')
        elif not dataset in ["baykal", "erie", "world"]:
            raise ProcessorExecuteError('Dataset name must be one of the following: baykal, erie, world')

        fileformat = data.get('fileformat')
        
        if fileformat is None:
            pass
        elif not fileformat in ["gpkg", "geojson", "shp"]:
            raise ProcessorExecuteError('Fileformat must be one of the following: gpkg, geojson, shp')
        # TODO include here a "conversion" into a different fileformat..?

        # # TODO access file
        # f"./pygeoapi/static/datasets/{dataset}"

        produced_outputs = {}

        if data.get('as_bytes', False):
            json.dumps(produced_outputs).encode('utf-8')

        return mimetype, produced_outputs

    def __repr__(self):
        return f'<TestPolygonProcessor> {self.name}'
