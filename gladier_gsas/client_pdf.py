from gladier import GladierBaseClient, generate_flow_definition


@generate_flow_definition()
class PDFClient(GladierBaseClient):
    gladier_tools = [
        'gladier_gsas.tools.TransferData',
        'gladier_gsas.tools.GSASPDF',
        'gladier_gsas.tools.TransferResult',
    ]

