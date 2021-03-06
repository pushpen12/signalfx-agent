import os

import pytest

from helpers.kubernetes.utils import get_discovery_rule, run_k8s_monitors_test

pytestmark = [pytest.mark.collectd, pytest.mark.genericjmx, pytest.mark.monitor_with_endpoints]


@pytest.mark.k8s
@pytest.mark.kubernetes
def test_genericjmx_in_k8s(agent_image, minikube, k8s_observer, k8s_test_timeout, k8s_namespace):
    yaml = os.path.join(os.path.dirname(os.path.realpath(__file__)), "genericjmx-k8s.yaml")
    monitors = [
        {
            "type": "collectd/genericjmx",
            "discoveryRule": get_discovery_rule(yaml, k8s_observer, namespace=k8s_namespace),
            "serviceURL": "service:jmx:rmi:///jndi/rmi://{{.Host}}:{{.Port}}/jmxrmi",
            "username": "testuser",
            "password": "testing123",
        }
    ]
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "metrics.txt"), "r") as fd:
        expected_metrics = {m.strip() for m in fd.readlines() if len(m.strip()) > 0}
    run_k8s_monitors_test(
        agent_image,
        minikube,
        monitors,
        namespace=k8s_namespace,
        yamls=[yaml],
        observer=k8s_observer,
        expected_metrics=expected_metrics,
        test_timeout=k8s_test_timeout,
    )
