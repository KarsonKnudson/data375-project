import os
import threading
from queue import Queue
from PIL import Image, ImageDraw

# Enable multi-threading queue
q_in = Queue(maxsize=0)
num_worker_threads = 12

def worker(thread_id):
	"""Get tasks from queue and execute them."""
	while True:
		folder = q_in.get()
		get_pal(folder, thread_id)
		q_in.task_done()

def get_colors(image_file, numcolors=5):
    # Resize image to speed up processing
    img = Image.open(image_file)

    # Reduce to palette
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=numcolors)

    # Find dominant colors
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    colors = list()
    
	# Check if there are less colors in image than specified
    if len(color_counts) < numcolors:
        numcolors = len(color_counts)
    
    # Add RGB colors of palette to tuple
    for i in range(numcolors):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
        colors.append(tuple(dominant_color))
    
    return colors

def save_palette(colors, swatchsize, outfile):
    """Saves palette of colors as image of squares."""
    num_colors = len(colors)
    palette = Image.new('RGB', (swatchsize*num_colors, swatchsize))
    draw = ImageDraw.Draw(palette)
    posx = 0
    for color in colors:
        draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=color) 
        posx = posx + swatchsize

    del draw
    palette.save(outfile, "PNG")

def get_pal(folder, id):
    """Analyze icon files and output palette information."""
    print("+ [Thread " + str(id) + "] Started file PAL\\" + folder)
    if not os.path.exists('PAL\\' + folder):
        os.makedirs('PAL\\' + folder)
    log_colors = open(".\\COLOR_DAT\\" + folder + ".info.dat", "w")
    for root, dirs_n, files in os.walk('.\ICONS\\' + folder):
        for filename in files:
            path = root + '\\' + filename
            error = 0
            try:
                colors = get_colors(path)
            except Exception as e:
                print("! [Thread " + str(id) + "] " + path + str(e))
                error = 1
            if error == 0:
                appId = filename.split('_')[0].rstrip('.png')
                rating = filename.split('_')[1].rstrip('.png')
                downloads = filename.split('_')[2].rstrip('.png')
                to_write = str(appId) + '\n' + str(colors) + '\n' + str(rating) + '\n' + str(downloads) + '\n'
                chars = ["[","]","(",")"," "]
                for char in chars:
                    to_write = to_write.replace(char, "")
                to_write =  to_write.replace(","," ")
                log_colors.write(to_write)
                save_palette(colors, 20, outfile = (".\\PAL\\" + folder + "\\" + filename.rstrip('.png') + "_pal.png"))
    log_colors.close()

def main():
    # Start threads
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(i,))
        t.daemon = True
        t.start()

    # Check if icon directory exists
    if not os.path.exists('ICONS'):
        print("! [ERROR] No 'ICONS' folder found.")
    else:
        if not os.path.exists('PAL'):
            os.makedirs('PAL')
        if not os.path.exists('COLOR_DAT'):
            os.makedirs('COLOR_DAT')
        # For each folder, start a new task to process images
        for root_n, dirs, files_n in os.walk('.\ICONS'):
            for folder in dirs:
                q_in.put(folder)

    q_in.join()
    print("Complete.")

main()