import os

from pydantic import Field, field_validator, BaseModel, ConfigDict
from typing import Optional, Tuple




class CameraConfig(BaseModel):
    """Camera configuration settings."""

    model_config = ConfigDict(strict=False) 

    @classmethod
    @field_validator("multimedia_path")
    def validate_path(cls, value: str) -> str:
        try:
            # Check if the relative path is valid
            os.path.relpath(value)
            return value
        except ValueError:
            raise ValueError("Multimedia_path: Invalid relative path format")       
    
    # General camera
    index: int = Field(..., description="Camera index.")
    hflip: int = Field(..., description="Horizontal flip.")
    vflip: int = Field(..., description="Vertical flip.")
    sensitivity: int = Field(..., description="Motion detection sensitivity.")

    # Tuning
    tuning_enabled: bool = Field(..., alias="tuning.enabled", description="Tuning enabled.")
    tuning_path: Optional[str] = Field(None, alias="tuning.path", description="Tuning path.")

    # Multimedia
    multimedia_path: str = Field(..., alias="multimedia.path", description="Relative Multimedia path.")

    # TimeStamp
    timestamp_enabled: bool = Field(..., alias="timestamp.enabled", description="Timestamp enabled.")
    timestamp_format: str = Field(..., alias="timestamp.format", description="Timestamp format.")
    timestamp_color: Tuple[int, int, int] = Field(..., alias="timestamp.color", description="Timestamp color.")
    timestamp_origin: Tuple[int, int] = Field(..., alias="timestamp.origin", description="Timestamp origin.")
    timestamp_font: str = Field(..., alias="timestamp.font", description="Timestamp font.")
    timestamp_fscale: int = Field(..., alias="timestamp.fscale", description="Timestamp font scale.")
    timestamp_thickness: int = Field(..., alias="timestamp.thickness", description="Timestamp thickness.")

    # Image
    image_prefix: str = Field(..., alias="image.prefix", description="Image prefix.")
    image_fmt: str = Field(..., alias="image.fmt", description="Image format.")
    image_size: str = Field(..., alias="image.size", description="Image size.")
    image_snapshots: int = Field(..., alias="image.snapshots", description="Image snapshots.")
    image_snapshots_t: int = Field(..., alias="image.snapshots.t", description="Image snapshot interval.")