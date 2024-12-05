from PIL import Image, ImageDraw
from JewelList import JewelList
import math


class JewelNecklace(JewelList):
    def __init__(self, n, *args):
        super().__init__(n, *args)


    def toImage(self, filename: str) -> None:
        # Create an image canvas
        img_size = (500, 500)
        img = Image.new("RGB", img_size, "white")
        draw = ImageDraw.Draw(img)
        center = (img_size[0] // 2, img_size[1] // 2)
        # Set different radii for x and y to create an ellipse
        radius_x = img_size[0] // 2 - 20  # width radius
        radius_y = img_size[1] // 2 - 50  # height radius, make it more elliptical
        jewel_radius = 15  # make jewels bigger

        # Place jewels along the circumference of an ellipse
        num_jewels = len(self.JL)
        jewel_centers = []
        for i, jewel in enumerate(self.JL):
            angle = 2 * math.pi * i / num_jewels
            x = center[0] + radius_x * math.cos(angle)
            y = center[1] + radius_y * math.sin(angle)
            jewel_centers.append((x, y))
            # Draw the jewel
            bbox = [x - jewel_radius, y - jewel_radius, x + jewel_radius, y + jewel_radius]
            color = jewel.gem
            draw.ellipse(bbox, fill=color)

        # Add a thin line connecting all jewels
        for i in range(num_jewels):
            start = jewel_centers[i]
            end = jewel_centers[(i + 1) % num_jewels]  # wrap around to the first jewel
            draw.line([start, end], fill='black', width=1)

        # Save the image
        img.save(filename + ".png")

    def toImageWithAnswer(self, filename: str, answer: list) -> None:
        # Create an image canvas
        img_width = 650
        img_height = 200
        img = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(img)
        # Multiply each element in answer by len(self.JL) to get even integer numbers
        scaled_answer = []
        for a in answer:
            if not isinstance(a, int):
                # Multiply by len(self.JL) and round to integer
                scaled_answer.append(int(a * len(self.JL)))
            else:
                scaled_answer.append(a)

        index = 0
        x_pos = 50  # starting x position
        jewel_width = 30  # make jewels bigger
        jewel_height = 30
        y_center = img_height // 2
        offset = 20  # amount to move up or down
        previous_center = None  # to store the previous jewel center

        for a in scaled_answer:
            num_jewels = abs(a)
            if num_jewels == 0:
                continue
            # Get the jewels from self.JL
            end_index = int(index + num_jewels)
            if end_index > len(self.JL):
                end_index = len(self.JL)
            jewels = self.JL[index:end_index]
            for jewel in jewels:
                # x position
                x = x_pos
                # y position
                if a > 0:
                    y = y_center - offset  # move up
                else:
                    y = y_center + offset  # move down
                bbox = [x, y, x + jewel_width, y + jewel_height]
                color = jewel.gem
                draw.ellipse(bbox, fill=color)
                # Draw line connecting jewels
                current_center = (x + jewel_width / 2, y + jewel_height / 2)
                if previous_center is not None:
                    draw.line([previous_center, current_center], fill='black', width=1)
                previous_center = current_center
                x_pos += jewel_width + 5  # increment x position
            # After each iteration, draw a thin vertical line
            if (end_index < len(self.JL)) and int(index + num_jewels) < len(self.JL): 
                draw.line([(x_pos, 0), (x_pos, img_height)], fill='black', width=1)
                index += num_jewels
        # Save the image
        img.save(filename + ".png")


