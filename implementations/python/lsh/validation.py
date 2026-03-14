"""
LSH Protocol Validation

属性验证模块

基于 PropertyDefinition 实现属性验证：
- 必填验证
- 类型验证
- 范围验证
- 枚举验证

使用方式：
    from lsh import validate_element, ValidationResult
    
    element = SceneElement.create({"name": "灯", "category": "device"})
    result = validate_element(element)
    if not result.valid:
        print(result.errors)
"""

from dataclasses import dataclass
from typing import List, Tuple, Any
from .properties import PropertyType, get_property_definition
from .core import SceneElement


@dataclass
class ValidationError:
    """验证错误"""
    property_key: str
    property_name: str
    message: str
    
    def __str__(self) -> str:
        return f"{self.property_name}: {self.message}"


@dataclass
class ValidationResult:
    """验证结果"""
    valid: bool
    errors: List[ValidationError]
    
    def __bool__(self) -> bool:
        return self.valid
    
    def __str__(self) -> str:
        if self.valid:
            return "验证通过"
        return "\n".join(f"- {e}" for e in self.errors)


def validate_element(element: SceneElement) -> ValidationResult:
    """验证元素属性
    
    Args:
        element: 要验证的元素
        
    Returns:
        ValidationResult: 验证结果
    """
    category = element.get_property("category")
    definition = get_property_definition(category)
    
    if not definition:
        return ValidationResult(valid=True, errors=[])
    
    errors = []
    
    all_props = (
        definition.get("base_properties", []) +
        definition.get("extra_properties", []) +
        definition.get("position_properties", [])
    )
    
    for prop in all_props:
        value = element.get_property(prop.key)
        error = _validate_property(prop, value)
        if error:
            errors.append(error)
    
    return ValidationResult(valid=len(errors) == 0, errors=errors)


def validate_property_value(prop, value: Any) -> List[str]:
    """验证单个属性值
    
    Args:
        prop: PropertyDefinition 实例
        value: 属性值
        
    Returns:
        错误消息列表
    """
    errors = []
    error = _validate_property(prop, value)
    if error:
        errors.append(error.message)
    return errors


def _validate_property(prop, value: Any) -> ValidationError:
    """验证单个属性"""
    if value is None:
        if prop.required:
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message="是必填项"
            )
        return None
    
    prop_type = prop.property_type
    
    if prop_type == PropertyType.TEXT:
        if not isinstance(value, str):
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"必须是文本，当前类型: {type(value).__name__}"
            )
    
    elif prop_type == PropertyType.NUMBER:
        if not isinstance(value, (int, float)):
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"必须是数字，当前类型: {type(value).__name__}"
            )
        if prop.min_value is not None and value < prop.min_value:
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"不能小于 {prop.min_value}"
            )
        if prop.max_value is not None and value > prop.max_value:
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"不能大于 {prop.max_value}"
            )
    
    elif prop_type == PropertyType.INTEGER:
        if not isinstance(value, int):
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"必须是整数，当前类型: {type(value).__name__}"
            )
        if prop.min_value is not None and value < prop.min_value:
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"不能小于 {int(prop.min_value)}"
            )
        if prop.max_value is not None and value > prop.max_value:
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"不能大于 {int(prop.max_value)}"
            )
    
    elif prop_type == PropertyType.BOOLEAN:
        if not isinstance(value, bool):
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"必须是布尔值，当前类型: {type(value).__name__}"
            )
    
    elif prop_type == PropertyType.SELECT:
        valid_values = [v for v, _ in prop.options]
        if value not in valid_values:
            valid_str = ", ".join(valid_values)
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"值无效，可选值: {valid_str}"
            )
    
    elif prop_type == PropertyType.COORDINATES:
        if not isinstance(value, (list, tuple)):
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"必须是坐标数组，当前类型: {type(value).__name__}"
            )
        if len(value) not in (2, 3):
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"坐标必须是 2 或 3 个数值"
            )
        for i, v in enumerate(value):
            if not isinstance(v, (int, float)):
                return ValidationError(
                    property_key=prop.key,
                    property_name=prop.display_name,
                    message=f"坐标第 {i+1} 个值必须是数字"
                )
    
    elif prop_type == PropertyType.DATE:
        if not isinstance(value, str):
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"必须是日期字符串，当前类型: {type(value).__name__}"
            )
    
    elif prop_type == PropertyType.COLOR:
        if not isinstance(value, str):
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"必须是颜色字符串，当前类型: {type(value).__name__}"
            )
    
    elif prop_type == PropertyType.FILE_PATH:
        if not isinstance(value, str):
            return ValidationError(
                property_key=prop.key,
                property_name=prop.display_name,
                message=f"必须是文件路径，当前类型: {type(value).__name__}"
            )
    
    return None
