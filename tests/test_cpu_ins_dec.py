"""
DEC - Decrement Memory.

M,Z,N = M-1

Subtracts one from the value held at a specified memory location setting the zero and negative flags as appropriate.

+------+-------------------+-------------------------------+
| Flag | Description       | State                         |
+======+===================+===============================+
|  C   | Carry Flag        | Not affected                  |
+------+-------------------+-------------------------------+
|  Z   | Zero Flag         | Set if result is zero         |
+------+-------------------+-------------------------------+
|  I   | Interrupt Disable | Not affected                  |
+------+-------------------+-------------------------------+
|  D   | Decimal Mode Flag | Not affected                  |
+------+-------------------+-------------------------------+
|  B   | Break Command     | Not affected                  |
+------+-------------------+-------------------------------+
|  V   | Overflow Flag     | Not affected                  |
+------+-------------------+-------------------------------+
|  N   | Negative Flag     | Set if bit 7 of result is set |
+------+-------------------+-------------------------------+

+-----------------+--------+-------+--------+
| Addressing Mode | Opcode | Bytes | Cycles |
+=================+========+=======+========+
| Zero Page       |  0xC6  |   2   |   5    |
+-----------------+--------+-------+--------+
| Zero Page, X    |  0xD6  |   2   |   6    |
+-----------------+--------+-------+--------+
| Absolute        |  0xCE  |   3   |   6    |
+-----------------+--------+-------+--------+
| Absolute, X     |  0xDE  |   3   |   7    |
+-----------------+--------+-------+--------+

See also: DEX, DEY

"""
import pytest
import m6502


@pytest.mark.parametrize(
    "value, expected, flag_z, flag_n", [
        (-1, -2, False, True),
        (0, -1, False, True),
        (1, 0, True, False),
        (2, 1, False, False)
    ])
def test_cpu_ins_dec_zp(value, expected, flag_z, flag_n) -> None:
    """
    Decrement Memory, Zero Page.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    memory[0xFCE2] = 0xC6
    memory[0xFCE3] = 0xFC
    memory[0xFC] = value
    cpu.execute(5)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        memory[0xFC],
    ) == (0xFCE4, 0x01FD, 5, flag_z, flag_n, expected)


@pytest.mark.parametrize(
    "value, expected, flag_z, flag_n", [
        (-1, -2, False, True),
        (0, -1, False, True),
        (1, 0, True, False),
        (2, 1, False, False)
    ])
def test_cpu_ins_dec_zpx(value, expected, flag_z, flag_n) -> None:
    """
    Decrement Memory, Zero Page, X.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_x = 1
    memory[0xFCE2] = 0xD6
    memory[0xFCE3] = 0xFC
    memory[0xFC + cpu.reg_x] = value
    cpu.execute(6)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        memory[0xFC + cpu.reg_x],
    ) == (0xFCE4, 0x01FD, 6, flag_z, flag_n, expected)


@pytest.mark.parametrize(
    "value, expected, flag_z, flag_n", [
        (-1, -2, False, True),
        (0, -1, False, True),
        (1, 0, True, False),
        (2, 1, False, False)
    ])
def test_cpu_ins_dec_abs(value, expected, flag_z, flag_n) -> None:
    """
    Decrement Memory, Absolute.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    memory[0xFCE2] = 0xCE
    memory[0xFCE3] = 0xFC
    memory[0xFCE4] = 0xFA
    memory[0xFAFC] = value
    cpu.execute(6)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        memory[0xFAFC],
    ) == (0xFCE5, 0x01FD, 6, flag_z, flag_n, expected)


@pytest.mark.parametrize(
    "value, expected, flag_z, flag_n", [
        (-1, -2, False, True),
        (0, -1, False, True),
        (1, 0, True, False),
        (2, 1, False, False)
    ])
def test_cpu_ins_dec_abx(value, expected, flag_z, flag_n) -> None:
    """
    Decrement Memory, Absolute, X.

    return: None
    """
    memory = m6502.Memory()
    cpu = m6502.Processor(memory)
    cpu.reset()
    cpu.reg_x = 1
    memory[0xFCE2] = 0xDE
    memory[0xFCE3] = 0xFC
    memory[0xFCE4] = 0xFA
    memory[0xFAFC + cpu.reg_x] = value
    cpu.execute(7)
    assert (
        cpu.program_counter,
        cpu.stack_pointer,
        cpu.cycles,
        cpu.flag_z,
        cpu.flag_n,
        memory[0xFAFC + cpu.reg_x],
    ) == (0xFCE5, 0x01FD, 7, flag_z, flag_n, expected)
