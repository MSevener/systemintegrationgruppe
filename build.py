from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.integrationtest")
use_plugin("python.install_dependencies")

default_task = "publish"

@init
def initialize(project):
	project.build_depends_on('mockito')
	project.build_depends_on('bottle')
	project.build_depends_on('boto3')
	project.build_depends_on('MySQL-python')
