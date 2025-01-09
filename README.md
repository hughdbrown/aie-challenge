# Purpose
This project is a response to the [AI Engineering Bootcamp challenge](https://aimakerspace.io/aie-challenge/). It is an application written in python that uses:
- python: chainlit, openai
- Docker

The instructions are not clear whether it is necessary that the app be a web app, so the final product may use FastAPI (or not).

# Setup
## src/.env
To run OpenAI models, you need the `OPENAI_API_KEY` environment variable. Adding the file `src/.env` will cause this to be injected into the runtime environment. Your `src/.env` file shold look like this:

```
OPENAI_API_KEY="<some-value>"
```

# Docker problem
My docker installation is currently a bit broken. I try to build a docker image from a Dockerfile and I get:
```
~/w/hu/aie-challenge main ?3 ❯ docker build .                                                               aie-challenge-3.11.0 3.11.0 13:18:33
failed to fetch metadata: signal: killed

DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/
```

So I `brew install` the plugin:

```
~/w/hu/aie-challenge main ?3 ❯ brew install docker-buildx                                     ✘ 255 1m 17s  aie-challenge-3.11.0 3.11.0 13:20:21
==> Auto-updating Homebrew...
Adjust how often this is run with HOMEBREW_AUTO_UPDATE_SECS or disable with
HOMEBREW_NO_AUTO_UPDATE. Hide these hints with HOMEBREW_NO_ENV_HINTS (see `man brew`).
==> Auto-updated Homebrew!
Updated 4 taps (homebrew/services, mongodb/brew, homebrew/core and homebrew/cask).

...

==> Downloading https://ghcr.io/v2/homebrew/core/docker-buildx/manifests/0.19.3
########################################################################################################################################### 100.0%
==> Fetching docker-buildx
==> Downloading https://ghcr.io/v2/homebrew/core/docker-buildx/blobs/sha256:35d5b5977910f33b2ed7c749477cd8de134ac8243511e9db5624c36d2c506aef
########################################################################################################################################### 100.0%
==> Pouring docker-buildx--0.19.3.arm64_sequoia.bottle.tar.gz
==> Caveats
docker-buildx is a Docker plugin. For Docker to find the plugin, add "cliPluginsExtraDirs" to ~/.docker/config.json:
  "cliPluginsExtraDirs": [
      "/opt/homebrew/lib/docker/cli-plugins"
  ]

zsh completions have been installed to:
  /opt/homebrew/share/zsh/site-functions
==> Summary
🍺  /opt/homebrew/Cellar/docker-buildx/0.19.3: 29 files, 55.5MB
==> Running `brew cleanup docker-buildx`...
Disable this behaviour by setting HOMEBREW_NO_INSTALL_CLEANUP.
Hide these hints with HOMEBREW_NO_ENV_HINTS (see `man brew`).
```

Then I update `~/.docker/config.json` as described:
```
~/w/hu/aie-challenge main !1 ?3 ❯ more ~/.docker/config.json                                        1m 23s  aie-challenge-3.11.0 3.11.0 13:26:15
{
        "auths": {
                "https://index.docker.io/v1/": {}
        },
        "credsStore": "desktop",
        "experimental": "disabled",
        "currentContext": "desktop-linux",
        "cliPluginsExtraDirs": [
                "/opt/homebrew/lib/docker/cli-plugins"
        ]
}
```

And my docker hangs when I build.
