import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def plot_all_queries(species, queries, **kwargs):

    if kwargs['out_format'] == 'pdf_one':
        pdf = PdfPages(os.path.join(kwargs['out_dir'] + '/all_queries.pdf'))

    if kwargs['plot_species'][0] is 'all':
        plot_species = species.keys()
    else:
        plot_species = kwargs['plot_species']

    for sp in plot_species:
        fig = plt.figure()
        for query in queries:
            plt.plot(query.t, query.concentrations[:, species[sp].index])
        plt.title(sp)
        plt.ylabel('Concentration (uM)')
        plt.xlabel('Time (seconds)')
        plt.legend(queries)
        plt.xticks(np.arange(0, kwargs['ttot']+1, kwargs['ttot']/2))
        plt.grid(True)

        if kwargs['out_format'] == 'pdf_mult':
            pdf = PdfPages(
                os.path.join(kwargs['out_dir'] + '/{}.pdf'.format(sp)))
            pdf.savefig()
            pdf.close()

        if kwargs['out_format'] == 'png':
            fig.savefig(os.path.join(kwargs['out_dir'] + '/{}.png'.format(sp)))

        if kwargs['out_format'] == 'pdf_one':
            pdf.savefig()

        plt.close()

    if kwargs['out_format'] == 'pdf_one':
        pdf.close()

    return


def plot_each_query(species, queries, **kwargs):

    if kwargs['plot_species'][0] is 'all':
        plot_species = species.keys()
    else:
        plot_species = kwargs['plot_species']

    for query in queries:

        if kwargs['out_format'] == 'pdf_one':
            pdf = PdfPages(
                os.path.join(
                    kwargs['out_dir'] + '/{}.pdf'.format(query.name)))

        for sp in plot_species:
            fig = plt.figure()
            plt.plot(query.t, query.concentrations[:, species[sp].index])
            plt.title('{}, {}'.format(sp, query.name))
            plt.ylabel('Concentration (uM)')
            plt.xlabel('Time (seconds)')
            plt.xticks(np.arange(0, kwargs['ttot']+1, kwargs['ttot']/2))
            plt.grid(True)

            if kwargs['out_format'] == 'pdf_mult':
                pdf = PdfPages(
                    os.path.join(
                        kwargs['out_dir'] + '/{}_{}.pdf'.format(
                            query.name, sp)))
                pdf.savefig()
                pdf.close()

            if kwargs['out_format'] == 'png':
                fig.savefig(
                    os.path.join(
                        kwargs['out_dir'] + '/{}_{}.png'.format(
                            query.name, sp)))

            if kwargs['out_format'] == 'pdf_one':
                pdf.savefig()

            plt.close()

        if kwargs['out_format'] == 'pdf_one':
            pdf.close()

    return
