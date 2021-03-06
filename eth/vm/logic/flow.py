from eth import constants
from eth.exceptions import (
    InvalidJumpDestination,
    InvalidInstruction,
    Halt,
)

from eth.vm.computation import BaseComputation
from eth.vm.opcode_values import (
    JUMPDEST,
)


def stop(computation: BaseComputation) -> None:
    raise Halt('STOP')


def jump(computation: BaseComputation) -> None:
    jump_dest = computation.stack_pop(type_hint=constants.UINT256)

    computation.code.pc = jump_dest

    next_opcode = computation.code.peek()

    if next_opcode != JUMPDEST:
        raise InvalidJumpDestination("Invalid Jump Destination")

    if not computation.code.is_valid_opcode(jump_dest):
        raise InvalidInstruction("Jump resulted in invalid instruction")


def jumpi(computation: BaseComputation) -> None:
    jump_dest, check_value = computation.stack_pop(num_items=2, type_hint=constants.UINT256)

    if check_value:
        computation.code.pc = jump_dest

        next_opcode = computation.code.peek()

        if next_opcode != JUMPDEST:
            raise InvalidJumpDestination("Invalid Jump Destination")

        if not computation.code.is_valid_opcode(jump_dest):
            raise InvalidInstruction("Jump resulted in invalid instruction")


def jumpdest(computation: BaseComputation) -> None:
    pass


def pc(computation: BaseComputation) -> None:
    pc = max(computation.code.pc - 1, 0)

    computation.stack_push(pc)


def gas(computation: BaseComputation) -> None:
    gas_remaining = computation.get_gas_remaining()

    computation.stack_push(gas_remaining)
