import pytest
import unittest
from unittest.mock import MagicMock, patch
from argparse import Namespace
from my_functions_beatzaplenty.resize_linode_instance import main

class TestMainFunction(unittest.TestCase):

    @patch('my_functions_beatzaplenty.resize_linode_instance.linode_api.LinodeClient')
    @patch('my_functions_beatzaplenty.resize_linode_instance.linode.wait_for_completion')
    @patch('my_functions_beatzaplenty.resize_linode_instance.linode.wait_for_instance_state')
    def test_main(self, mock_LinodeClient, mock_wait_for_completion, mock_wait_for_instance_state):
        # Set up environment variables
        monkeypatch = MagicMock()
        monkeypatch.setenv('LINODE_API_KEY', '49701e88c9484fdb67b1a86ebb8048837a72d15dd4921c91c77920f9397e2a5d')

        # Set up configuration
        config = MagicMock()
        config.get.return_value = 'docker'
        
        # Set up Linode instances to simulate the scenario where the Linode with label 'docker' is not found
        mock_linode_instances = []

        # Mock Linode API client and instance
        mock_linode_instance = MagicMock()
        mock_linode_instance.id = 53508525
        mock_linode_instance.label = 'docker'
        mock_linode_instance.type.id = 'g6-nanode-1'

        mock_api_client = MagicMock()
        mock_api_client.linode.instances.return_value = mock_linode_instances
        mock_LinodeClient.return_value = mock_api_client

        # Mock linode.polling.event_poller_create
        mock_event_poller = MagicMock()
        mock_api_client.polling.event_poller_create.return_value = mock_event_poller

        # Mock linode.get_type_label
        mock_get_type_label = MagicMock()
        mock_get_type_label.return_value = 'Nanode 1GB'

        # Execute main function and assert ValueError is raised
        with self.assertRaises(SystemExit) as cm:
            main(config, arg_direction=None, arg_monitor=False)

        # Assert that Linode API client is called with the correct parameters
        mock_LinodeClient.assert_called_once_with('49701e88c9484fdb67b1a86ebb8048837a72d15dd4921c91c77920f9397e2a5d')
        mock_api_client.linode.instances.assert_called_once_with(main.linode_api.Instance.label == 'docker', any())

        # Assert that linode.wait_for_completion is called
        mock_wait_for_completion.assert_called_once()

        # Assert that linode.wait_for_instance_state is not called when arg_monitor is False
        #mock_wait_for_instance_state.assert_not_called()


if __name__ == '__main__':
    pytest.main()
