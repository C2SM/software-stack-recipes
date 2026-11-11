# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Mir(CMakePackage):
    """Meteorological Interpolation and Regridding (MIR) library and tools."""

    homepage = "https://github.com/ecmwf/mir"
    git = "https://github.com/ecmwf/mir.git"
    url = "https://github.com/ecmwf/mir/archive/refs/tags/1.30.2.tar.gz"
    list_url = "https://github.com/ecmwf/mir/tags"

    license("Apache-2.0")

    version("1.30.2", sha256="7f9872884c065b989a0c82db92e0cf8b74c9284ab7af98bb1fbdd9c6c865c26b")

    variant("tools", default=True, description="Build the command line tools")
    variant("netcdf", default=False, description="Enable netCDF support")
    variant("metkit", default=True, description="Enable metkit support")
    variant("masks", default=True, description="Download LSM files at build time")
    variant("python", default=False, description="Build Python bindings")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.14:", type="build")
    depends_on("ecbuild@3.4:", type="build")

    depends_on("eckit@2.1:")
    depends_on("eccodes@2.47: +geo")
    depends_on("ecmwf-atlas@0.46:")
    depends_on("metkit@1.18.3:", when="+metkit")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("netcdf-cxx4", when="+netcdf")

    depends_on("python@3:", when="+python", type=("build", "link", "run"))
    depends_on("py-numpy@2:", when="+python", type="build")
    depends_on("py-cython@3:", when="+python", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_BUILD_TOOLS", "tools"),
            self.define_from_variant("ENABLE_NETCDF", "netcdf"),
            self.define_from_variant("ENABLE_METKIT", "metkit"),
            self.define_from_variant("ENABLE_MIR_DOWNLOAD_MASKS", "masks"),
            self.define_from_variant("ENABLE_PYTHON", "python"),
            self.define("ENABLE_TESTS", self.run_tests),
        ]
        if self.spec.satisfies("+python"):
            args.append(self.define("Python3_EXECUTABLE", self.spec["python"].command.path))
        return args
