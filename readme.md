## BEFORE STARTING

1. Download the entire directory to your computer.
2. Extract the folder 'node-modules'.
3. Ensure Node.js is installed and executable through your command line interface of choice.

## TO SCRAPE APP DATA:
1. Run 'scrape_data.js' using Node from the command line.
2. The scraped data, organized by category, will be available in folder '\data_xxxxxxxxxxxxx' where x is the data's timestamp (UNIX milliseconds since 1/1/1970).

## TO DOWNLOAD APP ICONS:
1. Install the os, json, and requests libraries to your Python environment.
2. Run 'download_icon_from_dat.py' using Python from the command line.
3. The output images are located within the same directory as the data files, organized by app category and named according to appId and number of installs.

## TO GET COLOR DATA AND PALLETTES
1. Move all of the folders of downloaded icons into a folder called 'ICONS'.
2. Run 'get_color_data.py' using Python from the command line.
3. The output data files will be in '\COLOR_DAT' and the color pallettes will be in '\PAL'.

## TO VISUALIZE/ANALYZE
1. Make sure 'analysis.Rmd' is in the same folder as '\COLOR_DAT'.
2. Run 'analysis.Rmd' in your R interpreter of choice.
3. The output visualizations will be in '\VIS'.
