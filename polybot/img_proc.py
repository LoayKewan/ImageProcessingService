from pathlib import Path
from matplotlib.image import imread, imsave


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self):

        # TODO remove the `raise` below, and write your implementation
        from PIL import Image

        # # Create a new grayscale image
        # data = [
        #     [124.3859, 114.8707, 104.5836, 94.1502, 78.0764, 58.8288, 48.9932, 48.0319, 66.0795, 71.1499, 82.0779,
        #      95.9948, 107.6669, 116.2746, 122.0613, 127.0222, 126.9235, 130.1404, 135.8625, 126.0053, 104.0183, 98.9865,
        #      103.3559, 98.8402, 102.8398, 106.1276, 103.3559, 98.0467, 94.9653, 91.243, 91.9979, 100.2852, 104.8826,
        #      109.8929, 112.9635, 114.6752, 121.0274, 130.6566, 141.8557, 147.9906, 132.1924, 134.0997, 139.6261,
        #      148.0983, 159.011, 169.3367, 176.0156, 179]
        # ]

        # Assuming each sublist represents a row in the image
        image_width = len(self.data[0])
        image_height = len(self.data)

        # Create a grayscale image from the data
        image = Image.new('L', (image_width, image_height))
        image.putdata(sum(self.data, []))

        # Rotate the image by 90 degrees
        rotated_image = image.rotate(90)

        self.data = rotated_image


    def salt_n_pepper(self):
        # TODO remove the `raise` below, and write your implementation
        raise NotImplementedError()

    def concat(self, other_img, direction='horizontal'):
        # TODO remove the `raise` below, and write your implementation
        raise NotImplementedError()

    def segment(self):
        # TODO remove the `raise` below, and write your implementation
        raise NotImplementedError()
