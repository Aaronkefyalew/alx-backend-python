#!/usr/bin/env python3
"""
Test module for client.py
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Test class for GithubOrgClient
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        test_payload = {"org": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected value"""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected list of repos"""
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = test_repos_payload

        test_repos_url = "https://api.github.com/orgs/testorg/repos"

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_repos_url

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            expected_repos = ["repo1", "repo2"]
            self.assertEqual(result, expected_repos)

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns expected boolean"""
        client = GithubOrgClient("testorg")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for GithubOrgClient
    """

    @classmethod
    def setUpClass(cls):
        """Set up class for integration tests"""
        cls.get_patcher = patch('client.requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if "orgs/google" in url:
                return Mock(json=lambda: cls.org_payload)
            elif "repos" in url and "google" in url:
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: {})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class after integration tests"""
        cls.get_patcher.stop()

    def test_public_repos_integration(self):
        """Integration test for public_repos method"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license_integration(self):
        """Integration test for public_repos with license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
