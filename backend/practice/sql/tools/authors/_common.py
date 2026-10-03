import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def only(data, *tables):
    return {t: data[t] for t in tables}
