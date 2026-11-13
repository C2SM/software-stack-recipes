This software stack uses spack v0.21, to macth the spack-c2sm distribution

## Build notes

### Custom spack packages (`repo/packages/`)

* `cosmo_eccodes_definitions` — not in upstream spack-packages.
  Ported from the old spack-c2sm package to Spack v1 style (`from spack.package import *`, `maintainers(...)`).
    * source: https://github.com/COSMO-ORG/eccodes-cosmo-resources, versions use release tags pinned to commits
      (`v2.47.0.2`, `v2.47.0.1`); older versions were dropped.
    * `@2.47.0.1:2.47.0.2` depends on `eccodes@2.47.0`: the COSMO definitions must match the ecCodes release.
      When bumping eccodes, add the matching `v<eccodes-version>.N` tag of eccodes-cosmo-resources.
    * installs `definitions/`, `samples/` and `RELEASE` under `<prefix>/cosmoDefinitions`.
    * `setup_run_environment` sets `ECCODES_DEFINITION_PATH`/`GRIB_DEFINITION_PATH` (COSMO definitions first, then eccodes')
      and `ECCODES_SAMPLES_PATH`/`GRIB_SAMPLES_PATH`. These end up both in the `mch`/`mch-serial` views and in the
      `cosmo-eccodes-definitions` module.
    * Verified: `codes_info` in the `mch` view reports the COSMO definitions path, and `grib_ls` reads
      `COSMO_GRIB2_default.tmpl` from the samples.

### Modules

* `gcc@15` gets no module by default: stackinator builds it in the compiler step, so it is an
  *implicit* spec in the store DB and `exclude_implicits: true` drops it. `modules.yaml` lists
  `include: ['gcc@15']`, which overrides `exclude_implicits` (it does not match the system `gcc@12.3.0` external).
  `hide_implicits` is `false`, otherwise the gcc module would be generated but hidden from `module avail`.
  Since every other implicit is excluded anyway, this setting only changes gcc.

### Mount point and build cache

* `store: /mch-environment/v9` — the image is mounted permanently at this path on boot (sysadmin-configured),
  not started with `uenv start`. The store path is baked into RPATHs, so it must not change.
* `mount_specific: true` keys the build cache at `uenv-cache/mch-environment/v9`. The first build at this mount
  (2026-10-09) was a cold, full from-source build; 105 specs were pushed.
* The two `perl` installs are never pushed: Stackinator's `cache-push` target excludes `perl`, `cuda` and `nvhpc`,
  so they are rebuilt every time. This is expected.

### Post-install hook (`post-install`) and `extra/`

`extra/` is copied to `<mount>/meta/extra`; the hook runs the scripts from there. Keep code out of the hook
itself: it is a Jinja template, so `{%`, `{{` and `{#` in it break `stack-config`.

* **Activate scripts** (`extra/make-activate.py`): writes `<mount>/activate-mch.sh` and
  `<mount>/activate-mch-serial.sh` from the view environments in `meta/env.json`, the same data `uenv` uses.
  The Spack-generated `env/<view>/activate.sh` must not be used: they reproduce Spack's build environment
  (build-time `PATH`, `SPACK_ENV` pointing at the build dir), not the view environment stackinator filters.
  Verified: sourcing them under a bare `squashfs-mount` gives an environment identical to
  `uenv run --view=<view>`, apart from `UENV_*`/`SQUASHFS_MOUNT_LIST` (deliberately not set: they would make
  `uenv` think a session is running) and `TMPDIR=/tmp` (set by uenv for every session).
* **README** (`extra/render-readme.py`, source `extra/README.md`): rendered with ANSI colours to `<mount>/README`,
  so `cat /mch-environment/v9/README` is readable. Markup: `# `/`## ` headings, `` `code` ``, `**bold**`,
  `$ ` command lines (continued with a trailing `\`), box-drawing tables. Keep rendered lines <= 80 columns.
  Package versions in the table are maintained by hand: update them when the specs change.

### Runtime notes

* `nf-config --flibs` gives `-L` for netcdf-fortran only, not netcdf-c, and no rpath (same under `uenv --view`).
  Link against the view with `-L<view>/lib -Wl,-rpath,<view>/lib`.
