import discord
from discord.ext.commands import Context

from ...core import Bot

allowed = {
    discord.Guild: {
        'name': None,
        'emojis': None,
        'region': None,
        'afk_timeout': None,
        'afk_channel': None,
        'icon': None,
        'id': None,
        'owner_id': None,
        'unavailable': None,
        'mfa_level': None,
        'verification_level': None,
        'explicit_content_filter': None,
        'default_notifications': None,
        'features': None,
        'splash': None,
        'channels': None,
        'large': None,
        'voice_channels': None,
        'me': None,
        'voice_client': None,
        'text_channels': None,
        'categories': None,
        'get_channel': None,
        'members': None,
        'get_member': None,
        'get_role': None,
        'default_role': None,
        'owner': None,
        'icon_url': None,
        'splash_url': None,
        'member_count': None,
        'created_at': None,
        'system_channel': None,
        'vanity_invite': None,
        'roles': None,
    },

    Bot: {
        'guilds': None,
        'emojis': None,
        'is_ready': None,
        'activity': None,
        'users': None,
    },

    discord.Member: {
        'joined_at': None,
        'activities': None,
        'guild': None,
        'nick': None,
        'status': None,
        'mobile_status': None,
        'desktop_status': None,
        'web_status': None,
        'is_on_mobile': None,
        'colour': None,
        'color': None,
        'display_name': None,
        'activity': None,
        'mentioned_in': None,
        'permissions_in': None,
        'top_role': None,
        'guild_permissions': None,
        'voice': None,
        'avatar_url': None,
        'bot': None,
        'created_at': None,
        'default_avatar_url': None,
        'discriminator': None,
        'id': None,
        'is_avatar_animated': None,
        'roles': None,
    },

    discord.ClientUser: {
        'name': None,
        'id': None,
        'discriminator': None,
        'avatar': None,
        'bot': None,
        'created_at': None,
        'default_avatar_url': None,
        'display_name': None,
        'is_avatar_animated': None,
    },

    discord.User: {
        'name': None,
        'id': None,
        'discriminator': None,
        'avatar_url': None,
        'bot': None,
        'created_at': None,
        'default_avatar_url': None,
        'display_name': None,
        'is_avatar_animated': None,
    },

    discord.Attachment: {
        'id': None,
        'size': None,
        'height': None,
        'width': None,
        'filename': None,
        'url': None,
        'proxy_url': None,
        'is_spoiler': None,
    },

    discord.Message: {
        'tts': None,
        'type': None,
        'author': None,
        'content': None,
        'nonce': None,
        'embeds': None,
        'channel': None,
        'call': None,
        'mention_everyone': None,
        'mentions': None,
        'channel_mentions': None,
        'role_mentions': None,
        'id': None,
        'webhook_id': None,
        'attachments': None,
        'pinned': None,
        'reactions': None,
        'activity': None,
        'application': None,
        'guild': None,
        'created_at': None,
        'edited_at': None,
        'jump_url': None,
    },

    discord.Reaction: {
        'emoji': None,
        'count': None,
        'me': None,
        'message': None,
        'custom_emoji': None
    },

    discord.Spotify: {
        'colour': None,
        'color': None,
        'name': None,
        'title': None,
        'artists': None,
        'artist': None,
        'album': None,
        'album_cover_url': None,
        'track_id': None,
        'start': None,
        'end': None,
        'duration': None,
        'party_id': None,
    },

    discord.VoiceState: {
        'deaf': None,
        'mute': None,
        'self_mute': None,
        'self_deaf': None,
        'self_video': None,
        'afk': None,
        'channel': None,
    },

    discord.Emoji: {
        'name': None,
        'id': None,
        'require_colons': None,
        'animated': None,
        'managed': None,
        'guild_id': None,
        'created_at': None,
        'url': None,
        'guild': None,
        'roles': None,
    },

    discord.PartialEmoji: {
        'name': None,
        'id': None,
        'animated': None,
        'url': None,
    },

    discord.Role: {
        'id': None,
        'name': None,
        'permissions': None,
        'guild': None,
        'colour': None,
        'color': None,
        'hoist': None,
        'position': None,
        'managed': None,
        'mentionable': None,
        'is_default': None,
        'created_at': None,
        'members': None,
    },

    discord.TextChannel: {
        'id': None,
        'name': None,
        'guild': None,
        'category_id': None,
        'topic': None,
        'position': None,
        'slowmode_delay': None,
        'members': None,
        'category': None,
        'created_at': None,
        'mention': None,
    },

    discord.VoiceChannel: {
        'id': None,
        'name': None,
        'guild': None,
        'category_id': None,
        'position': None,
    },

    discord.CategoryChannel: {
        'id': None,
        'name': None,
        'guild': None,
    },

    discord.DMChannel: {},
    discord.Invite: {},

    Context: {
        'message': None,
        'bot': None,
        'guild': None,
        'author': None,
    }
}
