"""
TSX - Transfer Stack Pointer to X.

X = S

Copies the current contents of the stack register into the X register and sets
the zero and negative flags as appropriate.

Processor Status after use:

+------+-------------------+--------------------------+
| Flag | Description       | State                    |
+======+===================+==========================+
|  C   | Carry Flag        | Not affected             |
+------+-------------------+--------------------------+
|  Z   | Zero Flag         | Set is X = 0             |
+------+-------------------+--------------------------+
|  I   | Interrupt Disable | Not affected             |
+------+-------------------+--------------------------+
|  D   | Decimal Mode Flag | Not affected             |
+------+-------------------+--------------------------+
|  B   | Break Command     | Not affected             |
+------+-------------------+--------------------------+
|  V   | Overflow Flag     | Not affected             |
+------+-------------------+--------------------------+
|  N   | Negative Flag     | Set if bit 7 of X is set |
+------+-------------------+--------------------------+

+-----------------+--------+-------+--------+
| Addressing Mode | Opcode | Bytes | Cycles |
+=================+========+=======+========+
| Implied         |  0xBA  |   1   |   2    |
+-----------------+--------+-------+--------+

See also: TXS
"""
import pytest

import m6502


@pytest.mark.parametrize(
    ("value", "flag_n", "flag_z"), [
        (0x0F, False, False),
        (0x00, False, True),
        (0xF0, True, False),
    ])
def test_cpu_ins_tsx_imm(value: int, flag_n: bool, flag_z: bool) -> None:
    """
    Transfer Stack Pointer to X, Implied.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_x = 0x00
    memory[0xFCE2] = 0xBA
    memory[cpu.stack_pointer] = value
    cpu.execute(2)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_n,
        cpu.flag_z,
        cpu.reg_x,
    ) == (0xFCE3, 0x01FE, 2, flag_n, flag_z, value)
