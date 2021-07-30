# Enable Gladier Logging
# import gladier.tests

import argparse
import os
import glob


def register_container():
    from funcx.sdk.client import FuncXClient
    fxc = FuncXClient()
    ##
    from gladier_gsas.tools.gsas_pdf import gsas_pdf
    cont_dir = '/eagle/APSDataAnalysis/GSAS_PDF/containers/'
    container_name = 'gsas2.sif'
    cont_id = fxc.register_container(location=cont_dir+container_name,container_type='singularity')
    return fxc.register_function(gsas_pdf, container_uuid=cont_id)

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hdf', help='Path to the hdf file',
                        default='/data/xpcs8/2019-1/comm201901/cluster_results/')

    return parser.parse_args()


datadirs = ["/eagle/APSDataAnalysis/GSAS_PDF/LiquidSulfur/Experimental data/Sample 1 Heat - Tues",
    "/eagle/APSDataAnalysis/GSAS_PDF/LiquidSulfur/Experimental data/Sample 1 Heat - Tues",
    ]


if __name__ == '__main__':

    args = arg_parse()

    pdfs = []

    datadir = datadirs[0]
    # for datadir in datadirs:

    base_input = {
        # 'filename': datadir + '/sulfur-test.gpx',
        # 'outputfig': datadir + '/sulfur.png',
        # 'datadir': datadir,
        # 'export': {
        #     'prefix': datadir + '/Sulfur_At2_413K-00147'
        # },
        # 'limits': {
        #     'xlim': [0.012914191411475429, 24.096733130017093],
        #     'ylim': [-1.937982691074275, 4.881099529628997]
        # },
        # 'images': {
        #     'CeO2': datadir2 + '/CeO2_0p1s30f-00001.tif',
        #     'Capillary': datadir2 + '/Capillary_413K-00471.tif',
        #     'Sulfur': datadir + '/Sulfur_At2_413K-00147.tif'
        # },
        # 'controls': {
        #     'CeO2': datadir2 + '/ceo2.imctrl',
        #     'Capillary': datadir2 + '/capillary.imctrl',
        #     'Sulfur': datadir2 + '/sulfur.imctrl'
        # },
        # 'powders': {
        #     'Sulfur': datadir2 + '/pwdr_Sulfur.instprm'
        # },

        'data_dir' : 'xxx',
        'proc_dir' : 'yyy',

        # Should think of moving those to a cfg with better naming
        'funcx_endpoint_non_compute':'e449e8b8-e114-4659-99af-a7de06feb847',
        'funcx_endpoint_compute':    '4c676cea-8382-4d5d-bc63-d6342bdb00ca',


        # globus endpoints
        'globus_endpoint_local': args.source_globus_ep,
        'globus_endpoint_theta': args.compute_globus_ep,

        # container hack for corr 
        'gsas_pdf_funcx_id': register_container()
    }

    tifs = glob.glob(datadir + "/*.tif")
    for tif in tifs:
        _tif = os.path.basename(tif)
        data['export']['prefix'] = datadir + '/' + _tif.split('.')[0]
        data['filename'] = datadir + '/' + _tif.split('.')[0] + '.gpx'
        data['outputfig'] = datadir + '/' + _tif.split('.')[0] + '.png'
        data['images']['Sulfur'] = datadir + '/' + _tif

        pdf = generate_pdf(inputs=[data])
        pdfs += [pdf]

    [pdf.result() for pdf in pdfs]


    from gladier_gsas.client_pdf import PDFClient
    pdf_cli = PDFClient()

    pdf_flow_label = hdf_name
    #print(pdf_flow_label)
    pdf_flow = pdf_cli.run_flow(flow_input=flow_input, label=pdf_flow_label)

    print('flow_id : ' + pdf_cli.get_flow_id)
    print('run_id : ' + pdf_flow['action_id'])
