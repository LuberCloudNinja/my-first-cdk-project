#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from my_first_cdk_project.MyArtifactBucketStack import MyArtifactBucketStack
from my_first_cdk_project.my_first_cdk_project_stack import MyFirstCdkProjectStack

env_US_EAST = core.Environment(region="us-east-1")
env_US_WEST = core.Environment(region="us-west-1")
app = core.App()
MyFirstCdkProjectStack(app, "MyFirstCdkProjectStack")

MyArtifactBucketStack(app, "MyDevStack", env=env_US_EAST)
MyArtifactBucketStack(app, "MyProdStack", is_prod=True, env=env_US_EAST)

app.synth()
