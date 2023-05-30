from typing import BinaryIO, Optional

from deta import Drive  # type: ignore
from deta.drive import DriveStreamingBody, _Drive  # type: ignore
from odetam.async_model import AsyncDetaModel
from pydantic import Field


class Group(AsyncDetaModel):
    # key is GetCourse group id
    gid: str  # duplicate key for optimized queries
    name: str
    # chat ids, where bot is connected to this group
    connected_chats: list[int] = Field(default_factory=list)
    # keys of Members, that are already checked by bot
    checked_members: list[str] = Field(default_factory=list)
    # keys of Members, that are not checked yet
    unchecked_members: list[str] = Field(default_factory=list)
    invite_text: Optional[str]
    invite_img: Optional[str]  # key of file in Storage

    def get_invite_image(self) -> Optional[DriveStreamingBody]:
        if not self.invite_img:
            return None

        images_storage: _Drive = Drive("invite_images")
        image_file: Optional[DriveStreamingBody] = images_storage.get(
            self.invite_img)
        return image_file

    def set_invite_image(self, image: BinaryIO):
        if not self.invite_img:
            self.invite_img = self.gid

        images_storage: _Drive = Drive("invite_images")
        images_storage.put(self.invite_img, image,
                           content_type='image')  # type: ignore

    def remove_invite_image(self):
        if not self.invite_img:
            return

        images_storage: _Drive = Drive(self.__db_name__)
        images_storage.delete(self.invite_img)
        self.invite_img = None
