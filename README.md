# Accordion Umbrel

An Umbrel community app store with one app, Accordion. It lets you install and update Accordion from the umbrelOS dashboard. [Decision 27](https://github.com/accordion-suite/accordion/blob/main/docs/decisions/0027-running-on-umbrelos.md) explains how it works.

This repo is part of [Accordion](https://github.com/accordion-suite/accordion), a self-hosted, zero-telemetry replacement for Google Workspace. Please open issues in the [main repo](https://github.com/accordion-suite/accordion/issues).

## Status

The Accordion app isn't here yet. It's planned once the container image is built and tested on umbrelOS. Until then, the store has no apps to install.

## Layout

```
umbrel-app-store.yml     the store's ID (accordion) and name
accordion-suite/         the app (planned)
  umbrel-app.yml         manifest: version, description, icon, and screenshots
  docker-compose.yml     the container, pinned by tag and digest
  icon.svg, 1.png ...    images the manifest points to
```

umbrelOS shows an app's icon from Umbrel's own gallery unless the manifest sets `icon`, so `icon` and `gallery` give full addresses to the images in this repo.

Each signed Accordion release updates the manifest's version and the image's digest. A script in the `accordion` repo makes that change, so don't edit them by hand.

## Checking

```
python3 scripts/check-store.py
```

CI runs the same check. It needs PyYAML.

## License

[AGPL-3.0 or later](LICENSE)
