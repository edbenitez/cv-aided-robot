from PIL.Image import fromarray
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype, load_default
from numpy import ceil, copyto, array

def jpeg_to_nparray(img_path):
    img = Image.open(img_path) # read using pillow
    data = np.asarray(img) # convert to numpy array
    return data

def print_hello():
    print('Hello I am in vis')

def draw_all_boxes_on_images(
        image,
        boxes,
        classes,
        scores):
    
    threshold = 0.50
    print('scores')
    print(scores)
    print('boxes')
    print(boxes)
    
    box_coord_list = []
    for i in range(5):
        if scores[i] > threshold:
            print("Detected object with score ", scores[i])
            box = tuple(boxes[i].tolist())
            print('Box coordinates', box)
            box_coord_list.append(box)

    for box in box_coord_list:
        print('Overlaying Box on Image')
        draw_bounding_box_on_image(
                image=image,
                ymin=box[0],
                xmin=box[1],
                ymax=box[2],
                xmax=box[3],
                color='red',
                thickness=4,
                display_str_list=['sample'],
                use_normalized_coordinates=True)
    
# receives an image in __ format along with box coordinates returned from net
def draw_bounding_box_on_image(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color='red',
                               thickness=4,
                               display_str_list=(),
                               use_normalized_coordinates=True):
    print('DRAWING BOX***********************************************************************************')
    # convert to Pillow image
    print('Converting image to Pillow img')
    image_pillow = fromarray(image) 

    print('Instantiated Draw object with input image')
    draw = Draw(image_pillow)

    print('Grabbing image dimensions')
    im_width, im_height = image_pillow.size

    if use_normalized_coordinates:
        (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                  ymin * im_height, ymax * im_height)
    else:
        (left, right, top, bottom) = (xmin, xmax, ymin, ymax)
    
    print('Drawing line')
    draw.line([(left, top), (left, bottom), (right, bottom),
               (right, top), (left, top)], width=thickness, fill=color)
    
    print('Setting font')
    try:
        font = truetype('arial.ttf', 24)
    except IOError:
        font = load_default()
    

    print('Calculating possible boundary exceed')
    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)


    
    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = bottom + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = ceil(0.05 * text_height)
        draw.rectangle(
            [(left, text_bottom - text_height - 2 * margin), (left + text_width,
                                                              text_bottom)],
            fill=color)
        draw.text(
            (left + margin, text_bottom - text_height - margin),
            display_str,
            fill='black',
            font=font)
        text_bottom -= text_height - 2 * margin
    # overwrite original image with (Pillow -> numpy array) image
    copyto(image, array(image_pillow)) 

    return image
