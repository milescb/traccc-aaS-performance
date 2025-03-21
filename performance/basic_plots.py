import matplotlib.pyplot as plt

# ploting style
import mplhep as hep
plt.style.use(hep.style.ATLAS)
plt.rcParams['legend.loc'] = 'upper left'
figsize = (7, 7)
colors = plt.get_cmap('tab10')

def plot_var(concurrency, data, ylabel, xlabel, filename='', yerr=None,
             device="NVIDIA A100 SXM4 40GB", 
             title=r'ODD detector, $\mu = 200$, traccc e7a03e9'):
    fig, ax = plt.subplots(figsize=figsize)
    plt.errorbar(concurrency, data, yerr=yerr)
    plt.xlabel(xlabel, loc='right')
    plt.ylabel(ylabel, loc='top')
    plt.xlim(min(concurrency), max(concurrency))
    plt.title(device+', '+title, fontsize=12, loc='left')
    if filename != '':
        plt.savefig(filename, bbox_inches='tight')
    plt.show()
    
def plot_multiple_vars(concurrency, data, data_labels, ylabel, xlabel, filename='',
                        device="NVIDIA A100 SXM4 40GB", 
                        title=r'ODD detector, $\mu = 200$, traccc e7a03e9'):
    fig, ax = plt.subplots(figsize=figsize)
    for i in range(len(data)):
        plt.plot(concurrency, data[i], label=data_labels[i])
    plt.xlabel(xlabel, loc='right')
    plt.ylabel(ylabel, loc='top')
    plt.xlim(min(concurrency), max(concurrency))
    plt.title(device+', '+title, fontsize=12, loc='left')
    plt.legend()
    if filename != '':
        plt.savefig(filename, bbox_inches='tight')
    plt.show()

def plot_var_and_compare(con, con_1gpu, data, data_1gpu, ylabel, xlabel, ylims=None,
                         filename='', yerr=None, yerr_1gpu=None, 
                         num_instances='One', num_GPUS=4,
                         device="NVIDIA A100 SXM4 40GB",
                         title=r'ODD detector, $\mu = 200$, traccc e7a03e9'):
    fig, ax = plt.subplots(figsize=figsize)
    plt.errorbar(con, data, yerr=yerr, label=f'{num_GPUS} {device} GPUs')
    plt.errorbar(con_1gpu, data_1gpu, yerr=yerr_1gpu, label=f'1 {device} GPU')
    plt.xlabel(xlabel, loc='right')
    plt.ylabel(ylabel, loc='top')
    plt.xlim(min(con)-0.1, max(con)+0.1)
    plt.title(device+', '+title, fontsize=12, loc='left')
    plt.legend(title=f'{num_instances} Triton model instance per:')
    if ylims is not None:
        plt.ylim(ylims)
    if filename != '':
        plt.savefig(filename, bbox_inches='tight')
    plt.show()