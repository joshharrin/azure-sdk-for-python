# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import functools
import os
from typing import Any, Optional, Dict

from azure.core.pipeline.transport import HttpRequest

from .._constants import EnvironmentVariables
from .._internal.managed_identity_client import ManagedIdentityClient
from .._internal.managed_identity_base import ManagedIdentityBase


class CloudShellCredential(ManagedIdentityBase):
    def get_client(self, **kwargs: Any) -> Optional[ManagedIdentityClient]:
        url = os.environ.get(EnvironmentVariables.MSI_ENDPOINT)
        if url:
            return ManagedIdentityClient(
                request_factory=functools.partial(_get_request, url), base_headers={"Metadata": "true"}, **kwargs
            )
        return None

    def get_unavailable_message(self, desc: str = "") -> str:
        return f"Cloud Shell managed identity configuration not found in environment. {desc}"


def _get_request(url: str, scope: str, identity_config: Dict) -> HttpRequest:
    request = HttpRequest("POST", url, data=dict({"resource": scope}, **identity_config))
    return request
