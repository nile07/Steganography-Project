from Crypto.Util.Padding import unpad
# from Crypto.Cipher import AES
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

class Steganography:
    @staticmethod
    def encrypt_message(image_path, message, password):
        # AES Encryption
        salt = get_random_bytes(16)
        key = PBKDF2(password, salt, dkLen=32, count=100000)
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
        
        # Prepare payload: [SALT + IV + CIPHERTEXT]
        payload = salt + cipher.iv + ct_bytes
        
        # LSB Embedding
        img = cv2.imread(image_path)
        max_bytes = img.shape[0] * img.shape[1] * 3 // 8
        if len(payload) > max_bytes:
            raise ValueError("Message too large for image capacity")
        
        binary_payload = ''.join(f"{byte:08b}" for byte in payload)
        flat = img.flatten()
        for i in range(len(binary_payload)):
            flat[i] = (flat[i] & 0xFE) | int(binary_payload[i])
        return flat.reshape(img.shape)
    
    @staticmethod
    def decrypt_message(encrypted_img, password):
        try:
            # Extract LSBs
            flat = encrypted_img.flatten()
            binary = ''.join(str(byte & 1) for byte in flat)
            payload = bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
            
            # Validate payload structure
            if len(payload) < 32:  # Salt (16) + IV (16) + min 1-byte ciphertext
                raise ValueError("Invalid payload: Image may not contain hidden data")
            
            salt = payload[:16]
            iv = payload[16:32]
            ct = payload[32:]
            
            # Key derivation
            key = PBKDF2(password, salt, dkLen=32, count=100000)
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            
            # Decrypt and unpad
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode()
        
        except ValueError as e:
            if "Padding is incorrect" in str(e):
                raise ValueError("Wrong passcode or corrupted data")
            else:
                raise
    # @staticmethod
    # def decrypt_message(encrypted_img, password):
    #     # Extract LSBs
    #     flat = encrypted_img.flatten()
    #     binary = ''.join(str(byte & 1) for byte in flat)
    #     payload = bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
        
    #     # Split payload
    #     salt = payload[:16]
    #     iv = payload[16:32]
    #     ct = payload[32:]
        
    #     # AES Decryption
    #     key = PBKDF2(password, salt, dkLen=32, count=100000)
    #     cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    #     pt = unpad(cipher.decrypt(ct), AES.block_size)
    #     return pt.decode()