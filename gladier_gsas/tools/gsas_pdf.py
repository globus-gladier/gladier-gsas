from gladier import GladierBaseTool, generate_flow_definition


def generate_sulfur_pdf(**inputdata):
    import os
    import sys
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import axhline
    from matplotlib.axis import Axis
    import GSASIIscriptable as G2sc
    import sys

    sys.path.append("/home/dgovoni/miniconda3/GSASII")
    data = inputdata.get('data')
    config = inputdata.get('config')

    def generate_charts(data, prefix, dest, xlabel, ylabel, volume):
        import plotly.graph_objects as go
        import plotly

        import numpy as np

        x, y = np.loadtxt(data, unpack=True)

        layout = go.Layout(
            title=prefix,
            xaxis=dict(
                title=xlabel
            ),
            yaxis=dict(
                title=ylabel
            ))

        fig = go.Figure(layout=layout, layout_xaxis_range=[
                        0, 20], layout_yaxis_range=[-20, 20])
        rho = 1.0

        if ylabel == 'S(Q)':
            fig.add_shape(type='line',
                          x0=min(x),
                          y0=1,
                          x1=max(x),
                          y1=1,
                          line_dash="dash",
                          line=dict(color='Red'))

        if ylabel == 'G(R)':
            fig.add_shape(type='line',
                          x0=min(x),
                          y0=0,
                          x1=max(x),
                          y1=0,
                          line_dash="dash",
                          line=dict(color='Blue'))

            # Get from gpx PDF controls sample information->element
            noa = config['Formula'][1]
            fig.add_trace(go.Scatter(x=x[:250], y=-4*3.142*x*noa/volume,
                                     name="Atomic Density Line", line=dict(color='Green')))

        line = dict(color="#ffe476")
        scatter = go.Scatter(x=x, y=y,
                             mode='lines',
                             line=dict(color="#003865"),
                             name='Sulfur')

        fig.add_trace(scatter)
        data = [scatter]
        div = plotly.offline.plot(
            data, include_plotlyjs=False, output_type='div')
        fig.write_html(dest + "/" + prefix + ".html")

    filename = data['filename']
    ceo2ImageFile = data['images']['CeO2']
    ceo2ControlFile = data['controls']['CeO2']
    capillaryImageFile = data['images']['Capillary']
    capillaryControlFile = data['controls']['Capillary']
    sulfurImageFile = data['images']['Sulfur']
    sulfurControlFile = data['controls']['Sulfur']

    # Create workflow GSAS2 project
    gpx = G2sc.G2Project(filename=filename)

    # Load tif images
    gpx.add_image(ceo2ImageFile)
    gpx.add_image(capillaryImageFile)
    gpx.add_image(sulfurImageFile)

    ceo2Image = gpx.images()[0]
    capillaryImage = gpx.images()[1]
    sulfurImage = gpx.images()[2]

    ceo2Image.loadControls(ceo2ControlFile)
    capillaryImage.loadControls(capillaryControlFile)
    sulfurImage.loadControls(sulfurControlFile)

    sulfurPWDRList = sulfurImage.Integrate()
    capillaryPWDRList = capillaryImage.Integrate()

    sulfurPWDRList[0].SaveProfile('pwdr_Sulfur')
    capillaryPWDRList[0].SaveProfile('pwdr_Capillary')

    sulfurPowerFile = data['powders']['Sulfur']

    pdf = gpx.add_PDF(sulfurPowerFile, 0)

    pdf.data['PDF Controls'].update(config)
    pdf.data['PDF Controls']['Container']['Name'] = capillaryPWDRList[0].name

    pdf.set_formula(config['Formula'])

    for i in range(5):
        if pdf.optimize():
            break

    pdf.calculate()

    pdf.export(data['export']['prefix'], 'I(Q), S(Q), F(Q), G(r)')

    gpx.save()

    x, y = np.loadtxt(data['export']['prefix'] + '.gr', unpack=True)

    plt.plot(x, y, label='Sulfur')
    fig = plt.figure(1)

    plt.title('Sulfur G(R)')
    plt.xlabel('x')
    plt.ylabel('y')

    axes = plt.gca()

    plt.xlim(data['limits']['xlim'])
    plt.ylim(data['limits']['ylim'])

    plt.savefig(data['outputfig'])
    os.makedirs(data['datadir'] + "/charts", exist_ok=True)

    volume = pdf.data['PDF Controls']['Form Vol']
    generate_charts(data['export']['prefix'] + '.gr', os.path.basename(data['export']
                    ['prefix']) + "-gr", data['datadir'] + "/charts", "Angstroms", "G(R)", volume)

    x, y = np.loadtxt(data['export']['prefix'] + '.sq', unpack=True)

    plt.plot(x, y, label='Sulfur')
    fig = plt.figure(1)

    plt.title('Sulfur S(Q)')
    plt.xlabel('x')
    plt.ylabel('y')

    axes = plt.gca()

    plt.xlim(data['limits']['xlim'])
    plt.ylim(data['limits']['ylim'])

    plt.savefig(data['outputfig'])
    os.makedirs(data['datadir'] + "/charts", exist_ok=True)

    generate_charts(data['export']['prefix'] + '.sq', os.path.basename(data['export']
                    ['prefix']) + "-sq", data['datadir'] + "/charts", "Inverse Angstroms", "S(Q)", volume)

    return True



@generate_flow_definition()
class GSASPDF(GladierBaseTool):

    required_input = [
    ]

    funcx_functions = [
        generate_sulfur_pdf
    ]
