import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
# Suppress all warnings
warnings.filterwarnings("ignore")
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import matplotlib.patheffects as path_effects
from scipy.stats import gaussian_kde

# -------- Scatterplot----------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def scatter(data, y_column, x_column,
               font_family='Sangha', font_color='#FDF0F0', font_size=20,
               title_pad=15, bg_color='#212946', grid_color='#FE53BB',
               bar_color=['#FE53BB', '#FEFFAC', '#97FEED', '#E384FF', '#FF8400'],
               width=0.8,
               plot_title=None,
               hue=None, 
               s=80,          
               alpha=0.7,
               rotation=0, figsize=(10,8), annotation='', ann_x=1.45,ann_y=-0.2, x_name=None, y_name=None):     
               
    plt.style.use("seaborn-dark")

    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    data_sorted = data.sort_values(by=y_column, ascending=False)  # Sort data globally in ascending order

    if hue:
        unique_hue_values = data[hue].unique()

        for hue_value in unique_hue_values:
            data_filtered = data_sorted[data_sorted[hue] == hue_value]
            label = f'{hue_value}'  # Label for the legend
            color_index = np.where(unique_hue_values == hue_value)[0][0]
            color = bar_color[color_index % len(bar_color)]
            # Explicitly assign labels to the bars
            bars = ax.scatter(data_filtered[x_column], data_filtered[y_column],color=color, s=s, edgecolor=color, label=label, alpha=0.7)
    else:
        [None]  # Get unique "hue" values
        data_filtered = data_sorted
        label = None
        color_index = 0
        color = bar_color[color_index % len(bar_color)]
        # Explicitly assign labels to the bars
        bars = ax.scatter(data_filtered[x_column], data_filtered[y_column], s=s,color=color, edgecolor=color, label=label, alpha=0.7)



    if hue:
        legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

        title = legend.get_title()
        title.set_color('white')  # Set the legend title's text color to white

        for text in legend.get_texts():
            text.set_color('white')  # Set the legend item text color to white

            
    if x_name==None:
        x_name=x_column
    if y_name==None:
        y_name=y_column
        
    plt.xlabel(x_name, fontname=font_family, fontsize=font_size, color=font_color)
    plt.ylabel(y_name, fontname=font_family, fontsize=font_size, color=font_color)

    if not plot_title is None:
        ax.set_title(plot_title, fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    else:
        ax.set_title(label=f'{x_column} by {y_column}', fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    plt.xticks(rotation=rotation, color=font_color)
    plt.yticks(color=font_color)

    plt.grid(axis='y', linestyle='--', color=grid_color, alpha=0.7)

    for i in range(4, 0, -1):
        alpha = i / 20  # Varies alpha from 1 to 0 (fully visible to fully transparent)
        linewidth = i * 3  # Varies line thickness
        if hue:
            for hue_value in unique_hue_values:
                color_index = np.where(unique_hue_values == hue_value)[0][0] if hue else 0
                color = bar_color[color_index % len(bar_color)]
                data_filtered = data_sorted[data_sorted[hue] == hue_value]
                bars = ax.scatter(data_filtered[x_column], data_filtered[y_column], edgecolor=color,
                              linewidth=linewidth, label=label,
                              alpha=alpha, s=s)

        else:
            bars = ax.scatter(data_filtered[x_column], data_filtered[y_column], edgecolor=color, 
                          linewidth=linewidth, label=label,
                          alpha=alpha, s=s)
            
            
    # adding padding to axis        
    for ax in plt.gcf().get_axes():
        ax.yaxis.labelpad = 10
        ax.xaxis.labelpad = 10        
            
    # annotation
    annotation_text = annotation
    annotation_x = ann_x  # Keep it at the right edge to position the annotation to the right
    annotation_y = ann_y  # Y-coordinate of the annotation (negative value to place it at the bottom)

    # Split the annotation text into lines with a maximum of 80 characters each
    max_line_length = 80
    lines = [annotation_text[i:i+max_line_length] for i in range(0, len(annotation_text), max_line_length)]

    # Calculate the vertical position for each line
    vertical_spacing = 0.03  # Adjust this value to control the vertical spacing
    vertical_position = annotation_y

    # Add each line of the annotation separately
    for line in lines:
        ax.annotate(line, xy=(annotation_x, vertical_position),
                    xycoords='axes fraction', fontsize=12, color='white', ha='right')  # Set ha='right' for right alignment
        vertical_position -= vertical_spacing         

 
            
    plt.show()
                
# -------- Barplot--------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

def bar(data, y_column, x_column,
               font_family='Sangha', font_color='#FDF0F0', font_size=20,
               title_pad=15, bg_color='#212946', grid_color='#FE53BB',
               bar_color=['#FE53BB', '#FEFFAC', '#97FEED', '#E384FF', '#FF8400'],
               width=0.8,
               plot_title=None,
               hue=None,
               bar_fill='empty',
               rotation=0, figsize=(10,8), annotation='', ann_x=1.45,ann_y=-0.2, x_name=None, y_name=None):
    
    plt.style.use("seaborn-dark")

    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    data_sorted = data.sort_values(by=y_column, ascending=False)  # Sort data globally in ascending order
    
    if hue:
        unique_hue_values = data[hue].unique()

        for hue_value in unique_hue_values:
            data_filtered = data_sorted[data_sorted[hue] == hue_value]
            label = f'{hue_value}'  # Label for the legend
            color_index = np.where(unique_hue_values == hue_value)[0][0]
            color = bar_color[color_index % len(bar_color)]
            # Explicitly assign labels to the bars
            if bar_fill == 'full':
                bars = ax.bar(data_filtered[x_column], data_filtered[y_column],alpha=0.8, facecolor=color, edgecolor=color, width=width, label=label)
            else:
                bars = ax.bar(data_filtered[x_column], data_filtered[y_column], color='none', edgecolor=color, width=width, label=label)
    else:
        [None]  # Get unique "hue" values
        data_filtered = data_sorted
        label = None
        color_index = 0
        color = bar_color[color_index % len(bar_color)]
        # Explicitly assign labels to the bars
        if bar_fill == 'full':
            bars = ax.bar(data_filtered[x_column], data_filtered[y_column], color=color, edgecolor=color, width=width, label=label, facecolor=color)
        else:
            bars = ax.bar(data_filtered[x_column], data_filtered[y_column], color='none', edgecolor=color, width=width, label=label)



    if hue:
        legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

        title = legend.get_title()
        title.set_color('white')  # Set the legend title's text color to white

        for text in legend.get_texts():
            text.set_color('white')  # Set the legend item text color to white
        # Get the handles (bars) and labels
        handles, labels = ax.get_legend().legendHandles, [text.get_text() for text in legend.get_texts()]    
        for handle, label in zip(handles, labels):
            # Set the color of the handle to match the label's color
            color = handle.get_edgecolor()
            handle.set_edgecolor(color)

            # Apply the path effect to the handle
            handle.set_path_effects([path_effects.withStroke(linewidth=3, foreground=color, alpha=0.5)])    

            
    if x_name==None:
        x_name=x_column
    if y_name==None:
        y_name=y_column
        
        
    plt.xlabel(x_name, fontname=font_family, fontsize=font_size, color=font_color)
    plt.ylabel(y_name, fontname=font_family, fontsize=font_size, color=font_color)

    if not plot_title is None:
        ax.set_title(plot_title, fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    else:
        ax.set_title(label=f'{x_column} by {y_column}', fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    plt.xticks(rotation=rotation, color=font_color)
    plt.yticks(color=font_color)

    plt.grid(axis='y', linestyle='--', color=grid_color, alpha=0.7)

    if bar_fill == 'empty':
        for i in range(4, 0, -1):
            alpha = i / 20  # Varies alpha from 1 to 0 (fully visible to fully transparent)
            linewidth = i * 3  # Varies line thickness
            if hue:
                for hue_value in unique_hue_values:
                    color_index = np.where(unique_hue_values == hue_value)[0][0] if hue else 0
                    color = bar_color[color_index % len(bar_color)]
                    data_filtered = data_sorted[data_sorted[hue] == hue_value]
                    bars = ax.bar(data_filtered[x_column], data_filtered[y_column],
                                  color='none', edgecolor=color,
                                  linewidth=linewidth, label=label,
                                  alpha=alpha)

            else:
                bars = ax.bar(data_filtered[x_column], data_filtered[y_column],
                              color='none', edgecolor=color, 
                              linewidth=linewidth, label=label,
                              alpha=alpha)

    elif bar_fill == 'full' or bar_fill=='semi':
        for i in range(4, 0, -1):
            alpha = i / 23  # Varies alpha from 1 to 0 (fully visible to fully transparent)
            linewidth = i * 3  # Varies line thickness
            if hue:
                for hue_value in unique_hue_values:
                    color_index = np.where(unique_hue_values == hue_value)[0][0] if hue else 0
                    color = bar_color[color_index % len(bar_color)]
                    data_filtered = data_sorted[data_sorted[hue] == hue_value]
                    bars = ax.bar(data_filtered[x_column], data_filtered[y_column],
                                  color='none', edgecolor=color,
                                  linewidth=linewidth, label=label,
                                  alpha=alpha,facecolor=color)

            else:
                bars = ax.bar(data_filtered[x_column], data_filtered[y_column],
                              color='none', edgecolor=color, facecolor=color,
                              linewidth=linewidth, label=label,
                              alpha=alpha)
                
                
    for ax in plt.gcf().get_axes():
        ax.yaxis.labelpad = 10
        ax.xaxis.labelpad = 10            
                
    # annotation
    annotation_text = annotation
    annotation_x = ann_x  # Keep it at the right edge to position the annotation to the right
    annotation_y = ann_y  # Y-coordinate of the annotation (negative value to place it at the bottom)

    # Split the annotation text into lines with a maximum of 80 characters each
    max_line_length = 80
    lines = [annotation_text[i:i+max_line_length] for i in range(0, len(annotation_text), max_line_length)]

    # Calculate the vertical position for each line
    vertical_spacing = 0.03  # Adjust this value to control the vertical spacing
    vertical_position = annotation_y

    # Add each line of the annotation separately
    for line in lines:
        ax.annotate(line, xy=(annotation_x, vertical_position),
                    xycoords='axes fraction', fontsize=12, color='white', ha='right')  # Set ha='right' for right alignment
        vertical_position -= vertical_spacing 
        
                        
    plt.show()        

# -------- Barhplot-------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
def barh(data, y_column, x_column,
               font_family='Sangha', font_color='#FDF0F0', font_size=20,
               title_pad=15, bg_color='#212946', grid_color='#FE53BB',
               bar_color=['#FE53BB', '#FEFFAC', '#97FEED', '#E384FF', '#FF8400'],
               width=0.8,
               plot_title=None,
               hue=None,
               bar_fill='empty',
               rotation=0, figsize=(10,8), annotation='', ann_x=1.45,ann_y=-0.2, y_name=None, x_name=None):
    
    plt.style.use("seaborn-dark")

    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    data_sorted = data.sort_values(by=y_column, ascending=False)  # Sort data globally in ascending order
    
    data_sorted = data.sort_values(by=x_column, ascending=True)
    
    if hue:
        unique_hue_values = data[hue].unique()

        for hue_value in unique_hue_values:
            data_filtered = data_sorted[data_sorted[hue] == hue_value]
            label = f'{hue_value}'  # Label for the legend
            color_index = np.where(unique_hue_values == hue_value)[0][0]
            color = bar_color[color_index % len(bar_color)]
            # Explicitly assign labels to the bars
            if bar_fill == 'full':
                bars = ax.barh(data_filtered[y_column], data_filtered[x_column],alpha=0.8, facecolor=color, edgecolor=color, label=label)
            else:
                bars = ax.barh(data_filtered[y_column], data_filtered[x_column], color='none', edgecolor=color, label=label)
    else:
        [None]  # Get unique "hue" values
        data_filtered = data_sorted
        label = None
        color_index = 0
        color = bar_color[color_index % len(bar_color)]
        # Explicitly assign labels to the bars
        if bar_fill == 'full':
            bars = ax.barh(data_filtered[y_column], data_filtered[x_column], color=color, edgecolor=color, label=label, facecolor=color)
        else:
            bars = ax.barh(data_filtered[y_column], data_filtered[x_column], color='none', edgecolor=color, label=label)



    if hue:
        legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        frame = legend.get_frame()
        frame.set_facecolor('white')  # Set the legend's background color to white

        title = legend.get_title()
        title.set_color('white')  # Set the legend title's text color to white

        for text in legend.get_texts():
            text.set_color('white')  # Set the legend item text color to white
        # Get the handles (bars) and labels
        handles, labels = ax.get_legend().legendHandles, [text.get_text() for text in legend.get_texts()]
        for handle, label in zip(handles, labels):
            # Set the color of the handle to match the label's color
            color = handle.get_edgecolor()
            handle.set_edgecolor(color)
            handle.set_alpha(0.8)

            # Apply the path effect to the handle
            handle.set_path_effects([path_effects.withStroke(linewidth=3, foreground=color, alpha=0.5)]) 
            
    if x_name==None:
        x_name=x_column
    if y_name==None:
        y_name=y_column        

    plt.xlabel(x_name, fontname=font_family, fontsize=font_size, color=font_color)
    plt.ylabel(y_name, fontname=font_family, fontsize=font_size, color=font_color)

    if not plot_title is None:
        ax.set_title(plot_title, fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    else:
        ax.set_title(label=f'{x_column} by {y_column}', fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    plt.xticks(rotation=rotation, color=font_color)
    plt.yticks(color=font_color)

    plt.grid(axis='x', linestyle='--', color=grid_color, alpha=0.7)

    if bar_fill == 'empty':
        for i in range(4, 0, -1):
            alpha = i / 20  # Varies alpha from 1 to 0 (fully visible to fully transparent)
            linewidth = i * 3  # Varies line thickness
            if hue:
                for hue_value in unique_hue_values:
                    color_index = np.where(unique_hue_values == hue_value)[0][0] if hue else 0
                    color = bar_color[color_index % len(bar_color)]
                    data_filtered = data_sorted[data_sorted[hue] == hue_value]
                    bars = ax.barh(data_filtered[y_column], data_filtered[x_column],
                                  color='none', edgecolor=color,
                                  linewidth=linewidth, label=label,
                                  alpha=alpha)

            else:
                bars = ax.barh(data_filtered[y_column], data_filtered[x_column],
                              color='none', edgecolor=color, 
                              linewidth=linewidth, label=label,
                              alpha=alpha)

    elif bar_fill == 'full' or bar_fill=='semi':
        for i in range(4, 0, -1):
            alpha = i / 23  # Varies alpha from 1 to 0 (fully visible to fully transparent)
            linewidth = i * 3  # Varies line thickness
            if hue:
                for hue_value in unique_hue_values:
                    color_index = np.where(unique_hue_values == hue_value)[0][0] if hue else 0
                    color = bar_color[color_index % len(bar_color)]
                    data_filtered = data_sorted[data_sorted[hue] == hue_value]
                    bars = ax.barh(data_filtered[y_column], data_filtered[x_column],
                                  color='none', edgecolor=color,
                                  linewidth=linewidth, label=label,
                                  alpha=alpha,facecolor=color)

            else:
                bars = ax.barh(data_filtered[y_column], data_filtered[x_column],
                              color='none', edgecolor=color, facecolor=color,
                              linewidth=linewidth, label=label,
                              alpha=alpha)
                
                
     # spacing for axis           
                
    for ax in plt.gcf().get_axes():
                ax.yaxis.labelpad = 10
                ax.xaxis.labelpad = 10

    # annotation
    annotation_text = annotation
    annotation_x = ann_x  # Keep it at the right edge to position the annotation to the right
    annotation_y = ann_y  # Y-coordinate of the annotation (negative value to place it at the bottom)

    # Split the annotation text into lines with a maximum of 60 characters each
    max_line_length = 80
    lines = [annotation_text[i:i+max_line_length] for i in range(0, len(annotation_text), max_line_length)]

    # Calculate the vertical position for each line
    vertical_spacing = 0.03  # Adjust this value to control the vertical spacing
    vertical_position = annotation_y

    # Add each line of the annotation separately
    for line in lines:
        ax.annotate(line, xy=(annotation_x, vertical_position),
                    xycoords='axes fraction', fontsize=12, color='white', ha='right')  # Set ha='right' for right alignment
        vertical_position -= vertical_spacing 
        
        
        
    plt.show()             





# -------- Lineplot-------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

def line(data, y_column, x_column,
         font_family='Sangha', font_color='#FDF0F0', font_size=20,
         title_pad=15, bg_color='#212946', grid_color='#FE53BB',
         bar_color=['#FE53BB', '#FEFFAC', '#97FEED', '#E384FF', '#FF8400'],
         width=0.8,
         plot_title=None,
         hue=None,
         dashes=True,     # lineplot param
         linestyle=None,  # lineplot param
         marker=None,
         rotation=0,
        figsize=(10,8), ann_x=1.15,ann_y=-0.2, x_name=None, y_name=None):

    plt.style.use("seaborn-dark")

    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    data=data.dropna()

    data_sorted = data.sort_values(by=y_column, ascending=False)  # Sort data globally in ascending order

    if hue:
        unique_hue_values = data[hue].unique()

        for hue_value in unique_hue_values:
            data_filtered = data_sorted[data_sorted[hue] == hue_value]
            label = f'{hue_value}'  # Label for the legend
            color_index = np.where(unique_hue_values == hue_value)[0][0]
            color = bar_color[color_index % len(bar_color)]
            # Explicitly assign labels to the bars
            valid_data = data_filtered.dropna(subset=[x_column, y_column])  # Remove rows with NaN values in x_column or y_column
            if not valid_data.empty:
                bars = ax.plot(valid_data[x_column], valid_data[y_column],
                               color=color, label=label, linestyle=linestyle, marker=marker)
    else:
        [None]  # Get unique "hue" values
        data_filtered = data_sorted
        label = None
        color_index = 0
        color = bar_color[color_index % len(bar_color)]
        # Explicitly assign labels to the bars
        valid_data = data_filtered.dropna(subset=[x_column, y_column])  # Remove rows with NaN values in x_column or y_column
        if not valid_data.empty:
            bars = ax.plot(valid_data[x_column], valid_data[y_column],
                           color=color, label=label, linestyle=linestyle, marker=marker)

    if hue:
        legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        frame = legend.get_frame()
        frame.set_facecolor('white')  # Set the legend's background color to white

        title = legend.get_title()
        title.set_color('white')  # Set the legend title's text color to white

        for text in legend.get_texts():
            text.set_color('white')  # Set the legend item text color to white
            
            
    if x_name==None:
        x_name=x_column
    if y_name==None:
        y_name=y_column        

    plt.xlabel(x_name, fontname=font_family, fontsize=font_size, color=font_color)
    plt.ylabel(y_name, fontname=font_family, fontsize=font_size, color=font_color)

    if not plot_title is None:
        ax.set_title(plot_title, fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    else:
        ax.set_title(label=f'{x_column} by {y_column}', fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    plt.xticks(rotation=rotation, color=font_color)
    plt.yticks(color=font_color)

    plt.grid(axis='y', linestyle='--', color=grid_color, alpha=0.7)

    for i in range(4, 0, -1):
        alpha = i / 20  # Varies alpha from 1 to 0 (fully visible to fully transparent)
        linewidth = i * 3  # Varies line thickness
        if hue:
            for hue_value in unique_hue_values:
                color_index = np.where(unique_hue_values == hue_value)[0][0] if hue else 0
                color = bar_color[color_index % len(bar_color)]
                data_filtered = data_sorted[data_sorted[hue] == hue_value]
                valid_data = data_filtered.dropna(subset=[x_column, y_column])  # Remove rows with NaN values in x_column or y_column
                if not valid_data.empty:
                    bars = ax.plot(valid_data[x_column], valid_data[y_column],
                                   color=color, linewidth=linewidth, label=label,
                                   alpha=alpha, linestyle=linestyle, marker=marker)
        else:
            valid_data = data_filtered.dropna(subset=[x_column, y_column])  # Remove rows with NaN values in x_column or y_column
            if not valid_data.empty:
                bars = ax.plot(valid_data[x_column], valid_data[y_column],
                               color=color, linewidth=linewidth, label=label,
                               alpha=alpha, linestyle=linestyle, marker=marker)

    for ax in plt.gcf().get_axes():
        ax.yaxis.labelpad = 10
        ax.xaxis.labelpad = 10
        
    # annotation
    annotation_text = annotation
    annotation_x = ann_x  # Keep it at the right edge to position the annotation to the right
    annotation_y = ann_y  # Y-coordinate of the annotation (negative value to place it at the bottom)

    # Split the annotation text into lines with a maximum of 60 characters each
    max_line_length = 60
    lines = [annotation_text[i:i+max_line_length] for i in range(0, len(annotation_text), max_line_length)]

    # Calculate the vertical position for each line
    vertical_spacing = 0.03  # Adjust this value to control the vertical spacing
    vertical_position = annotation_y

    # Add each line of the annotation separately
    for line in lines:
        ax.annotate(line, xy=(annotation_x, vertical_position),
                    xycoords='axes fraction', fontsize=12, color='white', ha='right')  # Set ha='right' for right alignment
        vertical_position -= vertical_spacing     

    plt.show()      





# -------- Histogram-------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

def hist(data, y_column, x_column=None, font_family='Sangha', font_color='#FDF0F0',
         font_size=20, title_pad=15, bg_color='#212946', grid_color='#FE53BB',
         bar_color=['#FE53BB', '#97FEED','#FEFFAC', '#E384FF', '#FF8400'],
         plot_title=None, hue=None, histtype='bar', stacked=False,
         bins=20, density=False, weights=None, cumulative=False, kde=False, 
         rotation=0, figsize=(10,8),
         annotation='', ann_x=1.45,ann_y=-0.2, x_name=None, y_name=None):

    plt.style.use("seaborn-dark")

    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    data_sorted = data.sort_values(by=y_column, ascending=False)

    if hue:
        data_filtered = data_sorted[pd.notna(data_sorted[hue])]
        unique_hue_values = data_filtered[hue].unique()

        for hue_value in unique_hue_values:
            data_filtered = data_sorted[data_sorted[hue] == hue_value]
            label = f'{hue_value}'
            color_index = np.where(unique_hue_values == hue_value)[0][0]
            color = bar_color[color_index % len(bar_color)]

            valid_data = data_filtered[y_column].dropna()

            if len(valid_data) > 0:
                if kde:
                    kde_obj = gaussian_kde(valid_data, bw_method='silverman')
                    x_values = np.linspace(valid_data.min(), valid_data.max(), 100)
                    kde_values = kde_obj(x_values)
                    plt.plot(x_values, kde_values, label=f'KDE ({hue_value})', color=color)

                hist, bins, patches = ax.hist(valid_data, color=color, edgecolor=color, label=label,
                                              histtype=histtype, stacked=stacked, bins=bins, density=True, weights=weights, cumulative=cumulative, alpha=0.5)

                for patch in patches:
                    patch.set_edgecolor(color)

    else:
        data_filtered = data_sorted
        label = None
        color_index = 0
        color = bar_color[color_index % len(bar_color)]

        valid_data = data_filtered[y_column].dropna()

        if len(valid_data) > 0:
            if kde:
                kde_obj = gaussian_kde(valid_data, bw_method='silverman')
                x_values = np.linspace(valid_data.min(), valid_data.max(), 100)
                kde_values = kde_obj(x_values)
                plt.plot(x_values, kde_values, label='KDE', color=color)

            hist, bins, patches = ax.hist(valid_data, color=color, edgecolor=color, label=label,
                                          histtype=histtype, stacked=stacked, bins=bins, density=True, weights=weights, cumulative=cumulative, alpha=0.5)

            for patch in patches:
                patch.set_edgecolor(color)
                
                

    if hue:
        legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        legend_handles = [mpatches.Rectangle((0, 0), 1, 1, color=bar_color[i % len(bar_color)],alpha=0.7, label=unique_hue_values[i]) for i in range(len(unique_hue_values))]
        ax.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1, 1))
        legend = ax.get_legend()
        for text in legend.get_texts():
            text.set_color(font_color)
            
    
    if y_name==None:
        y_name=y_column        

    plt.ylabel(y_name, fontname=font_family, fontsize=font_size, color=font_color)
    plt.xlabel(x_name, fontname=font_family, fontsize=font_size, color=font_color)

    if not plot_title is None:
        ax.set_title(plot_title, fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    else:
        ax.set_title(label=f'{y_column}', fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    plt.xticks(rotation=rotation, color=font_color)
    plt.yticks(color=font_color)
    plt.grid(axis='y', linestyle='--', color=grid_color, alpha=0.7)

    legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    for text in legend.get_texts():
        text.set_color(font_color)
    
    for i in range(4, 0, -1):
        alpha = i / 25
        linewidth = i * 1
        if hue:
            for hue_value in unique_hue_values:
                color_index = np.where(unique_hue_values == hue_value)[0][0] if hue else 0
                color = bar_color[color_index % len(bar_color)]
                data_filtered = data_sorted[data_sorted[hue] == hue_value]
                hist, bins, patches = ax.hist(data_filtered[y_column], edgecolor=color,
                                              linewidth=linewidth, label=label, alpha=alpha, histtype=histtype, stacked=stacked, bins=bins, density=True, weights=weights, cumulative=cumulative)
                if kde:
                    kde_obj = gaussian_kde(data_filtered[y_column].dropna(), bw_method='silverman')
                    x_values = np.linspace(data_filtered[y_column].min(), data_filtered[y_column].max(), 100)
                    kde_values = kde_obj(x_values)
                    plt.plot(x_values, kde_values, label=f'KDE ({hue_value})', color=color, alpha=i / 24, linewidth=i * 2)

        else:
            hist, bins, patches = ax.hist(data_filtered[y_column], edgecolor=color, linewidth=linewidth, label=label, alpha=alpha, histtype=histtype, stacked=stacked, bins=bins, density=True, weights=weights, cumulative=cumulative)
            if kde:
                kde_obj = gaussian_kde(valid_data, bw_method='silverman')
                x_values = np.linspace(valid_data.min(), valid_data.max(), 100)
                kde_values = kde_obj(x_values)
                plt.plot(x_values, kde_values, label='KDE', color=color, alpha=i / 24, linewidth=i * 2)
                
    for ax in plt.gcf().get_axes():
        ax.yaxis.labelpad = 10
        ax.xaxis.labelpad = 10
        
    # annotation
    annotation_text = annotation
    annotation_x = ann_x  # Keep it at the right edge to position the annotation to the right
    annotation_y = ann_y  # Y-coordinate of the annotation (negative value to place it at the bottom)

    # Split the annotation text into lines with a maximum of 60 characters each
    max_line_length = 60
    lines = [annotation_text[i:i+max_line_length] for i in range(0, len(annotation_text), max_line_length)]

    # Calculate the vertical position for each line
    vertical_spacing = 0.03  # Adjust this value to control the vertical spacing
    vertical_position = annotation_y

    # Add each line of the annotation separately
    for line in lines:
        ax.annotate(line, xy=(annotation_x, vertical_position),
                    xycoords='axes fraction', fontsize=12, color='white', ha='right')  # Set ha='right' for right alignment
        vertical_position -= vertical_spacing             
                

    plt.show()      




# -------- Violinplot-------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

def violin(data, y_column, x_column,
               font_family='Sangha', font_color='#FDF0F0', font_size=20,
               title_pad=15, bg_color='#212946', grid_color='#FE53BB',
               bar_color=['#FE53BB', '#FEFFAC', '#97FEED', '#E384FF', '#FF8400'],
               plot_title=None,
               hue=None,
               rotation=0,
               vert=True, 
               positions=None, 
               widths=0.5,
               showmeans=True, 
               showextrema=True, 
               showmedians=True, 
               split=False, figsize=(10,8), annotation='', ann_x=1.45,ann_y=-0.2, x_name=None, y_name=None):
    
    plt.style.use("seaborn-dark")

    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    data_sorted = data.sort_values(by=y_column, ascending=False)  # Sort data globally in ascending order
    
    
    if hue:
        data[hue] = data[hue].astype('category')

    unique_x_values = data[x_column].unique()

    if positions is None:
        positions = np.arange(len(unique_x_values))
        
    if x_name==None:
        x_name=x_column
    if y_name==None:
        y_name=y_column    

    plt.xlabel(x_name, fontname=font_family, fontsize=font_size, color=font_color)
    plt.ylabel(y_name, fontname=font_family, fontsize=font_size, color=font_color)

    if not plot_title:
        plot_title = f'{x_column} by {y_column}'

    ax.set_title(label=plot_title, fontsize=24, fontname=font_family, pad=title_pad, color=font_color)

    plt.xticks(rotation=rotation, color=font_color)
    plt.yticks(color=font_color)

    plt.grid(axis='y', linestyle='--', color=grid_color, alpha=0.7)

    if hue:
        if len(data[hue].unique()) > 2:
            ax.annotate("Too many hue values", xy=(0.5, 0.5), xycoords='axes fraction', color=font_color)
        if len(data[hue].unique()) == 2:
            bar_color = ['#FE53BB', '#97FEED']

    for x_value in unique_x_values:
        data_filtered = data[data[x_column] == x_value]
        label = str(x_value)
        color_index = np.where(unique_x_values == x_value)[0][0]
        color = bar_color[color_index % len(bar_color)]

        if hue is None:
            if fill is False:
                sns.violinplot(x=x_column, y=y_column, data=data_filtered, edgecolor=color, alpha=0.8, hue=hue, inner_kws=dict(color=".2", alpha=1))
            else:
                sns.violinplot(x=x_column, y=y_column, data=data_filtered, palette=[color], edgecolor=color,
                               alpha=0.8, hue=hue, inner_kws=dict(color=".2", alpha=1))
        else:
            if fill is False:
                sns.violinplot(x=x_column, y=y_column,palette=bar_color, 
                               data=data_filtered, edgecolor='gray', 
                               alpha=0.8, hue=hue, inner_kws=dict(color=".2", alpha=1), split=split)
                for patch in ax.patches:
                    clr = patch.get_facecolor()
                    patch.set_edgecolor(clr)
            else:

                data_filtered = data[data[x_column] == x_value]
                label = str(x_value)
                color_index = np.where(unique_x_values == x_value)[0][0]
                color = bar_color[color_index % len(bar_color)]
                sns.violinplot(x=x_column, y=y_column, data=data_filtered, palette=bar_color,
                               edgecolor='gray', alpha=0.8, hue=hue, inner_kws=dict(box_width=5, whis_width=2,color=".2", alpha=1),split=split)
                for patch in ax.patches:
                    clr = patch.get_facecolor()
                    patch.set_edgecolor(clr)

    if hue:
        legend_handles = []
        legend_labels = []

        for hue_value in data[hue].unique():
            data_filtered = data[data[hue] == hue_value]
            label = f'{hue_value}'
            color_index = np.where(data[hue] == hue_value)[0][0]
            color = bar_color[color_index % len(bar_color)]
            legend_handles.append(plt.Line2D([], [], color=color, label=label))
            legend_labels.append(label)

        legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), handles=legend_handles, labels=legend_labels)

        title = ax.get_legend().get_title()
        title.set_color('white')
        for text in legend.get_texts():
            text.set_color('white')

    if hue is None:
        for x_value in unique_x_values:
            data_filtered = data[data[x_column] == x_value]
            label = str(x_value)
            color_index = np.where(unique_x_values == x_value)[0][0]
            color = bar_color[color_index % len(bar_color)]
            for i in range(4, 0, -1):
                alpha = i / 25
                linewidth = i * 2
                sns.violinplot(x=x_column, y=y_column, data=data_filtered,
                               palette=[color], edgecolor=color, alpha=alpha, linewidth=linewidth,
                               inner_kws=dict(box_width=5, whis_width=2, alpha=1, color="0.2"))
                for patch in ax.patches:
                    clr = patch.get_facecolor()
                    patch.set_edgecolor(clr)

    else:
        for x_value in unique_x_values:
            data_filtered = data[data[x_column] == x_value]
            label = str(x_value)
            color_index = np.where(unique_x_values == x_value)[0][0]
            color = bar_color[color_index % len(bar_color)]


            for i in range(4, 0, -1):
                alpha = i / 25
                linewidth = i *2
                sns.violinplot(x=x_column, y=y_column,palette=bar_color, data=data_filtered, 
                               edgecolor='gray', alpha=alpha, hue=hue, 
                               inner_kws=dict(box_width=5, whis_width=2, alpha=1, color="0.2"), legend=False,
                              linewidth=linewidth, split=split)


    ax.set_ylim(bottom=0)
    
    for ax in plt.gcf().get_axes():
        ax.yaxis.labelpad = 10
        ax.xaxis.labelpad = 10
        
    # annotation
    annotation_text = annotation
    annotation_x = ann_x  # Keep it at the right edge to position the annotation to the right
    annotation_y = ann_y  # Y-coordinate of the annotation (negative value to place it at the bottom)

    # Split the annotation text into lines with a maximum of 60 characters each
    max_line_length = 60
    lines = [annotation_text[i:i+max_line_length] for i in range(0, len(annotation_text), max_line_length)]

    # Calculate the vertical position for each line
    vertical_spacing = 0.03  # Adjust this value to control the vertical spacing
    vertical_position = annotation_y

    # Add each line of the annotation separately
    for line in lines:
        ax.annotate(line, xy=(annotation_x, vertical_position),
                    xycoords='axes fraction', fontsize=12, color='white', ha='right')  # Set ha='right' for right alignment
        vertical_position -= vertical_spacing 
    
    plt.show() 


# -------- Pieplot-------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

def pie(data=None, y_column=None, x_column=None,
               font_family='Sangha', font_color='#FDF0F0', font_size=20,
               title_pad=15, bg_color='#212946', grid_color='#FE53BB',
               bar_color=['#FE53BB', '#FEFFAC', '#97FEED', '#E384FF', '#FF8400', '#45FFCA', '#0B666A', '#3E00FF'],
               width=0.8,
               plot_title=None,
               hue=None,
               rotation=0,
               explode=None,  # pie. default = False, example (0, 0, 0.1, 0)
               labels=None,    # pie
               shadow=None,   # pie
              startangle=0,    # pie
              ratios=None,     # pie
              ratios_labels=None,  # pie
              side_title=None,     # pie
              side_bar_color=1,    # pie default color for side bar. can be 1,2,3,4,5
              side_lines = False,
              connector=1.35,
              annotation=None,
              pie_legend=False, radius=1, figsize=(10,8), ann_x=315,ann_y=-0.1):  # pie
    
    plt.style.use("seaborn-dark")
     
    if ratios == None:    
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig, (ax,ax2) = plt.subplots(1,2, figsize=figsize)
        
                                
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)


        
    if pie_legend == True:
        colors = bar_color  # Use the bar_color parameter as colors for the pie chart
        bars, _ = ax.pie(x_column, colors=colors, explode=explode, startangle=startangle,
                         labeldistance=1.1, 
                         textprops={'color': '#FDF0F0', 'fontsize': 18, 'fontfamily': font_family},
                         shadow=shadow, radius=radius)
        if ratios== None:
            legend = ax.legend(loc='upper left', bbox_to_anchor=(1.1, 0.97), labels=labels, title=None)
        else:
            legend = ax.legend(loc='upper left', bbox_to_anchor=(247, 0.5), labels=labels, title=None)


        for text in legend.get_texts():
            text.set_color('white') 
        handles, labels = ax.get_legend().legendHandles, [text.get_text() for text in legend.get_texts()]

        for handle, label in zip(handles, labels):
                # Set the color of the handle to match the label's color
            color = handle.get_facecolor()
            handle.set_edgecolor(color)
            handle.set_alpha(0.7)
            handle.set_path_effects([path_effects.withStroke(linewidth=3)])



    else:    
        colors = bar_color  # Use the bar_color parameter as colors for the pie chart
        bars, labs = ax.pie(x_column, colors=colors, explode=explode, startangle=startangle,
                             labels=labels, labeldistance=1.1, 
                             textprops={'color': '#FDF0F0', 'fontsize': 18, 'fontfamily': font_family},
                             shadow=shadow)

    total = sum(x_column)  # Calculate the total value of all slices

    for i, (bar, color, label) in enumerate(zip(bars, colors, labels)):
        bar.set_edgecolor(color)  # Set the edgecolor to match the color of the slice
        bar.set_color(color)

        # Create a glowing effect by setting the same alpha and linewidth for each bar
        num_bars = len(bars)
        glow_alpha = [0.7] * num_bars
        glow_linewidth = [4] * num_bars

        bar.set_alpha(glow_alpha[i % num_bars])  # Cycle through alphas
        bar.set_linewidth(glow_linewidth[i % num_bars])

        # Calculate the percentage
        percentage = (x_column[i] / total) * 100

        # Calculate the position for the label within the bar
        angle = np.deg2rad(bar.theta1 + bar.theta2) / 2
        x = 0.5 * np.cos(angle)
        y = 0.5 * np.sin(angle)

        # Display the percentage label within the bar
        ax.text(x, y, f'{percentage:.1f} %', ha='center', va='center', fontsize=14, color='#170055')


    # create a side ratios bar for a slice
    if not ratios== None and not ratios_labels == None:
        ratios = sorted(ratios, reverse=False)
        bottom = 1
        width = .2
        if side_bar_color==1:
            side_bar_color='#FE53BB'    # rose
        elif side_bar_color==2: 
            side_bar_color='#FEFFAC'    # yellow
        elif side_bar_color==3:
            side_bar_color='#97FEED'   # blue
        elif side_bar_color==4:
            side_bar_color='#E384FF'   # violet
        elif side_bar_color==5:  
            side_bar_color='#FF8400'   #   orange     


        for j, (height, label) in enumerate(reversed([*zip(ratios, ratios_labels)])):
            bottom -= height
            bc = ax2.bar(0, height, width, bottom=bottom, color=side_bar_color, label=label,
                         alpha = 1/(j+1)+0.2 if j!=0 else 0.9, edgecolor=side_bar_color, linewidth=2)

            ax2.bar_label(bc, labels=[f"{height*1:0.1f}%"], label_type='center')


        #ax2.set_title(side_title)
        ax2.legend()
        ax2.axis('off')
        ax2.set_xlim(- 1.3 * width, 2.2 * width)
        ax.set_xlim(0.5 * width, 0.5 * width)


        # Drawing the lines
        if side_lines:
            from matplotlib.patches import ConnectionPatch
            center = bars[0].center
            r = bars[0].r
            bar_height = sum(ratios)

            # Calculate the coordinates for the connecting lines
            x = center[0]
            y = center[1]

            # Offset to make the lines meet closer to the center
            offset = 0.001  # Adjust this value to control the height of the connection point
            x_offset = x
            y_offset = y - offset * bar_height

            # Limit the length of the lines to the right
            line_length = connector  # Adjust this value to control the line length to the right (1.35 by default)

            # Calculate the endpoint coordinates for the lines
            x_end = x_offset + line_length
            y_end = y_offset

            # Create a common style for both connecting lines
            line_style = {'color': side_bar_color, 'linestyle': '--', 'linewidth': 1, 'alpha': 0.3}

            # Draw bottom connecting line
            con = ConnectionPatch(xyA=(-width / 2, -100), coordsA=ax2.transData, xyB=(x_end, y_end), coordsB=ax.transData, **line_style)
            ax2.add_artist(con)

            # Draw upper connecting line (using the same coordinates)
            con = ConnectionPatch(xyA=(-width / 2, 1), coordsA=ax2.transData, xyB=(x_end, y_end), coordsB=ax.transData, **line_style)
            ax2.add_artist(con)
            # End of creating lines


        legend = ax2.legend(loc='upper left', bbox_to_anchor=(0.6, 0.97))
        ax2.text(0.006, 5, side_title, ha='center', va='center', fontsize=10, color='white', fontname=font_family)
        for text in legend.get_texts():
            text.set_color('white')       





    if not plot_title is None:
        title = ax.set_title(plot_title, fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
        title.set_position([0.5, 1])
    else:
        ax.set_title(label=f'pie plot', fontsize=24, fontname=font_family, pad=title_pad, color=font_color)

    # these are just some invisible tricks lines to add the padding to the plot that would not work otherwise
    annotation_text_top = 'trick line'
    annotation_x_top = 0.5  # X-coordinate of the annotation
    annotation_y_top = 1.1  # Y-coordinate of the annotation (greater than 1 to place it at the top)
    ax.annotate(annotation_text_top, xy=(annotation_x_top, annotation_y_top),
                    xycoords='axes fraction', fontsize=12, color='none')


    # the actual annotation code
    annotation_text = annotation
    annotation_x = ann_x  # Keep it at the right edge to position the annotation to the right
    annotation_y = ann_y  # Y-coordinate of the annotation (negative value to place it at the bottom)

    # Split the annotation text into lines with a maximum of 80 characters each
    max_line_length = 80
    lines = [annotation_text[i:i+max_line_length] for i in range(0, len(annotation_text), max_line_length)]

    # Calculate the vertical position for each line
    vertical_spacing = 0.03  # Adjust this value to control the vertical spacing
    vertical_position = annotation_y

    # Add each line of the annotation separately
    for line in lines:
        ax.annotate(line, xy=(annotation_x, vertical_position),
                    xycoords='axes fraction', fontsize=12, color='white', ha='right')  # Set ha='right' for right alignment
        vertical_position -= vertical_spacing


    if annotation and not ratios==None:


        # these are just some invisible tricks lines to add the padding to the plot that would not work otherwise

        annotation_2_top = 0.5  # X-coordinate of the annotation
        annotation_2y_top = 1.13  # Y-coordinate of the annotation (greater than 1 to place it at the top)
        ax.annotate(annotation_text_top, xy=(annotation_2_top, annotation_2y_top),
                    xycoords='axes fraction', fontsize=12, color='none')
        annotation_text_vertical = "Vertical Annotation"
        annotation_x_vertical = -200  # X-coordinate of the annotation (greater than 1 to place it to the right)
        annotation_y_vertical = 0.5  # Y-coordinate of the annotation
        ax.annotate(annotation_text_vertical, xy=(0.5, -0.1), xycoords='axes fraction',
                    xytext=(annotation_x_vertical, annotation_y_vertical), textcoords='axes fraction',
                    fontsize=12, color='none', rotation=90)


    if ratios == None:
        plt.subplots_adjust(left=0.2, right=0.9, top=1.5, bottom=0.1)

    else:
        plt.subplots_adjust(left=0.2, right=1, top=0.6, bottom=0)

            

    plt.show()




# -------- Boxplot-------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

def box(x_column, font_family='Sangha', font_color='#FDF0F0', font_size=20,
               title_pad=15, bg_color='#212946', grid_color='#FE53BB',
               bar_color=['#FE53BB', '#FEFFAC', '#97FEED', '#E384FF', '#FF8400', '#45FFCA', '#0B666A', '#3E00FF'],
               width=0.8,
               plot_title=None,
               hue=None,
               rotation=0,
               notch=None, sym=None, vert=None, whis=None, 
               positions=None, widths=None, patch_artist=True, bootstrap=None, 
               usermedians=None, conf_intervals=None, meanline=None, showmeans=None, 
               showcaps=None, showbox=None, showfliers=None, boxprops=None, labels=None, 
               flierprops=None, medianprops=None, meanprops=None, capprops=None, 
               whiskerprops=None, manage_ticks=True, autorange=False, zorder=None, data=None, figsize=(10,8), x_name=None, y_name=None, annotation='', ann_x=1.1, ann_y=-0.2):

    plt.style.use("seaborn-dark")

    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    plt.grid(axis='y', linestyle='--', color=grid_color, alpha=0.7)

    # the plot starts here
    boxplots = ax.boxplot(x_column, 
                          notch=notch, sym=sym, vert=vert, whis=whis, 
                          positions=positions, widths=widths, patch_artist=True, bootstrap=bootstrap, 
                          usermedians=usermedians, conf_intervals=conf_intervals, meanline=meanline, showmeans=showmeans, 
                          showcaps=showcaps, showbox=showbox, showfliers=showfliers, boxprops=dict(linestyle='-', linewidth=2), labels=labels, 
                          flierprops=flierprops, medianprops=medianprops, meanprops=meanprops, capprops=capprops, 
                          whiskerprops=whiskerprops, manage_ticks=manage_ticks, autorange=autorange, zorder=zorder, data=data)

    # Color each box with a color from the bar_color list
    for patch, color in zip(boxplots['boxes'], bar_color):
        patch.set_facecolor(color + '60')  # Adding '60' for alpha (transparency)
        patch.set_edgecolor(color)  # Set edge color equal to facecolor
    
    # quick overwork for plt bug of coloring each half whisker with a differnt color. duplicated each color
    whisk_bar = ['#FE53BB', '#FE53BB', '#FEFFAC', '#FEFFAC', '#97FEED', '#97FEED', '#E384FF','#E384FF', '#FF8400','#FF8400', '#45FFCA','#45FFCA', '#0B666A','#0B666A', '#3E00FF', '#3E00FF']
    for whiskers, color in zip(boxplots['whiskers'], whisk_bar):  
            plt.setp(whiskers, color=color)
    for fliers, color in zip(boxplots['fliers'], bar_color):
            plt.setp(fliers, markeredgecolor=color)   
    for caps, color in zip(boxplots['caps'], whisk_bar):  
            plt.setp(caps, color=color)        
        

        
    # x and y labels
    # plt.xlabel(x_column, fontname=font_family, fontsize=font_size, color=font_color)

    # plot title
    if not plot_title is None:
        ax.set_title(plot_title, fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    else:
        ax.set_title(label=f'{plot_title}', fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    plt.xticks(rotation=rotation, color=font_color)
    plt.yticks(color=font_color)

    # the glow:
    plt.xticks(rotation=rotation)
    
    if x_name==None:
        x_name=x_column
    if y_name==None:
        y_name=y_column
 
    plt.ylabel(ylabel=x_name, fontname=font_family, fontsize=font_size, color=font_color)

    plt.xlabel(xlabel=y_name, fontname=font_family, fontsize=font_size, color=font_color)
    
    for ax in plt.gcf().get_axes():
        ax.yaxis.labelpad = 10
        ax.xaxis.labelpad = 10
        
    # annotation
    annotation_text = annotation
    annotation_x = ann_x  # Keep it at the right edge to position the annotation to the right
    annotation_y = ann_y  # Y-coordinate of the annotation (negative value to place it at the bottom)

    # Split the annotation text into lines with a maximum of 60 characters each
    max_line_length = 60
    lines = [annotation_text[i:i+max_line_length] for i in range(0, len(annotation_text), max_line_length)]

    # Calculate the vertical position for each line
    vertical_spacing = 0.03  # Adjust this value to control the vertical spacing
    vertical_position = annotation_y

    # Add each line of the annotation separately
    for line in lines:
        ax.annotate(line, xy=(annotation_x, vertical_position),
                    xycoords='axes fraction', fontsize=12, color='white', ha='right')  # Set ha='right' for right alignment
        vertical_position -= vertical_spacing 

    plt.show()

# -------- Scatterboxplot-------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

def scatterbox(x_column, font_family='Sangha', font_color='#FDF0F0', font_size=20,
               title_pad=15, bg_color='#212946', grid_color='#FE53BB',
               bar_color=['#FE53BB', '#FEFFAC', '#97FEED', '#E384FF', '#FF8400', '#45FFCA', '#0B666A', '#3E00FF'],
               width=0.8,
               plot_title=None,
               hue=None,figsize=(10,8),
               rotation=0, notch=None, sym=None, vert=None, whis=None,
               positions=None, widths=None, patch_artist=True, bootstrap=None,
               usermedians=None, conf_intervals=None, meanline=None, showmeans=None,
               showcaps=None, showbox=None, showfliers=None, boxprops=None, labels=None,
               flierprops=None, medianprops=None, meanprops=None, capprops=None,
               whiskerprops=None, manage_ticks=True, autorange=False, zorder=None, data=None, legend=False, x_name=None, y_name=None, annotation='', ann_x=1.1, ann_y=-0.2):

    plt.style.use("seaborn-dark")

    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    plt.grid(axis='y', linestyle='--', color=grid_color, alpha=0.7)

    # Box plot
    boxplots = ax.boxplot(x_column,
                          notch=notch, sym=sym, vert=vert, whis=whis,
                          positions=positions, widths=widths, patch_artist=True, bootstrap=bootstrap,
                          usermedians=usermedians, conf_intervals=conf_intervals, meanline=meanline, showmeans=showmeans,
                          showcaps=showcaps, showbox=showbox, showfliers=showfliers, boxprops=dict(linestyle='-', linewidth=2),
                          labels=labels, flierprops=flierprops, medianprops=medianprops, meanprops=meanprops,
                          capprops=capprops, whiskerprops=whiskerprops, manage_ticks=manage_ticks, autorange=autorange,
                          zorder=zorder, data=data)

    # Color each box with a color from the bar_color list
    for patch, color in zip(boxplots['boxes'], bar_color):
        patch.set_facecolor(color + '60')  # Adding '60' for alpha (transparency)
        patch.set_edgecolor(color)  # Set edge color equal to facecolor

    # Quick overwork for plt bug of coloring each half whisker with a different color. Duplicated each color
    whisk_bar = ['#FE53BB', '#FE53BB', '#FEFFAC', '#FEFFAC', '#97FEED', '#97FEED', '#E384FF', '#E384FF', '#FF8400',
                 '#FF8400', '#45FFCA', '#45FFCA', '#0B666A', '#0B666A', '#3E00FF', '#3E00FF']
    for whiskers, color in zip(boxplots['whiskers'], whisk_bar):
        plt.setp(whiskers, color=color)
    for fliers, color in zip(boxplots['fliers'], bar_color):
        plt.setp(fliers, markeredgecolor=color)

    for caps, color in zip(boxplots['caps'], whisk_bar):
        plt.setp(caps, color=color)

    # Scatter plot based on the same data as the boxes
    for lab, box_data, scatter_color in zip(labels, x_column, bar_color):
        scatter_x = np.full_like(box_data, lab)  # Create x positions for scatter dots
        ax.scatter(scatter_x, box_data, color=scatter_color, marker='o', label=lab)

    # x and y labels
    # plt.xlabel(x_column, fontname=font_family, fontsize=font_size, color=font_color)

    # Plot title
    if not plot_title is None:
        ax.set_title(plot_title, fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    else:
        ax.set_title(label=f'{plot_title}', fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    plt.xticks(rotation=rotation, color=font_color)
    plt.yticks(color=font_color)

    
    plt.xticks(rotation=rotation)
    
    if x_name==None:
        x_name=x_column
    if y_name==None:
        y_name=y_column
    
    plt.xlabel(x_name, fontname=font_family, fontsize=font_size, color=font_color)
    plt.ylabel(y_name, fontname=font_family, fontsize=font_size, color=font_color)

    if legend==True:
        legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

        for text in legend.get_texts():
            text.set_color('white')  # Set the legend item text color to white  # Add a legend for the scatter dots

            
            
    for ax in plt.gcf().get_axes():
        ax.yaxis.labelpad = 10
        ax.xaxis.labelpad = 10
        
    # annotation
    annotation_text = annotation
    annotation_x = ann_x  # Keep it at the right edge to position the annotation to the right
    annotation_y = ann_y  # Y-coordinate of the annotation (negative value to place it at the bottom)

    # Split the annotation text into lines with a maximum of 60 characters each
    max_line_length = 60
    lines = [annotation_text[i:i+max_line_length] for i in range(0, len(annotation_text), max_line_length)]

    # Calculate the vertical position for each line
    vertical_spacing = 0.03  # Adjust this value to control the vertical spacing
    vertical_position = annotation_y

    # Add each line of the annotation separately
    for line in lines:
        ax.annotate(line, xy=(annotation_x, vertical_position),
                    xycoords='axes fraction', fontsize=12, color='white', ha='right')  # Set ha='right' for right alignment
        vertical_position -= vertical_spacing         
            
    plt.show()



# -------- Jointplot-------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

def joint(data=None, x_column=None, y_column=None, hue=None, 
         kind='scatter', 
          space=0.2, dropna=False, 
         xlim=None, ylim=None, color=None, 
         palette=None, hue_order=None, hue_norm=None, marginal_ticks=False, 
         joint_kws=None, marginal_kws=None,
         font_family='Sangha', font_color='#FDF0F0', font_size=20,
         title_pad=15, bg_color='#212946', grid_color='#FE53BB',
         bar_color=['#FE53BB', '#FEFFAC', '#97FEED', '#E384FF', '#FF8400', '#45FFCA', '#0B666A', '#3E00FF'],
         width=0.8, plot_title=None, rotation=0,
         s=60,
         alpha=0.6,
         height=8,
         ratio=6,
         num=1,
         cut=5,
         marker=None,
         annotation = '', ann_x=0.85, ann_y=-0.2, x_name=None, y_name=None):
    
    # Set Seaborn style
    
    sns.set_style('ticks')
    sns.set_style("darkgrid", {
        "axes.facecolor": '#14192b', # this is the color of the upper and right plot
        "grid.color": "white",  # Set grid color to the same as the background
        "axes.titlepad": title_pad,
        "figure.facecolor":"#14192b"  # the area around the plots
    })
    
    
    
    #sns.set_theme(style="ticks")
    
    if hue==None:
        my_palette = bar_color[num-1]
    else:
        my_palette= sns.set_palette(sns.color_palette(bar_color))
 
    import warnings
    # Suppress all warnings
    warnings.filterwarnings("ignore")
   
    if kind == 'reg' or kind=='hex' or kind=='hist':
        plot = sns.jointplot(data=data, x=x_column, y=y_column, kind=kind, palette=my_palette,color=my_palette,
                         height=height, ratio=ratio, hue=hue, space=space)
        
        # setting the borders and bottom lines of the histograms to black
        for ax in [plot.ax_marg_x, plot.ax_marg_y]:
            for patch in ax.patches:
                patch.set_edgecolor('black')
            ax.spines['bottom'].set_color('black')  
            ax.spines['left'].set_color('black') 
            
    elif kind=='kde':
        plot = sns.jointplot(data=data, x=x_column, y=y_column, kind=kind, alpha=alpha, palette=my_palette,color=my_palette,
                         height=height, ratio=ratio, edgecolor=my_palette, s=s, hue=hue, space=space, joint_kws={"cut": cut, 'marker':marker})
        
        # setting the borders and bottom lines of the histograms to black
        for ax in [plot.ax_marg_x, plot.ax_marg_y]:
            for patch in ax.patches:
                patch.set_edgecolor('black')
            ax.spines['bottom'].set_color('black')  
            ax.spines['left'].set_color('black') 
    elif kind=='resid':
        plot = sns.jointplot(data=data, x=x_column, y=y_column, kind=kind, palette=my_palette,color=my_palette,
                         height=height, ratio=ratio, hue=hue, space=space)
        # setting the borders and bottom lines of the histograms to black
        for ax in [plot.ax_marg_x, plot.ax_marg_y]:
            for patch in ax.patches:
                patch.set_edgecolor('black')
            ax.spines['bottom'].set_color('black')  
            ax.spines['left'].set_color('black')
        
    else:
        plot = sns.jointplot(data=data, x=x_column, y=y_column, kind=kind, alpha=alpha, palette=my_palette,color=my_palette,
                         height=height, ratio=ratio, edgecolor=my_palette, s=s, hue=hue, space=space)
        
        # setting the borders and bottom lines of the histograms to black
        for ax in [plot.ax_marg_x, plot.ax_marg_y]:
            for patch in ax.patches:
                patch.set_edgecolor('black')
            ax.spines['bottom'].set_color('black')  
            ax.spines['left'].set_color('black') 
            
            
            
    plt.xticks(rotation=rotation)
    
    if x_name==None:
        x_name=x_column
    if y_name==None:
        y_name=y_column
    
    # Remove grid lines for the main joint plot
    plot.ax_joint.grid(False)
    
    # Remove grid lines for the histograms (marginal plots)
    plot.ax_marg_x.get_xaxis().grid(False)
    plot.ax_marg_y.get_yaxis().grid(False)
    
    
    plot.ax_joint.spines['top'].set_color('black')
    plot.ax_joint.spines['right'].set_color('black')
    
    plot.ax_joint.set_facecolor(bg_color)
    
    # Set the color of the space between the plots to match the background
    for spine in ['top', 'right', 'bottom', 'left']:
        plot.ax_joint.spines[spine].set_color('black')
        
    #sns.despine(bottom=True, left=True)    
    if hue:
        legend = plot.ax_joint.get_legend()
        for text in legend.get_texts():
            text.set_color('white') 
        #legend.set_fontcolor('white')  
  
    
    plot.ax_joint.set_xlabel(x_name, color=font_color, fontfamily=font_family, fontsize=16)
    plot.ax_joint.set_ylabel(y_name, color=font_color, fontfamily=font_family, fontsize=16)  
    plot.ax_joint.tick_params(axis='x', colors=font_color)
    plot.ax_joint.tick_params(axis='y', colors=font_color)
    x_label_pos = (0.5, -0.09)  # Adjust the second value to control the padding for x-label
    y_label_pos = (-0.09, 0.5)  # Adjust the first value to control the padding for y-label
    plot.ax_joint.xaxis.set_label_coords(*x_label_pos)
    plot.ax_joint.yaxis.set_label_coords(*y_label_pos)
    
    
    plot.fig.suptitle(plot_title, size=24, font=font_family, color=font_color).set_y(1.05)
    
    # these are just some invisible tricks lines to add the padding to the plot that would not work otherwise
    annotation_text_top = 'trick line'
    annotation_x_top = 0  # X-coordinate of the annotation
    annotation_y_top = 1.3  # Y-coordinate of the annotation (greater than 1 to place it at the top)
    ax.annotate(annotation_text_top, xy=(annotation_x_top, annotation_y_top),
                    xycoords='axes fraction', fontsize=12, color='none')


    # the actual annotation code
    annotation_text = annotation
    annotation_x = ann_x  # Keep it at the right edge to position the annotation to the right
    annotation_y = ann_y  # Y-coordinate of the annotation (negative value to place it at the bottom)

    # Split the annotation text into lines with a maximum of 60 characters each
    max_line_length = 60
    lines = [annotation_text[i:i+max_line_length] for i in range(0, len(annotation_text), max_line_length)]

    # Calculate the vertical position for each line
    vertical_spacing = 0.03  # Adjust this value to control the vertical spacing
    vertical_position = annotation_y

    # Add each line of the annotation separately
    for line in lines:
        ax.annotate(line, xy=(annotation_x, vertical_position),
                    xycoords='axes fraction', fontsize=12, color='white', ha='right')  # Set ha='right' for right alignment
        vertical_position -= vertical_spacing
    
    plt.show()



# -------- Displot-------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

def displot(data, y_column, font_family='Sangha', font_color='#FDF0F0', font_size=20,
         title_pad=15, bg_color='#212946', grid_color='#FE53BB',
         kde=False, hue=None, bar_color=['#FE53BB', '#FEFFAC', '#97FEED', '#E384FF', '#FF8400'],
           plot_title='', bins=30, y_name=None, x_name=None):
    
    plt.style.use("seaborn-dark")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    if hue:
        unique_hue_values = data[hue].unique()
        if len(unique_hue_values) == 0:
            print("No unique values found for 'hue'.")
            return

        for i, hue_value in enumerate(unique_hue_values):
            subset_data = data[data[hue] == hue_value]
            label = f'{hue_value}'
            color = bar_color[i % len(bar_color)]

            # Filter out 'nan' values
            valid_data = subset_data[y_column].dropna()
            
            if len(valid_data) > 0:
                # Create histogram with different colors for each hue
                hist, bins, patches = ax.hist(valid_data, bins=bins, alpha=0.5, label=label, color=color, density=True, edgecolor=color)

                if kde:
                    kde_obj = gaussian_kde(valid_data, bw_method='silverman')
                    x_values = np.linspace(valid_data.min(), valid_data.max(), 100)
                    kde_values = kde_obj(x_values)

                    # Create KDE plot with the same color as the distribution bars
                    plt.plot(x_values, kde_values, label=f'KDE ({hue_value})', color=color)

                    # Set edge color of the distribution bars to match the bar color
                    for patch in patches:
                        patch.set_edgecolor(color)

    else:
        label = 'Distribution'
        color = bar_color[0]

        # Filter out 'nan' values
        valid_data = data[y_column].dropna()

        if len(valid_data) > 0:
            # Create histogram with the same color for distribution bars and edges
            hist, bins, patches = ax.hist(valid_data, bins=30, alpha=0.5, label=label, color=color, density=True, edgecolor=color)

            if kde:
                kde_obj = gaussian_kde(valid_data, bw_method='silverman')
                x_values = np.linspace(valid_data.min(), valid_data.max(), 100)
                kde_values = kde_obj(x_values)

                # Create KDE plot with the same color as the distribution bars
                plt.plot(x_values, kde_values, label=f'KDE', color=color)
                
                
    if x_name==None:
        x_name=x_column
    if y_name==None:
        y_name=y_column  
        
    plt.xlabel(x_name, fontname=font_family, fontsize=font_size, color=font_color)    

    ax.set_title(plot_title, fontsize=24, fontname=font_family, pad=title_pad, color=font_color)
    plt.xticks(rotation=rotation, color=font_color)
    plt.yticks(color=font_color)
    plt.xlabel(y_name, fontname=font_family, fontsize=font_size, color=font_color)
    plt.grid(axis='y', linestyle='--', color=grid_color, alpha=0.7)

    # Set legend text color to font_color
    legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    for text in legend.get_texts():
        text.set_color(font_color)
    

    plt.show()


# -------- Pairplot-------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

def pairplot(data, hue=None, hue_order=None, 
             vars=None, x_vars=None, y_vars=None, kind='scatter', diag_kind='auto', 
             markers=None, height=2.5, aspect=1, corner=False, dropna=False, 
             plot_kws=None, 
             diag_kws=None, 
             grid_kws=None, size=None,
             rotation=0,
             annotation=None,
             font_family='Sangha', font_color='#FDF0F0', font_size=20,
             title_pad=15, bg_color='#212946', grid_color='#FE53BB',
             bar_color=['#FE53BB', '#FEFFAC', '#97FEED', '#E384FF', '#FF8400', '#45FFCA', '#0B666A', '#3E00FF'],
             num=1,
            plot_title=''):
    
    import warnings
    # Suppress all warnings
    warnings.filterwarnings("ignore")
    sns.set(rc={"axes.facecolor":"#212946","figure.facecolor":"#212946", 'ytick.color': font_color})
    
    if hue == None:
        my_palette = sns.set_palette(sns.color_palette(bar_color))
    else:
        my_palette = sns.set_palette(sns.color_palette(bar_color))
  
    sns.set_style({'grid.linestyle': ':', 'grid.color':'#2a365e'}) 
    
    
    # the plot itself
    if hue != None:
        plot = sns.pairplot(data, palette=my_palette, hue=hue, markers=markers, 
                        kind=kind, corner=corner, plot_kws=plot_kws, grid_kws=grid_kws, diag_kws=diag_kws)
    else:    
        plot = sns.pairplot(data, palette=my_palette, hue=hue, markers=markers, 
                        kind=kind, corner=corner, plot_kws=plot_kws, grid_kws=grid_kws, diag_kws=({'edgecolor':'black', 'linewidth':1}))
    
    # Set xticks and yticks font color and font size
    for ax in plot.axes.flat:
        ax.set_xticklabels(ax.get_xticklabels(), color=font_color, fontsize=12)
        #ax.set_yticklabels(ax.get_yticklabels(), color=font_color, fontsize=12)
        ax.set_xlabel(ax.get_xlabel(), color=font_color, fontsize=18)
        ax.set_ylabel(ax.get_ylabel(), color=font_color, fontsize=18)
        
 

    # Ensure both xticks and yticks are visible
    for ax in plot.axes.flat:
        ax.xaxis.set_visible(True)
        ax.yaxis.set_visible(True)
        
    if hue != None:    
        for text in plot.legend.texts:
            text.set_color(font_color)

        plot.legend.get_title().set_color(font_color)    
        
    for ax in plt.gcf().get_axes():
        ax.yaxis.labelpad = 10  
        ax.xaxis.labelpad = 10
    
        
        
    plot.fig.suptitle(plot_title, fontsize=26, color=font_color, y=1.05) 
    
    # these are just some invisible tricks lines to add the padding to the plot that would not work otherwise
    annotation_text_top = 'trick line'
    annotation_x_top = 0  # X-coordinate of the annotation
    annotation_y_top = 4.5  # Y-coordinate of the annotation (greater than 1 to place it at the top)
    ax.annotate(annotation_text_top, xy=(annotation_x_top, annotation_y_top),
                    xycoords='axes fraction', fontsize=12, color='none')
    
    plt.show()




