from dataclasses import dataclass
from enum import Enum
from typing import Optional

from blspy import G1Element, G2Element

from chia.types.blockchain_format.proof_of_space import ProofOfSpace
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.util.ints import uint64, uint16, uint32
from chia.util.streamable import Streamable, streamable


class PoolErrorCode(Enum):
    REVERTED_SIGNAGE_POINT = 1
    TOO_LATE = 2
    NOT_FOUND = 3
    INVALID_PROOF = 4
    PROOF_NOT_GOOD_ENOUGH = 5
    INVALID_DIFFICULTY = 6
    INVALID_SIGNATURE = 7
    SERVER_EXCEPTION = 8
    INVALID_P2_SINGLETON_PUZZLE_HASH = 9
    FARMER_NOT_KNOWN = 10
    FARMER_ALREADY_KNOWN = 11


# GET /pool_info
@dataclass(frozen=True)
@streamable
class GetPoolInfoResponse(Streamable):
    name: str
    logo_url: str
    minimum_difficulty: uint64
    relative_lock_height: uint32
    protocol_version: str
    fee: str
    description: str
    target_puzzle_hash: bytes32



@dataclass(frozen=True)
@streamable
class PostPartialPayload(Streamable):
    launcher_id: bytes32
    proof_of_space: ProofOfSpace
    sp_hash: bytes32
    end_of_sub_slot: bool
    suggested_difficulty: uint64  # This is suggested the difficulty threshold for this account
    owner_public_key: G1Element  # Current public key specified in the singleton
    payout_instructions: str  # The farmer can choose where to send the rewards. This can take a few minutes


# POST /partial
@dataclass(frozen=True)
@streamable
class PostPartialRequest(Streamable):
    payload: PostPartialPayload
    aggregate_signature: G2Element


# Response in success case
@dataclass(frozen=True)
@streamable
class PostPartialResponse(Streamable):
    points: uint64
    current_difficulty: uint64  # Current difficulty that the pool is using to give credit to this farmer

# Response in error case for all endpoints of the pool protocol
@dataclass(frozen=True)
@streamable
class ErrorResponse(Streamable):
    error_code: uint16
    error_message: Optional[str]
