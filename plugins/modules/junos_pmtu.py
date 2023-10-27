#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 1999-2018, Juniper Networks Inc.
#               2017, Martin Komon
#
# All rights reserved.
#
# License: Apache 2.0
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# * Neither the name of the Juniper Networks nor the
#   names of its contributors may be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Juniper Networks, Inc. ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Juniper Networks, Inc. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: junos_pmtu
short_description: Tests reachability using ping from devices running Juniper JUNOS
description:
- Tests reachability using ping from devices running Juniper JUNOS to a remote destination.
- Tested against Junos (17.3R1.10)
- For a general purpose network module, see the M(ansible.netcommon.net_ping) module.
- For Windows targets, use the M(ansible.windows.win_ping) module instead.
- For targets running Python, use the M(ansible.builtin.ping) module instead.
version_added: 1.0.0
extends_documentation_fragment:
- junipernetworks.junos.junos
author:
- Nilashish Chakraborty (@NilashishC)
options:
  dest:
    description:
    - The IP Address or hostname (resolvable by the device) of the remote node.
    type: str
    required: true
  df_bit:
    description:
    - Determines whether to set the DF bit.
    type: bool
    default: false
  rapid:
    description:
    - Determines whether to send the packets rapidly.
    type: bool
    default: false
  count:
    description:
    - Number of packets to send to check reachability.
    type: int
    default: 5
  source:
    description:
    - The IP Address to use while sending the ping packet(s).
    type: str
  interface:
    description:
    - The source interface to use while sending the ping packet(s).
    type: str
  ttl:
    description:
    - The time-to-live value for the ICMP packet(s).
    type: int
  size:
    description:
    - Determines the size (in bytes) of the ping packet(s).
    type: int
  interval:
    description:
    - Determines the interval (in seconds) between consecutive pings.
    type: int
  state:
    description:
    - Determines if the expected result is success or fail.
    type: str
    choices:
    - absent
    - present
    default: present
notes:
- For a general purpose network module, see the M(ansible.netcommon.net_ping) module.
- For Windows targets, use the M(ansible.windows.win_ping) module instead.
- For targets running Python, use the M(ansible.builtin.ping) module instead.
- This module works only with connection C(network_cli).
"""

EXAMPLES = """
---
- name: Examples of juniper_junos_mtud
  hosts: junos-all
  connection: local
  gather_facts: no
  roles:
    - Juniper.junos

  tasks:
    - name: Perform PMTUD to 192.68.1.1 with default parameters.
      juniper_junos_pmtud:
        dest: "192.68.1.1"

    - name: Perform PMTUD to 192.68.1.1. Register response.
      juniper_junos_pmtud:
        dest: "192.68.1.1"
      register: response
    - name: Print the discovered MTU.
      debug:
        var: response.inet_mtu

    - name: Perform PMTUD to 192.68.1.1. Search all possible MTU values.
      juniper_junos_pmtud:
        dest: "192.68.1.1"
        max_size: 65496
        max_range: 65536
      register: response
    - name: Print the discovered MTU.
      debug:
        var: response.inet_mtu

    - name: Perform PMTUD to 192.68.1.1. Source from ge-0/0/0.0 interface.
      juniper_junos_pmtud:
        dest: "192.68.1.1"
        interface: "ge-0/0/0.0"
      register: response
    - name: Print the discovered MTU.
      debug:
        var: response.inet_mtu

    - name: Perform PMTUD to 192.68.1.1. Source from 192.168.1.2.
      juniper_junos_pmtud:
        dest: "192.68.1.1"
        source: "192.168.1.2"
      register: response
    - name: Print the discovered MTU.
      debug:
        var: response.inet_mtu

    - name: Perform PMTUD to 192.68.1.1. Source from the red routing-instance.
      juniper_junos_pmtud:
        dest: "192.68.1.1"
        routing_instance: "red"
      register: response
    - name: Print the discovered MTU.
      debug:
        var: response.inet_mtu
"""

RETURN = """
changed:
  description:
    - Indicates if the device's state has changed. Since this module
      doesn't change the operational or configuration state of the
      device, the value is always set to C(false).
  returned: when PMTUD successfully executed.
  type: bool
failed:
  description:
    - Indicates if the task failed.
  returned: always
  type: bool
host:
  description:
    - The destination IP/host of the PMTUD as specified by the I(dest)
      option.
    - Keys I(dest) and I(dest_ip) are also returned for backwards
      compatibility.
  returned: when PMTUD successfully executed.
  type: str
inet_mtu:
  description:
    - The IPv4 path MTU size in bytes to the I(dest). This is the lesser of
      I(max_size) and the actual path MTU to I(dest). If the actual path
      MTU is less than I(min_test_size), then a failure is reported. Where
          I(min_test_size) = (I(max_size) - I(max_range) + 1)
  returned: when PMTUD successfully executed.
  type: str
interface:
  description:
    - The source interface of the PMTUD as specified by the I(interface)
      option.
  returned: when the I(interface) option was specified.
  type: str
routing_instance:
  description:
    - The routing-instance from which the PMTUD was performed as specified by
      the I(routing_instance) option.
  returned: when the I(routing_instance) option was specified.
  type: str
source:
  description:
    - The source IP/host of the PMTUD as specified by the I(source)
      option.
    - Key I(source_ip) is also returned for backwards compatibility.
  returned: when the I(source) option was specified.
  type: str
warnings:
  description:
    - A list of warning strings, if any, produced from the ping.
  returned: when warnings are present
  type: list
"""


"""From Ansible 2.1, Ansible uses Ansiballz framework for assembling modules
But custom module_utils directory is supported from Ansible 2.3
Reference for the issue: https://groups.google.com/forum/#!topic/ansible-project/J8FL7Z1J1Mw """


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.junipernetworks.junos.plugins.module_utils.network.junos.junos import (
    get_connection,
)
from ansible_collections.junipernetworks.junos.plugins.modules.junos_ping import (
    build_ping,
    parse_rate,
    parse_rtt,
)


def main():
    INET_MIN_MTU_SIZE = 68
    INET_MAX_MTU_SIZE = 65496

    INET_HEADER_SIZE = 20
    ICMP_HEADER_SIZE = 8
    INET_AND_ICMP_HEADER_SIZE = INET_HEADER_SIZE + ICMP_HEADER_SIZE

    MAX_SIZE_CHOICES = [0] + list(map(lambda x: 2**x, range(1, 17)))

    argument_spec = dict(
        count=dict(type="int", default=5),
        dest=dict(type="str", required=True),
        df_bit=dict(type="bool", default=False),
        rapid=dict(type="bool", default=True),
        source=dict(),
        interface=dict(),
        ttl=dict(type="int"),
        size=dict(type="int"),
        interval=dict(type="int"),
        max_size=dict(type="int", required=False, default=1600),
        max_range=dict(type="int", required=False, choices=MAX_SIZE_CHOICES, default=512),
        state=dict(
            type="str",
            choices=["absent", "present"],
            default="present",
        ),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    dest = module.params["dest"]
    max_size = module.params["max_size"]
    max_range = module.params["max_range"]

    if max_size < INET_MIN_MTU_SIZE or max_size > INET_MAX_MTU_SIZE:
        module.fail_json(
            msg=f"The value of the max_size option({max_size}) "
            f"must be between {INET_MIN_MTU_SIZE} and {INET_MAX_MTU_SIZE}."
        )

    results = {"changed": False, "failed": True, "inet_mtu": 0, "dest": dest}

    size = str(INET_MIN_MTU_SIZE - INET_AND_ICMP_HEADER_SIZE)

    reachability_results = run_ping(module, module.params, size, df_bit=False)
    if int(reachability_results.get("packet_loss", 100)) == 100:
        results["msg"] = f"Basic connectivity to {dest} failed."
        module.exit_json(**results)

    test_size = max_size
    step = max_range
    min_test_size = test_size - (max_range - 1)
    if min_test_size < INET_MIN_MTU_SIZE:
        min_test_size = INET_MIN_MTU_SIZE

    while True:
        if test_size < INET_MIN_MTU_SIZE:
            test_size = INET_MIN_MTU_SIZE
        elif test_size > max_size:
            test_size = max_size

        step = step // 2 if step >= 2 else 0
        size = str(test_size - INET_AND_ICMP_HEADER_SIZE)
        current_results = dict(results)
        current_results = run_ping(module, module.params, size, df_bit=True)
        loss = current_results.get("packet_loss", 100)
        if loss < 100 and test_size == max_size:
            results["failed"] = False
            results["inet_mtu"] = test_size
            break
        elif loss < 100:
            results["failed"] = False
            results["inet_mtu"] = test_size
            test_size += step
        else:
            test_size -= step
        if step < 1:
            break

    if results.get("inet_mtu", 0) == 0:
        module.fail_json(
            msg=f"The MTU of the path to {dest} is less than "
            f"the minimum tested size({min_test_size}). Try "
            f"decreasing max_size({max_size}) or increasing "
            f"max_range({max_range}).",
            **results,
        )

    module.exit_json(**results)


def run_ping(module, params, size, df_bit):
    results = dict()

    count = params["count"]
    dest = params["dest"]
    rapid = params["rapid"]
    source = params["source"]
    ttl = params["ttl"]
    interval = params["interval"]
    interface = params["interface"]

    results["commands"] = build_ping(
        dest,
        count,
        size,
        interval,
        source,
        ttl,
        interface,
        df_bit,
        rapid,
    )

    conn = get_connection(module)
    ping_results = conn.get(results["commands"])

    rtt_info, rate_info = None, None
    for line in ping_results.split("\n"):
        if line.startswith("round-trip"):
            rtt_info = line
        if line.startswith(f"{count} packets transmitted"):
            rate_info = line

    if rtt_info:
        rtt = parse_rtt(rtt_info)
        for k, v in rtt.items():
            if rtt[k] is not None:
                rtt[k] = float(v)
        results["rtt"] = rtt

    pkt_loss, rx, tx = parse_rate(rate_info)
    results["packet_loss"] = int(pkt_loss)
    results["packets_rx"] = int(rx)
    results["packets_tx"] = int(tx)
    return results


if __name__ == "__main__":
    main()
