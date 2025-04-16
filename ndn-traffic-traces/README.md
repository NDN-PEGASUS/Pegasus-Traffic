# NDN Traffic Data Repository

This repository contains captured trace files of NDN traffic from wide-area [NDN testbed](https://named-data.net/ndn-testbed/) routers.
As of this date, the repository contains traces from 4 NDN testbed routers, namely, `Washington University in St. Louis (WUSTL)`, `The University of Arizona`,
`University of Memphis`, and `University of California, Los Angeles (UCLA)` everyday from `2023-04-19` to `2023-06-09` for a duration of 3 hours each day.

Initially, the capture was started with just 2 routers, `WUSTL` and `UCLA` until `2023-05-26`. Then, it was extended to include `The University of Arizona`
and `University of Memphis`. The capture is performed with [unit configuration files](https://github.com/tntech-ngin/ndn-traffic-capture-scripts) deployed on the routers. These unit files make use of [NDN traffic
dumper](https://github.com/usnistgov/ndntdump) based docker container to capture the NDN traffic.

## Trace File Naming Convention
`output-<router-hostname>-<date>-<time>.pcapng.zst`

The `router-hostname` will be one of the following:
- `wundngw`: Washington University in St. Louis (WUSTL)
- `suns.cs.ucla.edu`: University of California, Los Angeles (UCLA)
- `hobo`: The University of Arizona
- `titan`: University of Memphis

## Testbed Topology
The testbed snapshot during the capture period is shown below. The topology is subject to change and thus the [current topology](http://ndndemo.arl.wustl.edu) may not be the same as the one during the capture period.

### Snapshots
- Topology: https://web.archive.org/web/20230328053047/http://ndndemo.arl.wustl.edu
- JSON: https://web.archive.org/web/20230328050116id_/https://ndndemo.arl.wustl.edu/testbed-nodes.json
