import sys

# Function to calculate percentage from pixel values
def calculate_percentage(start_x, start_y, end_x, end_y, img_width, img_height):
    left = (start_x / img_width) * 100
    top = (start_y / img_height) * 100
    width = ((end_x - start_x) / img_width) * 100
    height = ((end_y - start_y) / img_height) * 100
    return left, top, width, height

# Function to generate HTML for each square
def generate_html(coordinates, img_width=1666, img_height=770):
    template = '''
<a
  onclick="clicked('')"
  style="
    position: absolute;
    background-color: rgba(0, 255, 115, 0.3);
    transition: background-color 0.3s ease;
    top: {top:.2f}%;
    left: {left:.2f}%;
    width: {width:.2f}%;
    height: {height:.2f}%;
  "
  onmouseover="this.style.backgroundColor='rgba(0, 255, 21, 0.66)';"
  onmouseout="this.style.backgroundColor='rgba(0, 255, 115, 0.3)';"
></a>
'''
    html_output = ""

    for coord in coordinates:
        left, top, width, height = calculate_percentage(
            coord[0], coord[1], coord[2], coord[3], img_width, img_height
        )
        html_output += template.format(top=top, left=left, width=width, height=height)

    return html_output

# Main function to handle input and output
def main():
    # Image dimensions (you can also take these as command-line arguments if needed)
    img_width = 1666
    img_height = 770

    # Example coordinates input (format: start_x, start_y, end_x, end_y)
    coordinates = [
        (319, 327, 655, 633),
        (937, 331, 1285, 614),
        (1091, 636, 1212, 695),
        (991, 634, 1088, 650),
        (920, 330, 937, 479),
        (920, 480, 936, 611),
        (684, 481, 895, 499),
        (898, 455, 919, 553),
        (656, 424, 685, 568),
        (537, 451, 628, 530),
        (686, 330, 919, 424),
        (656, 568, 925, 632),
        (1299, 388, 1527, 586),
        (1299, 597, 1538, 633),
        (1539, 616, 1586, 636),
        (1319, 308, 1524, 378),
        (1293, 310, 1318, 378),
        (1526, 308, 1585, 542),
        (1508, 112, 1529, 165),
        (1506, 165, 1525, 308),
        (1346, 247, 1525, 266),
        (1345, 115, 1362, 166),
        (1344, 166, 1365, 247),
        (1422, 113, 1501, 239),
        (1178, 84, 1265, 304),
        (153, 3, 750, 39),
        (751, 4, 1183, 45),
        (1184, 5, 1671, 45),
        (753, 109, 834, 307),
        (476, 115, 498, 163),
        (478, 165, 497, 278),
        (402, 258, 686, 278),
        (402, 278, 424, 322),
        (601, 283, 684, 326),
        (189, 415, 249, 554),
        (552, 114, 636, 254),
        (282, 72, 425, 215),
        (427, 71, 753, 113),
        (823, 78, 1174, 108),
        (1266, 82, 1603, 111),
        (601, 634, 874, 695),
        (298, 634, 347, 684),
        (413, 635, 600, 693)
    ]

    html_output = generate_html(coordinates, img_width, img_height)

    # Output the result
    print(html_output)

# Run the script
if __name__ == "__main__":
    main()
