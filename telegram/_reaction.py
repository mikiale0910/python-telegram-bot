#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2023
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains objects that represents a Telegram ReactionType."""
from typing import TYPE_CHECKING, Final, Literal, Optional, Union

from telegram import constants
from telegram._telegramobject import TelegramObject
from telegram._utils import enum
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot


class ReactionType(TelegramObject):
    """Base class for Telegram ReactionType Objects.
    There exist :class:`telegram.ReactionTypeEmoji` and :class:`telegram.ReactionTypeCustomEmoji`.

    .. versionadded:: 20.8

    Args:
        type (:obj:`str`): Type of the reaction. Can be
            :attr:`~telegram.ReactionType.EMOJI` or :attr:`~telegram.ReactionType.CUSTOM_EMOJI`.
    Attributes:
        type (:obj:`str`): Type of the reaction. Can be
            :attr:`~telegram.ReactionType.EMOJI` or :attr:`~telegram.ReactionType.CUSTOM_EMOJI`.

    """

    __slots__ = ("type",)

    EMOJI: Final[constants.ReactionType] = constants.ReactionType.EMOJI
    """:const:`telegram.constants.ReactionType.EMOJI`"""
    CUSTOM_EMOJI: Final[constants.ReactionType] = constants.ReactionType.CUSTOM_EMOJI
    """:const:`telegram.constants.ReactionType.CUSTOM_EMOJI`"""

    def __init__(
        self,
        type: Union[  # pylint: disable=redefined-builtin
            Literal["emoji", "custom_emoji"], constants.ReactionType
        ],
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        # Required by all subclasses
        self.type: str = enum.get_member(constants.ReactionType, type, type)

        self._freeze()

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["ReactionType"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        if cls is ReactionType and data.get("type") in [cls.EMOJI, cls.CUSTOM_EMOJI]:
            reaction_type = data.pop("type")
            if reaction_type == cls.EMOJI:
                return ReactionTypeEmoji.de_json(data=data, bot=bot)
            return ReactionTypeCustomEmoji.de_json(data=data, bot=bot)

        return super().de_json(data=data, bot=bot)


class ReactionTypeEmoji(ReactionType):
    """
    Represents a reaction with a normal emoji.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if the :attr:`emoji` is equal.

    .. versionadded:: 20.8

    Args:
        emoji (:obj:`str`): Reaction emoji. It can be one of
            :const:`telegram.constants.ReactionEmoji`.

    Attributes:
        type (:obj:`str`): Type of the reaction,
            always :tg-const:`telegram.ReactionType.EMOJI`.
        emoji (:obj:`str`): Reaction emoji. It can be one of
        :const:`telegram.constants.ReactionEmoji`.
    """

    __slots__ = ("emoji",)

    def __init__(
        self,
        emoji: str,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(type=ReactionType.EMOJI, api_kwargs=api_kwargs)

        with self._unfrozen():
            self.emoji: str = emoji
            self._id_attrs = (self.emoji,)


class ReactionTypeCustomEmoji(ReactionType):
    """
    Represents a reaction with a custom emoji.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if the :attr:`custom_emoji_id` is equal.

    .. versionadded:: 20.8

    Args:
        custom_emoji_id (:obj:`str`): Custom emoji identifier.

    Attributes:
        type (:obj:`str`): Type of the reaction,
            always :tg-const:`telegram.ReactionType.CUSTOM_EMOJI`.
        custom_emoji_id (:obj:`str`): Custom emoji identifier.

    """

    __slots__ = ("custom_emoji_id",)

    def __init__(
        self,
        custom_emoji_id: str,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(type=ReactionType.CUSTOM_EMOJI, api_kwargs=api_kwargs)

        with self._unfrozen():
            self.custom_emoji_id: str = custom_emoji_id
            self._id_attrs = (self.custom_emoji_id,)


class ReactionCount(TelegramObject):
    """This class represents a reaction added to a message along with the number of times it was
    added.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if the :attr:`type` and :attr:`total_count` is equal.

    .. versionadded:: 20.8

    Args:
        type (:class:`telegram.ReactionType`): Type of the reaction.
        total_count (:obj:`int`): Number of times the reaction was added.

    Attributes:
        type (:class:`telegram.ReactionType`): Type of the reaction.
        total_count (:obj:`int`): Number of times the reaction was added.
    """

    __slots__ = (
        "total_count",
        "type",
    )

    def __init__(
        self,
        type: ReactionType,  # pylint: disable=redefined-builtin
        total_count: int,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        # Required
        self.type: ReactionType = type
        self.total_count: int = total_count

        self._id_attrs = (
            self.type,
            self.total_count,
        )
        self._freeze()

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["ReactionCount"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        data["type"] = ReactionType.de_json(data.get("type"), bot)

        return super().de_json(data=data, bot=bot)
