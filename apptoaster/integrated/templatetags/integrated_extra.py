import math
from django import template
import logging
logger = logging.getLogger('appToaster')
register = template.Library()

@register.filter
def div( value, arg ):
    try:
        value = int( value )
        arg = int( arg )
        result = math.floor(value / arg)
        return result
    except Exception as e:
        logger.info(e)
        return 0