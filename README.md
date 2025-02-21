# README

![test-coverage:main](https://github.com/Rxinui/fun-challenge/actions/workflows/ci.yaml/badge.svg?branch=main)
![test-coverage:push](https://github.com/Rxinui/fun-challenge/actions/workflows/ci.yaml/badge.svg?event=push)

:warning: _PLEASE DO READ ME ENTIRELY, IT IS VERY IMPORTANT._ :warning:

author: @Rxinui

## Introduction

This challenge is solved using Python3.12 with built-in modules only.
The structure of this repository lists the following

```
- yodelr.py: Yodelr model file
- BLOG.md: microblog file containing my thoughts at a given time
- tests/**/: tests files and datasets samples
- docs/: directory containing complementary docs and figures
- .github/**/: CI/CD workflows
```

Coincidentally, `yodelr.py` is about micro-message communications platform. As a result, it would be cool to use `BLOG.md` as a real-world dataset.
Hence, the content of `BLOG.md` represents my thoughts expressed with the Yodelr specifications:

- Maximum characters of 140 per message
- Timestamp and author (me) for each message
- Keywords are using `#` to emphasise (and represent a topic)

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

## Analysis, Strategy and Methodology

_WIP_

### Analysis

The Yodelr system induces 2 big challenges:

1. How to structure the data to implement getters in reasonable time (equal or less than `O(N)`)
2. Which of the operation should be more expensive between **write**, **read** or **delete** (inherent to the data structure chosen)

There are two types of data structures: **linear** and **non-linear**, where the latter is generally more performant at a cost of higher _Time To Market_ and more complex implementation.

On that basis, it seems to be interesting to start with a `v1` that uses a linear data structure to:

- Speed up the implementation of the Yodelr API to identify potential issues and edge cases
- Populate testings with the first prototype. In fact, since the API interface is immutable as a rule, the unit and performance testings once written for `v1` won't change for future releases.

### Strategy - Roadmap

In less than 2 hours, create `v1`:

1. Design an optimal linear data structure to implement Yodler API
2. Proceed with the joint implementation of tests and features
3. Confirm the test coverage of the Yodler API `v1`

By 24.02.2025, create `v2` which uses a non-linear data structure:

1. Design an optimal non-linear data structure to implement Yodler API and outperform `v1`
2. Proceed with to the implementation of helpers function that manages the data structure
3. Implement the Yodler API functions
4. Confirm the test coverage of the Yodler API `v2`

By the deadline, if my schedule allows it, create a `v3` which uses advanced algorithm to perform better than `v2`

1. Tweak methods, functions and if requires, the data structure, to reduce the time complexity.
2. Confirm the test coverage of the Yodler API `v3`

### Methodology

**NO AGILE METHODS. THAT IS SUCH A BAD IDEA (here)**

- For such small use case, the most important is to **remain organised** and set a clear direction (and stick to it).
- **Priority is given to tests**, to finish the Mission (`v1`). What is the purpose of having the most optimal solution (`v2`, maybe `v3`) if the mission is not achieved? :nerd_face:
- GitHub Release from tags `v1`, `v2` and potentially `v3`, through CI/CD
- Trunk-Based Development (TBD) as git flow is best-suited here for a single-engineer fan of CI.

## Setup

_NOTE: we do it the open-source way_

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
