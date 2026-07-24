# Language System for DDLC
# Adds a Language option to Preferences and handles language switching

# Default language is English
default persistent.language = "en"

# Available languages
init python:
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "fa": "\u0641\u0627\u0631\u0633\u06cc",
    }

    LANG_CODES = {
        "en": None,
        "fa": "fa",
    }

# Function to change language
init python:
    def change_language(lang_code):
        if lang_code in LANG_CODES:
            persistent.language = lang_code
            renpy.save_persistent()
            renpy.change_language(LANG_CODES[lang_code])
            renpy.restart_interaction()

# Initialize language from persistent on game start
init python:
    # Set config.language so _init_language() picks it up
    if persistent.language == "fa":
        config.language = "fa"
        _preferences.language = "fa"
    else:
        config.language = None
        _preferences.language = None

# Language selection screen
screen language_selection():
    tag menu
    use game_menu(_("Language")):
        vbox:
            xoffset 50
            spacing 20

            textbutton "English" action [Function(change_language, "en"), ShowMenu("preferences")]:
                style "radio_button"
                selected (persistent.language == "en")

            textbutton "\u0641\u0627\u0631\u0633\u06cc" action [Function(change_language, "fa"), ShowMenu("preferences")]:
                style "radio_button"
                selected (persistent.language == "fa")

# Modified preferences screen with Language option
screen preferences():
    tag menu

    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 4

    use game_menu(_("Settings"), scroll="viewport"):

        vbox:
            xoffset 50

            hbox:
                box_wrap True

                if renpy.variant("pc"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")
                if config.developer:
                    vbox:
                        style_prefix "radio"
                        label _("Rollback Side")
                        textbutton _("Disable") action Preference("rollback side", "disable")
                        textbutton _("Left") action Preference("rollback side", "left")
                        textbutton _("Right") action Preference("rollback side", "right")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")


            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Text Speed")


                    bar value FieldValue(_preferences, "text_cps", range=180, max_is_zero=False, style="slider", offset=20)

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"

            # Language Section
            null height (4 * gui.pref_spacing)

            vbox:
                style_prefix "radio"
                label _("Language")

                textbutton "English" action [Function(change_language, "en"), ShowMenu("preferences")]:
                    selected (persistent.language == "en")

                textbutton "\u0641\u0627\u0631\u0633\u06cc" action [Function(change_language, "fa"), ShowMenu("preferences")]:
                    selected (persistent.language == "fa")

    text "v[config.version]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"
