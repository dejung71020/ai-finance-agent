# app/core/encryption.py
import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.core.config import settings

def _get_key() -> bytes:
    # .env 에 저장된 ENCRYPTION_KEY 16진수 문자열을 Bytes로 변환
    return bytes.fromhex(settings.ENCRYPTION_KEY)

def encrypt(plaintext: str) -> str:
    '''
    1. 암호화 키를 장착한 암호기 aesgcm 을 생성
    2-1. 임시 번호 nonce를 12바이트만큼 랜덤 생성
    2-2. 같은 비밀번호여도 다르게 보임
    3. 임시 번호와 평문을 사용해 암호문 생성
    4. 임시번호 + 암호문 을 합친 뒤 Base64로 인코딩하여 문자열로 반환
    '''
    aesgcm = AESGCM(_get_key())
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return base64.b64encode(nonce + ciphertext).decode()

def decrypt(token: str) -> str:
    '''
    1. 똑같은 암호화 키를 장착한 암호기 aesgcm 생성
    2. 토큰을 bytes로 암호화
    3. 임시 번호와 암호문을 분리
    4. 임시 번호와 암호문을 사용해 decrypt(암호해독), 텍스트로 반환
    '''
    aesgcm = AESGCM(_get_key())
    data = base64.b64decode(token)
    nonce, ciphertext = [data[:12], data[12:]]
    return aesgcm.decrypt(nonce, ciphertext, None).decode()