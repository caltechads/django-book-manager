#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.templatetags.static import static
from academy_theme.wildewidgets import AcademyThemeMainMenu


#------------------------------------------------------
# Menus
#------------------------------------------------------

class MainMenu(AcademyThemeMainMenu):
    brand_image: str = static("core/images/logo.png")
    brand_text: str = "Book Manager"