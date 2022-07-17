from rest_framework.renderers import BaseRenderer

from utils.data import CONTENT_TYPE_TO_FILE_TYPE_MAPPING


class XLSXFileRenderer(BaseRenderer):
    @staticmethod
    def _get_xlsx_media_type() -> str:
        for key, value in CONTENT_TYPE_TO_FILE_TYPE_MAPPING.items():
            if value == 'xlsx':
                return key
        else:
            return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    media_type = _get_xlsx_media_type()
    format = 'xlsx'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class CSVFileRenderer(BaseRenderer):
    @staticmethod
    def _get_csv_media_type() -> str:
        for key, value in CONTENT_TYPE_TO_FILE_TYPE_MAPPING.items():
            if value == 'csv':
                return key
        else:
            return 'text/csv'

    media_type = _get_csv_media_type()
    format = 'csv'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
