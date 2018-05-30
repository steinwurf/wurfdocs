Introduction
============

Build Sphinx documentation for all the different
versions of your project.

Developer docs
==============

* If a developer is currently working on the docs he should
  be able to build locally his changes.

Build types
-----------

1. "workingtree" build.
2. "remote" build
   1. Tag
   2. Branch

* If the repository is a path

  1. Copy it over and make a "workingtree" build
  2. Run the remote builds

A build returns the following dict::

    build = {
        'type': 'workingtree' | 'branch' | 'tag',
        'sha1': commit-id,
        'name': string
        'directory': string,
        'build_path: string
    }

The cache will contain the following::

  stub-8423ds.json = {
      'builds' : [
          build,
          build
      ]
  }


Factories and Dependency Injection
----------------------------------

Testability is a key feature of any modern software library and one of the key
techniques for writing testable code is dependency injection (DI).

In Python DI is relatively simple to implement due to the dynamic nature of the
language.


Deployment
----------

We need a way to publish documentation such that developers can inspect
and verify changes before exposing them to users.

Using Source Branch
-------------------

One way to do this is to separate builds/output based on the source
branch.

So if we are building the ``master`` branch builds will go to the root
of the output directory.

Other branches are placed in a ``development/branch-name`` sub-folder.

Update flow:

 * I'm building some branch ``my-update``.
 * This is now available under ``development/my-update`` on the
   ``gh_pages`` site.


Generating index
................

To make it easy to see the different development versions of the
documentation. We can generate an index in the root of the
``development`` folder.

Cleaning up old branches
------------------------

If the ``prune`` flag is passed any branches not available on the
remote will be removed.

Describe builds
---------------

wurfpipe.json
{
    'build': [
        {
            'type': 'python',
            'recurse': true,
            'cwd': ${CLONE_PATH}/docs,
            'requirements': '${CLONE_PATH}/docs/requirements.txt',
            'workingtree':
                'script': 'python sphinx-build -b html . ${BUILD_PATH}/workingtree'
            'branches':
                'script: 'python sphinx-build -b html . ${BUILD_PATH}/branches/${RECURSE_ID}'
            'tags':
                'script: 'python sphinx-build -b html . ${BUILD_PATH}/docs/${RECURSE_ID}'
        },
        {
            'type': 'python',
            'cwd': ${CLONE_PATH}/landing_page,
            'requirements': '${CLONE_PATH}/landing_page/requirements.txt',
            'script': 'python generate.py --versions=${BUILD_PATH}/docs --output_path=${BUILD_PATH}'
         }
    ],
    'publish': [
        {
            'type': 'push',
            'include_branch: 'master',
            'remote_branch': 'gh_pages',
            'remote_path': '.',
            'source_path': '${BUILD_PATH}'
        },
        {
            'type': 'push',
            'exclude_branch: 'master',
            'remote_branch': 'gh_pages',
            'remote_path': 'experimental/${SOURCE_BRANCH}',
            'source_path': '${BUILD_PATH}'
        }
    ]
}

./wurfdocs build https://stub.git --build_path=/tmp/out --clone_path=/tmp/clone
./wurfdocs publish https://stub.git --build_path=/tmp/out


def build(ctx):

    ctx.add_step(type='python',
                 recurse=True,
                 cwd='${CLONE_PATH},
                 requirements='${CLONE_PATH}/docs/requirements.txt',
                'script': 'python sphinx-build -b html . ${BUILD_PATH}/docs/${RECURSE_ID}'

def publish(ctx):

    ctx.add_step(type='push',
                recurse=True,
                cwd='${CLONE_PATH},
                requirements='${CLONE_PATH}/docs/requirements.txt',
            'script': 'python sphinx-build -b html . ${BUILD_PATH}/docs/${RECURSE_ID}'


./wurfdocs build https://stub.git --build_path=/tmp/build --working_path=/tmp/clone --checkout=api


Source checkout
===============

A build is always done from a ``source checkout`` which can be any branch.

If no explicit ``source checkout`` is specified ``wurfdocs`` will use the PATH
or URL for the repository to determine one.

* For a URL the ``source checkout`` will always be master.
* For a PATH the ``source checkout`` will be the current branch.

Publishing results
==================

What results should be the main ones. If we are building the latest i.e. the
master branch we want those to become the main docs. Other docs should go in a
subdirectory:


'versions': {
    'latest': {
        'type': 'branch',
        'name': 'master',
        'build_path': '${BUILD_ROOT}/${BUILD_NAME}/docs/latest'
    },
    'development': {
        'type': 'branch',
        'name': '*',
        'build_path': '${BUILD_ROOT}/${BUILD_NAME}/experimental/${SOURCE_BRANCH}'
    }
},
'build': [
    { 'type': 'python',
      'script: 'python sphinx-build -b html . ${BUILD_PATH}/docs/${RECURSE_ID}',
      'cwd': ${CLONE_PATH}/docs',
      'requirements': '${CLONE_PATH}/docs/requirements.txt'
    }


]

sphinx/docs/1.0.0
sphinx/docs/2.0.0
sphinx/docs/2.1.0
sphinx/docs/3.0.0
sphinx/docs/latest
sphinx/experimental/trying_new_stuff
sphinx/experimental/new_idea


landing_page/experimental/trying_new_stuff
landing_page/experimental/new_idea
landing_page/latest


We also need to support if the ``script`` to run changes over time. This means
that we have to be able to version build steps:

The following variables are available:

* Globally
    * build_path
    * clone_path

* ``tag`` scope
    * tag_name
* ``branch`` scope
    * branch_name
* ``workingtree`` scope

variables are defined as a 3 tuple:
scope:selector:name

scope = { 'tag', 'source_branch', 'workingtree'}

for 'tag and 'branch' scope the optional selector can be used to match either
branch or tag name. The selector has to be an exact match.

The final element is the name of the variable.

    'build':[
    {
        'type': 'python'
        'script': python sphinx-build -b html . ${output_path},
        'requirements': '${clone_path}/docs/requirements.txt'
        'cwd': ${clone_path}/docs',
        'allow_failure': True,
        'recurse_tags': True,
        'variables':
            'source_branch:master:output_path': '{build_path}/docs/latest'
            'source_branch:output_path': '{build_path}/sphinx/experiments/${branch_name}
            'tag:output_path': '{build_path]/docs/${tag_name$}'
            'workingtree:output_path': '{build_path}/sphinx/experiments/workingtree
    },
    {
        'type': 'python'
        'script': 'python generate.py --versions=${build_path}/docs --output_path=${output_path}'
        'requirements': '${clone_path}/landing_page/requirements.txt'
        'cwd': ${clone_path}/landing_page',
        'allow_failure': True,
        'variables':
            'source_branch:master:output_path': '{build_path}'
            'source_branch:output_path': '{build_path}/landing_page/experiments/${branch_name}
            'workingtree:output_path': '{build_path}/landing_page/experiments/workingtree
    }],
    'publish':[
        {
            'type': 'push',
            'remote_branch': 'gh_pages',
            'exclude_paths: [
                '{build_path}/landing_page/experiments/workingtree',
                '{build_path}/sphinx/experiments/workingtree'
            ],
            'remote_path': '.',
            'source_path': '${build_path}'
        }
    ]




Use-case: Branch changes build

    * We are on a branch and moves some files. Since source branch is not the
      we only update the '*' catch all build command. Everything works fine
      and now we merge. But on the master it fails since we forgot to change the
      'master' source branch command.



