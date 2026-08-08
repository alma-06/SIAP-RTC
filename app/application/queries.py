"""Read-only historical queries for the SIAP-RTC application layer."""

from __future__ import annotations

from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.orm import RtcRecordModel


class RtcQueryService:
    """Expose filtered historical records for reports and the future GUI."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def list_records(
        self,
        start: date | None = None,
        end: date | None = None,
        campaign: str | None = None,
        channel: str | None = None,
    ) -> list[RtcRecordModel]:
        query = select(RtcRecordModel).where(RtcRecordModel.dependencia == "CAM. SEN.")
        if start is not None:
            query = query.where(RtcRecordModel.fecha >= start)
        if end is not None:
            query = query.where(RtcRecordModel.fecha <= end)
        if campaign:
            query = query.where(RtcRecordModel.campana == campaign)
        if channel:
            query = query.where(RtcRecordModel.canal_base == channel)
        return list(self._session.scalars(query.order_by(RtcRecordModel.fecha)).all())
