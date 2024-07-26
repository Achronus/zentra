import pytest
import string

from zentra_api.auth.enums import JWTAlgorithm
from zentra_api.auth.utils import generate_secret_key


class TestGenerateJWTSecretKey:
    @staticmethod
    def test_key_length_for_algorithms():
        algorithms = {
            JWTAlgorithm.HS256: 256 // 8,
            JWTAlgorithm.HS384: 384 // 8,
            JWTAlgorithm.HS512: 512 // 8,
        }

        for algo, expected_length in algorithms.items():
            key = generate_secret_key(algo)
            assert len(key) == expected_length

    @staticmethod
    def test_key_character_set():
        valid_chars = string.ascii_letters + string.digits + "-_"

        for algo in JWTAlgorithm:
            key = generate_secret_key(algo)
            assert all(c in valid_chars for c in key)

    @staticmethod
    def test_default_algorithm():
        key = generate_secret_key()
        expected_length = 256 // 8
        assert len(key) == expected_length

    @staticmethod
    def test_invalid_algorithm():
        invalid_algorithms = [128, 1024, "string", None]

        for algo in invalid_algorithms:
            with pytest.raises(ValueError):
                generate_secret_key(algo)
