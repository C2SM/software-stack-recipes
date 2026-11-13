# prgenv-mch v9 — the MCH software stack

prgenv-mch replaces the MCH v8 software stack (`/mch-environment/v8`).
Like v8, it is mounted permanently on every node at `/mch-environment/v9`:
there is nothing to pull or start with the `uenv` command.

It is built with Spack v1.2 (v8 used Spack v0.22) and GCC 15 (v8 used GCC 12).
The most recent Spack release was used because ICON is the only MCH
production code that is built directly with Spack.

## Getting started

Set up the environment by sourcing the activate script of one of the views:

$ source /mch-environment/v9/activate-mch.sh          # MPI HDF5/NetCDF
$ source /mch-environment/v9/activate-mch-serial.sh   # serial HDF5/NetCDF

Or use modules:

$ module use /mch-environment/v9/modules

Each activate script has exactly the same effect as starting the image as a
uenv with `--view=mch` or `--view=mch-serial`.
Source only one of them per shell: the views are mutually exclusive, and
sourcing a script twice prepends its paths twice.

Because the image is mounted outside a uenv session, it can be combined with a
uenv: `uenv start` and `uenv run` still work with the v9 environment loaded.

## Views

Each view gives a complete build environment with all packages on its own;
the two views differ only in the build of the I/O libraries:

┌────────────┬─────────────────────────────────────────────────┐
│ view       │ HDF5, NetCDF-C and NetCDF-Fortran builds        │
├────────────┼─────────────────────────────────────────────────┤
│ mch        │ MPI                                             │
│ mch-serial │ serial                                          │
└────────────┴─────────────────────────────────────────────────┘

The `mch-serial` view only swaps the I/O libraries: `cray-mpich` and the MPI
compiler wrappers are present in both views.

Both views put gcc, cmake, python and ruby on `PATH`, set `CMAKE_PREFIX_PATH`
and `PKG_CONFIG_PATH`, and set these variables:

  • compilers: `CC`, `CXX`, `FC`, `F77` (gcc 15) and
    `MPICC`, `MPICXX`, `MPIF77`, `MPIF90`
  • eccodes:   `ECCODES_DEFINITION_PATH`, `ECCODES_SAMPLES_PATH`,
               `GRIB_DEFINITION_PATH`, `GRIB_SAMPLES_PATH` (COSMO first)
  • others:    `PROJ_LIB`, `UDUNITS2_XML_PATH`, `HDF5_PLUGIN_PATH`, `GSL_ROOT_DIR`

`CC`/`CXX`/`FC` are new in v9: build systems that read them will now pick up
gcc 15 by default.

## Modules

There is only one compiler, so the `-gcc` suffix has been dropped from
module names:

┌─────────────────┬────────────────────────┬────────────────────────┐
│                 │ v8                     │ v9                     │
├─────────────────┼────────────────────────┼────────────────────────┤
│ most packages   │ eccodes/2.36.4-gcc     │ eccodes/2.47.0         │
│ serial variants │ hdf5/1.12.2-serial-gcc │ hdf5/1.14.6-serial     │
│ MPI             │ cray-mpich-gcc/8.1.30  │ cray-mpich/8.1.32      │
│ gcc, python     │ gcc/12.3.0             │ gcc/15.3.0 (unchanged) │
└─────────────────┴────────────────────────┴────────────────────────┘

The `-serial` suffix is still used for the non-MPI builds of hdf5, netcdf-c
and netcdf-fortran. Modules do not load their dependencies: load gcc,
cray-mpich and the libraries you need explicitly:

$ module use /mch-environment/v9/modules
$ module load gcc cray-mpich hdf5 netcdf-c netcdf-fortran \
      eccodes cosmo-eccodes-definitions

## Packages

┌─────────────────────────────────┬──────────────┬────────────────┐
│ package                         │ v8           │ v9             │
├─────────────────────────────────┼──────────────┼────────────────┤
│ gcc                             │ 12.3.0       │ 15.3.0         │
│ cray-mpich                      │ 8.1.30       │ 8.1.32         │
│ libfabric                       │ 1.15.2.0     │ 2.3.1          │
│ cmake                           │ 3.24.4       │ 3.31.12        │
│ python                          │ 3.10.13      │ 3.12.14        │
│ ruby                            │ 3.1.0        │ 3.3.5          │
│ osu-micro-benchmarks            │ 5.9          │ 5.9            │
│ openblas                        │ 0.3.26       │ 0.3.34         │
│ netlib-scalapack                │ 2.2.0        │ 2.2.3          │
│ libfyaml                        │ 0.7.12 / 0.8 │ 0.9            │
│ libaec                          │ 1.0.6        │ 1.1.7          │
│ eccodes                         │ 2.36.4       │ 2.47.0         │
│ cosmo-eccodes-definitions       │ —            │ 2.47.0.2 (new) │
│ hdf5 (MPI and serial)           │ 1.12.2       │ 1.14.6         │
│ netcdf-c (MPI and serial)       │ 4.8.1        │ 4.10.0         │
│ netcdf-fortran (MPI and serial) │ 4.5.4        │ 4.6.4          │
│ nco                             │ 5.0.1        │ 5.4.0          │
│ cdo                             │ 2.0.5        │ 2.6.4          │
│ nvhpc, cuda                     │ 24.5, 12.3.0 │ removed        │
│ libtree, tree                   │ 3.1.1, 2.1.0 │ removed        │
└─────────────────────────────────┴──────────────┴────────────────┘

## Removed in v9

  • ICON build dependencies: ICON is the only MCH production code built
    directly with Spack, so the packages that existed only to build it are
    gone: the whole prgenv-nvidia environment (nvhpc, cuda, and the NVHPC
    builds of eccodes, hdf5, netcdf-c/fortran, openblas and
    osu-micro-benchmarks), python/3.11.7 and cray-pals.
  • The tools environment: python and ruby moved into the main environment.
    libtree and tree were dropped.
  • Modules for dependencies: v8 made modules for most dependencies
    (autoconf, curl, perl, zlib-ng, proj, ...). v9 only makes modules for
    the packages listed above.

## cosmo-eccodes-definitions

cosmo-eccodes-definitions is new: it was not in the v8 software stack.
C2SM used to maintain a Spack package for it, but `spack-c2sm` no longer
provides one, and the old one did not support the requested version.

**A Spack package was created for the requested version: it is up to MCH to**
**validate it and fix any issues with it.**

It installs the COSMO GRIB definitions and samples that match eccodes 2.47.0.
Loading its module, or sourcing either activate script, sets
`ECCODES_DEFINITION_PATH`, `GRIB_DEFINITION_PATH`, `ECCODES_SAMPLES_PATH` and
`GRIB_SAMPLES_PATH`, with the COSMO definitions ahead of the eccodes defaults.

## More information

The recipe used to build this image is in `/mch-environment/v9/meta/recipe`.
