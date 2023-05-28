# Workshop rig powered by nodemcu + esphome

## Setup after cloaning

Make sure that you have esp8266/secrets.yaml

There you need to define:

```yaml
wifi_ssid: "SSID1234"
wifi_pass: "password1234"
ota_pass: "password1234"
api_pass: "password1234"
```

NOTICE: api password is obsolete method for authentication.

## Building

Mind the context being the parent directory.

```sh
$ esphome compile esp8266/esp-maze.yaml
```

## Local usage

You can also run the image for local usage. Password is set to `my-password`.

```sh
$ esphome dashboard esp8266/ --open-ui
```
