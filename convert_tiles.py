#!/usr/bin/env python3


import click
import png


@click.command()
@click.argument('filename')
def convert_tiles(filename):
    reader = png.Reader(filename)
    image_info = reader.asRGB()

    width = image_info[0]
    height = image_info[1]
    rows = list(image_info[2])
    info = image_info[3]

    if width % 8 != 0 or height % 8 != 0:
        print('width and height must both be divisible by 8: ({}, {})'.format(width, height))
        return

    print('w x h: {} x {}'.format(width, height))

    colors = find_colors(rows)
    if len(colors) > 4:
        print('too many colors in input: {}'.format(len(colors)))
        return

    tiles = generate_tiles(rows)

    
def generate_tiles(rows):
    tile_length = 8
    stride = 3
    tile_rows = []

    for row_offset in range(0, len(rows), tile_length):
        rows_for_tile = rows[row_offset:row_offset + tile_length]
        tile_columns = []

        for column_offset in range(0, len(rows[row_offset]), tile_length * stride):
            current_tile_rows = []

            for row in rows_for_tile:
                rgb_row = row[column_offset:column_offset + (tile_length * stride)]
                color_row = []

                for i in range(0, len(rgb_row), stride):
                    color = (rgb_row[i], rgb_row[i + 1], rgb_row[i + 2])
                    color_row.append(color)
                
                current_tile_rows.append(color_row)

            tile_columns.append(current_tile_rows)
        
        tile_rows.append(tile_columns)

    return tile_rows


def find_colors(rows):
    found_colors = []

    for row in rows:
        for i in range(0, len(row), 3):
            color = (row[i], row[i + 1], row[i + 2])

            if color not in found_colors:
                found_colors.append(color)

    return sorted(found_colors, key=lambda color: color[0])


if __name__ == '__main__':
    convert_tiles()
