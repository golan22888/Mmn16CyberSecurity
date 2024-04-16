from abc import ABC, abstractmethod


class PayloadSerializer(ABC):
    @staticmethod
    @abstractmethod
    def serialize(payload):
        pass


class EmptyPayloadSerializer(PayloadSerializer):
    @staticmethod
    def serialize(payload):
        return b''
