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

