from PIL import Image
import requests
from StringIO import StringIO

def find_most_used_color(image):
    width = image.width
    height = image.height

    print 'Flatting pixels...'

    pixels = image.load()
    flat_pixels = [pixels[i, j] for i in range(width) for j in range(height)]

    # for map
    def pixel_to_dict(pixel):
        def floor_tuple(values):
            def floor_10(value):
                return value - (value % 10)

            return tuple(floor_10(value) for value in values) # rgb

        return {floor_tuple(pixel): 1}

    # for reduce
    def merge_dicts(dict1, dict2):
        def put_all(source, destination):
            for key, value in source.iteritems():
                if key not in destination:
                    destination[key] = value
                else:
                    destination[key] += value

        result = {}

        put_all(dict1, result)
        put_all(dict2, result)

        return result

    print 'Convertting to reduceable objects...'
    dicts = map(pixel_to_dict, flat_pixels)

    print 'Reducing mapped objects...'
    print reduce(merge_dicts, dicts)

if __name__ == "__main__":
    print 'Getting image...'
    image_url = ''.join([
        'https://cdn3.vox-cdn.com/',
        'thumbor/wHxhv-dJn4itKsdqbWTqPlSwGto=/',
        '180x0:1872x952/1280x720/cdn0.vox-cdn.com/',
        'uploads/chorus_image/image/37251612/pokemon-list.0.0.png'
    ])
    response = requests.get(image_url)
    image = Image.open(StringIO(response.content))

    print 'Finding most used color...'
    find_most_used_color(image)

