import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def plot_all_queries(species, queries, out_dir, out_format,
                     plot_species, ttot, **kwargs):
    '''
    Description:
        This method creates plots for each species, plotting timecourse curves
        from all queries on the same plot.
    Input:
        species - a dictionary mapping strings to Species objects.
        queries - a list of query objects.
        out_dir - the path to the output directory.
        out_format - the file format for output figures.
        plot_species - a list containing species names to be plotted. default
            is to generate plots for all species.
        ttot - the total length of simulation.
    '''

    if out_format == 'pdf_one':
        pdf = PdfPages(os.path.join(out_dir + '/all_queries.pdf'))

    if plot_species[0] is 'all':
        plot_species = species.keys()

    for sp in plot_species:
        fig = plt.figure()
        for query in queries:
            plt.plot(query.t, query.concentrations[:, species[sp].index])
        plt.title(sp)
        plt.ylabel('Concentration (uM)')
        plt.xlabel('Time (seconds)')
        plt.legend(queries)
        plt.xticks(np.arange(0, ttot+1, ttot/2))
        plt.grid(True)

        if out_format == 'pdf_mult':
            pdf = PdfPages(
                os.path.join(out_dir + '/{}.pdf'.format(sp)))
            pdf.savefig()
            pdf.close()

        if out_format == 'png':
            fig.savefig(os.path.join(out_dir + '/{}.png'.format(sp)))

        if out_format == 'pdf_one':
            pdf.savefig()

        plt.close()

    if out_format == 'pdf_one':
        pdf.close()

    return


def plot_each_query(species, queries, out_dir, out_format,
                    plot_species, ttot, **kwargs):
    '''
    Description:
        This method creates plots for each species, plotting timecourse curves
        from each query separately.
    Input:
        species - a dictionary mapping strings to Species objects.
        queries - a list of query objects.
        out_dir - the path to the output directory.
        out_format - the file format for output figures.
        plot_species - a list containing species names to be plotted. default
            is to generate plots for all species.
        ttot - the total length of simulation.
    '''

    if plot_species[0] is 'all':
        plot_species = species.keys()

    for query in queries:

        if out_format == 'pdf_one':
            pdf = PdfPages(
                os.path.join(
                    out_dir + '/{}.pdf'.format(query.name)))

        for sp in plot_species:
            fig = plt.figure()
            plt.plot(query.t, query.concentrations[:, species[sp].index])
            plt.title('{}, {}'.format(sp, query.name))
            plt.ylabel('Concentration (uM)')
            plt.xlabel('Time (seconds)')
            plt.xticks(np.arange(0, ttot+1, ttot/2))
            plt.grid(True)

            if out_format == 'pdf_mult':
                pdf = PdfPages(
                    os.path.join(
                        out_dir + '/{}_{}.pdf'.format(
                            query.name, sp)))
                pdf.savefig()
                pdf.close()

            if out_format == 'png':
                fig.savefig(
                    os.path.join(
                        out_dir + '/{}_{}.png'.format(
                            query.name, sp)))

            if out_format == 'pdf_one':
                pdf.savefig()

            plt.close()

        if out_format == 'pdf_one':
            pdf.close()

    return
