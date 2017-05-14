import numpy as np
import matplotlib.pyplot as plt


def plot_all_species_separate_plots(y, t, species, args, output):
    '''
    Description:
        This method plots the concentration curves obtained from odeint. The
        user can choose between various plotting styles from the command line.
    Input:
        y - the numpy ndarray returned by odeint (y-axis)
        t - the numpy ndarray representing time (x-axis)
        species - the dictionary containing all Species objects
        args - the Namespace object containing the user provided arguments

    Returns: None
    '''
    if args.plot is "all":
        species_plotted = species
    else:
        species_plotted = args.plot.split(",")
    for sp in species_plotted:
        if sp in species:
            fig = plt.figure()
            plt.plot(t, y[:, species[sp].index])
            plt.title(sp)
            plt.ylabel('Concentration (uM)')
            plt.xlabel('Time (seconds)')
            plt.xticks(np.arange(0, int(args.t)+1, int(args.t)/2))
            plt.grid(True)
            # plt.tight_layout()
            fig.savefig(output + 'fig_{}.png'.format(sp))
    return


def plot_all_species_one_plot(y, t, species, args, output):

    # plot subplot of all
    fig = plt.figure(figsize=(15, 8))
    for i in range(y.shape[1]):

        # NOTE: must fix shape of subplot grid to use this method
        ax = fig.add_subplot(2, 4, i+1)
        ax.plot(t, y[:, i])
        for sp in species:
            if species[sp].index is i:
                plt.title(sp)
                plt.ylabel('Concentration (uM)')
                plt.xlabel('Time (seconds)')
                plt.xticks(np.arange(0, int(args.t)+1, int(args.t)/2))
                plt.grid(True)
    fig.suptitle("All Species, total time = {} seconds".format(args.t),
                 fontsize=16)
    plt.tight_layout()
    fig.subplots_adjust(top=.9)
    fig.savefig(output + 'all_species.png')

    return


def plot_species_percent(y, t, species, args, output):

    # plot Ran Species together with Pi
    ran_tot = species['Ran'].conc0  \
        + species['RanGTP'].conc0 \
        + species['RanGDP'].conc0

    # p_tot = species['GTP'].conc0 + species['RanGTP'].conc0
    # s_tot = species['Sensor'].conc0
    fig = plt.figure()
    for each in ['RanGTP', 'RanGDP', 'Ran']:
        plt.plot(t, y[:, species[each].index] / ran_tot)
    # for each in ['Pi']:
    #   plt.plot(t, y[:,species[each].index]/p_tot)
    # for each in ['SensorPi']:
    #   plt.plot(t, y[:,species[each].index]/s_tot)
    plt.title('Ran species')
    plt.ylabel('Fraction of Total Species Type')
    plt.xlabel('Time (seconds)')
    # plt.legend(['RanGTP','RanGDP','Ran','Pi','Sensor','SensorPi'])
    plt.legend(['RanGTP', 'RanGDP', 'Ran'])
    plt.xticks(np.arange(0, int(args.t)+1, int(args.t)/2))
    plt.grid(True)
    fig.savefig(output + 'ran_species.png')

    # plot GTP species together
    nuc_tot = species['GTP'].conc0 \
        + species['GDP'].conc0 \
        + species['RanGTP'].conc0 \
        + species['RanGDP'].conc0
    fig = plt.figure()
    plt.plot(t, y[:, species['GTP'].index] / nuc_tot)
    plt.plot(t, y[:, species['GDP'].index] / nuc_tot)
    plt.title('Nucleotide species')
    plt.ylabel('Fraction of Total Nucleotide')
    plt.xlabel('Time (seconds)')
    plt.legend(['GTP', 'GDP'])
    plt.xticks(np.arange(0, int(args.t)+1, int(args.t)/2))
    plt.grid(True)
    fig.savefig(output + 'nuc_species.png')

    return


def plot_ran_ratios(y, t, species, args, output, figure):

    all_ran_species = [name for name in species if 'Ran' in name]
    ran_tot = sum([species[name].conc0 for name in all_ran_species])

    plotted_species = ['nucRanGTP',
                       'nucRanGDP',
                       'nucRanGTP/nucRanGDP',
                       'nucRanGTP/cytoRanGTP',
                       'cytoRanGTP',
                       'cytoRanGDP',
                       'cytoRanGTP/cytoRanGDP',
                       'nucRanGDP/cytoRanGDP']

    for each in plotted_species:

        if each == 'nucRanGTP/nucRanGDP':

            ax = plt.subplot(2, 4, 3)
            ratio = y[:, species['nucRanGTP'].index] \
                / y[:, species['nucRanGDP'].index]
            ax.plot(t, ratio)
            plt.title(each)
            plt.ylabel('Ratio')
            plt.xlabel('Time (seconds)')
            plt.xticks(np.arange(0, int(args.t)+1, int(args.t)/2))
            plt.grid(True)

        elif each == 'nucRanGTP/cytoRanGTP':

            ax = plt.subplot(2, 4, 4)
            ratio = y[:, species['nucRanGTP'].index] \
                / y[:, species['cytoRanGTP'].index]
            ax.plot(t, ratio)
            plt.title(each)
            plt.ylabel('Ratio')
            plt.xlabel('Time (seconds)')
            plt.xticks(np.arange(0, int(args.t)+1, int(args.t)/2))
            plt.grid(True)

        elif each == 'cytoRanGTP/cytoRanGDP':

            ax = plt.subplot(2, 4, 7)
            ratio = y[:, species['cytoRanGTP'].index] \
                / y[:, species['cytoRanGDP'].index]
            ax.plot(t, ratio)
            plt.title(each)
            plt.ylabel('Ratio')
            plt.xlabel('Time (seconds)')
            plt.xticks(np.arange(0, int(args.t)+1, int(args.t)/2))
            plt.grid(True)

        elif each == 'nucRanGDP/cytoRanGDP':

            ax = plt.subplot(2, 4, 8)
            ratio = y[:, species['nucRanGDP'].index] \
                / y[:, species['cytoRanGDP'].index]
            ax.plot(t, ratio)
            plt.title(each)
            plt.ylabel('Ratio')
            plt.xlabel('Time (seconds)')
            plt.xticks(np.arange(0, int(args.t)+1, int(args.t)/2))
            plt.grid(True)

        else:

            ax = plt.subplot(2, 4, plotted_species.index(each)+1)
            ax.plot(t, y[:, species[each].index] / ran_tot * 100)
            plt.title(each)
            plt.ylabel('Percentage')
            plt.xlabel('Time (seconds)')
            plt.xticks(np.arange(0, int(args.t)+1, int(args.t)/2))
            plt.yticks(np.arange(0, 110, 10))
            plt.grid(True)

    # fig.suptitle("Ran Species, total time = %s seconds" %args.t,fontsize=16)
    # plt.tight_layout()
    # fig.subplots_adjust(top=.9)
    # fig.savefig(output + 'ran_species.png')

    return
