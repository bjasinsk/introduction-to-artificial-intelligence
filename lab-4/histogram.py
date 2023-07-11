import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

if __name__ == '__main__':
    data = pd.read_csv('nursery.data', header=None, names=['parents', 'has_nurs', 'form', 'children', 'housing', 'finance', 'social', 'health','class'])

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.histplot(data=data, x='health', hue='class', multiple='stack', stat='count', binwidth=1, edgecolor='white', alpha=0.8, palette='bright', discrete=True)


    ax.set_xlabel('health')
    ax.set_ylabel('Count')
    ax.set_title('Histogram of health attribute')

    for p in ax.patches:
        ax.annotate(f"{np.ceil(p.get_height()):.0f}", xy=(p.get_x() + p.get_width() / 2, p.get_height()), xytext=(0, 5), textcoords='offset points', ha='center', va='bottom', fontsize=8)

    plt.show()
