from abc import ABC, abstractmethod

class IOHandler(ABC):

    @abstractmethod
    def send_output(self, content: str, from_name: str, from_queue: str, from_persona: str, to_queue: str, to_persona: str, cc_queue: str) -> None:
        """
        Abstract method to send output.
        Should send a message to the specified recipient.
        """
        pass

    @abstractmethod
    def graceful_shutdown(self) -> None:
        """
        Abstract method to perform a graceful shutdown of the IOHandler.
        This should close any open connections and clean up resources.
        """
        pass

    @abstractmethod
    def purge_queue(self) -> None:
        """
        Abstract method to purge the queue.
        This should remove all messages from the queue.
        """
        pass

    @abstractmethod
    def start_consuming(self) -> None:
        """
        Abstract method to start consuming messages from the queue.
        This should start the IOHandler listening for messages.
        """
        pass

    @abstractmethod
    def get_single_message(self, queue=None) -> dict:
        """
        Abstract method to get a single message from the specified queue.
        Should return the message if available, None otherwise.
        """
        pass

    @abstractmethod
    def inspect_queue(self, queue=None) -> dict:
        """
        Abstract method to inspect the specified queue.
        Should return details like message count and consumer count.
        """
        pass

    @abstractmethod
    def purge_queue(self, queue=None) -> None:
        """
        Abstract method to purge all messages from the specified queue.
        Should clear the queue of all messages.
        """
        pass
