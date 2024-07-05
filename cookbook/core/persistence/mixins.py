from datetime import datetime

from sqlalchemy import ForeignKey, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column


class AuthoringMixin:
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    created_by: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True, index=True)
    modified_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    modified_by: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True, index=True)


class FileMixin:
    filename: Mapped[str] = mapped_column(String(180), nullable=False)
    mimetype: Mapped[str] = mapped_column(String(180), nullable=False)
    content: Mapped[bytes] = mapped_column(
        LargeBinary(length=(2**24-1)),
        nullable=False,
        deferred=True
    )

    @property
    def basename(self):
        return self.filename.rsplit('.', 1)[0] if '.' in self.filename else self.filename

    @property
    def extension(self):
        return '' if '.' not in self.filename else self.filename.rsplit('.', 1)[1]
