"""
LSH Protocol Coordinate Transformation

LSH 协议使用右手坐标系（建筑/BIM 风格）：
- X 向右 (width 宽度)
- Y 向前 (depth 深度)
- Z 向上 (height 高度)

与其他引擎的转换关系：
- Godot: X=右, Y=上, Z=后 (左手坐标系)
- VTK: X=右, Y=上, Z=前 (右手坐标系)
- Blender: 与 LSH 完全一致

转换公式：
  Godot(X, Y, Z) = LSH(X, Z, -Y)
  VTK(X, Y, Z) = LSH(X, Z, Y)
  LSH(X, Y, Z) = Godot(X, -Z, Y)
"""

from typing import Tuple, List, Union

Position = Union[Tuple[float, float, float], List[float]]


def lsh_to_godot_position(pos: Position) -> List[float]:
    """
    LSH 坐标转 Godot 坐标
    
    LSH:  X=右(width), Y=前(depth), Z=上(height)
    Godot: X=右, Y=上, Z=后
    
    转换: Godot(X, Y, Z) = LSH(X, Z, -Y)
    """
    x, y, z = pos[0], pos[1], pos[2] if len(pos) > 2 else 0
    return [x, z, -y]


def lsh_to_godot_size(size: Position) -> List[float]:
    """
    LSH 尺寸转 Godot 尺寸
    
    LSH:  width=X, depth=Y, height=Z
    Godot: width=X, height=Y, depth=Z
    
    转换: Godot(width, height, depth) = LSH(width, height, depth)
    """
    w, d, h = size[0], size[1], size[2] if len(size) > 2 else 0
    return [w, h, d]


def lsh_to_godot_rotation(rot: Position) -> List[float]:
    """
    LSH 旋转角度转 Godot 旋转角度
    
    LSH: X=右, Y=前, Z=上
    Godot: X=右, Y=上, Z=后
    
    旋转轴映射:
    - LSH 绕 X 轴旋转 -> Godot 绕 X 轴旋转
    - LSH 绕 Y 轴旋转(深度轴) -> Godot 绕 Z 轴旋转(取反)
    - LSH 绕 Z 轴旋转(高度轴) -> Godot 绕 Y 轴旋转(取反)
    
    转换: Godot(rx, ry, rz) = LSH(rx, -rz, -ry)
    """
    rx, ry, rz = rot[0], rot[1], rot[2] if len(rot) > 2 else 0
    return [rx, -rz, -ry]


def godot_to_lsh_position(pos: Position) -> List[float]:
    """
    Godot 坐标转 LSH 坐标
    
    转换: LSH(X, Y, Z) = Godot(X, -Z, Y)
    """
    x, y, z = pos[0], pos[1], pos[2] if len(pos) > 2 else 0
    return [x, -z, y]


def lsh_to_godot_bounds(min_pos: Position, max_pos: Position) -> Tuple[List[float], List[float]]:
    """
    LSH 边界转 Godot 边界
    
    边界转换需要考虑坐标轴方向变化
    """
    godot_min = [
        min_pos[0],
        min_pos[2],
        -max_pos[1]
    ]
    godot_max = [
        max_pos[0],
        max_pos[2],
        -min_pos[1]
    ]
    return godot_min, godot_max


def godot_to_lsh_bounds(min_pos: Position, max_pos: Position) -> Tuple[List[float], List[float]]:
    """
    Godot 边界转 LSH 边界
    """
    lsh_min = [
        min_pos[0],
        -max_pos[2],
        min_pos[1]
    ]
    lsh_max = [
        max_pos[0],
        -min_pos[2],
        max_pos[1]
    ]
    return lsh_min, lsh_max


def lsh_to_vtk_position(pos: Position) -> List[float]:
    """
    LSH 坐标转 VTK 坐标
    
    LSH: X=右(width), Y=前(depth), Z=上(height)
    VTK: X=右, Y=上, Z=前
    
    转换: VTK(X, Y, Z) = LSH(X, Z, -Y)
    
    注意：Y 取负是因为 LSH Y+ 向前，VTK Z+ 向前，
    但为了与 2D 视图方向一致（Y+ 在屏幕下方），
    需要将 LSH Y+ 映射到 VTK Z-（屏幕下方）。
    """
    x, y, z = pos[0], pos[1], pos[2] if len(pos) > 2 else 0
    return [x, z, -y]


def lsh_to_vtk_size(size: Position) -> List[float]:
    """
    LSH 尺寸转 VTK 尺寸
    
    LSH: width=X, depth=Y, height=Z
    VTK: width=X, height=Y, depth=Z
    
    转换: VTK(width, height, depth) = LSH(width, height, depth)
    """
    w, d, h = size[0], size[1], size[2] if len(size) > 2 else 0
    return [w, h, d]


def lsh_to_vtk_rotation(rot: Position) -> List[float]:
    """
    LSH 旋转角度转 VTK 旋转角度
    
    LSH: X=右, Y=前, Z=上
    VTK: X=右, Y=上, Z=前
    
    旋转轴映射:
    - LSH 绕 X 轴旋转 -> VTK 绕 X 轴旋转
    - LSH 绕 Y 轴旋转(深度轴) -> VTK 绕 Z 轴旋转(取负)
    - LSH 绕 Z 轴旋转(高度轴) -> VTK 绕 Y 轴旋转
    
    转换: VTK(rx, ry, rz) = LSH(rx, rz, -ry)
    """
    rx, ry, rz = rot[0], rot[1], rot[2] if len(rot) > 2 else 0
    return [rx, rz, -ry]


def lsh_to_vtk_bounds(min_pos: Position, max_pos: Position) -> Tuple[List[float], List[float]]:
    """
    LSH 边界转 VTK 边界
    
    转换: VTK(X, Y, Z) = LSH(X, Z, -Y)
    """
    vtk_min = [
        min_pos[0],
        min_pos[2],
        -max_pos[1]
    ]
    vtk_max = [
        max_pos[0],
        max_pos[2],
        -min_pos[1]
    ]
    return vtk_min, vtk_max


def vtk_to_lsh_position(pos: Position) -> List[float]:
    """
    VTK 坐标转 LSH 坐标
    
    转换: LSH(X, Y, Z) = VTK(X, -Z, Y)
    """
    x, y, z = pos[0], pos[1], pos[2] if len(pos) > 2 else 0
    return [x, -z, y]


def vtk_to_lsh_bounds(min_pos: Position, max_pos: Position) -> Tuple[List[float], List[float]]:
    """
    VTK 边界转 LSH 边界
    """
    lsh_min = [
        min_pos[0],
        -max_pos[2],
        min_pos[1]
    ]
    lsh_max = [
        max_pos[0],
        -min_pos[2],
        max_pos[1]
    ]
    return lsh_min, lsh_max
