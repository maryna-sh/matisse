{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "07cfd4e5",
   "metadata": {},
   "outputs": [],
   "source": [
    "def neon_tokyo(data, x_column, y_column, font_family='Sangha', font_color='#FDF0F0', font_size=20, title_pad=15, bg_color='#212946', grid_color='#FE53BB', bar_color='#FE53BB'):\n",
    "    plt.style.use(\"seaborn-dark\")\n",
    "    \n",
    "    fig, ax = plt.subplots(figsize=(8, 6))\n",
    "    fig.set_facecolor(bg_color)\n",
    "    ax.set_facecolor(bg_color)\n",
    "\n",
    "    # Create the bar plot with see-through bars\n",
    "    bars = ax.bar(data[x_column], data[y_column], color='none', edgecolor=bar_color)\n",
    "    \n",
    "    # Customize the labels and title\n",
    "    plt.xlabel(x_column, fontname=font_family, fontsize=font_size, color=font_color)\n",
    "    plt.ylabel(y_column, fontname=font_family, fontsize=font_size, color=font_color)\n",
    "    plt.title(f'{x_column} vs. {y_column}', fontsize=24, fontname=font_family, pad=title_pad, color=font_color)\n",
    "    plt.xticks(rotation=45, color=font_color)\n",
    "    plt.yticks(color=font_color)\n",
    "\n",
    "    # Create multiple sets of bars with different alpha and line thickness settings\n",
    "    for i in range(4, 0, -1):\n",
    "        alpha = i / 7  # Varies alpha from 1 to 0 (fully visible to fully transparent)\n",
    "        linewidth = i*2 + 5  # Varies line thickness\n",
    "        ax.bar(data[x_column], data[y_column], color='none', edgecolor=bar_color, alpha=0.12, linewidth=linewidth)\n",
    "    \n",
    "    plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
