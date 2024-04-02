from abc import ABC, abstractmethod
import struct


class PayloadSerializer(ABC):
    @staticmethod
    @abstractmethod
    def serialize(payload):
        pass


class EmptyPayloadSerializer(PayloadSerializer):
    @staticmethod
    def serialize(payload):
        return b''
