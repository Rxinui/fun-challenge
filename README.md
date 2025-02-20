# README

Main: ![test-coverage:main](https://github.com/Rxinui/fun-challenge/actions/workflows/ci.yaml/badge.svg?branch=main)

Latest commit pushed: ![test-coverage:push](https://github.com/Rxinui/fun-challenge/actions/workflows/ci.yaml/badge.svg?event=push)

:warning: _PLEASE DO READ ME ENTIRELY, IT IS VERY IMPORTANT._ :warning:

author: @Rxinui

## Introduction

This challenge is solved using Python3.12 with built-in modules only.
The structure of this repository lists the following

```
- yodelr.py: Yodelr model file
- tests/**/: tests files and datasets samples
- docs/: directory containing complementary docs and figures if any
- .github/**/: CI/CD workflows
```

## Analysis, Strategy and Methodology

### Analysis

The Yodelr system induces 2 big challenges:

1. How to structure the data to implement getters in reasonable time
2. How to minimise the time-space complexity of `getTrendingTopic`

On that basis, it seems to be interesting to start with a `v1` to:

- Speed up the implementation of the Yodelr API to identify potential issues and edge cases
- Populate testings with the first prototype. Adapt from `v1` to `v2` if necessary

### Strategy - Roadmap

Create rapidly `v1`:

1. Design a data structure to implement Yodler API
2. Proceed with the joint implementation of tests and features
3. Confirm the test coverage of the Yodler API `v1`

By 26.02.2025, create `v2` which uses a non-linear data structure:

1. Design an optimal (non-)linear data structure to implement Yodler API and outperform `v1`
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

To facilitate the setup and ensure compliance accross machines, a `Dockerfile` is present as evidence and utility to build-and-run the challenge in a clean environment.
In addition, a `Makefile` is provided to initiate manual and automated testing

### Pre-requisites

#### Option 1. All-in-one container (recommended)

- Container Runtime: `podman >=5.4.0`

### Option 1 - Build and run unit tests

```shell
make unittest-in-container
make perftest-in-container # if you want to run perf tests
```

### Option 2 - Build and run main.py

Add your own manual instructions within `main.py` and execute the script

```shell
make run-main # Run main.py within a container
```

### Option 3 - Run tests and perftests on the CI (recommended)

1. Go to [CI workflow](https://github.com/Rxinui/fun-challenge/actions/workflows/ci.yaml) > `Run workflow` > Click on run
2. If workflow is a success, [a new workflow for performance tests will be triggered](https://github.com/Rxinui/fun-challenge/actions/workflows/perftest.yaml)

## Results

### `v1` data structure

![v1](./docs/v1.png)

`v1` uses 3 dictionnaries. The idea behind is to associate an index to a getter's parameter:

- `getPostsForUser` -> one `Index(User,Timestamps)`
- `getPostsForTopic` -> one `Index(Topic,Timestamps)`

and one index to store the data by timestamp `Index(Timestamp,PostData)`. This enable:

- From a `user`, fetch its list of timestamp and get its posts from it
- From a `topic`, fetch its list of timestamp and get its posts from it

However, this _stupid and simple_ idea complexify the `getTrendingTopics` in exchange of quick access using other getters and `addPost`.

**This is not elegant, but it helps to build tests quickly and have a baseline for benchmark.**

### `v2` data structure

![v2](./docs/v2.png)

`v2` uses the same concept as time-serie database (ie. Prometheus), since it is driven by timestamp, having a list of data and an invertedindex allows to balance performance with getters and setters.
- Pros: Quick access from the inverted index -> list of data
- Cons: Processing of extract topics at every call of `getTrendingTopics`. Since, the limitation of a post is 140 chars, it is not that much of an inconvenience.

### Compare `v1` and `v2`


