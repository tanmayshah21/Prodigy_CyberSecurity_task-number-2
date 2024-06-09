from PIL import Image
import random
import sys

def divide_blocks(image, block_size):
    width, height = image.size
    blocks = []
    for x in range(0, width, block_size):
        for y in range(0, height, block_size):
            block = image.crop((x, y, x + block_size, y + block_size))
            blocks.append((block, (x, y)))
    return blocks

def combine_blocks(image, blocks, block_size):
    for block, (x, y) in blocks:
        image.paste(block, (x, y))
    return image

def encrypt_image(input_image_path, output_image_path, key, block_size=8):
    with Image.open(input_image_path) as img:
        img = img.convert('RGB')
        blocks = divide_blocks(img, block_size)
        
        random.seed(key)
        random.shuffle(blocks)
        
        for i in range(len(blocks)):
            block, (x, y) = blocks[i]
            pixels = block.load()
            for i in range(block.size[0]):
                for j in range(block.size[1]):
                    r, g, b = pixels[i, j]
                    r = (r + key) % 256
                    g = (g + key) % 256
                    b = (b + key) % 256
                    pixels[i, j] = (r ^ key, g ^ key, b ^ key)
        
        encrypted_img = Image.new('RGB', img.size)
        encrypted_img = combine_blocks(encrypted_img, blocks, block_size)
        encrypted_img.save(output_image_path)

def decrypt_image(input_image_path, output_image_path, key, block_size=8):
    with Image.open(input_image_path) as img:
        img = img.convert('RGB')
        blocks = divide_blocks(img, block_size)
        
        random.seed(key)
        random.shuffle(blocks)
        
        for i in range(len(blocks)):
            block, (x, y) = blocks[i]
            pixels = block.load()
            for i in range(block.size[0]):
                for j in range(block.size[1]):
                    r, g, b = pixels[i, j]
                    r = (r ^ key)
                    g = (g ^ key)
                    b = (b ^ key)
                    pixels[i, j] = ((r - key) % 256, (g - key) % 256, (b - key) % 256)
        
        decrypted_img = Image.new('RGB', img.size)
        decrypted_img = combine_blocks(decrypted_img, blocks, block_size)
        decrypted_img.save(output_image_path)

def main():
    if len(sys.argv) != 5:
        print("Usage: python image_encryptor.py <encrypt/decrypt> <input_image> <output_image> <key>")
        return

    operation = sys.argv[1].lower()
    input_image_path = sys.argv[2]
    output_image_path = sys.argv[3]
    key = int(sys.argv[4])

    if operation == 'encrypt':
        encrypt_image(input_image_path, output_image_path, key)
        print(f"Image encrypted and saved to {output_image_path}")
    elif operation == 'decrypt':
        decrypt_image(input_image_path, output_image_path, key)
        print(f"Image decrypted and saved to {output_image_path}")
    else:
        print("Invalid operation. Use 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()
