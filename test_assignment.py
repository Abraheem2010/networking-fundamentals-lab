"""Unit tests for the networking lab.

Run with either:
    python -m pytest test_assignment.py
    python test_assignment.py          (built-in fallback runner, no pytest needed)

Covers the pure-logic tasks: Task 2 (AIMD) and Task 3 (IPv4 / CIDR).
Task 1 is network-dependent (needs the echo server) and is exercised manually.
"""
import random

import task2_tcp_window as t2
import task3_ip_calc as t3


# ---------- Task 2: AIMD ----------

def test_aimd_additive_increase():
    # no loss -> window grows by one MSS
    assert t2.aimd_step(4, False) == 5


def test_aimd_multiplicative_decrease():
    # loss -> window is halved
    assert t2.aimd_step(8, True) == 4


def test_aimd_floor_is_one():
    # halving must never drop the window below 1 MSS
    assert t2.aimd_step(1, True) == 1


def test_trial_loss_is_deterministic_with_seed():
    # the same seed must reproduce the same loss sequence
    seq1 = [t2.trial_loss(0.2, random.Random(42)) for _ in range(5)]
    seq2 = [t2.trial_loss(0.2, random.Random(42)) for _ in range(5)]
    assert seq1 == seq2


def test_trial_loss_bounds():
    assert t2.trial_loss(0.0, random.Random(0)) is False   # never lose
    assert t2.trial_loss(1.0, random.Random(0)) is True    # always lose


# ---------- Task 3: IPv4 / CIDR ----------

def test_ip_to_int_roundtrip():
    for ip in ["0.0.0.0", "192.168.1.1", "255.255.255.255", "10.100.102.32"]:
        assert t3.int_to_ip(t3.ip_to_int(ip)) == ip


def test_ip_to_int_known_value():
    assert t3.ip_to_int("192.168.1.1") == 0xC0A80101


def test_cidr_to_mask():
    assert t3.cidr_to_mask(24) == 0xFFFFFF00
    assert t3.cidr_to_mask(0) == 0x00000000
    assert t3.cidr_to_mask(32) == 0xFFFFFFFF


def test_network_info_class_c():
    info = t3.network_info_from_cidr("192.168.1.0/24")
    assert info["network"] == "192.168.1.0"
    assert info["broadcast"] == "192.168.1.255"
    assert info["first_host"] == "192.168.1.1"
    assert info["last_host"] == "192.168.1.254"
    assert info["hosts_count"] == 254


def test_network_info_from_host_address():
    # a host address inside the block resolves to the same network
    info = t3.network_info_from_cidr("192.168.1.89/24")
    assert info["network"] == "192.168.1.0"
    assert info["broadcast"] == "192.168.1.255"
    assert info["hosts_count"] == 254


def test_network_info_slash30():
    info = t3.network_info_from_cidr("10.0.0.0/30")
    assert info["network"] == "10.0.0.0"
    assert info["broadcast"] == "10.0.0.3"
    assert info["first_host"] == "10.0.0.1"
    assert info["last_host"] == "10.0.0.2"
    assert info["hosts_count"] == 2


def test_network_info_slash32_single_host():
    info = t3.network_info_from_cidr("8.8.8.8/32")
    assert info["network"] == "8.8.8.8"
    assert info["broadcast"] == "8.8.8.8"
    assert info["hosts_count"] == 1


def test_network_info_slash31_point_to_point():
    info = t3.network_info_from_cidr("192.168.1.0/31")
    assert info["network"] == "192.168.1.0"
    assert info["broadcast"] == "192.168.1.1"
    assert info["first_host"] == "192.168.1.0"
    assert info["last_host"] == "192.168.1.1"
    assert info["hosts_count"] == 2


def test_ip_to_int_rejects_invalid_octet():
    # an octet above 255 must be rejected, not silently wrapped
    try:
        t3.ip_to_int("999.1.1.1")
        assert False, "expected ValueError for an octet > 255"
    except ValueError:
        pass


# ---------- simple fallback runner (no pytest required) ----------

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in tests:
        try:
            fn()
            print(f"PASS  {fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {fn.__name__}: {e}")
        except Exception as e:  # noqa: BLE001 - report unexpected errors
            print(f"ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
    # exit non-zero when something failed, so CI fails too
    raise SystemExit(0 if passed == len(tests) else 1)
