# worlds/mario_party_7/patch_format.py
from dataclasses import dataclass, asdict
from typing import List, Optional
import json

@dataclass
class BoardData:
    grand_canal: List[int]
    pagoda_peak: List[int]
    pyramid_peak: List[int]
    windmillville: List[int]
    neon_heights: List[int]
    bowsers_enchanted_inferno: List[int]


@dataclass
class PatchData:
    progressive_dice_blocks: bool
    board_data: Optional[BoardData]

    def to_json(self) -> bytes:
        """Convert to JSON bytes for storage"""
        return json.dumps(asdict(self), indent=2).encode()

    @classmethod
    def from_json(cls, data: bytes) -> 'PatchData':
        parsed = json.loads(data)

        return cls(
            parsed['progressive_dice_blocks'],
            parsed['board_data']
        )