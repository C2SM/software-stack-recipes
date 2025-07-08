# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gribjump(CMakePackage):
    """GribJump is a C++ library for extracting subsets of data from GRIB files, 
    particularly data archived in the FDB
    """

    homepage = "https://github.com/ecmwf/gribjump"
    url = "https://github.com/ecmwf/gribjump/archive/refs/tags/0.10.0.tar.gz"
    git = "https://github.com/ecmwf/fdb.git"

    maintainers("cosunae")

    license("Apache-2.0")

    version("0.10.0", sha256="04a6c7322e585acb7e432e74d68f073ab584a42af9dcb2b4b97f17aebf17d07f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.12:", type="build")
    depends_on("ecbuild", type="build")
    depends_on("eckit")
    depends_on("eccodes")
    depends_on("fdb")
    depends_on("metkit")
    depends_on("libaec@1.1.1:")

    def cmake_args(self):
        args = [
            self.define("ENABLE_MEMFS", True),
            self.define("ENABLE_ECCODES_THREADS", True),
            self.define("ENABLE_AEC", True),
        ]
        return args
