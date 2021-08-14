from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from RenameBot.database import BASE, SESSION


class Users(BASE):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, primary_key=True)
    thumbnail = Column(LargeBinary, nullable=True)
    thumbnail_status = Column(Boolean)
    video_to = Column(String)
    running = Column(Boolean)

    def __init__(self, user_id, thumbnail=None, thumbnail_status=False, video_to="video", running=False):
        self.user_id = user_id
        self.thumbnail = thumbnail
        self.thumbnail_status = thumbnail_status
        self.video_to = video_to
        self.running = running

    def __repr__(self):
        return "<User {} {} {} {} ({})>".format(self.thumbnail, self.thumbnail_status, self.video_to, self.running, self.user_id)


Users.__table__.create(checkfirst=True)


def num_users():
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()
