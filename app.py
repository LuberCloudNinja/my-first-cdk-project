#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.

from aws_cdk import core

""" Importing stacks from code modules: """
from my_first_cdk_project.MyArtifactBucketStack import MyArtifactBucketStack
from my_first_cdk_project.my_first_cdk_project_stack import MyFirstCdkProjectStack

""" Environment Variables below: """
app = core.App()
prod_east = region = app.node.try_get_context("Prod")["regions"]["east"]
prod_west = app.node.try_get_context("Prod")["regions"]["west"]
dev_east = app.node.try_get_context("Dev")["regions"]["east"]
dev_west = app.node.try_get_context("Dev")["regions"]["west"]
master_east = app.node.try_get_context("Master")["regions"]["east"]
master_west = app.node.try_get_context("Master")["regions"]["west"]

env_US_EAST = core.Environment(account="721918345279", region=master_east)
env_US_WEST = core.Environment(account="721918345279", region=master_west)

"Stacks: "
MyFirstCdkProjectStack(app, "MyFirstCdkProjectStack")
MyArtifactBucketStack(app, "MyDevStack", env=env_US_WEST)
MyArtifactBucketStack(app, "MyMasterStack", is_prod=True, env=env_US_EAST)

app.synth()
