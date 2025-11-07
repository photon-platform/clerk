from ablog.conf import *
from photon_platform.publish.global_conf import *
import photon_platform.clerk as module

version = module.__version__

org = "photon-platform"
org_name = "photon-platform"

repo = "clerk"
repo_name = "clerk"

setup_globals(org, org_name, repo, repo_name)
