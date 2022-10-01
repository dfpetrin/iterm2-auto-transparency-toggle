#!/usr/bin/env python3.7

import iterm2

WINDOW_SELECTED = iterm2.FocusUpdateWindowChanged.Reason.TERMINAL_WINDOW_BECAME_KEY


async def update_tab_transparency(connection, tab, reason):
    # Apply to any and all sessions in tab
    for session in tab.sessions:
        try:
            profile = await session.async_get_profile()
        except iterm2.rpc.RPCException as exc:
            # The last session in the tab closed after we got a ref to it
            if exc.args[0] == "SESSION_NOT_FOUND":
                continue
            else:
                raise
        change = iterm2.LocalWriteOnlyProfile()

        # For window change events bringing a window into focus,
        # make sure transparency matches the original profile
        if reason is WINDOW_SELECTED:
            # But, only need to do anything if the profile has been changed
            # from the original
            if profile.original_guid:
                original, *__ = await iterm2.Profile.async_get(
                    connection, [profile.original_guid]
                )
                change.set_transparency(original.transparency)
        # For window change events taking a window out of focus,
        # change transparency to zero
        else:
            change.set_transparency(0)

        await session.async_set_profile_properties(change)


async def main(connection):
    app = await iterm2.async_get_app(connection)

    async with iterm2.FocusMonitor(connection) as mon:
        while True:
            # Block until a window change
            update = await mon.async_get_next_update()
            if update.window_changed:
                window = app.get_window_by_id(update.window_changed.window_id)
                tab = window.current_tab if window else None
                reason = update.window_changed.event
                if tab:
                    await update_tab_transparency(connection, tab, reason)


iterm2.run_forever(main)
