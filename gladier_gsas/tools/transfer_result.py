
from gladier import GladierBaseTool


class TransferResult(GladierBaseTool):

    flow_definition = {
        'Comment': 'Transfer a file or directory in Globus',
        'StartAt': 'TransferResult',
        'States': {
            "TransferResult": {
                "Comment": "Result transfer",
                "Type": "Action",
                "ActionUrl": "https://actions.automate.globus.org/transfer/transfer",
                "Parameters": {
                    "source_endpoint_id": "08925f04-569f-11e7-bef8-22000b9a448b",
                    "destination_endpoint_id": "4f331976-e823-11ea-8bc2-029866a337f1",
                    "sync_level": 1,
                    "transfer_items": [
                      {
                          "source_path": "/grand/APSWorkflows/dgovoni/input/Experimental\ data/Sample\ 1\ Heat\ -\ Tues/charts/",
                          "destination_path": "/LiquidSulfur/Experimental data/Sample 1 Heat - Tues/charts",
                          "recursive": True
                      }
                    ]
                },
                "ResultPath": "$.TransferResult",
                "WaitTime": 600,
                'End': True
            }
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
    #     'transfer_recursive',
    # ]
