# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Metkit(CMakePackage):
    """Toolkit for manipulating and describing meteorological objects,
    implementing the MARS language and associated processing and semantics."""

    homepage = "https://github.com/ecmwf/metkit"
    url = "https://github.com/ecmwf/metkit/archive/refs/tags/1.7.0.tar.gz"
    git = "https://github.com/ecmwf/metkit.git"
    list_url = "https://github.com/ecmwf/metkit/tags"

    maintainers("skosukhin", "victoria-cherkas", "dominichofer")

    license("Apache-2.0")

    # As of 04.03.2026, the levelist branch has been rebased on top of v1.16.2
    version("levelist", branch="levelist")

    version("1.16.2", sha256="30a65a2cc14942e7ce64ea5539a1b6b85ecce336811014aba70e1f4f9e651f68")
    version("1.16.1", sha256="0520cba65afeaede6553c8b62941e67c0f88123602e19d0898538a52e2b0f522")
    version("1.16.0", sha256="7b93e4fc1608c1ac205fbf3e094d50ba8a88e7223b65eab7a12362f55550c8e1")
    version("1.15.9", sha256="19e656fdafd52375d076303f710bfb71d24298866960e479082d7cb8c730efee")
    version(
        "1.15.2-levelist",
        sha256="25cebe7610949848671131ee3681e3e7e01d376e7b74e1a269872b9fba15ab54",
    )
    version(
        "9999.99",
        sha256="d63181aecd6e3128609145e381b214b81b79072b414313351e7d3914377eda13",
        url="https://github.com/ecmwf/metkit/archive/refs/tags/levelist-double.tar.gz",
    )
    version("1.14.1", sha256="996cc1d4b569c73b20490bfccbd8ee09d78a94dd9c15e643528d7d9a360f3d2e")
    version("1.11.22", sha256="e2a2ea1532f9e187e37b807dbf35cd09325b2aef29bd5117203d57ba2e65a0d6")
    version("1.11.5", sha256="717e0d92499d7a1b49338c3762d829aa83c75f8095dc9e7cdc7f49c209bb847b")
    version("1.10.17", sha256="1c525891d77ed28cd4c87b065ba4d1aea24d0905452c18d885ccbd567bbfc9b1")
    version("1.10.2", sha256="a038050962aecffda27b755c40b0a6ed0db04a2c22cad3d8c93e6109c8ab4b34")
    version("1.9.2", sha256="35d5f67196197cc06e5c2afc6d1354981e7c85a441df79a2fbd774e0c343b0b4")
    version("1.7.0", sha256="8c34f6d8ea5381bd1bcfb22462349d03e1592e67d8137e76b3cecf134a9d338c")


    depends_on("c", type="build")
    depends_on("cxx", type="build")  # generated

    variant("tools", default=True, description="Build the command line tools")
    variant("grib", default=True, description="Enable support for GRIB format")
    variant("odb", default=False, description="Enable support for ODB data")

    depends_on("cmake@3.12:", type="build")
    depends_on("ecbuild@3.4:", type="build")

    depends_on("eckit@1.16:")
    depends_on("eckit@1.21:", when="@1.10:")
    depends_on("eckit@:1.21", when="@:1.10")

    depends_on("eccodes@2.5:", when="+grib")
    depends_on("eccodes@2.27:", when="@1.10.2: +grib")

    depends_on("odc", when="+odb")

    conflicts(
        "+tools",
        when="~grib~odb",
        msg="None of the command line tools is built when both "
        "GRIB format and ODB data support are disabled",
    )

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_BUILD_TOOLS", "tools"),
            self.define_from_variant("ENABLE_GRIB", "grib"),
            self.define_from_variant("ENABLE_ODC", "odb"),
            # The tests download additional data (~4KB):
            self.define("ENABLE_TESTS", self.run_tests),
            # The library does not really implement support for BUFR format:
            self.define("ENABLE_BUFR", False),
            # The library does not really implement support for NetCDF format:
            self.define("ENABLE_NETCDF", False),
            # We do not need any experimental features:
            self.define("ENABLE_EXPERIMENTAL", False),
        ]
        return args
