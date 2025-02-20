# README

**author: @Rxinui**

## Introduction

This challenge is solved using Python3.12 with built-in modules only.
This repository structure lists the following
```
- main.py: main program running yodelr model
- yodelr.py: Yodelr model file
- BLOG.md: microblog file containing my thoughts at a given time
- docs/: directory containing complementary docs and figures
- .github/**/: CI/CD workflow
- tests/**/: tests files and datasets samples   
```

Concidentally, `yodelr.py` is about micro-message communications platform. As a result, it would be cool to use `BLOG.md` as a real-world dataset.
Hence, the content of `BLOG.md` represents my thoughts expressed with the Yodelr specifications:
- Maximum characters of 140 per message
- Timestamp and author (me) for each message
- Keywords are translated as topics using `#`

## Methodology and strategy

*WIP*

### The `BLOG.md` format

To use this file as a real-world dataset and microblog of my own, the file is structured as follow:
```
@<author> <date -iso-8601> # metadata of the message (author and timestamp)
<                          # start of message right below metadata
  content of the 
  140-max-chars message
>
EOF                        # end of message
                           # newline for visibility
```

with a **First In Last Out** approach -- the most recent message at the top of the file.

#### Example
```
@Rxinui 2025-02-20T15:18:12+01:00
My last one!
EOF

@Rxinui 2025-02-20T15:17:54+01:00
My #first #micromessage.
EOF
```

## Setup

*NOTE: we do it the open-source way*

To facilitate the setup and ensure compliance accross machines, a `Containerfile` is present as evidence and utility to build-and-run the challenge in a clean environment.
In addition, a `Makefile` is provided to initiate manual and automated testing

### Pre-requisites

#### Option 1. All-in-one container (recommended)

- Container Runtime: `podman >=5.4.0` 

### Run yodelr

```shell
make build-podman # Run the container with sandbox and clean environment
```

Create and run a clean Python 3.12 environment with my testing library of my choice.

### Execute automated tests

```shell
make test-in-podman # Run automated tests within container
```

Execute the tests