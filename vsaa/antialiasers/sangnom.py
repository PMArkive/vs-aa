from dataclasses import dataclass
from typing import Any

import vapoursynth as vs

from ..abstract import _Antialiaser, Antialiaser, DoubleRater, SingleRater, SuperSampler

__all__ = ['SangNom', 'SangNomSS', 'SangNomSR', 'SangNomDR']

core = vs.core


@dataclass
class SANGNOM(_Antialiaser):
    aa_strength: int | tuple[int, ...] = 48
    double_fps: bool = False

    def preprocess_clip(self, clip: vs.VideoNode) -> vs.VideoNode:
        if self.double_fps:
            return clip.std.SeparateFields(self.field).std.DoubleWeave(self.field)
        return clip

    def get_aa_args(self, clip: vs.VideoNode, **kwargs: Any) -> dict[str, Any]:
        return dict(aa=self.aa_strength, order=0 if self.double_fps else self.field + 1)

    def _interpolate(self, clip: vs.VideoNode, double_y: bool, **kwargs: Any) -> vs.VideoNode:
        return core.sangnom.SangNom(clip, dh=double_y, **kwargs)

    _shift = -0.5


class SangNomSS(SANGNOM, SuperSampler):
    ...


class SangNomSR(SANGNOM, SingleRater):
    ...


class SangNomDR(SANGNOM, DoubleRater):
    ...


class SangNom(SANGNOM, Antialiaser):
    ...