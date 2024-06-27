from PIL import Image
import numpy as np


def encrypt_image(image_path, output_path, key):
    # Open the image
    img = Image.open(image_path)
    img = img.convert("RGB")
    np_img = np.array(img, dtype=np.int16)  # Use a higher data type to prevent overflow

    # Encrypt the image by modifying pixel values
    encrypted_img = (np_img + key) % 256

    # Perform pixel swapping for additional encryption
    encrypted_img = encrypted_img.flatten()
    np.random.seed(key)
    np.random.shuffle(encrypted_img)
    encrypted_img = encrypted_img.reshape(np_img.shape)

    # Convert back to uint8
    encrypted_img = encrypted_img.astype(np.uint8)

    # Save the encrypted image
    encrypted_img = Image.fromarray(encrypted_img)
    encrypted_img.save(output_path)


def decrypt_image(image_path, output_path, key):
    # Open the encrypted image
    img = Image.open(image_path)
    img = img.convert("RGB")
    np_img = np.array(img, dtype=np.int16)  # Use a higher data type to prevent overflow

    # Reverse pixel swapping
    shape = np_img.shape
    np_img = np_img.flatten()
    np.random.seed(key)
    indices = np.arange(np_img.size)
    np.random.shuffle(indices)
    original_indices = np.argsort(indices)
    decrypted_img = np_img[original_indices]
    decrypted_img = decrypted_img.reshape(shape)

    # Decrypt the image by reversing the pixel value modification
    decrypted_img = (decrypted_img - key) % 256

    # Convert back to uint8
    decrypted_img = decrypted_img.astype(np.uint8)

    # Save the decrypted image
    decrypted_img = Image.fromarray(decrypted_img)
    decrypted_img.save(output_path)


def main():
    while True:
        choice = input("Type 'encrypt' to encrypt an image, 'decrypt' to decrypt an image, or 'exit' to quit: ").lower()
        if choice == 'exit':
            break
        if choice not in ['encrypt', 'decrypt']:
            print("Invalid choice. Please type 'encrypt', 'decrypt', or 'exit'.")
            continue

        image_path = input("Enter the path to the image: ").strip().strip('"')
        output_path = input("Enter the path for the output image: ").strip().strip('"')
        try:
            key = int(input("Enter an encryption key (integer): "))
        except ValueError:
            print("Invalid key. Please enter an integer.")
            continue

        if choice == 'encrypt':
            encrypt_image(image_path, output_path, key)
            print(f"Image encrypted and saved to {output_path}")
        elif choice == 'decrypt':
            decrypt_image(image_path, output_path, key)
            print(f"Image decrypted and saved to {output_path}")


if __name__ == "__main__":
    main()
