"""Query and indicator services for the SIAP-RTC historical dataset."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.infrastructure.orm import RtcRecordModel


@dataclass(frozen=True, slots=True)
class RtcIndicators:
    total_spots: int
    campaigns: int
    versions: int
    channels: int
    states: int


class RtcIndicatorService:
    """Provide aggregate indicators without exposing persistence details to the UI."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def summary(self, start: date | None = None, end: date | None = None) -> RtcIndicators:
        query = select(RtcRecordModel).where(RtcRecordModel.dependencia == "CAM. SEN.")
        if start is not None:
            query = query.where(RtcRecordModel.fecha >= start)
        if end is not None:
            query = query.where(RtcRecordModel.fecha <= end)
        records = self._session.scalars(query).all()
        return RtcIndicators(
            total_spots=len(records),
            campaigns=len({r.campana for r in records}),
            versions=len({r.version for r in records}),
            channels=len({r.canal_base for r in records}),
            states=len({r.estado for r in records}),
        )

    def spots_by_date(self, start: date | None = None, end: date | None = None) -> list[tuple[date, int]]:
        query = select(RtcRecordModel.fecha, func.count(RtcRecordModel.id)).where(
            RtcRecordModel.dependencia == "CAM. SEN."
        ).group_by(RtcRecordModel.fecha).order_by(RtcRecordModel.fecha)
        if start is not None:
            query = query.where(RtcRecordModel.fecha >= start)
        if end is not None:
            query = query.where(RtcRecordModel.fecha <= end)
        return [(row[0], int(row[1])) for row in self._session.execute(query)]
