from gladier import GladierBaseTool


class TransferData(GladierBaseTool):

    flow_definition = {
        'Comment': 'Transfer a file or directory in Globus',
        'StartAt': 'TransferData',
        'States': {
            "TransferData": {
                "Comment": "Data out of beamline",
                "Type": "Action",
                "ActionUrl": "https://actions.automate.globus.org/transfer/transfer",
                "Parameters": {
                    "source_endpoint_id.$": "$.input.globus_dest_ep",
                    "destination_endpoint_id.$": "$.input.globus_local_ep",
                    "transfer_items": [
                      {
                          "source_path.$": "$.input.local_data_dir",
                          "destination_path.$": "$.input.data_dir",
                          "recursive": True
                      }
                    ]
                },
                "ResultPath": "$.TransferData",
                "WaitTime": 600,
                'End': True
            },
        }
    }

    flow_input = {
        'transfer_sync_level': 'checksum'
    }
    # required_input = [
    #     'transfer_source_path',
    #     'transfer_destination_path',
    #     'transfer_source_endpoint_id',
    #     'transfer_destination_endpoint_id',
    # ]
