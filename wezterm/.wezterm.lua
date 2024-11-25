-- Pull in the wezterm API
local wezterm = require("wezterm")
local mux = wezterm.mux
-- This will hold the configuration.
local config = wezterm.config_builder()

-- This is where you actually apply your config choices
-- For example, changing the color scheme:
config.front_end = "WebGpu"
config.font_size = 18
config.unix_domains = {
	{
		name = "unix",
	},
}

config.enable_tab_bar = false
--config.window_decorations = "RESIZE"
----config.window_decorations = "TITLE"
config.font = wezterm.font("JetBrains Mono")
config.color_scheme = "AdventureTime"
config.keys = {
	-- Make Option-Left equivalent to Alt-b which many line editors interpret as backward-word
	{ key = "LeftArrow", mods = "OPT", action = wezterm.action({ SendString = "\x1bb" }) },
	-- Make Option-Right equivalent to Alt-f; forward-word
	{ key = "RightArrow", mods = "OPT", action = wezterm.action({ SendString = "\x1bf" }) },
}

wezterm.on("gui-startup", function()
	local tab, pane, window = mux.spawn_window({})
	window:gui_window():maximize()
	-- window:gui_window():toggle_fullscreen()
end)

config.cursor_blink_rate = 0
config.window_background_opacity = 0.9
config.macos_window_background_blur = 20

return config
