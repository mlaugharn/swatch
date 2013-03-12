    usage: swatch.py [-h] [--light] [-r R] [-n N] [-c C] [--unique] image
    
    A tool to generate Textmate/Sublime Text themes from images.
    
    positional arguments:
      image       The image to extract colors from.
    
    optional arguments:
      -h, --help  show this help message and exit
      --light     Switch to light-background color scheme.
      -r R        Reduction of RGB colors. A reduction of 64 rounds RGB values to
    			  the nearest multiple of 64.
      -n N        Number of reduced colors to choose from.
      -c C        Minimum contrast between background and colors. 256 is the
    			  contrast between black and white.
      --unique    Use each color only once.