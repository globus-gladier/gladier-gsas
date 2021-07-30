
from gladier import GladierBaseTool


class TransferResult(GladierBaseTool):

    flow_definition = {
        'Comment': 'Transfer a file or directory in Globus',
        'StartAt': 'TransferResult',
        'States': {
      "TransferResult": {
      "Comment": "Initial transfer",
      "Type": "Action",
      "ActionUrl": "https://actions.automate.globus.org/transfer/transfer",
      "Parameters": {
        "source_endpoint_id.$": "$.input.globus_local_ep", 
        "destination_endpoint_id.$": "$.input.globus_dest_ep",
        "sync_level": 1,
        "transfer_items": [
          {
            "source_path.$": "$.input.proc_dir",
            "destination_path.$": "$.input.local_dir",
            "recursive": True
          }
        ]
      },
      "ResultPath": "$.TransferResult",
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
    #     'transfer_recursive',
    # ]

