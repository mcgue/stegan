# Hide message in an image

# import module (need to have pillow installed)
from PIL import Image

# Function to hide a message in an image
def hide_message(image_path, message):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    message += '\0'  # Add null character as end marker
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    if len(binary_message) > (width * height * 3):  # Check if message can fit
        print("Message is too long to be hidden in this image.")
        return

    idx = 0
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            new_pixel = []
            for value in pixel:
                if idx < len(binary_message):
                    new_value = (value & 254) | int(binary_message[idx])
                    idx += 1
                else:
                    new_value = value
                new_pixel.append(new_value)
            pixels[x, y] = tuple(new_pixel)

    img.save('hidden_message.png')
    print("Message hidden successfully.")

# Function to extract a message from an image
def extract_message(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    binary_message = ''

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            r = pixel[0]
            binary_message += str(r & 1)

            if binary_message[-8:] == '00000000':  # Check for null character as end marker
                break
        else:
            continue
        break

    message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message) - 8, 8))
    print("Extracted message:", message)

# Example usage
image_path = 'image.png'
message_to_hide = "Hello, this is a hidden message!"

# Hide message
hide_message(image_path, message_to_hide)

# Extract message from the modified image
extract_message('hidden_message.png')
