

#'filename':'workflow.gpx'
#'image':'CeO2_0p1s30f-00001.tif'
#'profile':'pwdr_Sulfur'

def pdf_calc(**data):
    import GSASIIscriptable as G2sc
    filename = data.get('filename')

    # Create workflow GSAS2 project
    gpx = G2sc.G2Project(filename=filename)

    # Load tif images
    g2image = gpx.add_image('CeO2_0p1s30f-00001.tif')
    capillary = gpx.add_image(
        'Capillary_413K-00471.tif')
    gpx.add_image(
        'Sulfur_At2_413K-00147.tif')

    sulfurImage = gpx.images()[2]

    # Load image preset controls (including pre-run calibration) for all images
    for image in gpx.images():
        image.loadControls(
            'parms2.imctrl')

    # Set the background image for sulfur tif
    # sulfurImage.setControls(
    #    {'background image': ['IMG Capillary_413K-00471.tif', -1.0]})

    # Perform the integration and acquire powder list
    pwdrList = sulfurImage.Integrate()
    # G2PwdrData
    pwdrList[0].SaveProfile('pwdr_Sulfur')
    print(pwdrList)

    pdf = gpx.add_PDF('pwdr_Sulfur.instprm', 0)
    pdf.set_formula(['S', 1])
    pdf.data['PDF Controls']['Container']['Name'] = pwdrList[0].name
    pdf.data['PDF Controls']['Container']['Mult'] = -0.988
    pdf.data['PDF Controls']['Form Vol'] = 13.306
    pdf.data['PDF Controls']['Geometry'] = 'Cylinder'
    pdf.data['PDF Controls']['DetType'] = 'Area Detector'
    pdf.data['PDF Controls']['ObliqCoeff'] = 0.2
    pdf.data['PDF Controls']['Flat Bkg'] = 5081
    pdf.data['PDF Controls']['BackRatio'] = 0.184
    pdf.data['PDF Controls']['Ruland'] = 0.1
    pdf.data['PDF Controls']['Lorch'] = True
    pdf.data['PDF Controls']['QScaleLim'] = [23.4, 26.0]
    pdf.data['PDF Controls']['Pack'] = 1.0
    pdf.data['PDF Controls']['Diam'] = 1.5
    pdf.data['PDF Controls']['Trans'] = 0.2
    pdf.data['PDF Controls']['Ruland'] = 0.1
    pdf.data['PDF Controls']['BackRatio'] = 0.184

    pdf.calculate()
    pdf.optimize()
    pdf.export('CeO2', 'I(Q), S(Q), F(Q), G(r), g(r)')

    gpx.save()

@generate_flow_definition()
class GsasPDF(GladierBaseTool):

    required_input = [
        'proc_dir',
        'hdf_file',
        'pilot',
    ]

    funcx_functions = [
        pdf_calc
    ]