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
        # change transparency to zero
        if reason is WINDOW_SELECTED:
            change.set_transparency(0)
        # For window change events taking a window out of focus,
        # make sure transparency matches the original profile
        else:
            # But, only need to do anything if the profile has been changed
            # from the original
            if profile.original_guid:
                original, *__ = await iterm2.Profile.async_get(
                    connection, [profile.original_guid]
                )
                change.set_transparency(original.transparency)

        await session.async_set_profile_properties(change)


async def main(connection):
    app = await iterm2.async_get_app(connection)
    tab = None
    update = None

    async with iterm2.FocusMonitor(connection) as mon:
        while True:
            # Initialize for first window
            if not update:
                window = app.current_window
                tab = window.current_tab if window else None
                reason = WINDOW_SELECTED
            # When switching to a new tab, treat as selecting a window
            elif update.selected_tab_changed:
                tab = app.get_tab_by_id(update.selected_tab_changed.tab_id)
                reason = WINDOW_SELECTED
            # For window change events, use the provided event reason
            elif update.window_changed:
                window = app.get_window_by_id(update.window_changed.window_id)
                tab = window.current_tab if window else None
                reason = update.window_changed.event

            if tab:
                await update_tab_transparency(connection, tab, reason)
                tab = None

            # Block until a tab or window change
            update = await mon.async_get_next_update()


iterm2.run_forever(main)
