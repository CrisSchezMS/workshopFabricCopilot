import io
import json
import unittest

from tools.preflight import BASE, inspect, pages


class Response(io.BytesIO):
    def __init__(self, value):
        super().__init__(json.dumps(value).encode())


class Opener:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def open(self, request, timeout):
        self.calls.append(request)
        return Response(next(self.responses))


class PreflightTests(unittest.TestCase):
    def test_pagination_and_header(self):
        client = Opener([{"value": [{"displayName": "other"}],
                          "continuationUri": BASE + "/v1/workspaces?page=2"},
                         {"value": [{"displayName": "target", "id": "id", "capacityId": "c"}]},
                         {"value": [{"id": "c", "state": "Active", "sku": "F16"}]},
                         {"value": [{"displayName": "demo", "type": "Lakehouse"}]}])
        result = inspect("target", "fake", client)
        self.assertEqual(result["capacity_state"], "Active")
        self.assertEqual(result["items"], [{"name": "demo", "type": "Lakehouse"}])
        self.assertTrue(all(c.get_header("X-ms-fabric-skill") == "search-consumption-cli" for c in client.calls))

    def test_rejects_external_continuation_without_sending_token(self):
        client = Opener([{"value": [], "continuationUri": "https://evil.invalid/v1/workspaces"}])
        with self.assertRaises(ValueError):
            pages(BASE + "/v1/workspaces", "fake", client)
        self.assertEqual(len(client.calls), 1)

    def test_unavailable_workspace_is_not_created(self):
        with self.assertRaisesRegex(ValueError, "0 workspaces"):
            inspect("missing", "fake", Opener([{"value": []}]))


if __name__ == "__main__":
    unittest.main()
