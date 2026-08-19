"""Exactly-once logical processing over at-least-once delivery."""

from dataclasses import dataclass, field


class EquivocationError(ValueError):
    pass


class ReorderWindowError(ValueError):
    pass


@dataclass
class DeliveryInbox:
    next_step: int = 1
    window: int = 4
    played: dict[int, str] = field(default_factory=dict)
    buffered: dict[int, dict] = field(default_factory=dict)

    def offer(self, message: dict) -> list[dict]:
        step, digest = message["step"], message["commit"]
        if step in self.played:
            if self.played[step] != digest:
                raise EquivocationError(f"different commit for step {step}")
            return []
        if step < self.next_step:
            return []
        if step > self.next_step + self.window:
            raise ReorderWindowError(f"step {step} exceeds reorder window")
        if step > self.next_step:
            previous = self.buffered.get(step)
            if previous is not None and previous["commit"] != digest:
                raise EquivocationError(f"different buffered commit for step {step}")
            self.buffered[step] = message
            return []
        ready = [message]
        self.played[step] = digest
        self.next_step += 1
        while self.next_step in self.buffered:
            item = self.buffered.pop(self.next_step)
            self.played[self.next_step] = item["commit"]
            ready.append(item)
            self.next_step += 1
        return ready
