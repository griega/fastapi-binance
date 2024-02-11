import logging
import sys

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
FORMAT = "%(asctime)s :: %(levelname)s:: %(message)s"
sh = logging.StreamHandler(stream=sys.stdout)
sh.setFormatter(logging.Formatter(FORMAT))
log.addHandler(sh)