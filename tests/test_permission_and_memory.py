"""文件权限与内存分配的单元测试。"""
import pytest

from conftest import load

permission_module = load("permission", "filesystem/permission.py")
memory_module = load("memory_allocator", "memory/memory_allocator.py")

Permission = permission_module.Permission
MemoryAllocator = memory_module.MemoryAllocator


def test_default_permission_is_755():
    perm = Permission()

    assert perm.to_octal() == 755
    assert perm.to_string() == "rwxr-xr-x"


def test_permission_checks_each_role():
    perm = Permission()

    for bit in (Permission.READ, Permission.WRITE, Permission.EXECUTE):
        assert perm.check(Permission.OWNER, bit) is True

    assert perm.check(Permission.GROUP, Permission.READ) is True
    assert perm.check(Permission.GROUP, Permission.WRITE) is False
    assert perm.check(Permission.OTHERS, Permission.EXECUTE) is True
    assert perm.check(Permission.OTHERS, Permission.WRITE) is False


def test_set_permission_updates_single_role():
    perm = Permission()
    perm.set_permission(Permission.OTHERS, 0)

    assert perm.to_octal() == 750
    assert perm.check(Permission.OTHERS, Permission.EXECUTE) is False


def test_chmod_applies_whole_mode():
    perm = Permission("rwxrwxrwx")
    perm.chmod("644")

    assert perm.to_octal() == 644
    assert perm.to_string() == "rw-r--r--"


def test_memory_allocator_hands_out_contiguous_blocks():
    allocator = MemoryAllocator()

    assert allocator.allocate("P1", 100) == 0
    assert allocator.allocate("P2", 200) == 100

    status = allocator.get_status()

    assert status["total"] == 640
    assert status["used"] == 300
    assert status["free"] == 340
    assert status["usage_percent"] == pytest.approx(46.88, abs=0.01)


def test_memory_allocator_rejects_invalid_requests():
    allocator = MemoryAllocator()

    assert allocator.allocate("P_zero", 0) is None
    assert allocator.allocate("P_huge", 700) is None  # 总量只有 640KB
    assert allocator.get_status()["used"] == 0


def test_memory_allocator_frees_and_reuses_space():
    allocator = MemoryAllocator()
    allocator.allocate("P1", 100)

    assert allocator.free("P1") is True
    assert allocator.free("P_unknown") is False

    status = allocator.get_status()

    assert status["used"] == 0
    assert status["free"] == 640
    assert status["fragments"] == 1  # 释放后空闲块应已被合并
