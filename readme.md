# uenv Recipes for Alps

A repository with the uenv recipes used by C2SM, EXCLAIM and MeteoSchweiz.

## Accessing private repositories

Some images require cloning private git repositories.
The credentials for providers must be set as environment variables inside the pipeline.
These variables are set in the `climate-weather-uenv` project on the [CSCS CI-CD service](https://cicd-ext-mw.cscs.ch/ci/overview).

Note that only project admins can set these variables, so you should contact @bcumming

```bash
# the number of configurations, currently one
# increment when adding new credentials
UENV_CIBUILDV_GIT_CONFIG_COUNT=1

# for each provider set the following values (with a new index):
# replace ${NAME} and ${TOKEN} with literal values
UENV_CIBUILDV_GIT_CONFIG_VALUE_0=git@gitlab.dkrz.de:
UENV_CIBUILDV_GIT_CONFIG_KEY_0=url.https://${NAME}:${TOKEN}@gitlab.dkrz.de/.insteadOf
```

The `NAME` is specific to the git provider:

| provider | `NAME`           |
| -------- | ---------------- |
| GitHub   | `x-access-token` |
| GitLab   | `oauth2`         |

