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

wurfdocs.json
{
    'build': [
        {'type': 'sphinx',
         'recurse': true,
         'output_path': 'docs',
         'source_path': 'docs'
         }
        {'type': 'python',
         'output_path': '.',
         'source_path': 'landing_page',
         'requirements': 'landing_page\requriements.txt',
         'shell': 'python generate.py %(versions_json)s'
         }
    ]
}
