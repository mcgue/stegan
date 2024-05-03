# Hides a message in an image

from PIL import Image

# Function to convert an integer to binary string
def int_to_bin(number):
    return bin(number)[2:].zfill(8)

# Function to hide a message in an image
def hide_message(image_path, message):
    img = Image.open(image_path)
    pixels = img.load()

    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Check if the message can fit in the image
    if len(binary_message) > img.width * img.height * 3:
        raise ValueError("Message is too large to fit in the image")

    index = 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]

            if index < len(binary_message):
                r = int_to_bin(r)
                g = int_to_bin(g)
                b = int_to_bin(b)

                r = int(r[:-1] + binary_message[index], 2)
                index += 1
                if index < len(binary_message):
                    g = int(g[:-1] + binary_message[index], 2)
                    index += 1
                if index < len(binary_message):
                    b = int(b[:-1] + binary_message[index], 2)
                    index += 1

                pixels[x, y] = (r, g, b)

    img.save("hidden_message.png")

# Function to extract a message from an image
def extract_message(image_path):
    img = Image.open(image_path)
    pixels = img.load()

    binary_message = ''
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary_message += int_to_bin(r)[-1]
            binary_message += int_to_bin(g)[-1]
            binary_message += int_to_bin(b)[-1]

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        message += chr(int(byte, 2))

    return message

# Example usage
message_to_hide = "Hello, this is a secret message!"
hide_message("image.png", message_to_hide)

extracted_message = extract_message("hidden_message.png")
print("Extracted message:", extracted_message)
