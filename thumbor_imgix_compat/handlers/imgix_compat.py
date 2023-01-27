# -*- coding: utf-8 -*-

# Copyright (c) 2016, thumbor-community
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.


from hashlib import md5
import tornado.web
from urllib.parse import urlparse, parse_qs

from thumbor.handlers.imaging import ImagingHandler
from thumbor.utils import logger

from thumbor_imgix_compat.imgix_compat import ImgixCompat
from tc_core.web import RequestParser


class ImgxCompatHandler(ImagingHandler):

    should_return_image = True

    @classmethod
    def regex(cls):
        '''
        :return: The list of regex used for routing.
        :rtype: string
        '''
        return [
            r'^/listing-assets/.*',
            r'^/uploads/.*',
            r'^/.*png$',
        ]


    def check_imgix_signature(self, qs: map) -> bool:
        imgix_hash = self.context.config.get('IMGIX_COMPAT_TOKEN', None)
        if imgix_hash is None:
            return False


        if 's' not in qs:
            return False

        query_signature = qs['s']

        request_uri = self.request.uri.replace(f'&s={query_signature}', '')

        return md5((imgix_hash + request_uri).encode('utf8')).hexdigest() == query_signature


    def build_request(self):
        parsed = urlparse(self.request.uri)
        qs = {k: v[-1] for k, v in parse_qs(parsed.query).items()}

        if not self.check_imgix_signature(qs):
            raise tornado.web.HTTPError(403)

        filters = []
        smart = None
        halign = None
        valign = None
        height = None
        width = None
        unsafe = 'unsafe'
        fit_in = None
        adaptive = None
        full = None

        if 'q' in qs:
            filters.append('quality({})'.format(qs['q']))
        elif 'auto' in qs and qs['auto'] == 'compress':
            filters.append('quality({})'.format(self.context.config.get('IMGIX_COMPAT_AUTO_QUALITY')))

        
        if 'fill' in qs and qs['fill'] == 'blur':
                filters.append('fill(blur)')

        if 'fit' in qs:
            if qs['fit'] == 'crop':
                pass
            else:
                fit_in = 'fit-in'

        if 'h' in qs:
            height = qs['h']

        if 'w' in qs:
            width = qs['w']


        return {
            'unsafe': unsafe,
            'hash': None,
            'debug': None,
            'meta': None,
            'trim': None,
            'crop_left': None,
            'crop_top': None,
            'crop_right': None,
            'crop_bottom': None,
            'adaptive': adaptive,
            'full': full,
            'fit_in': fit_in,
            'horizontal_flip': None,
            'width': width,
            'vertical_flip': None,
            'height': height,
            'halign': halign,
            'valign': valign,
            'smart': smart,
            'filters': ':'.join(filters) if len(filters) > 0 else None,
            'image': self.context.config.get('IMGIX_COMPAT_STORAGE_ROOT') + parsed.path,
        }


    async def get(self, **kwargs):
        # Get the url from the shortener and parse the values.
        options = self.build_request()

        if not options:
            raise tornado.web.HTTPError(404)

        # Call the original ImageHandler.get method to serve the image.
        await super(ImgxCompatHandler, self).get(**options)
