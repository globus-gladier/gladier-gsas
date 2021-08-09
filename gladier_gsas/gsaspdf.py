import json

from gladier import GladierBaseClient, generate_flow_definition, GladierBaseTool


@generate_flow_definition()
class PDFClient(GladierBaseClient):
    gladier_tools = [
        #'gladier_gsas.tools.TransferData',
        'gladier_gsas.tools.GSASPDF',
        #'gladier_gsas.tools.TransferResult',
    ]


pdfClient = PDFClient()

print(pdfClient.flow_definition)

##Remote endpoints
fx_endpoint_queue = '09d6ff75-c4fd-4a38-a716-705cabe34178'
fx_endpoint_local = 'ebd3738f-4070-4513-b9db-da70f3167108'

fx_endpoint = '09d6ff75-c4fd-4a38-a716-705cabe34178'  # queue

datadir = "/grand/APSWorkflows/LiquidSulfur/Experimental data/Sample 1 Heat - Tues"
datadir2 = "/grand/APSWorkflows/LiquidSulfur/Experimental data/Sample 2 Heat - Wed"

data = {
    'filename': datadir + '/sulfur-test.gpx',
    'outputfig': datadir + '/sulfur.png',
    'datadir': datadir,
    'export': {
        'prefix': datadir + '/Sulfur_At2_413K-00147'
    },
    'limits': {
        'xlim': [0.012914191411475429, 24.096733130017093],
        'ylim': [-1.937982691074275, 4.881099529628997]
    },
    'images': {
        'CeO2': datadir + '/CeO2_0p1s30f-00001.tif',
        'Capillary': datadir2 + '/Capillary_413K-00471.tif',  # Default capillary
        'Sulfur': datadir2 + '/Sulfur_At2_413K-00147.tif'
    },
    'controls': {
        'CeO2': datadir2 + '/ceo2.imctrl',  # Presaved control settings
        'Capillary': datadir2 + '/capillary.imctrl',  # Presaved control settings
        'Sulfur': datadir2 + '/sulfur.imctrl'  # Presaved control settings
    },
    'powders': {
        'Sulfur': datadir2 + '/pwdr_Sulfur.instprm'  # Presaved powder
    }
}


##Input with automate format.
flow_input = {
    "input": {
        "funcx_endpoint_compute": fx_endpoint,
        "data": data,
        "config": {
            "Formula": ['S', 1],
            "Container": {
                "Mult": -0.988
            },
            "Form Vol": 13.306,
            "Geometry": "Cylinder",
            "DetType": "Area Detector",
            "ObliqCoeff": 0.2,
            "Flat Bkg": 5081,
            "BackRatio": 0.184,
            "Ruland": 0.1,
            "Lorch": True,
            "QScaleLim": [
                23.4,
                26.0
            ],
            "Pack": 1.0,
            "Diam": 1.5,
            "Trans": 0.2,
            "Rmax": 20.0
        }
    }
}

# notice this input can be used directly on automate website.
print(json.dumps(flow_input, indent=2))

run_label = 'GladierTest_v1'

example_flow = pdfClient.run_flow(flow_input=flow_input)
pdfClient.progress(example_flow['action_id'])

print(pdfClient.get_details(example_flow['action_id'], 'GSASPDF'))

print('https://app.globus.org/flows/%s/runs/%s' %
      (example_flow['flow_id'], example_flow['action_id']))

#pdfClient.get_details(example_flow['action_id'], 'GSASPDF')
